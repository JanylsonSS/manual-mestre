"""Demonstra assinaturas flexíveis — e a armadilha do default mutável.

Cinco cenas:
    [1] o default mutável que persiste entre chamadas
    [2] o default avaliado UMA vez, na definição
    [3] *args e **kwargs: o que cada um recebe
    [4] o repasse (*args, **kwargs) — a base dos decoradores (04.04)
    [5] keyword-only (*) e positional-only (/)

Uso:
    python codigo/cap01/assinaturas.py
"""

import datetime
import inspect
import time


# ---------------------------------------------------------------
# [1] A ARMADILHA. O default é criado UMA vez, quando a função é
#     definida — não a cada chamada. Uma lista como default é a
#     mesma lista para sempre.
# ---------------------------------------------------------------
def adicionar_errado(item, lista=[]):
    lista.append(item)
    return lista


def adicionar_certo(item, lista=None):
    """None como sentinela: o objeto novo nasce DENTRO da função."""
    if lista is None:
        lista = []
    lista.append(item)
    return lista


# ---------------------------------------------------------------
# [2] O mesmo mecanismo, outra roupa: o "agora" congela na
#     definição do módulo, não na chamada.
# ---------------------------------------------------------------
def registrar_errado(quando=datetime.datetime.now()):
    return quando


def registrar_certo(quando=None):
    return quando if quando is not None else datetime.datetime.now()


# ---------------------------------------------------------------
# [3] *args junta os posicionais numa TUPLA; **kwargs junta os
#     nomeados num DICIONÁRIO. Os nomes são convenção — o que
#     importa são o * e o **.
# ---------------------------------------------------------------
def inspecionar(*args, **kwargs):
    return args, kwargs


# ---------------------------------------------------------------
# [4] O REPASSE: receber com *, ** e reenviar com *, **. É o que
#     permite envolver uma função sem saber a assinatura dela —
#     a base de todo decorador (04.04).
# ---------------------------------------------------------------
def cronometrar(funcao, *args, **kwargs):
    inicio = time.perf_counter()
    resultado = funcao(*args, **kwargs)          # desempacota de volta
    ms = (time.perf_counter() - inicio) * 1000
    return resultado, ms


# ---------------------------------------------------------------
# [5] A barra e o asterisco na assinatura:
#       antes da /  -> SÓ posicional
#       depois do * -> SÓ nomeado
# ---------------------------------------------------------------
def relatorio(dados, /, formato="texto", *, incluir_zeros=False):
    return (len(dados), formato, incluir_zeros)


def main() -> None:
    print("[1] DEFAULT MUTÁVEL")
    print("    adicionar_errado('a') ->", adicionar_errado("a"))
    print("    adicionar_errado('b') ->", adicionar_errado("b"), " <<< persistiu")
    print("    adicionar_certo('a')  ->", adicionar_certo("a"))
    print("    adicionar_certo('b')  ->", adicionar_certo("b"))
    print()

    print("[2] O DEFAULT É AVALIADO NA DEFINIÇÃO")
    primeiro = registrar_errado()
    time.sleep(0.01)
    segundo = registrar_errado()
    print("    duas chamadas, mesmo instante?", primeiro == segundo)
    print("    com a correção?             ",
          registrar_certo() == (time.sleep(0.01) or registrar_certo()))
    print()

    print("[3] *args E **kwargs")
    print("    inspecionar(1, 2, x=3) ->", inspecionar(1, 2, x=3))
    print("    args é", type(inspecionar(1)[0]).__name__,
          "· kwargs é", type(inspecionar(x=1)[1]).__name__)
    print()

    print("[4] REPASSE — envolver sem conhecer a assinatura")
    resultado, ms = cronometrar(sorted, [3, 1, 2], reverse=True)
    print("    cronometrar(sorted, [3,1,2], reverse=True) ->", resultado)
    print("    levou %.4f ms" % ms)
    print()

    print("[5] POSITIONAL-ONLY (/) E KEYWORD-ONLY (*)")
    print("    assinatura:", inspect.signature(relatorio))
    print("    relatorio([1,2], 'json', incluir_zeros=True) ->",
          relatorio([1, 2], "json", incluir_zeros=True))

    for chamada, funcao in [
        ("relatorio(dados=[1,2])", lambda: relatorio(dados=[1, 2])),
        ("relatorio([1,2], 'json', True)", lambda: relatorio([1, 2], "json", True)),
    ]:
        try:
            funcao()
            print("    %-32s -> passou" % chamada)
        except TypeError as erro:
            print("    %-32s -> TypeError: %s" % (chamada, erro))


if __name__ == "__main__":
    main()
