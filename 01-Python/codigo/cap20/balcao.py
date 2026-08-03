# ------------------------------------------------------------
# balcao.py
# Capítulo 01.20 — Módulos e imports
# O que este arquivo demonstra: um SEGUNDO programa consumindo a
#   MESMA biblioteca — zero duplicação de funções
# Como executar: python balcao.py   (a partir da pasta cap20)
# ------------------------------------------------------------

from biblioteca_aurora import formatar_reais, separar_parcelas   # nomes específicos


def simular(valor_centavos, parcelas):
    """Devolve o texto da simulação de parcelamento (não imprime)."""
    primeira, demais = separar_parcelas(valor_centavos, parcelas)
    return (f"Simulação: {formatar_reais(valor_centavos)} em {parcelas}x -> "
            f"primeira {formatar_reais(primeira)}, demais {formatar_reais(demais)}")


def main():
    """Ponto de entrada do balcão."""
    print("=== Balcão Aurora (mesma biblioteca, outro programa) ===")
    print(simular(139_990, 3))


if __name__ == "__main__":
    main()
