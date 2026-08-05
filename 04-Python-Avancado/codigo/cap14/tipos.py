"""Type hints: a anotação que o Python ignora e as ferramentas leem.

Este arquivo RODA e passa no mypy. O companheiro `defeitos.py` faz o
contrário: reúne cinco erros que o mypy encontra antes de você rodar.

ATENÇÃO ao nome (D-021): chamá-lo de `typing.py` quebraria
`from typing import ...` — o arquivo sombrearia o módulo da biblioteca
padrão. Por isso: `tipos.py`.

Seis cenas:
    [1] a anotação não é verificada em execução — e onde ela fica
    [2] o vocabulário: básicos, coleções, união, apelido
    [3] `X | None` e a verificação que o mypy passa a exigir
    [4] Protocol — o duck typing do 04.11, agora verificável
    [5] a Aurora tipada
    [6] o custo: definição × chamada

Uso:
    python codigo/cap14/tipos.py
    mypy codigo/cap14/tipos.py
"""

import timeit
from dataclasses import dataclass
from typing import Callable, Protocol

# ---------------------------------------------------------------
# [2] APELIDO DE TIPO: um nome para uma construção que se repete.
#     Lê melhor e muda num lugar só.
# ---------------------------------------------------------------
Centavos = int
TabelaDePrecos = dict[str, Centavos]
Formatador = Callable[[Centavos], str]


# ---------------------------------------------------------------
# [1] A anotação não impede nada em execução.
# ---------------------------------------------------------------
def dobrar(n: int) -> int:
    return n * 2


# ---------------------------------------------------------------
# [2] Coleções: o que entra E o que sai.
# ---------------------------------------------------------------
def somar(valores: list[Centavos]) -> Centavos:
    return sum(valores)


def agrupar_por_inicial(nomes: list[str]) -> dict[str, list[str]]:
    grupos: dict[str, list[str]] = {}
    for nome in nomes:
        grupos.setdefault(nome[0].upper(), []).append(nome)
    return grupos


def formatar_reais(centavos: Centavos) -> str:
    return "R$ %.2f" % (centavos / 100)


def aplicar(formatador: Formatador, valores: list[Centavos]) -> list[str]:
    return [formatador(valor) for valor in valores]


# ---------------------------------------------------------------
# [3] `X | None` é a assinatura mais honesta que existe: ela avisa
#     que a função às vezes não devolve nada.
# ---------------------------------------------------------------
TABELA: TabelaDePrecos = {"mouse": 8990, "teclado": 32900, "monitor": 89900}


def preco_de(nome: str) -> Centavos | None:
    return TABELA.get(nome)


def preco_formatado(nome: str) -> str:
    preco = preco_de(nome)
    if preco is None:                    # a guarda que o mypy exige
        return "produto não encontrado"
    return formatar_reais(preco)


# ---------------------------------------------------------------
# [4] PROTOCOL: descreve o que o objeto precisa TER, não de quem
#     ele precisa HERDAR. É o duck typing do 04.11, verificável.
# ---------------------------------------------------------------
class PoliticaFrete(Protocol):
    def calcular(self, peso_kg: float) -> Centavos: ...


class FreteGratis:
    def calcular(self, peso_kg: float) -> Centavos:
        return 0


class FretePorPeso:
    def __init__(self, por_kg: Centavos = 500) -> None:
        self.por_kg = por_kg

    def calcular(self, peso_kg: float) -> Centavos:
        return int(peso_kg * self.por_kg)


def cobrar_frete(politica: PoliticaFrete, peso_kg: float) -> Centavos:
    return politica.calcular(peso_kg)


# ---------------------------------------------------------------
# [5] A AURORA TIPADA. A dataclass do 04.13 já pedia anotação;
#     agora ela também diz alguma coisa às ferramentas.
# ---------------------------------------------------------------
@dataclass(frozen=True, slots=True)
class Produto:
    nome: str
    preco_centavos: Centavos
    categoria: str

    def com_desconto(self, porcento: int) -> "Produto":
        # A aspas em "Produto": a classe ainda não terminou de existir
        # quando esta linha é avaliada (§6.6).
        novo = self.preco_centavos * (100 - porcento) // 100
        return Produto(self.nome, novo, self.categoria)


def mais_caro(produtos: list[Produto]) -> Produto | None:
    if not produtos:
        return None
    return max(produtos, key=lambda p: p.preco_centavos)


