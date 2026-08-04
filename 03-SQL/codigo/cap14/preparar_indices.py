"""Cria dados/indices.db com 500.000 eventos para medir índices.

Motivo de existir: o efeito de um índice não aparece em 71 linhas. Com
meio milhão, a diferença entre varrer e buscar é a diferença entre 46 ms
e 0,03 ms — e isso você vê no relógio, não no argumento.

As quatro colunas têm cardinalidades deliberadamente diferentes, porque
é a cardinalidade que decide se o índice vale a pena (§6.5):

    cliente_id  ~50.000 valores distintos  (~10 linhas cada)
    valor       ~90.000 valores distintos  (~5 linhas cada)
    data           ~224 valores distintos  (~2.200 linhas cada)
    tipo              5 valores distintos  (~100.000 linhas cada)

Uso:
    python codigo/cap14/preparar_indices.py
    python codigo/cap14/medir.py
"""

import os
import random
import sqlite3
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "..", "..", "dados")
DESTINO = os.path.join(DADOS, "indices.db")

LINHAS = 500_000
TIPOS = ["login", "compra", "carrinho", "busca", "logout"]


def gerar():
    """Devolve as linhas. random.seed fixo: seus números batem com os do livro."""
    random.seed(42)
    for i in range(1, LINHAS + 1):
        yield (
            i,
            random.randint(1, 50_000),
            random.choice(TIPOS),
            "2026-%02d-%02d" % (random.randint(1, 8), random.randint(1, 28)),
            random.randint(100, 90_000),
        )


def main() -> int:
    os.makedirs(DADOS, exist_ok=True)
    if os.path.exists(DESTINO):
        os.remove(DESTINO)

    conexao = sqlite3.connect(DESTINO)
    conexao.isolation_level = None           # controle explícito (03.11)
    conexao.execute(
        "CREATE TABLE eventos ("
        "    id         INTEGER PRIMARY KEY,"
        "    cliente_id INTEGER NOT NULL,"
        "    tipo       TEXT    NOT NULL,"
        "    data       TEXT    NOT NULL,"
        "    valor      INTEGER NOT NULL"
        ") STRICT"
    )

    inicio = time.perf_counter()
    conexao.execute("BEGIN")                 # uma transação, não 500.000
    conexao.executemany("INSERT INTO eventos VALUES (?, ?, ?, ?, ?)", gerar())
    conexao.execute("COMMIT")
    segundos = time.perf_counter() - inicio
    conexao.close()

    mb = os.path.getsize(DESTINO) / 1e6
    print("Banco criado: %s" % os.path.normpath(DESTINO))
    print("%d linhas em %.1f s · %.1f MB · NENHUM índice ainda" % (LINHAS, segundos, mb))
    print()
    print("Próximo passo:  python codigo/cap14/medir.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
