"""Métodos especiais: os que a linguagem chama por você.

Seis cenas:
    [1] __repr__ × __str__ — e por que só um serve de reserva
    [2] __eq__ torna o objeto NÃO-hasheável (o efeito colateral)
    [3] __len__ decide a verdade booleana
    [4] __getitem__ dá indexação, iteração E `in` de graça
    [5] operadores: __add__, __lt__ e a reflexão que dá `>` grátis
    [6] a Aurora: um Dinheiro que se comporta como número

Uso:
    python codigo/cap12/dunder.py
"""

import functools


# ---------------------------------------------------------------
# [1] A regra: __repr__ é para QUEM DEPURA (deve ser inequívoco);
#     __str__ é para QUEM LÊ (deve ser legível).
# ---------------------------------------------------------------
class Produto:
    def __init__(self, nome, preco_centavos):
        self.nome = nome
        self.preco_centavos = preco_centavos

    def __repr__(self):
        # type(self).__name__, não "Produto" fixo (04.10/A1.6).
        return "%s(nome=%r, preco_centavos=%d)" % (
            type(self).__name__, self.nome, self.preco_centavos)

    def __str__(self):
        return "%s — R$ %.2f" % (self.nome, self.preco_centavos / 100)

    # [2] __eq__ define igualdade POR VALOR…
    def __eq__(self, outro):
        if not isinstance(outro, Produto):
            return NotImplemented          # deixa o outro lado tentar
        return (self.nome, self.preco_centavos) == (outro.nome,
                                                    outro.preco_centavos)

    # …e sem __hash__ o objeto deixaria de entrar em set/dict.
    def __hash__(self):
        return hash((self.nome, self.preco_centavos))


class ProdutoSemHash:
    """Errada de propósito: define __eq__ e esquece __hash__."""

    def __init__(self, nome):
        self.nome = nome

    def __eq__(self, outro):
        return isinstance(outro, ProdutoSemHash) and self.nome == outro.nome


# ---------------------------------------------------------------
# [3] e [4] Uma coleção que se comporta como as embutidas.
# ---------------------------------------------------------------
class Catalogo:
    def __init__(self, produtos=None):
        self._produtos = list(produtos or [])

    def __len__(self):
        return len(self._produtos)              # dá len() E bool()

    def __getitem__(self, indice):
        return self._produtos[indice]           # dá [], for, in e fatias

    def __repr__(self):
        return "Catalogo(%d produtos)" % len(self._produtos)


# ---------------------------------------------------------------
# [5] e [6] Operadores. @total_ordering gera os outros três a
#     partir de __eq__ e __lt__.
# ---------------------------------------------------------------
@functools.total_ordering
class Dinheiro:
    def __init__(self, centavos):
        self.centavos = int(centavos)

    def __repr__(self):
        return "Dinheiro(%d)" % self.centavos

    def __str__(self):
        return "R$ %.2f" % (self.centavos / 100)

    def __eq__(self, outro):
        if not isinstance(outro, Dinheiro):
            return NotImplemented
        return self.centavos == outro.centavos

    def __lt__(self, outro):
        if not isinstance(outro, Dinheiro):
            return NotImplemented
        return self.centavos < outro.centavos

    def __add__(self, outro):
        if not isinstance(outro, Dinheiro):
            return NotImplemented
        return Dinheiro(self.centavos + outro.centavos)

    def __mul__(self, fator):
        return Dinheiro(round(self.centavos * fator))

    def __rmul__(self, fator):
        return self * fator                     # 3 * dinheiro

    def __hash__(self):
        return hash(self.centavos)

    def __bool__(self):
        return self.centavos != 0


def cena_1_repr_str():
    print("[1] __repr__ × __str__")
    produto = Produto("Mouse", 8990)
    print("    str(p): ", str(produto))
    print("    repr(p):", repr(produto))
    print("    print(p):", produto)
    print("    numa lista:", [produto], "<- listas usam __repr__")

    class SoStr:
        def __str__(self):
            return "bonito"

    print("    só __str__ -> repr:", repr(SoStr())[:38] + "…")
    print("    >>> __repr__ serve de reserva para __str__; o contrário não")
    print()


def cena_2_eq_e_hash():
    print("[2] __eq__ TORNA O OBJETO NÃO-HASHEÁVEL")
    sem_hash = ProdutoSemHash("Mouse")
    print("    igualdade funciona:", sem_hash == ProdutoSemHash("Mouse"))
    try:
        {sem_hash}
    except TypeError as erro:
        print("    mas em set ->", erro)

    com_hash = Produto("Mouse", 8990)
    iguais = {com_hash, Produto("Mouse", 8990)}
    print("    com __hash__ -> set com dois iguais tem", len(iguais), "elemento")
    print("    >>> definir __eq__ apaga o __hash__ herdado; declare os dois")
    print()


def cena_3_len_e_bool():
    print("[3] __len__ DECIDE A VERDADE BOOLEANA")
    vazio, cheio = Catalogo(), Catalogo([1, 2, 3])
    print("    len:", len(vazio), len(cheio))
    print("    bool:", bool(vazio), bool(cheio))
    print("    `if catalogo:` funciona sem escrever __bool__")

    class SemNada:
        pass

    print("    objeto sem __len__ nem __bool__:", bool(SemNada()), "<- sempre True")
    print()


def cena_4_getitem():
    print("[4] __getitem__ DÁ QUATRO COISAS DE GRAÇA")
    catalogo = Catalogo(["Mouse", "Teclado", "Monitor"])
    print("    indexação: ", catalogo[0], "·", catalogo[-1])
    print("    fatia:     ", catalogo[0:2])
    print("    iteração:  ", [p for p in catalogo], "<- SEM __iter__")
    print("    operador in:", "Teclado" in catalogo)
    print("    >>> é o protocolo antigo de sequência (04.05 §7)")
    print()


def cena_5_operadores():
    print("[5] OPERADORES")
    a, b = Dinheiro(8990), Dinheiro(1010)
    print("    a + b:  ", a + b)
    print("    a * 3:  ", a * 3)
    print("    3 * a:  ", 3 * a, "<- __rmul__")
    print("    a > b:  ", a > b, "<- gerado por @total_ordering")
    print("    sorted: ", sorted([Dinheiro(500), Dinheiro(100), Dinheiro(300)]))
    print("    bool(Dinheiro(0)):", bool(Dinheiro(0)))

    try:
        a + 100
    except TypeError as erro:
        print("    a + 100 ->", erro)
    print("    >>> NotImplemented vira TypeError com mensagem útil")


def main() -> None:
    cena_1_repr_str()
    cena_2_eq_e_hash()
    cena_3_len_e_bool()
    cena_4_getitem()
    cena_5_operadores()


if __name__ == "__main__":
    main()
