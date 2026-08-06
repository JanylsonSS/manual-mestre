"""O ponto de entrada: o único lugar que configura log e cria o laço."""

import argparse
import asyncio
import sys

from aurora_coletor.coletor import Coletor
from aurora_coletor.fonte import FonteSimulada
from aurora_coletor.modelo import Relatorio
from aurora_coletor.registro import configurar
from aurora_coletor.tempo import agora, para_exibir


def argumentos() -> argparse.Namespace:
    analisador = argparse.ArgumentParser(description="Coletor da Aurora")
    analisador.add_argument("--itens", type=int, default=50)
    analisador.add_argument("--limite", type=int, default=10)
    analisador.add_argument("--prazo", type=float, default=1.0)
    analisador.add_argument("--tentativas", type=int, default=3)
    analisador.add_argument("--falhas", type=float, default=0.15)
    analisador.add_argument("--formato", choices=("texto", "json"),
                            default="texto")
    analisador.add_argument("--nivel", default="INFO")
    return analisador.parse_args()


def imprimir_relatorio(relatorio: Relatorio, consultas: int) -> None:
    # `print` aqui é a SAÍDA do programa, não diagnóstico (D-030).
    print()
    print("Coleta de %s" % para_exibir(agora()))
    print("  itens:        %d" % relatorio.total)
    print("  coletados:    %d (%.0f%%)" % (len(relatorio.produtos),
                                           relatorio.taxa_sucesso * 100))
    print("  falhas:       %d" % len(relatorio.falhas))
    print("  consultas:    %d (inclui as repetidas)" % consultas)
    print("  duração:      %.0f ms" % relatorio.duracao_ms)
    if relatorio.falhas:
        print("  primeiras falhas:")
        for falha in relatorio.falhas[:3]:
            print("    %-10s %d tentativas · %s"
                  % (falha.sku, falha.tentativas, falha.motivo[:52]))


async def executar(opcoes: argparse.Namespace) -> Relatorio:
    fonte = FonteSimulada(taxa_falha=opcoes.falhas)
    coletor = Coletor(fonte, limite=opcoes.limite, prazo_s=opcoes.prazo,
                      tentativas=opcoes.tentativas)
    skus = ["SKU-%04d" % n for n in range(opcoes.itens)]
    relatorio = await coletor.coletar(skus)
    imprimir_relatorio(relatorio, fonte.consultas)
    return relatorio


def main() -> int:
    opcoes = argumentos()
    configurar(nivel=opcoes.nivel, formato=opcoes.formato)
    relatorio = asyncio.run(executar(opcoes))
    # Código de saída diferente de zero quando houve falha (02.07).
    return 0 if not relatorio.falhas else 1


if __name__ == "__main__":
    sys.exit(main())
