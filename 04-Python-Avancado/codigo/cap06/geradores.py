"""Geradores: funções que pausam.

Seis cenas:
    [1] o gerador PAUSA — e nada roda até o primeiro next()
    [2] gerador É iterador (o protocolo do 04.05, de graça)
    [3] as 20 linhas do Baralho do 04.05 viram 4
    [4] memória: lista contra gerador, medido
    [5] sequência infinita — possível porque nada é materializado
    [6] `yield from` e o pipeline preguiçoso

Uso:
    python codigo/cap06/geradores.py
"""

import itertools
import tracemalloc


# ---------------------------------------------------------------
# [1] Os prints revelam o que ninguém vê: onde a função para.
# ---------------------------------------------------------------
def contar_narrando():
    print("      (entrou na função)")
    yield 1
    print("      (retomou depois do 1º yield)")
    yield 2
    print("      (retomou; vai terminar)")


# ---------------------------------------------------------------
# [3] O mesmo Baralho do 04.05 §6.5 — que precisou de DUAS classes
#     e ~20 linhas. Aqui: uma classe, quatro linhas, e continua
#     percorrível várias vezes E com iteradores independentes.
# ---------------------------------------------------------------
class Baralho:
    def __init__(self, cartas):
        self._cartas = list(cartas)

    def __iter__(self):
        # Cada chamada cria um gerador NOVO — é o que garante as
        # duas propriedades que as duas classes garantiam antes.
        for carta in self._cartas:
            yield carta


# ---------------------------------------------------------------
# [5] Sem materializar, "infinito" deixa de ser problema: só se
#     produz o que for pedido.
# ---------------------------------------------------------------
def naturais():
    numero = 0
    while True:
        yield numero
        numero += 1


# ---------------------------------------------------------------
# [6] Pipeline preguiçoso: cada etapa é um gerador, e nenhuma
#     lista intermediária existe. `yield from` delega a outro
#     iterável sem escrever o laço.
# ---------------------------------------------------------------
def limpar(linhas):
    for linha in linhas:
        limpa = linha.strip()
        if limpa:
            yield limpa


def numerar(linhas, inicio=1):
    for posicao, linha in enumerate(linhas, inicio):
        yield "%03d %s" % (posicao, linha)


def cabecalho_e_corpo(linhas):
    yield "=== RELATÓRIO ==="
    yield from numerar(limpar(linhas))     # delega, sem laço
    yield "=== FIM ==="


def cena_1_pausa():
    print("[1] O GERADOR PAUSA")
    gerador = contar_narrando()
    print("    chamou a função -> tipo:", type(gerador).__name__)
    print("    >>> nenhum print apareceu: nada executou ainda")
    print("    next ->", next(gerador))
    print("    next ->", next(gerador))
    try:
        next(gerador)
    except StopIteration:
        print("    3º next -> StopIteration")
    print()


def cena_2_e_iterador():
    print("[2] GERADOR É ITERADOR")
    gerador = contar_narrando()
    print("    __iter__:%s · __next__:%s · iter(g) is g:%s"
          % (hasattr(gerador, "__iter__"), hasattr(gerador, "__next__"),
             iter(gerador) is gerador))
    print("    >>> o protocolo do 04.05, sem escrever nenhuma classe")
    print()


def cena_3_baralho():
    print("[3] O BARALHO DO 04.05, EM 4 LINHAS")
    baralho = Baralho(["A♠", "K♥", "Q♦"])
    print("    1ª passada:", list(baralho))
    print("    2ª passada:", list(baralho), "<- continua reutilizável")
    a, b = iter(baralho), iter(baralho)
    print("    dois simultâneos:", next(a), next(b), next(a))
    print()


def cena_4_memoria():
    print("[4] MEMÓRIA — 1 MILHÃO DE QUADRADOS")

    tracemalloc.start()
    lista = [x * x for x in range(1_000_000)]
    soma_lista = sum(lista)
    _, pico_lista = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    del lista

    tracemalloc.start()
    gerador = (x * x for x in range(1_000_000))
    soma_gerador = sum(gerador)
    _, pico_gerador = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("    lista:   %8.2f MB" % (pico_lista / 1e6))
    print("    gerador: %8.4f MB" % (pico_gerador / 1e6))
    print("    razão: %.0fx menos memória" % (pico_lista / pico_gerador))
    print("    mesmo resultado?", soma_lista == soma_gerador)
    print()


def cena_5_infinito():
    print("[5] SEQUÊNCIA INFINITA")
    print("    primeiros 5 de naturais():",
          list(itertools.islice(naturais(), 5)))
    pares = (n for n in naturais() if n % 2 == 0)
    print("    primeiros 4 pares:", list(itertools.islice(pares, 4)))
    print("    >>> um `while True` que não trava, porque ninguém pediu tudo")
    print()


def cena_6_yield_from():
    print("[6] PIPELINE PREGUIÇOSO com `yield from`")
    entrada = ["  venda 1  ", "", "venda 2", "   ", "venda 3"]
    for linha in cabecalho_e_corpo(entrada):
        print("   ", linha)


def main() -> None:
    cena_1_pausa()
    cena_2_e_iterador()
    cena_3_baralho()
    cena_4_memoria()
    cena_5_infinito()
    cena_6_yield_from()


if __name__ == "__main__":
    main()
