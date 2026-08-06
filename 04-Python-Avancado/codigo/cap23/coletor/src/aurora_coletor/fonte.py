"""A fonte lenta, simulada.

Ela existe para o projeto rodar sem rede: cada consulta espera um tempo
sorteado e falha com a probabilidade configurada. `random.seed` no
construtor torna a demonstração reproduzível.
"""

import asyncio
import random
from typing import Any


class FonteSimulada:
    """Uma API de mentira, com latência e falhas controladas."""

    def __init__(self, latencia_s: float = 0.2, taxa_falha: float = 0.15,
                 semente: int = 42) -> None:
        self.latencia_s = latencia_s
        self.taxa_falha = taxa_falha
        self._sorteio = random.Random(semente)
        self.consultas = 0

    async def consultar(self, sku: str) -> dict[str, Any]:
        self.consultas += 1
        # A latência varia: parte fixa e parte sorteada, como na vida real.
        await asyncio.sleep(self.latencia_s * self._sorteio.uniform(0.5, 1.5))

        if self._sorteio.random() < self.taxa_falha:
            raise ConnectionError("a fonte não respondeu (%s)" % sku)

        numero = int(sku.split("-")[-1])
        categorias = ("acessorios", "audio", "perifericos", "video")
        return {
            "sku": sku,
            "nome": "  Produto %d  " % numero,
            "preco_centavos": 1000 + numero * 37,
            "categoria": categorias[numero % 4],
        }
