"""Operações sobre coleções de produtos."""

from aurora.modelo import Centavos, Produto


def buscar(catalogo: list[Produto], nome: str) -> Produto | None:
    for produto in catalogo:
        if produto.nome.lower() == nome.lower():
            return produto
    return None


def por_categoria(catalogo: list[Produto], categoria: str) -> list[Produto]:
    return [p for p in catalogo if p.categoria == categoria]


def total(catalogo: list[Produto]) -> Centavos:
    return sum(p.preco_centavos for p in catalogo)
