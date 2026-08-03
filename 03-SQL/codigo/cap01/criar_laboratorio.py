#!/usr/bin/env python3
# ------------------------------------------------------------
# criar_laboratorio.py
# Capítulo 03.01 — Por que bancos relacionais existem
# O que este arquivo faz: cria o banco de laboratório aurora.db,
#   com as quatro tabelas da Aurora e dados de exemplo
# Como executar: python criar_laboratorio.py
# Rode de novo a qualquer momento: ele recria o banco do zero.
# ------------------------------------------------------------

import os
import sqlite3

AQUI = os.path.dirname(os.path.abspath(__file__))
PADRAO = os.path.join(AQUI, "..", "..", "dados", "aurora.db")
# Configuração pelo ambiente, com padrão de desenvolvimento (02.06):
BANCO = os.environ.get("AURORA_BANCO", PADRAO)
PASTA_DADOS = os.path.dirname(os.path.abspath(BANCO))

# --- 1. Estrutura (o DDL completo vem no 03.12; aqui é só o laboratório) ---

ESTRUTURA = """
DROP TABLE IF EXISTS itens_pedido;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes (
    id             INTEGER PRIMARY KEY,
    nome           TEXT    NOT NULL,
    email          TEXT,                      -- pode ser NULL (03.03)
    cidade         TEXT,
    data_cadastro  TEXT    NOT NULL
);

CREATE TABLE produtos (
    id              INTEGER PRIMARY KEY,
    nome            TEXT    NOT NULL,
    categoria       TEXT    NOT NULL,
    preco_centavos  INTEGER NOT NULL,          -- dinheiro em centavos (01.04)
    ativo           INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE pedidos (
    id          INTEGER PRIMARY KEY,
    cliente_id  INTEGER NOT NULL,
    data        TEXT    NOT NULL,
    status      TEXT    NOT NULL,              -- concluido, pendente, cancelado
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE itens_pedido (
    id                      INTEGER PRIMARY KEY,
    pedido_id               INTEGER NOT NULL,
    produto_id              INTEGER NOT NULL,
    quantidade              INTEGER NOT NULL,
    preco_unitario_centavos INTEGER NOT NULL,  -- preco no momento da venda
    FOREIGN KEY (pedido_id)  REFERENCES pedidos(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);
"""

# --- 2. Dados ------------------------------------------------------------
# Casos de ensino embutidos de proposito:
#   - Rafael nunca comprou           -> anti-join (03.08)
#   - Beatriz tem email NULL         -> IS NULL (03.03)
#   - Helena tem cidade NULL         -> agregacao com NULL (03.05)
#   - pedido 20 cancelado            -> filtro por status (03.03)
#   - produto 12 inativo e sem venda -> LEFT JOIN (03.08)

CLIENTES = [
    (1, "Fernanda Lima",    "fernanda@aurora.com",  "campinas",  "2025-03-14"),
    (2, "Ana Souza",        "ana@aurora.com",       "santos",    "2025-05-02"),
    (3, "Beatriz Nogueira", None,                   "campinas",  "2025-06-21"),
    (4, "Carlos Menezes",   "carlos@aurora.com",    "sorocaba",  "2025-08-09"),
    (5, "Diego Alves",      "diego@aurora.com",     "santos",    "2025-11-30"),
    (6, "Helena Prado",     "helena@aurora.com",    None,        "2026-01-15"),
    (7, "Rafael Torres",    "rafael@aurora.com",    "campinas",  "2026-02-03"),
    (8, "Juliana Castro",   "juliana@aurora.com",   "sorocaba",  "2026-04-27"),
]

PRODUTOS = [
    (1,  "Fone Bluetooth XZ-9",  "audio",        46990, 1),
    (2,  "Mouse Sem Fio",        "perifericos",   8990, 1),
    (3,  "Teclado Mecanico K2",  "perifericos",  32900, 1),
    (4,  "Webcam HD 1080",       "video",        19990, 1),
    (5,  "Monitor 24 polegadas", "video",        89900, 1),
    (6,  "Caixa de Som BT",      "audio",        15990, 1),
    (7,  "Hub USB-C 6 portas",   "acessorios",   12990, 1),
    (8,  "Suporte para Notebook","acessorios",    7990, 1),
    (9,  "Microfone Condensador","audio",        45900, 1),
    (10, "Cabo HDMI 2m",         "acessorios",    3490, 1),
    (11, "Headset Gamer H7",     "audio",        27900, 1),
    (12, "Mousepad Grande",      "acessorios",    4990, 0),   # inativo, sem vendas
]

