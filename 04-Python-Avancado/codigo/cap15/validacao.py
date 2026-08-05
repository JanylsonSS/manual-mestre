"""Pydantic: a mesma anotação do 04.14, agora conferida em execução.

ATENÇÃO ao nome (D-021): `pydantic.py` sombrearia a biblioteca.

Primeiro código tipado do manual sob a política do D-023: passa em
`mypy --strict`.

Seis cenas:
    [1] a fronteira — o que o verificador estático não podia conferir
    [2] coerção: o que ela aceita, e o `True` que vira 1
    [3] os erros, todos de uma vez, com o caminho até o campo aninhado
    [4] Field, validador de campo e validador de modelo
    [5] os três padrões que enganam
    [6] a Aurora: do JSON cru ao JSON de saída

Uso:
    python codigo/cap15/validacao.py
    mypy --strict codigo/cap15/validacao.py
"""

from datetime import date
from typing import Any, Literal

from pydantic import (BaseModel, ConfigDict, Field, ValidationError,
                      computed_field, field_validator, model_validator)

CATEGORIAS = Literal["acessorios", "audio", "perifericos", "video"]


# ---------------------------------------------------------------
# [1] A MESMA SINTAXE DO 04.14 — e agora ela confere.
# ---------------------------------------------------------------
class ProdutoSimples(BaseModel):
    nome: str
    preco_centavos: int
    categoria: str


