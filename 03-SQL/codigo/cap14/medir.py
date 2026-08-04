"""Mede o efeito de um índice: plano de execução e tempo, com e sem.

Três experimentos, nesta ordem:
    1. alta seletividade  — o índice devolve ~10 de 500.000 linhas
    2. baixa seletividade — o índice devolve ~100.000 de 500.000
    3. custo de escrita   — 20.000 INSERTs com 0, 1 e 3 índices

O detalhe que faz a medição valer: cada medição abre uma CONEXÃO NOVA.
O SQLite guarda o plano da consulta em cache, e reaproveitá-lo depois de
criar ou apagar um índice mede o plano antigo — foi o erro que este
arquivo existe para não repetir.

Uso:
    python codigo/cap14/preparar_indices.py
    python codigo/cap14/medir.py
"""

import os
import sqlite3
import statistics
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
BANCO = os.path.join(AQUI, "..", "..", "dados", "indices.db")

REPETICOES = 7


def sem_indices(nomes):
    """Apaga índices numa conexão que será descartada em seguida."""
    conexao = sqlite3.connect(BANCO)
    conexao.isolation_level = None
    for nome in nomes:
        conexao.execute("DROP INDEX IF EXISTS %s" % nome)
    conexao.close()


def criar_indice(nome, coluna):
    conexao = sqlite3.connect(BANCO)
    conexao.isolation_level = None
    inicio = time.perf_counter()
    conexao.execute("CREATE INDEX %s ON eventos(%s)" % (nome, coluna))
    segundos = time.perf_counter() - inicio
    conexao.close()
    return segundos


def medir(consulta):
    """Conexão nova -> plano recalculado. Devolve (plano, mediana em ms)."""
    conexao = sqlite3.connect(BANCO)
    plano = conexao.execute("EXPLAIN QUERY PLAN " + consulta).fetchall()[0][-1]

    tempos = []
    for _ in range(REPETICOES):
        inicio = time.perf_counter()
        conexao.execute(consulta).fetchall()
        tempos.append((time.perf_counter() - inicio) * 1000)
    conexao.close()

    # Mediana, não média: uma leitura de disco atrasada distorce a média.
    return plano, statistics.median(tempos)


def experimento(titulo, consulta, indice, coluna):
    print(titulo)
    sem_indices([indice])
    plano_sem, ms_sem = medir(consulta)
    print("  SEM  %-46s %9.3f ms" % (plano_sem[:46], ms_sem))

    criar_indice(indice, coluna)
    plano_com, ms_com = medir(consulta)
    print("  COM  %-46s %9.3f ms" % (plano_com[:46], ms_com))

    if ms_com < ms_sem:
        print("  >>> %.0fx mais rápido" % (ms_sem / ms_com))
    else:
        print("  >>> nenhum ganho")
    print()


def custo_de_escrita():
    print("[3] CUSTO DE ESCRITA — 20.000 INSERTs")
    extras = [("idx_a", "cliente_id"), ("idx_b", "tipo"), ("idx_c", "valor")]

    for quantos in (0, 1, 3):
        sem_indices([nome for nome, _ in extras])
        for nome, coluna in extras[:quantos]:
            criar_indice(nome, coluna)

        conexao = sqlite3.connect(BANCO)
        conexao.isolation_level = None
        linhas = [(1_000_000 + i, i % 50_000, "login", "2026-08-04", i)
                  for i in range(20_000)]

        inicio = time.perf_counter()
        conexao.execute("BEGIN")
        conexao.executemany("INSERT INTO eventos VALUES (?, ?, ?, ?, ?)", linhas)
        conexao.execute("COMMIT")
        ms = (time.perf_counter() - inicio) * 1000

        conexao.execute("DELETE FROM eventos WHERE id >= 1000000")  # limpa
        conexao.close()
        print("  %d índices extras -> %7.1f ms" % (quantos, ms))

    sem_indices([nome for nome, _ in extras])
    print()


def main() -> int:
    if not os.path.exists(BANCO):
        print("Banco não encontrado:", os.path.normpath(BANCO), file=sys.stderr)
        print("Rode antes: python codigo/cap14/preparar_indices.py", file=sys.stderr)
        return 1

    experimento(
        "[1] ALTA SELETIVIDADE — cliente_id = 27384 (~10 de 500.000)",
        "SELECT * FROM eventos WHERE cliente_id = 27384",
        "idx_cliente", "cliente_id",
    )
    experimento(
        "[2] BAIXA SELETIVIDADE — tipo = 'login' (~100.000 de 500.000)",
        "SELECT * FROM eventos WHERE tipo = 'login'",
        "idx_tipo", "tipo",
    )
    custo_de_escrita()

    print("Mesma tabela, mesmo índice, resultados opostos.")
    print("A diferença não está no índice: está em QUANTAS LINHAS ele devolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
