"""A borda: o que chega da fonte externa (04.15 / D-024)."""

from pydantic import BaseModel, ConfigDict, Field, field_validator

from aurora_coletor.modelo import CATEGORIAS


class ProdutoBruto(BaseModel):
    """O formato que a fonte devolve. Nada aqui é confiável até validar."""

    model_config = ConfigDict(extra="forbid", strict=False)

    sku: str = Field(min_length=3, max_length=20)
    nome: str = Field(min_length=2, max_length=120)
    preco_centavos: int = Field(gt=0, le=10_000_00)
    categoria: str

    @field_validator("sku")
    @classmethod
    def sku_maiusculo(cls, valor: str) -> str:
        return valor.strip().upper()

    @field_validator("nome")
    @classmethod
    def nome_sem_espacos_sobrando(cls, valor: str) -> str:
        return " ".join(valor.split())

    @field_validator("categoria")
    @classmethod
    def categoria_conhecida(cls, valor: str) -> str:
        if valor not in CATEGORIAS:
            raise ValueError("categoria desconhecida: %r" % valor)
        return valor
