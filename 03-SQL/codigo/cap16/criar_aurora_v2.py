"""Cria dados/aurora_v2.db a partir de schema.sql e carrega os dados.

Diferença para o criar_laboratorio.py do 03.01: lá o schema estava
embutido no Python. Aqui ele mora num arquivo .sql versionado, e o
Python só executa e carrega — separação que permite ler o schema sem
ler código, e alterá-lo sem tocar na carga.

A carga é TRANSACIONAL (03.15): ou o banco fica completo, ou não
existe. E a conferência ao final compara com o aurora.db do 03.01 —
schema diferente, mesmos números.

Uso:
    python codigo/cap16/criar_aurora_v2.py
"""

import os
import sqlite3
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "..", "..", "dados")
DESTINO = os.path.join(DADOS, "aurora_v2.db")
SCHEMA = os.path.join(AQUI, "schema.sql")

CATEGORIAS = ["perifericos", "video", "audio", "acessorios"]

CLIENTES = [
    (1, "Fernanda Lima",    "fernanda@aurora.com", "campinas", "2025-01-12"),
    (2, "Ana Souza",        "ana@aurora.com",      "santos",   "2025-02-03"),
    (3, "Beatriz Nogueira",  None,                 "campinas", "2025-02-20"),
    (4, "Carlos Menezes",   "carlos@aurora.com",   "sorocaba", "2025-03-05"),
    (5, "Diego Alves",      "diego@aurora.com",    "santos",   "2025-03-19"),
    (6, "Helena Prado",     "helena@aurora.com",    None,      "2025-04-01"),
    (7, "Rafael Torres",    "rafael@aurora.com",   "campinas", "2025-04-15"),
    (8, "Juliana Castro",   "juliana@aurora.com",  "sorocaba", "2025-05-02"),
]


def carregar_schema(conexao):
    with open(SCHEMA, encoding="utf-8") as arquivo:
        conexao.executescript(arquivo.read())


def copiar_dados(conexao, origem):
    """Le do aurora.db do 03.01 e grava no schema novo.

    A tabela 'categorias' nao existe la: o texto solto vira id aqui.
    E o resto passa direto — as colunas coincidem de proposito, para
    que a comparacao final seja legitima.
    """
    conexao.executemany(
        "INSERT INTO categorias (id, nome) VALUES (?, ?)",
        list(enumerate(CATEGORIAS, start=1)),
    )
    mapa = {nome: i for i, nome in enumerate(CATEGORIAS, start=1)}

    conexao.executemany(
        "INSERT INTO clientes VALUES (?, ?, ?, ?, ?)", CLIENTES
    )

    produtos = origem.execute(
        "SELECT id, nome, categoria, preco_centavos, ativo FROM produtos"
    ).fetchall()
    conexao.executemany(
        "INSERT INTO produtos "
        "(id, nome, categoria_id, preco_centavos, ativo) VALUES (?, ?, ?, ?, ?)",
        [(i, nome, mapa[cat], preco, ativo)
         for i, nome, cat, preco, ativo in produtos],
    )

    conexao.executemany(
        "INSERT INTO pedidos VALUES (?, ?, ?, ?)",
        origem.execute(
            "SELECT id, cliente_id, data, status FROM pedidos"
        ).fetchall(),
    )
    conexao.executemany(
        "INSERT INTO itens_pedido VALUES (?, ?, ?, ?, ?)",
        origem.execute(
            "SELECT id, pedido_id, produto_id, quantidade, "
            "       preco_unitario_centavos FROM itens_pedido"
        ).fetchall(),
    )


def conferir(conexao, origem):
    """A prova dos nove: schema diferente, MESMOS numeros (03.05)."""
    faturamento = (
        "SELECT SUM(i.quantidade * i.preco_unitario_centavos) "
        "FROM itens_pedido i JOIN pedidos p ON p.id = i.pedido_id "
        "WHERE p.status = 'concluido'"
    )
    novo = conexao.execute(faturamento).fetchone()[0]
    velho = origem.execute(faturamento).fetchone()[0]

    print("Faturamento (centavos) — v2: %d · original: %d" % (novo, velho))
    if novo != velho:
        print("DIVERGENCIA: a migracao perdeu ou inventou dados.")
        return False

    for tabela in ("clientes", "produtos", "pedidos", "itens_pedido"):
        n = conexao.execute("SELECT COUNT(*) FROM " + tabela).fetchone()[0]
        v = origem.execute("SELECT COUNT(*) FROM " + tabela).fetchone()[0]
        marca = "ok" if n == v else "DIVERGE"
        print("  %-14s v2: %3d · original: %3d  %s" % (tabela, n, v, marca))
        if n != v:
            return False
    return True


def main() -> int:
    caminho_origem = os.path.join(DADOS, "aurora.db")
    if not os.path.exists(caminho_origem):
        print("Rode antes: python codigo/cap01/criar_laboratorio.py",
              file=sys.stderr)
        return 1

    if os.path.exists(DESTINO):
        os.remove(DESTINO)

    origem = sqlite3.connect(caminho_origem)
    conexao = sqlite3.connect(DESTINO)
    conexao.isolation_level = None
    conexao.execute("PRAGMA foreign_keys = ON")

    try:
        carregar_schema(conexao)
        # Carga transacional: ou tudo entra, ou o banco nao existe (03.15).
        conexao.execute("BEGIN")
        copiar_dados(conexao, origem)
        conexao.execute("COMMIT")
    except sqlite3.Error as erro:
        try:
            conexao.execute("ROLLBACK")
        except sqlite3.Error:
            pass
        conexao.close()
        origem.close()
        os.remove(DESTINO)                  # banco pela metade nao serve
        print("Falha na carga: %s" % erro, file=sys.stderr)
        return 1

    print("Banco criado:", os.path.normpath(DESTINO))
    ok = conferir(conexao, origem)
    conexao.close()
    origem.close()

    if not ok:
        return 1
    print()
    print("Schema diferente, mesmos numeros: a migracao preservou os dados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
