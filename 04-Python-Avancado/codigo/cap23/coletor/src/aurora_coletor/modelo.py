"""O domínio: dataclasses congeladas, porque o dado já foi conferido
na borda (D-024)."""

from dataclasses import dataclass
from datetime import datetime

Centavos = int

CATEGORIAS = ("acessorios", "audio", "perifericos", "video")


@dataclass(frozen=True, slots=True)
class Produto:
    sku: str
    nome: str
    preco_centavos: Centavos
    categoria: str
    coletado_em: datetime          # sempre em UTC (04.18)

    def __post_init__(self) -> None:
        if self.preco_centavos < 0:
            raise ValueError("preço negativo: %d" % self.preco_centavos)
        if self.categoria not in CATEGORIAS:
            raise ValueError("categoria desconhecida: %r" % self.categoria)


@dataclass(frozen=True, slots=True)
class Falha:
    sku: str
    motivo: str
    tentativas: int


@dataclass(frozen=True, slots=True)
class Relatorio:
    produtos: tuple[Produto, ...]
    falhas: tuple[Falha, ...]
    duracao_ms: float

    @property
    def total(self) -> int:
        return len(self.produtos) + len(self.falhas)

    @property
    def taxa_sucesso(self) -> float:
        return len(self.produtos) / self.total if self.total else 0.0
