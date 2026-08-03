# ------------------------------------------------------------
# relatorio_com_bug.py
# Capítulo 01.24 — Depuração no VS Code
# O que este arquivo demonstra: dois bugs SILENCIOSOS plantados
#   para serem caçados com o depurador (nenhum quebra o programa)
# Como executar: python relatorio_com_bug.py   (ou F5 no VS Code)
# ------------------------------------------------------------

VENDAS = [
    ("PED-1", 46_990, "Campinas"),
    ("PED-2", 8_990, " santos "),
    ("PED-3", 34_900, "CAMPINAS"),
    ("PED-4", 9_890, "Sorocaba"),
    ("PED-5", 47_890, "campinas"),
    ("PED-6", 34_900, "São Paulo"),
    ("PED-7", 12_990, "Santos"),
    ("PED-8", 15_990, "são paulo"),
    ("PED-9", 4_990, "Campinas"),
    ("PED-10", 23_900, "Santos"),
]


def formatar_reais(centavos):
    """Converte centavos no formato monetário brasileiro."""
    texto = f"{centavos / 100:,.2f}"
    return texto.replace(",", "@").replace(".", ",").replace("@", ".")


def agregar(vendas):
    """Devolve (totais, contagem) por cidade canônica."""
    totais = {}
    contagem = {}
    for codigo, valor, cidade in vendas:
        chave = cidade.strip().lower()
        totais[chave] = totais.get(chave, 0) + valor
        contagem[chave] = contagem.get(chave, 0) + 1
    return totais, contagem


def main():
    """Monta e imprime o relatório (com os bugs plantados)."""
    print("=== Relatório de vendas (COM BUG) ===")
    totais, contagem = agregar(VENDAS)

    total_geral = 0
    for cidade, total in totais.items():
        plural = "pedidos" if contagem[cidade] > 1 else "pedido "
        print(f"{cidade:<11} | {contagem[cidade]} {plural} | R$ {formatar_reais(total):>10}")

        # >>> BUG 1 (breakpoint aqui): atribuição no lugar de acumulação.
        # A hipótese da seção 9 se confirma observando esta variável por volta.
        total_geral = total           # deveria ser: total_geral += total

    print(f"\nTotal geral: R$ {formatar_reais(total_geral)}")

    # >>> BUG 2 (para o exercício AP3): o ticket médio usa o denominador errado.
    # Sintoma: o valor sai maior do que deveria. Cace-o com o depurador —
    # dica: ponha 'len(totais)' e 'sum(contagem.values())' no painel Watch.
    ticket_medio = total_geral // len(totais)
    print(f"Ticket médio: R$ {formatar_reais(ticket_medio)}")


if __name__ == "__main__":
    main()
