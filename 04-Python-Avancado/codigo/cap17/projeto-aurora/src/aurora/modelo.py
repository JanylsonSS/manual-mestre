"""Os objetos de domínio. Dataclasses, porque o dado já foi conferido
na borda (D-024)."""

from dataclasses import dataclass

Centavos = int

CATEGORIAS = ("acessorios", "audio", "perifericos", "video")


@dataclass(frozen=True, slots=True)
class Produto:
    nome: str
    preco_centavos: Centavos
    categoria: str = "acessorios"

    def __post_init__(self) -> None:
        if self.preco_centavos < 0:
            raise ValueError("preço negativo: %d" % self.preco_centavos)
        if self.categoria not in CATEGORIAS:
            raise ValueError("categoria desconhecida: %r" % self.categoria)
