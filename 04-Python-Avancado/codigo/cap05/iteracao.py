"""O protocolo de iteração: o que o `for` faz por baixo.

Seis cenas:
    [1] o `for` desmontado em iter() + next() + StopIteration
    [2] iterável × iterador — a distinção que explica tudo
    [3] por que `map` esgota (a pergunta que o 04.02 deixou)
    [4] duas passadas: lista sim, iterador não
    [5] `range` NÃO é iterador — e por isso não esgota
    [6] uma classe que o `for` percorre

Uso:
    python codigo/cap05/iteracao.py
"""


# ---------------------------------------------------------------
# [6] Iterável PRÓPRIO. Repare na separação: a coleção devolve um
#     iterador NOVO a cada `iter()`, e é o iterador que guarda a
#     posição. Misturar os dois é o erro do §6.6.
# ---------------------------------------------------------------
class Baralho:
    """Uma coleção que o `for` percorre — quantas vezes você quiser."""

    def __init__(self, cartas):
        self._cartas = list(cartas)

    def __iter__(self):
        return IteradorDeBaralho(self._cartas)

    def __len__(self):
        return len(self._cartas)


class IteradorDeBaralho:
    """Guarda a POSIÇÃO. Um por passada."""

    def __init__(self, cartas):
        self._cartas = cartas
        self._posicao = 0

    def __iter__(self):
        return self                      # iterador devolve a si mesmo

    def __next__(self):
        if self._posicao >= len(self._cartas):
            raise StopIteration          # é assim que o `for` sabe parar
        carta = self._cartas[self._posicao]
        self._posicao += 1
        return carta


def cena_1_for_desmontado():
    print("[1] O `for` DESMONTADO")
    lista = [10, 20, 30]
    iterador = iter(lista)
    print("    iter(lista) ->", type(iterador).__name__)
    print("    next:", next(iterador), next(iterador), next(iterador))
    try:
        next(iterador)
    except StopIteration:
        print("    4º next -> StopIteration  (o `for` para AQUI)")
    print()


def cena_2_iteravel_vs_iterador():
    print("[2] ITERÁVEL × ITERADOR")
    lista = [1, 2]
    iterador = iter(lista)
    print("    lista    __iter__:%-5s __next__:%s"
          % (hasattr(lista, "__iter__"), hasattr(lista, "__next__")))
    print("    iterador __iter__:%-5s __next__:%s"
          % (hasattr(iterador, "__iter__"), hasattr(iterador, "__next__")))
    print("    iter(iterador) is iterador:", iter(iterador) is iterador)
    print("    iter(lista) is iter(lista):", iter(lista) is iter(lista),
          " <- cria um NOVO a cada vez")
    print()


def cena_3_map_esgota():
    print("[3] POR QUE `map` ESGOTA (a pergunta do 04.02)")
    resultado = map(str.upper, ["a", "b"])
    print("    map tem __next__?", hasattr(resultado, "__next__"),
          "-> é um ITERADOR, não uma coleção")
    print("    list(resultado):", list(resultado))
    print("    list(resultado):", list(resultado), "<<< vazio")
    print()


def cena_4_duas_passadas():
    print("[4] DUAS PASSADAS")
    lista = [10, 20, 30]
    print("    lista, 1ª:", [x for x in lista])
    print("    lista, 2ª:", [x for x in lista])
    iterador = iter(lista)
    print("    iterador, 1ª:", [x for x in iterador])
    print("    iterador, 2ª:", [x for x in iterador], "<<< vazio")
    print()


def cena_5_range():
    print("[5] `range` NÃO É ITERADOR")
    intervalo = range(3)
    print("    range tem __next__?", hasattr(intervalo, "__next__"))
    print("    list:", list(intervalo), "· de novo:", list(intervalo))
    print("    >>> é um ITERÁVEL: cria um iterador novo a cada `for`")
    print()


def cena_6_classe_iteravel():
    print("[6] UMA CLASSE QUE O `for` PERCORRE")
    baralho = Baralho(["A♠", "K♥", "Q♦"])
    print("    1ª passada:", [c for c in baralho])
    print("    2ª passada:", [c for c in baralho], "<- funciona de novo")
    print("    len(baralho):", len(baralho))

    # Duas passadas SIMULTÂNEAS: só é possível porque cada `iter()`
    # devolve um iterador independente.
    a, b = iter(baralho), iter(baralho)
    print("    dois iteradores ao mesmo tempo:", next(a), next(b), next(a))


def main() -> None:
    cena_1_for_desmontado()
    cena_2_iteravel_vs_iterador()
    cena_3_map_esgota()
    cena_4_duas_passadas()
    cena_5_range()
    cena_6_classe_iteravel()


if __name__ == "__main__":
    main()
