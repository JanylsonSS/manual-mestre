"""Herança: reaproveitar, sobrescrever e estender.

Seis cenas:
    [1] a busca de atributos sobe a cadeia — o MRO
    [2] super() no __init__, e o que quebra sem ele
    [3] super() ESTENDE em vez de substituir
    [4] isinstance × type — e por que a diferença importa
    [5] herança múltipla: super() segue o MRO, não a mãe direta
    [6] o MRO impossível

Uso:
    python codigo/cap10/heranca.py
"""


class Produto:
    """A classe base da Aurora."""

    def __init__(self, nome, preco_centavos):
        self.nome = nome
        self.preco_centavos = preco_centavos

    def descrever(self):
        return "%s: R$ %.2f" % (self.nome, self.preco_centavos / 100)

    def frete_centavos(self):
        return 2000                     # frete padrão


class ProdutoDigital(Produto):
    """Sobrescreve o frete e ESTENDE o __init__."""

    def __init__(self, nome, preco_centavos, tamanho_mb):
        super().__init__(nome, preco_centavos)      # a mãe primeiro
        self.tamanho_mb = tamanho_mb

    def frete_centavos(self):
        return 0                        # substitui por completo

    def descrever(self):
        # ESTENDE: aproveita a da mãe e acrescenta.
        return "%s (%d MB, sem frete)" % (super().descrever(), self.tamanho_mb)


class ProdutoSemSuper(Produto):
    """Errada de propósito: esquece a inicialização da mãe."""

    def __init__(self, nome, preco_centavos, tamanho_mb):
        self.tamanho_mb = tamanho_mb    # e o resto?


# ---------------------------------------------------------------
# [5] O diamante clássico. Note que `B.quem` chama `super()`, e o
#     `super()` de B resolve para C — não para A. Quem decide é o
#     MRO da classe da INSTÂNCIA, não a herança escrita em B.
# ---------------------------------------------------------------
class A:
    def quem(self):
        return "A"


class B(A):
    def quem(self):
        return "B -> " + super().quem()


class C(A):
    def quem(self):
        return "C -> " + super().quem()


class D(B, C):
    def quem(self):
        return "D -> " + super().quem()


def cena_1_busca():
    print("[1] A BUSCA SOBE A CADEIA")
    digital = ProdutoDigital("Ebook", 4990, 12)
    print("    MRO:", [c.__name__ for c in ProdutoDigital.__mro__])
    print("    frete (sobrescrito):", digital.frete_centavos())
    print("    frete da mãe:       ", Produto.frete_centavos(digital))
    print()


def cena_2_super_no_init():
    print("[2] super() NO __init__")
    errado = ProdutoSemSuper("Ebook", 4990, 12)
    try:
        errado.nome
    except AttributeError as erro:
        print("    sem super() ->", erro)
    print("    >>> o __init__ da mãe NÃO roda sozinho")

    certo = ProdutoDigital("Ebook", 4990, 12)
    print("    com super() -> nome: %s · tamanho: %d MB"
          % (certo.nome, certo.tamanho_mb))
    print()


def cena_3_estender():
    print("[3] super() ESTENDE EM VEZ DE SUBSTITUIR")
    print("    mãe:  ", Produto("Ebook", 4990).descrever())
    print("    filha:", ProdutoDigital("Ebook", 4990, 12).descrever())
    print("    >>> a filha reaproveita e acrescenta")
    print()


def cena_4_isinstance():
    print("[4] isinstance × type")
    digital = ProdutoDigital("Ebook", 4990, 12)
    print("    isinstance(d, Produto):    ", isinstance(digital, Produto))
    print("    type(d) is Produto:        ", type(digital) is Produto)
    print("    issubclass(Digital, Produto):", issubclass(ProdutoDigital, Produto))
    print("    >>> `type is` recusa subclasses; `isinstance` as aceita")
    print()


def cena_5_diamante():
    print("[5] HERANÇA MÚLTIPLA — super() SEGUE O MRO")
    print("    D().quem():", D().quem())
    print("    MRO de D:  ", [c.__name__ for c in D.__mro__])
    print("    >>> o super() escrito em B chamou C, não A")
    print("        B não conhece C; quem decidiu foi o MRO de D")
    print()


def cena_6_mro_impossivel():
    print("[6] MRO IMPOSSÍVEL")
    try:
        type("X", (B, A, C), {})        # class X(B, A, C)
    except TypeError as erro:
        print("    class X(B, A, C) ->", str(erro).split("\n")[0])
    print("    >>> A antes de C contradiz o MRO de B; o Python recusa")


def main() -> None:
    cena_1_busca()
    cena_2_super_no_init()
    cena_3_estender()
    cena_4_isinstance()
    cena_5_diamante()
    cena_6_mro_impossivel()


if __name__ == "__main__":
    main()