# ---------------------------------------------------------------
# [4] Field() declara a restrição; os validadores fazem o que não
#     cabe numa restrição declarativa.
# ---------------------------------------------------------------
class Produto(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    nome: str = Field(min_length=2, max_length=60)
    preco_centavos: int = Field(gt=0, le=10_000_00)
    categoria: CATEGORIAS
    codigo_fornecedor: str = Field(default="", repr=False)
    estoque: int = Field(default=0, ge=0)

    @field_validator("nome")
    @classmethod
    def nome_sem_espacos_sobrando(cls, valor: str) -> str:
        return " ".join(valor.split())


class Item(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sku: str = Field(min_length=3)
    quantidade: int = Field(gt=0)
    preco_unitario_centavos: int = Field(ge=0)
    desconto_centavos: int = Field(default=0, ge=0)

    @field_validator("sku")
    @classmethod
    def sku_maiusculo(cls, valor: str) -> str:
        return valor.strip().upper()

    @model_validator(mode="after")
    def desconto_cabe_no_total(self) -> "Item":
        # Regra ENTRE campos: só dá para conferir com todos prontos.
        bruto = self.quantidade * self.preco_unitario_centavos
        if self.desconto_centavos > bruto:
            raise ValueError("desconto %d maior que o total %d"
                             % (self.desconto_centavos, bruto))
        return self

    @computed_field  # type: ignore[prop-decorator]  # limitação conhecida do mypy
    @property
    def total_centavos(self) -> int:
        return self.quantidade * self.preco_unitario_centavos - self.desconto_centavos


class Pedido(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cliente: str = Field(min_length=2)
    data: date
    itens: list[Item] = Field(min_length=1)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def total_centavos(self) -> int:
        return sum(item.total_centavos for item in self.itens)


def cena_1_a_fronteira() -> None:
    print("[1] A FRONTEIRA")
    bruto: dict[str, Any] = {"nome": "Mouse", "preco_centavos": "8990",
                             "categoria": "perifericos"}
    produto = ProdutoSimples(**bruto)
    print("    entrou como texto:", repr(bruto["preco_centavos"]))
    print("    saiu como       :", repr(produto.preco_centavos),
          "· tipo", type(produto.preco_centavos).__name__)
    print("    >>> o 04.14 conferiu o SEU código; isto confere o DADO")
    print()


def cena_2_coercao() -> None:
    print("[2] O QUE A COERÇÃO ACEITA")
    candidatos: list[object] = ["8990", 8990.0, 8990.7, True, "  8990  ",
                                b"8990", "8_990", None]
    for valor in candidatos:
        try:
            # O mypy recusa `object` onde a anotação diz `int`, e está certo:
            # o contrato declarado é `int`. O Pydantic aceita e converte, e
            # também está certo: ele confere o DADO, não a declaração. As duas
            # ferramentas discordam porque olham coisas diferentes (§6.2).
            convertido = ProdutoSimples(nome="Mouse",
                                        preco_centavos=valor,  # type: ignore[arg-type]
                                        categoria="perifericos")
            print("    %-12r -> %r" % (valor, convertido.preco_centavos))
        except ValidationError as erro:
            print("    %-12r -> RECUSADO (%s)"
                  % (valor, erro.errors()[0]["type"]))
    print("    >>> `True` vira 1: um preço de UM CENTAVO, sem erro nenhum")
    print()


def cena_3_erros() -> None:
    print("[3] TODOS OS ERROS DE UMA VEZ")
    try:
        Produto(nome="M", preco_centavos=-1, categoria="mobiliario",  # type: ignore[arg-type]
                estoque=-5)
    except ValidationError as erro:
        for detalhe in erro.errors():
            print("    %-18s %s" % (detalhe["loc"][0], detalhe["msg"][:64]))
    print("    >>> quatro campos, quatro mensagens — como o mypy no 04.14")

    print("    -- e o caminho até o campo aninhado --")
    ruim = ('{"cliente": "Ana", "data": "15/07/2026",'
            ' "itens": [{"sku": "MOU-1", "quantidade": 0,'
            ' "preco_unitario_centavos": 8990}]}')
    try:
        Pedido.model_validate_json(ruim)
    except ValidationError as erro:
        for detalhe in erro.errors():
            print("    loc=%-28s %s" % (str(detalhe["loc"]), detalhe["msg"][:44]))
    print("    >>> ('itens', 0, 'quantidade') aponta o item exato da lista")
    print()


def cena_4_validadores() -> None:
    print("[4] Field, VALIDADOR DE CAMPO E VALIDADOR DE MODELO")
    print("    normalizado:", Item(sku="  mou-1 ", quantidade=2,
                                   preco_unitario_centavos=8990))
    try:
        Item(sku="MOU-1", quantidade=1, preco_unitario_centavos=100,
             desconto_centavos=500)
    except ValidationError as erro:
        print("    regra entre campos ->", erro.errors()[0]["msg"])
    print("    >>> Field para o que cabe numa restrição; validador para o resto")
    print()


def cena_5_os_tres_que_enganam() -> None:
    print("[5] OS TRÊS PADRÕES QUE ENGANAM")

    class PedidoIngenuo(BaseModel):
        cliente: str
        desconto_centavos: int = 0

    typo = PedidoIngenuo(cliente="Ana", descconto_centavos=5000)  # type: ignore[call-arg]
    print("    (a) campo com erro de digitação:", typo)
    print("        o desconto de R$ 50,00 SUMIU, sem aviso")
    print("        correção: model_config = ConfigDict(extra='forbid')")

    produto = ProdutoSimples(nome="Mouse", preco_centavos=8990,
                             categoria="perifericos")
    produto.preco_centavos = -999
    print("    (b) atribuição depois da criação:", produto.preco_centavos)
    print("        validação acontece na ENTRADA; correção: validate_assignment")

    class ComOpcional(BaseModel):
        talvez: int | None

    try:
        ComOpcional()  # type: ignore[call-arg]
    except ValidationError as erro:
        print("    (c) `int | None` SEM default ->", erro.errors()[0]["msg"])
        print("        `| None` fala do tipo, não da obrigatoriedade")
    print()


def cena_6_aurora() -> None:
    print("[6] A AURORA: DO JSON CRU AO JSON DE SAÍDA")
    bruto = ('{"cliente": "Ana", "data": "2026-07-15",'
             ' "itens": [{"sku": "mou-1", "quantidade": "2",'
             ' "preco_unitario_centavos": 8990},'
             ' {"sku": "tec-9", "quantidade": 1,'
             ' "preco_unitario_centavos": 32900}]}')
    pedido = Pedido.model_validate_json(bruto)
    print("    cliente:", pedido.cliente, "· data:", pedido.data,
          "(%s)" % type(pedido.data).__name__)
    print("    sku normalizado:", pedido.itens[0].sku,
          "· quantidade '2' ->", pedido.itens[0].quantidade)
    print("    total:", pedido.total_centavos)
    print("    saída:", pedido.model_dump_json())
    print("    >>> o total é @computed_field e ENTRA na saída (04.13/D1)")


def main() -> None:
    cena_1_a_fronteira()
    cena_2_coercao()
    cena_3_erros()
    cena_4_validadores()
    cena_5_os_tres_que_enganam()
    cena_6_aurora()


if __name__ == "__main__":
    main()
