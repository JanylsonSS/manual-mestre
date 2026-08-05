"""Formatação para leitura humana. Sem dependências, de propósito:
é o módulo mais importado do pacote."""

Centavos = int


def formatar_reais(centavos: Centavos) -> str:
    return "R$ %.2f" % (centavos / 100)
