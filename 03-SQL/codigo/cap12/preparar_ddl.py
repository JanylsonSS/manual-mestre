"""Cria dados/ddl.db vazio para os experimentos de DDL do 03.12.

Motivo de existir: este capítulo cria, altera e destrói tabelas. Fazer
isso no banco do laboratório atrapalharia os capítulos 03.01-03.11, e
fazer no rascunho do 03.11 misturaria dois assuntos. Aqui o banco
começa vazio de propósito — você constrói tudo.

Uso:
    python codigo/cap12/preparar_ddl.py
    AURORA_BANCO=dados/ddl.db python codigo/sql.py codigo/cap12/tipos.sql
"""

import os
import sqlite3
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "..", "..", "dados")
DESTINO = os.path.join(DADOS, "ddl.db")


def main() -> int:
    os.makedirs(DADOS, exist_ok=True)

    if os.path.exists(DESTINO):
        os.remove(DESTINO)                  # recomeçar limpo é o ponto

    conexao = sqlite3.connect(DESTINO)      # conectar já cria o arquivo
    versao = conexao.execute("SELECT sqlite_version()").fetchone()[0]
    conexao.close()

    print("Banco de DDL criado (vazio):", os.path.normpath(DESTINO))
    print("Versão do SQLite:", versao)

    if tuple(int(p) for p in versao.split(".")[:2]) < (3, 37):
        print()
        print("AVISO: tabelas STRICT exigem SQLite 3.37 ou superior.")
        print("O comando [6] de tipos.sql vai falhar por versão,")
        print("não pelo motivo que o capítulo explica.")

    print()
    print("Use assim:")
    print("    AURORA_BANCO=dados/ddl.db python codigo/sql.py ...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
