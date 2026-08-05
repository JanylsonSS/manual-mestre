"""O mesmo arquivo, para rodar em dois ambientes diferentes.

Ele usa `model_dump_json()`, que existe no Pydantic 2 e não existe no 1.
Nada aqui está errado: o código é correto para uma versão e inválido
para a outra, e é exatamente esse o ponto do capítulo.

Uso (pelo `conflito.sh`, ou à mão):
    .venv/bin/python codigo/cap16/modelo.py
"""

import pydantic
from pydantic import BaseModel


class Produto(BaseModel):
    nome: str
    preco_centavos: int


def main() -> None:
    produto = Produto(nome="Mouse", preco_centavos="8990")  # type: ignore[arg-type]
    print("pydantic", pydantic.VERSION)
    # A construção acima funciona nas DUAS versões — as duas convertem
    # texto para inteiro. O que muda é o nome do método de saída.
    print("saída:", produto.model_dump_json())


if __name__ == "__main__":
    main()
