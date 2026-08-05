"""O ponto de entrada do comando `aurora`, declarado em
[project.scripts] do pyproject.toml."""

import sys

from aurora.catalogo import buscar, total
from aurora.formato import formatar_reais
from aurora.modelo import Produto

EXEMPLO = [
    Produto("Mouse Sem Fio", 8990, "perifericos"),
    Produto("Teclado Mecanico K2", 32900, "perifericos"),
    Produto("Fone Bluetooth XZ-9", 46990, "audio"),
]


def main() -> int:
    if len(sys.argv) > 1:
        achado = buscar(EXEMPLO, sys.argv[1])
        if achado is None:
            print("produto não encontrado:", sys.argv[1])
            return 1
        print(achado.nome, "-", formatar_reais(achado.preco_centavos))
        return 0

    for produto in EXEMPLO:
        print("%-24s %s" % (produto.nome, formatar_reais(produto.preco_centavos)))
    print("%-24s %s" % ("TOTAL", formatar_reais(total(EXEMPLO))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
