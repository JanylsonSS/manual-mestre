"""O coração do projeto: concorrência com limite, prazo e tentativas.

Cada peça responde a uma pergunta diferente:

    Semaphore   quantas ao mesmo tempo?   (o teto é do OUTRO lado)
    wait_for    até quando esperar?
    tentativas  o que fazer quando falha por motivo temporário?
    gather      como juntar tudo sem perder os resultados bons?
"""

import asyncio
import logging
import time
from collections.abc import Sequence

from pydantic import ValidationError

from aurora_coletor.esquemas import ProdutoBruto
from aurora_coletor.fonte import FonteSimulada
from aurora_coletor.modelo import Falha, Produto, Relatorio
from aurora_coletor.tempo import agora

log = logging.getLogger(__name__)

# Erros que valem uma nova tentativa: são temporários por natureza.
# Um dado inválido (ValidationError) NÃO entra aqui — tentar de novo
# devolveria o mesmo dado inválido.
TEMPORARIOS = (ConnectionError, TimeoutError, asyncio.TimeoutError)


class Coletor:
    """Coleta produtos de uma fonte lenta, com limite e tentativas."""

    def __init__(self, fonte: FonteSimulada, *, limite: int = 10,
                 prazo_s: float = 1.0, tentativas: int = 3,
                 espera_base_s: float = 0.05) -> None:
        self.fonte = fonte
        self.limite = limite
        self.prazo_s = prazo_s
        self.tentativas = tentativas
        self.espera_base_s = espera_base_s
        self._semaforo = asyncio.Semaphore(limite)

    async def _uma_tentativa(self, sku: str) -> Produto:
        """Uma consulta, com prazo. Levanta o que a fonte levantar."""
        bruto = await asyncio.wait_for(self.fonte.consultar(sku),
                                       timeout=self.prazo_s)
        # A borda: o que veio de fora só vira domínio depois de validado.
        validado = ProdutoBruto.model_validate(bruto)
        return Produto(sku=validado.sku, nome=validado.nome,
                       preco_centavos=validado.preco_centavos,
                       categoria=validado.categoria, coletado_em=agora())

    async def coletar_um(self, sku: str) -> Produto | Falha:
        """Coleta um SKU. Nunca levanta — devolve Produto ou Falha."""
        async with self._semaforo:            # o teto de concorrência
            ultimo = "desconhecido"
            for numero in range(1, self.tentativas + 1):
                try:
                    produto = await self._uma_tentativa(sku)
                except TEMPORARIOS as erro:
                    ultimo = "%s: %s" % (type(erro).__name__, erro)
                    log.warning("tentativa %d de %d falhou", numero,
                                self.tentativas, extra={"sku": sku})
                    if numero < self.tentativas:
                        # Espera crescente: 1×, 2×, 4×… (§6.4)
                        await asyncio.sleep(self.espera_base_s * 2 ** (numero - 1))
                    continue
                except ValidationError as erro:
                    # Dado inválido não melhora com nova tentativa.
                    log.error("dado inválido", extra={"sku": sku})
                    return Falha(sku=sku, motivo="dado inválido: %s"
                                 % erro.errors()[0]["msg"], tentativas=numero)
                else:
                    log.info("coletado", extra={"sku": sku,
                                                "tentativas": numero})
                    return produto
            return Falha(sku=sku, motivo=ultimo, tentativas=self.tentativas)

    async def coletar(self, skus: Sequence[str]) -> Relatorio:
        inicio = time.perf_counter()
        log.info("coleta iniciada", extra={"itens": len(skus),
                                           "limite": self.limite})

        resultados = await asyncio.gather(
            *[self.coletar_um(sku) for sku in skus])

        produtos = tuple(r for r in resultados if isinstance(r, Produto))
        falhas = tuple(r for r in resultados if isinstance(r, Falha))
        duracao = (time.perf_counter() - inicio) * 1000

        log.info("coleta concluída", extra={"ok": len(produtos),
                                            "falhas": len(falhas),
                                            "ms": round(duracao, 1)})
        return Relatorio(produtos=produtos, falhas=falhas, duracao_ms=duracao)