PEDIDOS = [
    (1,  1, "2025-04-02", "concluido"),
    (2,  1, "2025-07-18", "concluido"),
    (3,  2, "2025-06-11", "concluido"),
    (4,  3, "2025-07-05", "concluido"),
    (5,  1, "2025-09-23", "concluido"),
    (6,  4, "2025-09-30", "concluido"),
    (7,  2, "2025-10-14", "concluido"),
    (8,  5, "2025-12-08", "concluido"),
    (9,  1, "2026-01-09", "concluido"),
    (10, 6, "2026-01-28", "concluido"),
    (11, 4, "2026-02-11", "concluido"),
    (12, 8, "2026-05-03", "concluido"),
    (13, 1, "2026-05-19", "concluido"),
    (14, 2, "2026-06-02", "concluido"),
    (15, 5, "2026-06-15", "pendente"),
    (16, 6, "2026-06-21", "concluido"),
    (17, 8, "2026-07-04", "concluido"),
    (18, 3, "2026-07-12", "pendente"),
    (19, 4, "2026-07-20", "concluido"),
    (20, 2, "2026-07-25", "cancelado"),
]

# (id, pedido_id, produto_id, quantidade, preco_unitario_centavos)
ITENS = [
    (1,   1,  1, 1, 46990), (2,   1, 10, 2,  3490),
    (3,   2,  3, 1, 32900),
    (4,   3,  2, 2,  8990), (5,   3,  8, 1,  7990),
    (6,   4,  5, 1, 89900),
    (7,   5,  6, 1, 15990), (8,   5, 10, 1,  3490),
    (9,   6,  4, 1, 19990), (10,  6,  7, 1, 12990),
    (11,  7,  1, 1, 44990),                              # preco promocional
    (12,  8, 11, 1, 27900), (13,  8,  2, 1,  8990),
    (14,  9,  9, 1, 45900),
    (15, 10,  3, 1, 32900), (16, 10,  2, 1,  8990),
    (17, 11,  5, 1, 89900), (18, 11,  4, 1, 19990),
    (19, 12,  6, 2, 15990),
    (20, 13,  7, 1, 12990), (21, 13,  8, 2,  7990),
    (22, 14, 11, 1, 27900),
    (23, 15,  1, 1, 46990),                              # pedido pendente
    (24, 16,  9, 1, 45900), (25, 16, 10, 3,  3490),
    (26, 17,  3, 1, 32900), (27, 17,  2, 1,  8990),
    (28, 18,  5, 1, 89900),                              # pedido pendente
    (29, 19,  1, 2, 46990), (30, 19,  6, 1, 15990),
    (31, 20,  4, 1, 19990),                              # pedido cancelado
]


def criar_banco():
    """Recria o banco do zero e devolve um resumo do que foi carregado."""
    os.makedirs(PASTA_DADOS, exist_ok=True)

    conexao = sqlite3.connect(BANCO)
    try:
        conexao.executescript(ESTRUTURA)

        conexao.executemany(
            "INSERT INTO clientes VALUES (?, ?, ?, ?, ?)", CLIENTES)
        conexao.executemany(
            "INSERT INTO produtos VALUES (?, ?, ?, ?, ?)", PRODUTOS)
        conexao.executemany(
            "INSERT INTO pedidos VALUES (?, ?, ?, ?)", PEDIDOS)
        conexao.executemany(
            "INSERT INTO itens_pedido VALUES (?, ?, ?, ?, ?)", ITENS)

        conexao.commit()

        resumo = {}
        for tabela in ("clientes", "produtos", "pedidos", "itens_pedido"):
            cursor = conexao.execute(f"SELECT COUNT(*) FROM {tabela}")
            resumo[tabela] = cursor.fetchone()[0]
        return resumo
    finally:
        conexao.close()


def main():
    resumo = criar_banco()
    print("Laboratorio Aurora criado!")
    print(f"  Arquivo: {os.path.normpath(BANCO)}")
    print("  Tabelas carregadas:")
    for tabela, quantidade in resumo.items():
        print(f"    {tabela:<14} {quantidade:>3} linhas")
    print()
    print("  Primeira consulta:")
    print('    python codigo/sql.py "SELECT nome, cidade FROM clientes LIMIT 3"')


if __name__ == "__main__":
    main()
