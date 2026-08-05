"""Encapsulamento em Python: convenção, mangling, property e slots.

Seis cenas:
    [1] os três níveis de "privado" — e nenhum esconde de verdade
    [2] o propósito REAL do __ : evitar colisão em herança
    [3] property: intercepta leitura e escrita sem mudar a interface
    [4] property somente-leitura para valores derivados
    [5] __slots__: a única forma de recusar atributo inventado
    [6] a Aurora: validação que não depende de ninguém lembrar

Uso:
    python codigo/cap09/encapsulamento.py
"""

import time
import tracemalloc


# ---------------------------------------------------------------
# [1] Três atributos, três convenções — e o `__dict__` revela tudo.
# ---------------------------------------------------------------
class Conta:
    def __init__(self):
        self.saldo = 100            # público
        self._interno = "conv"      # convenção: "não mexa"
        self.__secreto = "mangle"   # name mangling: vira _Conta__secreto


# ---------------------------------------------------------------
# [2] O motivo de o `__` existir: uma subclasse pode ter um
#     atributo de mesmo nome sem sobrescrever o da mãe.
# ---------------------------------------------------------------
class Base:
    def __init__(self):
        self.__estado = "da base"       # vira _Base__estado

    def ler_base(self):
        return self.__estado


class Filha(Base):
    def __init__(self):
        super().__init__()
        self.__estado = "da filha"      # vira _Filha__estado — NÃO colide

    def ler_filha(self):
        return self.__estado


# ---------------------------------------------------------------
# [3] e [6] property: a validação vira parte do objeto, e a
#     interface de quem usa não muda uma vírgula.
# ---------------------------------------------------------------
class Produto:
    def __init__(self, nome, preco_centavos):
        self.nome = nome
        self.preco_centavos = preco_centavos    # passa pelo setter

    @property
    def preco_centavos(self):
        return self._preco_centavos

    @preco_centavos.setter
    def preco_centavos(self, valor):
        if not isinstance(valor, int):
            raise TypeError("preço deve ser inteiro em centavos, não %s"
                            % type(valor).__name__)
        if valor < 0:
            raise ValueError("preço não pode ser negativo: %d" % valor)
        self._preco_centavos = valor

    # ---------- [4] somente-leitura: derivado, não guardado
    @property
    def preco_reais(self):
        return self._preco_centavos / 100


# ---------------------------------------------------------------
# [5] __slots__ recusa o atributo que não foi declarado — e é a
#     única defesa contra `self.prceo = 10` (04.07/A3.4).
# ---------------------------------------------------------------
class ProdutoComSlots:
    __slots__ = ("nome", "preco_centavos")

    def __init__(self, nome, preco_centavos):
        self.nome = nome
        self.preco_centavos = preco_centavos


def cena_1_tres_niveis():
    print("[1] OS TRÊS NÍVEIS DE 'PRIVADO'")
    conta = Conta()
    print("    público:  ", conta.saldo)
    print("    _interno: ", conta._interno, "<- só convenção, acessível")
    try:
        conta.__secreto
    except AttributeError as erro:
        print("    __secreto:", erro)
    print("    mas:      ", conta._Conta__secreto, "<- foi RENOMEADO, não escondido")
    print("    __dict__: ", conta.__dict__)
    print()


def cena_2_proposito_do_mangling():
    print("[2] O PROPÓSITO REAL DO `__`")
    filha = Filha()
    print("    ler_base(): ", filha.ler_base())
    print("    ler_filha():", filha.ler_filha())
    print("    __dict__:   ", filha.__dict__)
    print("    >>> os dois convivem — é para ISSO que o mangling existe")
    print()


def cena_3_property():
    print("[3] property — MESMA INTERFACE, CÓDIGO POR TRÁS")
    produto = Produto("Mouse", 8990)
    print("    p.preco_centavos:", produto.preco_centavos, "(parece atributo)")
    produto.preco_centavos = 7990
    print("    após atribuir 7990:", produto.preco_centavos)

    for valor, rotulo in [(-100, "negativo"), (89.9, "float")]:
        try:
            produto.preco_centavos = valor
        except (ValueError, TypeError) as erro:
            print("    %-9s -> %s: %s" % (rotulo, type(erro).__name__, erro))
    print("    o que está na classe:", type(Produto.__dict__["preco_centavos"]).__name__)
    print()


def cena_4_somente_leitura():
    print("[4] property SOMENTE-LEITURA (valor derivado)")
    produto = Produto("Mouse", 8990)
    print("    p.preco_reais:", produto.preco_reais)
    try:
        produto.preco_reais = 99
    except AttributeError as erro:
        print("    p.preco_reais = 99 ->", erro)
    print("    >>> derivado não se guarda: não há como ficar dessincronizado")
    print()


def cena_5_slots():
    print("[5] __slots__ — RECUSA O ATRIBUTO INVENTADO")
    sem = Produto("Mouse", 8990)
    sem.prceo = 10                      # erro de digitação, aceito em silêncio
    print("    sem slots -> p.prceo =", sem.prceo, "(nenhum erro!)")

    com = ProdutoComSlots("Mouse", 8990)
    try:
        com.prceo = 10
    except AttributeError as erro:
        print("    com slots ->", erro)

    print("    tem __dict__?  sem:", hasattr(sem, "__dict__"),
          "· com:", hasattr(com, "__dict__"))

    # A memória, medida.
    quantidade = 200_000
    for rotulo, classe in (("sem slots", Produto), ("com slots", ProdutoComSlots)):
        tracemalloc.start()
        objetos = [classe("x", i) for i in range(quantidade)]
        _, pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print("    %s: %5.1f MB para %d objetos" % (rotulo, pico / 1e6, quantidade))
        del objetos
    print()


def cena_6_o_custo():
    print("[6] O CUSTO DA property")

    class Direto:
        def __init__(self):
            self.x = 1

    class ComProperty:
        def __init__(self):
            self._x = 1

        @property
        def x(self):
            return self._x

    for rotulo, objeto in (("atributo direto", Direto()), ("property", ComProperty())):
        inicio = time.perf_counter()
        for _ in range(1_000_000):
            objeto.x
        print("    %-16s %6.1f ms por 1M leituras"
              % (rotulo, (time.perf_counter() - inicio) * 1000))
    print("    >>> ~45% mais lento, e irrelevante fora de laço quente")


def main() -> None:
    cena_1_tres_niveis()
    cena_2_proposito_do_mangling()
    cena_3_property()
    cena_4_somente_leitura()
    cena_5_slots()
    cena_6_o_custo()


if __name__ == "__main__":
    main()
