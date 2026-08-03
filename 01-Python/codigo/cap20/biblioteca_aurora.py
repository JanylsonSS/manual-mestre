# ------------------------------------------------------------
# biblioteca_aurora.py
# Capítulo 01.20 — Módulos e imports
# O que este arquivo demonstra: um MÓDULO — só definições, com
#   autoteste protegido pelo if __name__ == "__main__"
# Como executar: python biblioteca_aurora.py   (roda o autoteste)
#   ou, de outro arquivo: import biblioteca_aurora
# ------------------------------------------------------------

# Constantes do módulo (o "Global" deste espaço de nomes — 01.19)
CIDADE_SEDE = "campinas"
FRETE_CHEIO = 1_990
FRETE_MEIO = 990


def formatar_reais(centavos, com_simbolo=True):
    """Converte centavos (int) no formato monetário brasileiro."""
    texto = f"{centavos / 100:,.2f}"
    texto = texto.replace(",", "@").replace(".", ",").replace("@", ".")
    return "R$ " + texto if com_simbolo else texto


def limpar_texto(bruto):
    """Devolve a forma canônica de um texto vindo de fora."""
    return bruto.strip().lower()


def calcular_frete(total_centavos, cidade):
    """Devolve o frete em centavos conforme a política da Aurora."""
    if limpar_texto(cidade) == CIDADE_SEDE:
        return 0
    if total_centavos >= 29_900:
        return 0
    if total_centavos >= 10_000:
        return FRETE_MEIO
    return FRETE_CHEIO


def separar_parcelas(total_centavos, parcelas):
    """Devolve (primeira, demais) em centavos, com a sobra na primeira."""
    base = total_centavos // parcelas
    return base + total_centavos % parcelas, base


def validar_codigo(codigo):
    """Diz se o código segue o formato PED-AAAA-NNNNN."""
    if len(codigo) != 14 or not codigo.startswith("PED-") or codigo[8] != "-":
        return False
    return "2000" <= codigo[4:8] <= "2100"


def montar_linha(codigo, produto, valor, cidade):
    """Devolve (não imprime!) uma linha formatada de relatório."""
    return f"{codigo} | {produto:<15} | {formatar_reais(valor):>12} | {cidade}"


# --- O INTERRUPTOR: só roda se este arquivo for executado diretamente ---
if __name__ == "__main__":
    print("--- Autoteste da biblioteca (só roda em execução direta) ---")
    casos = [
        ("formatar_reais(139990)", formatar_reais(139_990), "R$ 1.399,90"),
        ("calcular_frete(5000, 'campinas')", calcular_frete(5_000, "campinas"), 0),
        ("validar_codigo('PED-2026-00123')", validar_codigo("PED-2026-00123"), True),
    ]
    passaram = 0
    for descricao, obtido, esperado in casos:
        marca = "✓" if obtido == esperado else "✗"
        if obtido == esperado:
            passaram += 1
        print(f"{descricao} -> {obtido} [esperado {esperado}] {marca}")
    print(f"{passaram}/{len(casos)} verificações passaram.")
