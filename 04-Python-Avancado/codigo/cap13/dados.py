"""Dataclasses: a linha que gera os métodos que você escreveria.

ATENÇÃO ao nome deste arquivo: chamá-lo de `dataclasses.py` quebraria o
`import dataclasses` — o seu arquivo sombreia o módulo da biblioteca padrão
e o erro é `ImportError: cannot import name 'dataclass' from partially
initialized module`. Por isso: `dados.py`.

Seis cenas:
    [1] antes e depois — a contagem
    [2] a anotação é obrigatória e NÃO é verificada
    [3] default mutável: o erro que o @dataclass levanta na sua cara
    [4] frozen=True devolve o __hash__ — e o limite raso do congelamento
    [5] order, field() e __post_init__
    [6] a Aurora: catálogo, validação e serialização

Uso:
    python codigo/cap13/dados.py
"""

from dataclasses import dataclass, field, fields, asdict, replace
from dataclasses import FrozenInstanceError
from typing import ClassVar


# ---------------------------------------------------------------
# [1] A MESMA CLASSE, DUAS VEZES.
# ---------------------------------------------------------------
class ProdutoManual:
    """O que o 04.12 pediu: quatro métodos que só declaram campos."""

    def __init__(self, nome, preco_centavos, categoria):
        self.nome = nome
        self.preco_centavos = preco_centavos
        self.categoria = categoria

    def __repr__(self):
        return "%s(nome=%r, preco_centavos=%d, categoria=%r)" % (
            type(self).__name__, self.nome, self.preco_centavos, self.categoria)

    def __eq__(self, outro):
        if not isinstance(outro, ProdutoManual):
            return NotImplemented
        return ((self.nome, self.preco_centavos, self.categoria)
                == (outro.nome, outro.preco_centavos, outro.categoria))

    def __hash__(self):
        return hash((self.nome, self.preco_centavos, self.categoria))


@dataclass
class Produto:
    nome: str
    preco_centavos: int
    categoria: str


# ---------------------------------------------------------------
# [2] A ANOTAÇÃO É O QUE DEFINE O CAMPO. Sem ela, o atributo vira
#     atributo de CLASSE e some do __init__, do __repr__ e do __eq__.
# ---------------------------------------------------------------
@dataclass
class ProdutoSemAnotacao:
    """Errada de propósito: `preco_centavos` não tem anotação."""

    nome: str
    preco_centavos = 0


# ---------------------------------------------------------------
# [3] e [4] Pedido com lista, e Dinheiro congelado.
# ---------------------------------------------------------------
@dataclass
class Pedido:
    cliente: str
    itens: list = field(default_factory=list)     # nunca `itens: list = []`


@dataclass(frozen=True)
class Dinheiro:
    centavos: int

    def __str__(self):
        return "R$ %.2f" % (self.centavos / 100)


@dataclass(frozen=True)
class PedidoCongelado:
    """Congelado por fora, com uma lista mutável por dentro."""

    cliente: str
    itens: list = field(default_factory=list)


# ---------------------------------------------------------------
# [5] order compara na ORDEM DE DECLARAÇÃO dos campos.
# ---------------------------------------------------------------
@dataclass(order=True)
class ProdutoOrdenavel:
    nome: str
    preco_centavos: int


@dataclass(order=True)
class ProdutoPorPreco:
    preco_centavos: int          # primeiro campo = primeiro critério
    nome: str


# ---------------------------------------------------------------
# [6] A AURORA. __post_init__ valida e normaliza; field() esconde
#     o que não deve aparecer; ClassVar não é campo.
# ---------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class ItemPedido:
    sku: str
    quantidade: int
    preco_unitario_centavos: int

    def __post_init__(self):
        if self.quantidade <= 0:
            raise ValueError("quantidade deve ser positiva: %d" % self.quantidade)

    @property
    def total_centavos(self):
        return self.quantidade * self.preco_unitario_centavos


@dataclass
class ProdutoAurora:
    nome: str
    preco_centavos: int
    categoria: str = "acessorios"
    codigo_fornecedor: str = field(default="", repr=False)   # fora do repr
    visualizacoes: int = field(default=0, compare=False)     # fora do ==
    CATEGORIAS: ClassVar[tuple] = ("acessorios", "audio", "perifericos", "video")

    def __post_init__(self):
        self.nome = self.nome.strip()
        if self.preco_centavos < 0:
            raise ValueError("preço negativo: %d" % self.preco_centavos)
        if self.categoria not in self.CATEGORIAS:
            raise ValueError("categoria desconhecida: %r" % self.categoria)


def cena_1_a_contagem():
    print("[1] A MESMA CLASSE, DUAS VEZES")
    manual = ProdutoManual("Mouse", 8990, "perifericos")
    gerado = Produto("Mouse", 8990, "perifericos")
    print("    manual:", manual)
    print("    gerado:", gerado)
    print("    igualdade por valor:", gerado == Produto("Mouse", 8990, "perifericos"))
    print("    métodos gerados:", [n for n in ("__init__", "__repr__", "__eq__")
                                   if n in Produto.__dict__])
    print("    >>> 20 linhas viraram 4, e o __init__ gerado custa o mesmo (§13)")
    print()


