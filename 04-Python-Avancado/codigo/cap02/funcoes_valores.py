"""Funções como valores: atributos, key=, despacho e as armadilhas.

Seis cenas:
    [1] a função é um objeto — tem atributos, e você pode criar novos
    [2] guardar em variável, lista e dicionário
    [3] key= em sorted, e por que ela é chamada n vezes (não n log n)
    [4] despacho por dicionário no lugar de if/elif
    [5] lambda × def: o que se perde
    [6] map/filter esgotam; compreensões não

Uso:
    python codigo/cap02/funcoes_valores.py
"""

import random
from operator import itemgetter

PESSOAS = [
    ("Ana", "sp", 30),
    ("Bruno", "rj", 25),
    ("Carla", "sp", 40),
    ("Diego", "rj", 35),
]


def saudar(nome):
    """Cumprimenta alguém pelo nome."""
    return "Olá, %s" % nome


# ---------------------------------------------------------------
# [4] Despacho: cada operação é um valor num dicionário. Acrescentar
#     uma operação nova é acrescentar uma CHAVE — não editar um
#     if/elif que cresce para sempre.
# ---------------------------------------------------------------
def area_circulo(r):
    return 3.14159 * r * r


def area_quadrado(lado):
    return lado * lado


AREAS = {
    "circulo": area_circulo,
    "quadrado": area_quadrado,
}


def cena_1_funcao_e_objeto():
    print("[1] A FUNÇÃO É UM OBJETO")
    print("    __name__:", saudar.__name__)
    print("    __doc__: ", saudar.__doc__)
    saudar.chamadas = 0                  # atributo que não existia
    print("    atributo inventado:", saudar.chamadas)
    print("    isinstance(saudar, object):", isinstance(saudar, object))
    print()


def cena_2_como_valor():
    print("[2] FUNÇÃO COMO VALOR")
    f = saudar                           # SEM parênteses: a função, não o resultado
    print("    f('Ana') ->", f("Ana"))
    print("    f is saudar ->", f is saudar)

    operacoes = {"soma": lambda a, b: a + b, "sub": lambda a, b: a - b}
    print("    operacoes['soma'](2, 3) ->", operacoes["soma"](2, 3))
    print()


def cena_3_key():
    print("[3] key= EM sorted")
    print("    por idade:  ", sorted(PESSOAS, key=lambda p: p[2]))
    print("    com itemgetter:", sorted(PESSOAS, key=itemgetter(2)))
    # Chave composta: cidade crescente, idade DECRESCENTE (o menos).
    print("    (cidade, -idade):", sorted(PESSOAS, key=lambda p: (p[1], -p[2])))

    # key é chamada UMA vez por elemento — não a cada comparação.
    chamadas = []

    def contar(x):
        chamadas.append(x)
        return x

    dados = list(range(1000))
    random.shuffle(dados)
    sorted(dados, key=contar)
    print("    1000 elementos -> key chamada %d vezes" % len(chamadas))
    print("    (uma comparação por par seria ~9965)")
    print()


def cena_4_despacho():
    print("[4] DESPACHO POR DICIONÁRIO")
    print("    AREAS['circulo'](2) ->", round(AREAS["circulo"](2), 3))
    print("    AREAS['quadrado'](2) ->", AREAS["quadrado"](2))
    # .get com padrão: forma desconhecida não quebra o programa.
    desconhecida = AREAS.get("triangulo")
    print("    AREAS.get('triangulo') ->", desconhecida)
    print()


def cena_5_lambda_vs_def():
    print("[5] LAMBDA × DEF")
    quadrado_lambda = lambda x: x * x           # noqa: E731 — didático

    def quadrado_def(x):
        """Eleva ao quadrado."""
        return x * x

    print("    lambda.__name__:", quadrado_lambda.__name__)
    print("    def.__name__:   ", quadrado_def.__name__)
    print("    lambda.__doc__: ", quadrado_lambda.__doc__)
    print("    >>> num traceback, o lambda aparece como <lambda>")
    print()


def cena_6_map_esgota():
    print("[6] map/filter ESGOTAM")
    resultado = map(str.upper, ["a", "b"])
    print("    tipo:", type(resultado).__name__)
    print("    list(resultado):", list(resultado))
    print("    list(resultado) de novo:", list(resultado), "<<< vazio")
    print("    compreensão:", [s.upper() for s in ["a", "b"]], "(sempre disponível)")


def main() -> None:
    cena_1_funcao_e_objeto()
    cena_2_como_valor()
    cena_3_key()
    cena_4_despacho()
    cena_5_lambda_vs_def()
    cena_6_map_esgota()


if __name__ == "__main__":
    main()
