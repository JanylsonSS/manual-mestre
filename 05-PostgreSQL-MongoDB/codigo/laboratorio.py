"""O laboratório PostgreSQL do módulo 05.

Ele existe para você rodar os exemplos **sem instalar nada**. O capítulo
05.01 ensina a instalação de verdade — a que você vai usar no trabalho —
e este arquivo é o atalho para quem quer executar os exemplos hoje.

Como funciona: o pacote `pgserver` traz os binários do PostgreSQL dentro
de um pacote pip e sobe um servidor local, com soquete Unix, sem serviço
do sistema e sem porta de rede. É um Postgres de verdade, versão 16.

    pip install pgserver "psycopg[binary]"
    python codigo/laboratorio.py            # cria e popula o banco
    python codigo/laboratorio.py --uri      # só imprime a URI

Se você **já instalou** o PostgreSQL (05.01), ignore este arquivo e
aponte a variável de ambiente:

    export AURORA_URI="postgresql://aurora:senha@localhost:5432/aurora"
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

PASTA_DADOS = Path(__file__).resolve().parent.parent / "dados" / "pgdata"

ESQUEMA = """
DROP TABLE IF EXISTS itens_pedido, pedidos, produtos, clientes CASCADE;

CREATE TABLE clientes (
    id          integer PRIMARY KEY,
    nome        text    NOT NULL,
    email       text    UNIQUE,
    cidade      text,
    criado_em   timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE produtos (
    id              integer PRIMARY KEY,
    nome            text    NOT NULL,
    categoria       text    NOT NULL,
    preco_centavos  integer NOT NULL CHECK (preco_centavos >= 0),
    ativo           boolean NOT NULL DEFAULT true
);

CREATE TABLE pedidos (
    id          integer PRIMARY KEY,
    cliente_id  integer NOT NULL REFERENCES clientes(id),
    data        date    NOT NULL,
    status      text    NOT NULL CHECK (status IN ('pago', 'pendente', 'cancelado'))
);

CREATE TABLE itens_pedido (
    id                      integer PRIMARY KEY,
    pedido_id               integer NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    produto_id              integer NOT NULL REFERENCES produtos(id),
    quantidade              integer NOT NULL CHECK (quantidade > 0),
    preco_unitario_centavos integer NOT NULL
);
"""

CLIENTES = [
    (1, "Ana Souza", "ana@exemplo.com", "Sao Paulo"),
    (2, "Bruno Lima", "bruno@exemplo.com", "Rio de Janeiro"),
    (3, "Carla Dias", "carla@exemplo.com", "Sao Paulo"),
    (4, "Diego Alves", None, "Belo Horizonte"),
    (5, "Elena Rocha", "elena@exemplo.com", "Curitiba"),
    (6, "Fabio Nunes", "fabio@exemplo.com", "Sao Paulo"),
    (7, "Gabi Martins", "gabi@exemplo.com", "Porto Alegre"),
    (8, "Hugo Pinto", "hugo@exemplo.com", "Recife"),
]

PRODUTOS = [
    (1, "Fone Bluetooth XZ-9", "audio", 46990),
    (2, "Mouse Sem Fio", "perifericos", 8990),
    (3, "Teclado Mecanico K2", "perifericos", 32900),
    (4, "Webcam HD 1080", "video", 19990),
    (5, "Suporte de Notebook", "acessorios", 12900),
    (6, "Hub USB-C 7 portas", "acessorios", 15900),
    (7, "Caixa de Som Mini", "audio", 24900),
    (8, "Monitor 24 polegadas", "video", 89900),
    (9, "Mousepad Grande", "acessorios", 4990),
    (10, "Headset Gamer H7", "audio", 37900),
    (11, "Teclado Compacto 60%", "perifericos", 27900),
    (12, "Ring Light 10 polegadas", "video", 13900),
]

PEDIDOS = [
    (1, 1, "2026-06-02", "pago"), (2, 2, "2026-06-05", "pago"),
    (3, 1, "2026-06-11", "pago"), (4, 3, "2026-06-14", "cancelado"),
    (5, 5, "2026-06-18", "pago"), (6, 2, "2026-06-21", "pago"),
    (7, 6, "2026-06-25", "pendente"), (8, 1, "2026-06-28", "pago"),
    (9, 7, "2026-07-01", "pago"), (10, 3, "2026-07-04", "pago"),
    (11, 5, "2026-07-08", "pago"), (12, 8, "2026-07-10", "pendente"),
    (13, 2, "2026-07-13", "pago"), (14, 6, "2026-07-16", "pago"),
    (15, 1, "2026-07-19", "pago"), (16, 7, "2026-07-21", "cancelado"),
    (17, 3, "2026-07-24", "pago"), (18, 5, "2026-07-26", "pago"),
    (19, 8, "2026-07-29", "pago"), (20, 2, "2026-07-31", "pago"),
]

ITENS = [
    (1, 1, 2, 1, 8990), (2, 1, 9, 2, 4990), (3, 2, 1, 1, 46990),
    (4, 3, 3, 1, 32900), (5, 3, 2, 1, 8990), (6, 4, 8, 1, 89900),
    (7, 5, 5, 2, 12900), (8, 6, 4, 1, 19990), (9, 6, 6, 1, 15900),
    (10, 7, 10, 1, 37900), (11, 8, 7, 2, 24900), (12, 9, 11, 1, 27900),
    (13, 9, 9, 3, 4990), (14, 10, 1, 1, 46990), (15, 10, 12, 1, 13900),
    (16, 11, 3, 2, 32900), (17, 12, 8, 1, 89900), (18, 13, 2, 4, 8990),
    (19, 14, 5, 1, 12900), (20, 14, 6, 2, 15900), (21, 15, 10, 1, 37900),
    (22, 16, 4, 1, 19990), (23, 17, 7, 1, 24900), (24, 17, 9, 2, 4990),
    (25, 18, 11, 1, 27900), (26, 19, 12, 3, 13900), (27, 19, 2, 1, 8990),
    (28, 20, 1, 1, 46990), (29, 20, 3, 1, 32900), (30, 20, 9, 1, 4990),
    (31, 15, 6, 1, 15900),
]


def uri() -> str:
    """A URI de conexão. Respeita AURORA_URI se você já tem um servidor."""
    externa = os.environ.get("AURORA_URI")
    if externa:
        return externa
    import pgserver                                   # só quando necessário

    PASTA_DADOS.mkdir(parents=True, exist_ok=True)
    return pgserver.get_server(str(PASTA_DADOS)).get_uri()


def criar_e_popular(endereco: str) -> dict[str, int]:
    import psycopg

    with psycopg.connect(endereco) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(ESQUEMA)
            cursor.executemany(
                "INSERT INTO clientes (id, nome, email, cidade) "
                "VALUES (%s, %s, %s, %s)", CLIENTES)
            cursor.executemany(
                "INSERT INTO produtos (id, nome, categoria, preco_centavos) "
                "VALUES (%s, %s, %s, %s)", PRODUTOS)
            cursor.executemany(
                "INSERT INTO pedidos (id, cliente_id, data, status) "
                "VALUES (%s, %s, %s, %s)", PEDIDOS)
            cursor.executemany(
                "INSERT INTO itens_pedido (id, pedido_id, produto_id, "
                "quantidade, preco_unitario_centavos) VALUES (%s, %s, %s, %s, %s)",
                ITENS)
        conexao.commit()

        contagem: dict[str, int] = {}
        with conexao.cursor() as cursor:
            for tabela in ("clientes", "produtos", "pedidos", "itens_pedido"):
                cursor.execute("SELECT count(*) FROM " + tabela)
                linha = cursor.fetchone()
                contagem[tabela] = linha[0] if linha else 0
    return contagem


def main() -> int:
    analisador = argparse.ArgumentParser(description="Laboratório do módulo 05")
    analisador.add_argument("--uri", action="store_true",
                            help="imprime a URI e sai")
    opcoes = analisador.parse_args()

    endereco = uri()
    if opcoes.uri:
        print(endereco)
        return 0

    contagem = criar_e_popular(endereco)
    print("Banco da Aurora pronto.")
    print("  URI:", endereco)
    for tabela, linhas in contagem.items():
        print("  %-14s %3d linhas" % (tabela, linhas))
    print()
    print("Para usar em outro terminal:")
    print('  export AURORA_URI="%s"' % endereco)
    return 0


if __name__ == "__main__":
    sys.exit(main())
