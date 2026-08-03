# ------------------------------------------------------------
# relatorio.py
# Capítulo 01.20 — Módulos e imports
# O que este arquivo demonstra: um PROGRAMA que importa a
#   biblioteca e usa a biblioteca padrão (datetime)
# Como executar: python relatorio.py   (a partir da pasta cap20)
# ------------------------------------------------------------

from datetime import date                 # biblioteca padrão: datas prontas
import biblioteca_aurora as aurora        # nosso módulo, com apelido

PEDIDOS = [
    ("PED-2026-00123", "Fone Bluetooth", 46_990, "Campinas"),
    ("PED-2026-00124", "Mouse Sem Fio", 8_990, "Santos"),
]


def main():
    """Ponto de entrada: monta e imprime o relatório do dia."""
    print("=== Relatório Aurora (usando a biblioteca importada) ===")
    total = 0
    for codigo, produto, valor, cidade in PEDIDOS:
        total += valor
        print(aurora.montar_linha(codigo, produto, valor, cidade))
    hoje = date.today().isoformat()        # '2026-07-31' — sem formatar à mão
    print(f"Total: {aurora.formatar_reais(total)} | Gerado em {hoje}")


if __name__ == "__main__":
    main()