def cena_2_a_anotacao():
    print("[2] A ANOTAÇÃO É OBRIGATÓRIA E NÃO É VERIFICADA")
    torto = Produto(123, "isto não é int", None)
    print("    Produto(123, 'isto não é int', None):", torto)
    print("    type(.nome):", type(torto.nome).__name__, "<- ninguém reclamou")

    print("    -- e sem anotação o campo SOME --")
    a = ProdutoSemAnotacao("Mouse")
    b = ProdutoSemAnotacao("Mouse")
    b.preco_centavos = 99999
    print("    campos reconhecidos:", [f.name for f in fields(ProdutoSemAnotacao)])
    print("    repr:", a, "<- preço ausente")
    print("    preços 0 e 99999 são iguais?", a == b, "<- o __eq__ nem olha")
    print("    >>> `preco = 0` é atributo de classe; `preco: int = 0` é campo")
    print()


def cena_3_default_mutavel():
    print("[3] DEFAULT MUTÁVEL: O ERRO QUE O @dataclass LEVANTA")
    try:
        @dataclass
        class PedidoRuim:
            itens: list = []
    except ValueError as erro:
        print("    itens: list = [] ->", erro)

    ana, bruno = Pedido("Ana"), Pedido("Bruno")
    ana.itens.append("Mouse")
    print("    com default_factory -> ana:", ana)
    print("                          bruno:", bruno, "<- listas separadas")
    print("    >>> é a armadilha do 04.01, agora detectada na DEFINIÇÃO da classe")
    print()


def cena_4_frozen():
    print("[4] frozen=True DEVOLVE O __hash__ — E CONGELA SÓ A SUPERFÍCIE")
    preco = Dinheiro(8990)
    print("    Dinheiro tem __hash__:", Dinheiro.__hash__ is not None)
    print("    em set:", {preco, Dinheiro(8990)}, "<- dois iguais, um elemento")
    try:
        preco.centavos = 1
    except FrozenInstanceError as erro:
        print("    atribuir ->", type(erro).__name__ + ":", erro)

    congelado = PedidoCongelado("Ana")
    congelado.itens.append("Mouse")
    print("    frozen com lista dentro:", congelado, "<- a lista MUDOU")
    try:
        hash(congelado)
    except TypeError as erro:
        print("    hash(congelado) ->", erro)
    print("    >>> frozen impede reatribuir o campo, não mutar o objeto dentro dele")
    print()


def cena_5_order_e_post_init():
    print("[5] order COMPARA NA ORDEM DE DECLARAÇÃO")
    catalogo = [("Monitor", 89900), ("Mouse", 8990), ("Cabo", 3490)]
    por_nome = sorted(ProdutoOrdenavel(n, p) for n, p in catalogo)
    por_preco = sorted(ProdutoPorPreco(p, n) for n, p in catalogo)
    print("    nome declarado 1º:  ", [p.nome for p in por_nome])
    print("    preço declarado 1º: ", [p.nome for p in por_preco])
    print("    >>> mover uma linha muda a ordenação de todo o sistema, sem erro")

    print("    -- __post_init__ valida DEPOIS que os campos existem --")
    try:
        ItemPedido("MOU-1", 0, 8990)
    except ValueError as erro:
        print("    quantidade 0 ->", type(erro).__name__ + ":", erro)
    item = ItemPedido("MOU-1", 2, 8990)
    print("    item válido:", item, "· total:", item.total_centavos)
    print()


def cena_6_aurora():
    print("[6] A AURORA")
    produto = ProdutoAurora("  Mouse Gamer  ", 8990, "perifericos", "FOR-77", 12)
    print("    repr:", produto)
    print("    >>> nome sem espaços, codigo_fornecedor fora do repr")
    print("    visualizações diferentes, produto igual?",
          produto == ProdutoAurora("Mouse Gamer", 8990, "perifericos", "FOR-77", 9999))

    try:
        ProdutoAurora("Mesa", 12000, "mobiliario")
    except ValueError as erro:
        print("    categoria inválida ->", erro)

    pedido = Pedido("Ana", [ItemPedido("MOU-1", 2, 8990), ItemPedido("TEC-9", 1, 24900)])
    print("    asdict recursivo:", asdict(pedido))
    print("    replace:", replace(produto, preco_centavos=7990))
    print("    >>> replace devolve um NOVO objeto; o original fica intacto:",
          produto.preco_centavos)


def main() -> None:
    cena_1_a_contagem()
    cena_2_a_anotacao()
    cena_3_default_mutavel()
    cena_4_frozen()
    cena_5_order_e_post_init()
    cena_6_aurora()


if __name__ == "__main__":
    main()
