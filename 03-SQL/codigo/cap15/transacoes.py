"""Demonstra ACID e concorrência com DUAS conexões ao mesmo banco.

Por que Python e não um arquivo .sql: concorrência precisa de dois
clientes simultâneos, e um arquivo .sql tem um só. Aqui, `a` e `b` são
duas conexões independentes — o equivalente a duas pessoas mexendo no
mesmo banco ao mesmo tempo.

Cinco cenas:
    [1] Atomicidade      — o erro NÃO desfaz a transação sozinho
    [2] Isolamento       — B não enxerga o que A ainda não confirmou
    [3] Dois escritores  — "database is locked"
    [4] Lost update      — R$ 100,00 somem sem erro nenhum
    [5] As correções     — deixar o banco contar, e BEGIN IMMEDIATE

Uso:
    python codigo/cap15/transacoes.py
"""

import os
import sqlite3
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "..", "..", "dados")
BANCO = os.path.join(DADOS, "tx.db")

SALDO_INICIAL = 100000          # R$ 1.000,00 em centavos (03.12)


def conectar():
    """timeout=1: em vez de esperar 5s pelo bloqueio, falha rápido e mostra."""
    conexao = sqlite3.connect(BANCO, timeout=1.0)
    conexao.isolation_level = None          # controle explícito (D-016)
    return conexao


def recriar():
    os.makedirs(DADOS, exist_ok=True)
    if os.path.exists(BANCO):
        os.remove(BANCO)
    conexao = conectar()
    conexao.execute(
        "CREATE TABLE contas ("
        "    id             INTEGER PRIMARY KEY,"
        "    nome           TEXT    NOT NULL,"
        "    saldo_centavos INTEGER NOT NULL CHECK (saldo_centavos >= 0)"
        ") STRICT"
    )
    conexao.execute(
        "INSERT INTO contas VALUES (1, 'Ana', ?), (2, 'Bruno', 50000)",
        (SALDO_INICIAL,),
    )
    conexao.close()


def repor():
    conexao = conectar()
    conexao.execute("UPDATE contas SET saldo_centavos = ? WHERE id = 1",
                    (SALDO_INICIAL,))
    conexao.close()


def saldo(conexao, conta=1):
    return conexao.execute(
        "SELECT saldo_centavos FROM contas WHERE id = ?", (conta,)
    ).fetchone()[0]


def cena_1_atomicidade():
    print("[1] ATOMICIDADE — o erro NAO desfaz a transacao")
    repor()
    a = conectar()
    a.execute("BEGIN")
    a.execute("UPDATE contas SET saldo_centavos = saldo_centavos - 30000 WHERE id = 1")
    print("    passo 1 aplicado: Ana com %d" % saldo(a))

    try:
        # O CHECK (saldo >= 0) barra este: Bruno tem 50000.
        a.execute("UPDATE contas SET saldo_centavos = saldo_centavos - 999999 WHERE id = 2")
    except sqlite3.Error as erro:
        print("    passo 2 FALHOU: %s" % erro)

    # O ponto da cena: o erro nao fechou nada.
    print("    transacao ainda aberta? %s" % a.in_transaction)
    print("    >>> um COMMIT aqui gravaria METADE da operacao")
    a.execute("ROLLBACK")
    print("    apos ROLLBACK: Ana com %d\n" % saldo(a))
    a.close()


def cena_2_isolamento():
    print("[2] ISOLAMENTO — B nao enxerga o que A nao confirmou")
    repor()
    a, b = conectar(), conectar()
    a.execute("BEGIN")
    a.execute("UPDATE contas SET saldo_centavos = 1 WHERE id = 1")
    print("    A ve: %d" % saldo(a))
    print("    B ve: %d   <- o valor antigo" % saldo(b))
    a.execute("ROLLBACK")
    print("    apos ROLLBACK, B ve: %d\n" % saldo(b))
    a.close()
    b.close()


def cena_3_dois_escritores():
    print("[3] DOIS ESCRITORES — o banco serializa")
    repor()
    a, b = conectar(), conectar()
    a.execute("BEGIN")
    a.execute("UPDATE contas SET saldo_centavos = 90000 WHERE id = 1")
    b.execute("BEGIN")
    try:
        b.execute("UPDATE contas SET saldo_centavos = 80000 WHERE id = 1")
        print("    B escreveu junto (nao deveria)")
    except sqlite3.Error as erro:
        print("    B tentou escrever -> %s" % erro)
    a.execute("COMMIT")
    b.execute("UPDATE contas SET saldo_centavos = 80000 WHERE id = 1")
    b.execute("COMMIT")
    print("    depois que A confirmou, B passou. Saldo: %d\n" % saldo(a))
    a.close()
    b.close()


def cena_4_lost_update():
    print("[4] LOST UPDATE — o dinheiro some sem erro nenhum")
    repor()
    a, b = conectar(), conectar()

    # Os dois LEEM o mesmo saldo antes de qualquer um escrever.
    lido_a = saldo(a)
    lido_b = saldo(b)
    print("    A leu %d · B leu %d" % (lido_a, lido_b))

    a.execute("UPDATE contas SET saldo_centavos = ? WHERE id = 1", (lido_a - 10000,))
    b.execute("UPDATE contas SET saldo_centavos = ? WHERE id = 1", (lido_b - 20000,))

    final = saldo(a)
    print("    A sacou 100, B sacou 200 de 1000.")
    print("    esperado R$ 700,00 · real R$ %.2f" % (final / 100))
    print("    >>> o saque de A sumiu, e nada deu erro\n")
    a.close()
    b.close()


def cena_5_correcoes():
    print("[5] AS DUAS CORRECOES")

    print("  (a) deixar o BANCO fazer a conta")
    repor()
    a, b = conectar(), conectar()
    a.execute("UPDATE contas SET saldo_centavos = saldo_centavos - 10000 WHERE id = 1")
    b.execute("UPDATE contas SET saldo_centavos = saldo_centavos - 20000 WHERE id = 1")
    print("      esperado R$ 700,00 · real R$ %.2f" % (saldo(a) / 100))
    a.close()
    b.close()

    print("  (b) BEGIN IMMEDIATE quando a leitura decide a escrita")
    repor()
    a, b = conectar(), conectar()
    a.execute("BEGIN IMMEDIATE")             # reserva a escrita ANTES de ler
    lido_a = saldo(a)
    try:
        b.execute("BEGIN IMMEDIATE")
        print("      B entrou junto (nao deveria)")
    except sqlite3.Error as erro:
        print("      B tentou abrir -> %s (espera a vez)" % erro)

    a.execute("UPDATE contas SET saldo_centavos = ? WHERE id = 1", (lido_a - 10000,))
    a.execute("COMMIT")

    b.execute("BEGIN IMMEDIATE")
    lido_b = saldo(b)                        # agora le o valor JA atualizado
    b.execute("UPDATE contas SET saldo_centavos = ? WHERE id = 1", (lido_b - 20000,))
    b.execute("COMMIT")
    print("      B leu %d (com o saque de A) · real R$ %.2f"
          % (lido_b, saldo(b) / 100))
    a.close()
    b.close()


def main() -> int:
    recriar()
    cena_1_atomicidade()
    cena_2_isolamento()
    cena_3_dois_escritores()
    cena_4_lost_update()
    cena_5_correcoes()
    print()
    print("A cena [4] e a unica sem mensagem de erro — e a unica que perdeu dinheiro.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
