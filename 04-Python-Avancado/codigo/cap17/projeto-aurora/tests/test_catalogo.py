"""Os testes importam `aurora` como qualquer pessoa de fora importaria
— pelo pacote instalado, não por caminho relativo (§6.4)."""

import pytest

from aurora import Produto, formatar_reais
from aurora.catalogo import buscar, por_categoria, total

CATALOGO = [
    Produto("Mouse", 8990, "perifericos"),
    Produto("Fone", 46990, "audio"),
]


def test_formatar_reais() -> None:
    assert formatar_reais(8990) == "R$ 89.90"


def test_buscar_ignora_maiusculas() -> None:
    achado = buscar(CATALOGO, "mOuSe")
    assert achado is not None and achado.preco_centavos == 8990


def test_buscar_devolve_none() -> None:
    assert buscar(CATALOGO, "Mesa") is None


def test_por_categoria() -> None:
    assert [p.nome for p in por_categoria(CATALOGO, "audio")] == ["Fone"]


def test_total() -> None:
    assert total(CATALOGO) == 55980


def test_categoria_invalida() -> None:
    with pytest.raises(ValueError, match="categoria desconhecida"):
        Produto("Mesa", 12000, "mobiliario")
