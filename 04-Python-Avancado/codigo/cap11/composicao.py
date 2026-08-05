"""Composição × herança: a contagem que decide, e os dois casos legítimos.

Seis cenas:
    [1] a explosão combinatória, contada
    [2] herança múltipla escolhendo por você — em silêncio
    [3] a mesma coisa com composição
    [4] duck typing: a política nem precisa de classe base
    [5] mixin — o caso legítimo de herança múltipla
    [6] o híbrido, que é o que se entrega na prática

Uso:
    python codigo/cap11/composicao.py
"""

import json


# ---------------------------------------------------------------
# [2] HERANÇA. Dois eixos (digital? importado?) e o kit misto
#     exige uma classe cujo nome é a JUNÇÃO dos dois.
# ---------------------------------------------------------------
class ProdutoH:
    def __init__(self, nome, preco_centavos):
        self.nome = nome
        self.preco_centavos = preco_centavos

    def frete_centavos(self):
        return 2000


class DigitalH(ProdutoH):
    def frete_centavos(self):
        return 0


class ImportadoH(ProdutoH):
    def frete_centavos(self):
        return 5000


class DigitalImportadoH(DigitalH, ImportadoH):
    """Nome que é a junção de dois — o sinal do 04.10 §9."""


# ---------------------------------------------------------------
# [3] COMPOSIÇÃO. Cada política é um objeto; a combinação é
#     escolhida na CRIAÇÃO, não codificada numa hierarquia.
# ---------------------------------------------------------------
class FreteGratis:
    def calcular(self, produto):
        return 0


class FreteFixo:
    def __init__(self, centavos):
        self.centavos = centavos

    def calcular(self, produto):
        return self.centavos


class FretePorPeso:
    def __init__(self, por_kg=500):
        self.por_kg = por_kg

    def calcular(self, produto):
        return int(produto.peso_kg * self.por_kg)


class Produto:
    def __init__(self, nome, preco_centavos, politica_frete=None, **extras):
        self.nome = nome
        self.preco_centavos = preco_centavos
        self._politica_frete = politica_frete or FreteFixo(2000)
        self.__dict__.update(extras)          # peso_kg, tamanho_mb…

    def frete_centavos(self):
        # [4] Duck typing: aceita objeto com `calcular` OU função.
        politica = self._politica_frete
        if hasattr(politica, "calcular"):
            return politica.calcular(self)
        return politica(self)


# ---------------------------------------------------------------
# [5] MIXINS: classes pequenas que acrescentam UMA capacidade e
#     não fazem sentido sozinhas. É herança múltipla disciplinada.
# ---------------------------------------------------------------
class SerializavelJSON:
    """Mixin: não tem __init__ nem estado próprio."""

    def para_json(self):
        publicos = {c: v for c, v in self.__dict__.items()
                    if not c.startswith("_")}
        return json.dumps(publicos, ensure_ascii=False)


class Comparavel:
    def __eq__(self, outro):
        return type(self) is type(outro) and self.__dict__ == outro.__dict__


class ProdutoComMixins(SerializavelJSON, Comparavel):
    def __init__(self, nome, preco_centavos):
        self.nome = nome
        self.preco_centavos = preco_centavos


# ---------------------------------------------------------------
# [6] O HÍBRIDO: herança onde há especialização real (campos
#     próprios), composição onde há eixos que se combinam.
# ---------------------------------------------------------------
class ProdutoFisico(Produto):
    def __init__(self, nome, preco_centavos, peso_kg, politica_frete=None):
        super().__init__(nome, preco_centavos,
                         politica_frete or FretePorPeso())
        self.peso_kg = peso_kg


def cena_1_contagem():
    print("[1] A EXPLOSÃO COMBINATÓRIA")
    for n in (1, 2, 3, 4):
        print("    %d característica(s): herança até %2d classes · composição %d objetos"
              % (n, 2 ** n, n))
    print()


def cena_2_heranca_decide_por_voce():
    print("[2] HERANÇA MÚLTIPLA DECIDE POR VOCÊ")
    misto = DigitalImportadoH("Ebook importado", 4990)
    print("    MRO:", [c.__name__ for c in DigitalImportadoH.__mro__])
    print("    frete:", misto.frete_centavos())
    print("    >>> DigitalH veio antes no MRO e ganhou — em SILÊNCIO")
    print("        trocar a ordem das bases muda o resultado")
    print()


def cena_3_composicao():
    print("[3] COMPOSIÇÃO — A COMBINAÇÃO É ESCOLHIDA NA CRIAÇÃO")
    print("    digital:  ", Produto("Ebook", 4990, FreteGratis()).frete_centavos())
    print("    importado:", Produto("Vinil", 9900, FreteFixo(5000)).frete_centavos())
    pesado = Produto("Monitor", 89900, FretePorPeso(), peso_kg=3)
    print("    por peso: ", pesado.frete_centavos())
    print("    >>> nenhuma classe nova para nenhuma combinação")
    print()


def cena_4_duck_typing():
    print("[4] DUCK TYPING — A POLÍTICA NEM PRECISA SER CLASSE")

    def frete_promocional(produto):
        return 0 if produto.preco_centavos > 10000 else 1500

    barato = Produto("Cabo", 3490, frete_promocional)
    caro = Produto("Monitor", 89900, frete_promocional)
    print("    função como política -> barato:", barato.frete_centavos(),
          "· caro:", caro.frete_centavos())
    print("    >>> não há classe base obrigatória: o que importa é o comportamento")
    print()


def cena_5_mixins():
    print("[5] MIXINS — HERANÇA MÚLTIPLA DISCIPLINADA")
    produto = ProdutoComMixins("Mouse", 8990)
    print("    para_json():", produto.para_json())
    print("    igualdade: ", produto == ProdutoComMixins("Mouse", 8990))
    print("    MRO:", [c.__name__ for c in ProdutoComMixins.__mro__])
    print("    >>> cada mixin dá UMA capacidade e não tem estado próprio")
    print()


def cena_6_hibrido():
    print("[6] O HÍBRIDO — O QUE SE ENTREGA NA PRÁTICA")
    fisico = ProdutoFisico("Monitor", 89900, peso_kg=3)
    print("    ProdutoFisico (herança: tem peso_kg):", fisico.frete_centavos())
    fisico_gratis = ProdutoFisico("Brinde", 0, peso_kg=1,
                                  politica_frete=FreteGratis())
    print("    o mesmo, com política trocada:      ", fisico_gratis.frete_centavos())
    print("    >>> herança para 'que coisa é'; composição para 'como se comporta'")


def main() -> None:
    cena_1_contagem()
    cena_2_heranca_decide_por_voce()
    cena_3_composicao()
    cena_4_duck_typing()
    cena_5_mixins()
    cena_6_hibrido()


if __name__ == "__main__":
    main()