def total_por_categoria(produtos: list[Produto]) -> dict[str, Centavos]:
    totais: dict[str, Centavos] = {}
    for produto in produtos:
        totais[produto.categoria] = (totais.get(produto.categoria, 0)
                                     + produto.preco_centavos)
    return totais


def cena_1_nao_verifica() -> None:
    print("[1] A ANOTAÇÃO NÃO É VERIFICADA EM EXECUÇÃO")
    print("    dobrar(4)    =", dobrar(4))
    # O `type: ignore` abaixo é a demonstração do capítulo, não um
    # descuido: a chamada é errada de propósito. O código do erro vem
    # entre colchetes, e o comentário diz o motivo (§6.8).
    errado = dobrar("ab")  # type: ignore[arg-type]  # erro proposital: §1
    print("    dobrar('ab') =", errado, "<- roda, sem reclamação")
    print("    onde ela fica:", dobrar.__annotations__)
    print("    >>> é um dicionário comum num atributo comum")
    print()


def cena_2_vocabulario() -> None:
    print("[2] O VOCABULÁRIO")
    print("    somar([8990, 32900]) ->", somar([8990, 32900]))
    print("    agrupar ->", agrupar_por_inicial(["Ana", "Bruno", "Alice"]))
    print("    aplicar(formatar_reais, ...) ->", aplicar(formatar_reais, [8990, 32900]))
    print("    apelidos: Centavos = int · TabelaDePrecos = dict[str, Centavos]")
    print("    >>> Centavos não é tipo novo: é int com um nome que explica")
    print()


def cena_3_opcional() -> None:
    print("[3] `X | None` — A ASSINATURA QUE AVISA")
    print("    preco_de('mouse')  ->", preco_de("mouse"))
    print("    preco_de('mesa')   ->", preco_de("mesa"))
    print("    preco_formatado('mouse') ->", preco_formatado("mouse"))
    print("    preco_formatado('mesa')  ->", preco_formatado("mesa"))
    print("    >>> sem a guarda `if preco is None`, o mypy recusa o código")
    print()


def cena_4_protocol() -> None:
    print("[4] PROTOCOL — DUCK TYPING VERIFICÁVEL")
    print("    FreteGratis:  ", cobrar_frete(FreteGratis(), 3.0))
    print("    FretePorPeso: ", cobrar_frete(FretePorPeso(), 3.0))
    print("    nenhuma das duas herda de PoliticaFrete:",
          FreteGratis.__bases__[0].__name__)
    print("    >>> o critério é ter o método com a assinatura certa")
    print()


def cena_5_aurora() -> None:
    print("[5] A AURORA TIPADA")
    catalogo = [
        Produto("Mouse Sem Fio", 8990, "perifericos"),
        Produto("Teclado Mecanico K2", 32900, "perifericos"),
        Produto("Fone Bluetooth XZ-9", 46990, "audio"),
    ]
    caro = mais_caro(catalogo)
    print("    mais caro:", caro.nome if caro else "catálogo vazio")
    print("    mais_caro([]) ->", mais_caro([]))
    print("    por categoria:", total_por_categoria(catalogo))
    print("    com_desconto(10):", catalogo[0].com_desconto(10))
    print()


def cena_6_custo() -> None:
    print("[6] O CUSTO ESTÁ NA DEFINIÇÃO, NÃO NA CHAMADA")
    sem = min(timeit.repeat("def f(a, b, c): pass", number=200000, repeat=3))
    com = min(timeit.repeat(
        "def f(a: int, b: str, c: list[int]) -> dict[str, int]: pass",
        number=200000, repeat=3))
    print("    definir 200 mil funções — sem: %5.1f ms · com: %5.1f ms"
          % (sem * 1000, com * 1000))

    chamada_sem = min(timeit.repeat("f(1, 'x')", "def f(a, b): return a",
                                    number=1000000, repeat=3))
    chamada_com = min(timeit.repeat("f(1, 'x')", "def f(a: int, b: str) -> int: return a",
                                    number=1000000, repeat=3))
    print("    chamar 1 milhão de vezes — sem: %5.1f ms · com: %5.1f ms"
          % (chamada_sem * 1000, chamada_com * 1000))
    print("    >>> a anotação é avaliada UMA vez, na definição; a chamada não a vê")


def main() -> None:
    cena_1_nao_verifica()
    cena_2_vocabulario()
    cena_3_opcional()
    cena_4_protocol()
    cena_5_aurora()
    cena_6_custo()


if __name__ == "__main__":
    main()
