"""Cinco defeitos que o mypy encontra antes de o programa rodar.

Este arquivo QUEBRA DE PROPÓSITO. Rode as duas coisas e compare:

    mypy codigo/cap14/defeitos.py      # aponta os seis erros de uma vez
    python codigo/cap14/defeitos.py    # explode no primeiro e para

A diferença entre as duas saídas é o argumento inteiro do capítulo.
"""


# ---------------------------------------------------------------
# [1] Tipo de argumento errado. Roda — e produz "abab", que é lixo
#     circulando com aparência de resultado.
# ---------------------------------------------------------------
def dobrar(n: int) -> int:
    return n * 2


dobrar("ab")


# ---------------------------------------------------------------
# [2] Um ramo sem `return`. Quem chamar recebe None sem saber.
# ---------------------------------------------------------------
def classificar(preco_centavos: int) -> str:
    if preco_centavos > 10000:
        return "caro"
    elif preco_centavos > 1000:
        return "medio"
    # o ramo "barato" não devolve nada


# ---------------------------------------------------------------
# [3] O clássico: `X | None` usado sem verificar. É o único destes
#     que o interpretador também pega — e só quando o dado certo
#     (o ausente) aparecer, que pode ser em produção.
# ---------------------------------------------------------------
def buscar_nome(id_cliente: int) -> str | None:
    if id_cliente == 1:
        return "Ana"
    return None


nome = buscar_nome(2)
print(nome.upper())


# ---------------------------------------------------------------
# [4] Retorno com o tipo errado. `/` devolve float; a assinatura
#     promete int. Roda em silêncio e contamina tudo adiante.
# ---------------------------------------------------------------
def total_centavos(itens: list[int]) -> int:
    return sum(itens) / 100


# ---------------------------------------------------------------
# [5] Chave e valor trocados num dicionário declarado.
# ---------------------------------------------------------------
precos: dict[str, int] = {"mouse": 8990}
precos[1] = "caro"
