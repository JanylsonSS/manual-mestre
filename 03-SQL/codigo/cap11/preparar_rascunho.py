"""Cria dados/rascunho.db como cópia descartável do banco do laboratório.

Motivo de existir: a partir do 03.11 você escreve no banco, e escrita
apaga. Todo exercício de INSERT/UPDATE/DELETE roda no rascunho; quando
ele fica bagunçado, você roda este script de novo e recomeça limpo.

Uso:
    python codigo/cap11/preparar_rascunho.py
    AURORA_BANCO=dados/rascunho.db python codigo/sql.py "SELECT 1"
"""

import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(AQUI, "..", "..", "dados")
ORIGEM = os.path.join(DADOS, "aurora.db")
DESTINO = os.path.join(DADOS, "rascunho.db")


def main() -> int:
    if not os.path.exists(ORIGEM):
        print("Banco do laboratório não encontrado:", ORIGEM)
        print("Rode antes: python codigo/cap01/criar_laboratorio.py")
        return 1

    existia = os.path.exists(DESTINO)
    shutil.copyfile(ORIGEM, DESTINO)

    acao = "recriado" if existia else "criado"
    print("Rascunho {}: {}".format(acao, os.path.normpath(DESTINO)))
    print()
    print("Use assim (o banco bom fica intocado):")
    print("    AURORA_BANCO=dados/rascunho.db python codigo/sql.py ...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
