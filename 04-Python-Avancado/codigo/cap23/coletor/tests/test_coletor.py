"""Os testes importam o pacote pelo nome, como qualquer pessoa faria."""

import asyncio

import pytest

from aurora_coletor import Coletor, Falha, FonteSimulada, Produto


async def test_coleta_sem_falhas() -> None:
    coletor = Coletor(FonteSimulada(latencia_s=0.01, taxa_falha=0.0),
                      limite=10)
    relatorio = await coletor.coletar(["SKU-%04d" % n for n in range(20)])
    assert len(relatorio.produtos) == 20
    assert relatorio.falhas == ()
    assert relatorio.taxa_sucesso == 1.0


async def test_sku_normalizado_e_nome_limpo() -> None:
    coletor = Coletor(FonteSimulada(latencia_s=0.01, taxa_falha=0.0))
    relatorio = await coletor.coletar(["sku-0007"])
    produto = relatorio.produtos[0]
    assert produto.sku == "SKU-0007"          # validador do 04.15
    assert produto.nome == "Produto 7"        # sem espaços sobrando


async def test_produto_e_congelado() -> None:
    coletor = Coletor(FonteSimulada(latencia_s=0.01, taxa_falha=0.0))
    relatorio = await coletor.coletar(["SKU-0001"])
    with pytest.raises(Exception):            # FrozenInstanceError
        relatorio.produtos[0].preco_centavos = 1  # type: ignore[misc]


async def test_data_em_utc() -> None:
    coletor = Coletor(FonteSimulada(latencia_s=0.01, taxa_falha=0.0))
    relatorio = await coletor.coletar(["SKU-0001"])
    momento = relatorio.produtos[0].coletado_em
    assert momento.tzinfo is not None          # consciente (04.18)
    assert momento.utcoffset() is not None
    assert momento.utcoffset().total_seconds() == 0


async def test_falha_permanente_vira_Falha() -> None:
    coletor = Coletor(FonteSimulada(latencia_s=0.01, taxa_falha=1.0),
                      tentativas=2, espera_base_s=0.001)
    relatorio = await coletor.coletar(["SKU-0001"])
    assert relatorio.produtos == ()
    assert relatorio.falhas[0].tentativas == 2
    assert isinstance(relatorio.falhas[0], Falha)


async def test_uma_falha_nao_derruba_as_outras() -> None:
    coletor = Coletor(FonteSimulada(latencia_s=0.01, taxa_falha=0.3),
                      tentativas=1, espera_base_s=0.001)
    relatorio = await coletor.coletar(["SKU-%04d" % n for n in range(30)])
    assert relatorio.total == 30
    assert relatorio.produtos                  # sobrou trabalho bom
    assert relatorio.falhas                    # e houve falhas


async def test_semaforo_limita_a_concorrencia() -> None:
    ativos, pico = 0, 0
    fonte = FonteSimulada(latencia_s=0.02, taxa_falha=0.0)
    original = fonte.consultar

    async def contando(sku: str) -> dict[str, object]:
        nonlocal ativos, pico
        ativos += 1
        pico = max(pico, ativos)
        try:
            return await original(sku)
        finally:
            ativos -= 1

    fonte.consultar = contando                 # type: ignore[method-assign]
    coletor = Coletor(fonte, limite=5)
    await coletor.coletar(["SKU-%04d" % n for n in range(40)])
    assert pico <= 5


async def test_prazo_estourado_vira_falha() -> None:
    coletor = Coletor(FonteSimulada(latencia_s=1.0, taxa_falha=0.0),
                      prazo_s=0.05, tentativas=2, espera_base_s=0.001)
    relatorio = await coletor.coletar(["SKU-0001"])
    assert len(relatorio.falhas) == 1
    assert "Timeout" in relatorio.falhas[0].motivo


async def test_coleta_concorrente_e_mais_rapida_que_sequencial() -> None:
    skus = ["SKU-%04d" % n for n in range(20)]
    fonte = FonteSimulada(latencia_s=0.05, taxa_falha=0.0)

    lento = Coletor(fonte, limite=1)
    relatorio_lento = await lento.coletar(skus)

    rapido = Coletor(FonteSimulada(latencia_s=0.05, taxa_falha=0.0),
                     limite=20)
    relatorio_rapido = await rapido.coletar(skus)

    assert relatorio_rapido.duracao_ms < relatorio_lento.duracao_ms / 3
