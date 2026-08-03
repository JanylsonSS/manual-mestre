# ------------------------------------------------------------
# ferramentas_aurora.py
# Capítulo 01.18 — Funções — parte 1
# O que este arquivo demonstra: funções com parâmetros, retorno,
#   early return, padrões imutáveis e responsabilidade única
# Como executar: python ferramentas_aurora.py
# ------------------------------------------------------------

def formatar_reais(centavos, com_simbolo=True):
    """Converte centavos (int) no formato monetário brasileiro."""
    texto = f"{centavos / 100:,.2f}"
    # O truque do 01.06, agora em UM lugar só do repositório inteiro:
    texto = texto.replace(",", "@").replace(".", ",").replace("@", ".")
    if com_simbolo:
        return "R$ " + texto
    return texto


def limpar_texto(bruto):
    """Devolve a forma canônica de um texto vindo de fora (01.06)."""
    return bruto.strip().lower()


def calcular_frete(total_centavos, cidade):
    """Devolve o frete em centavos conforme a política da Aurora."""
    # EARLY RETURN: cada caso sai na hora — sem else, sem variável temporária
    if limpar_texto(cidade) == "campinas":
        return 0                     # sede: frete grátis sempre
    if total_centavos >= 29_900:
        return 0                     # acima de R$ 299: grátis
    if total_centavos >= 10_000:
        return 990                   # entre R$ 100 e R$ 299: meio frete
    return 1_990                     # demais: frete cheio


def separar_parcelas(total_centavos, parcelas):
    """Devolve (primeira, demais) em centavos, com a sobra na primeira."""
    base = total_centavos // parcelas
    sobra = total_centavos % parcelas
    return base + sobra, base        # a vírgula monta a tupla (01.14)


def validar_codigo(codigo):
    """Diz se o código segue o formato PED-AAAA-NNNNN."""
    if len(codigo) != 14:
        return False                 # guarda barata primeiro (01.08)
    if not codigo.startswith("PED-"):
        return False
    if codigo[8] != "-":
        return False
    return "2000" <= codigo[4:8] <= "2100"


print("--- A caixa de ferramentas da Aurora ---")
print("formatar_reais(139990)          ->", formatar_reais(139_990))
print("calcular_frete(29900, 'santos') ->", calcular_frete(29_900, "santos"), "(grátis por valor)")
print("calcular_frete(5000, 'santos')  ->", calcular_frete(5_000, "santos"), "(cheio)")
print("calcular_frete(5000, 'campinas')->", calcular_frete(5_000, "campinas"), "(sede)")
primeira, demais = separar_parcelas(139_990, 3)      # desempacotamento (01.14)
print(f"separar_parcelas(139990, 3)     -> primeira {primeira}, demais {demais}")
print("limpar_texto('  CAMPINAS ')     ->", limpar_texto("  CAMPINAS "))
print("validar_codigo('PED-2026-00123')->", validar_codigo("PED-2026-00123"))
print("validar_codigo('XX-1')          ->", validar_codigo("XX-1"))

print()
print("--- O relatório, agora composto de chamadas ---")
pedidos = [
    ("PED-2026-00123", "Fone Bluetooth", 46_990, "Campinas"),
    ("PED-2026-00124", "Mouse Sem Fio", 8_990, "Santos"),
]

total_geral = 0
frete_geral = 0
for codigo, produto, valor, cidade in pedidos:
    frete = calcular_frete(valor, cidade)
    total_geral += valor
    frete_geral += frete
    # Uma linha de relatório = quatro chamadas com nome em português:
    print(f"{codigo} | {produto:<15} | {formatar_reais(valor, com_simbolo=False):>9}"
          f" | {cidade:<8} | frete {formatar_reais(frete)}")

print(f"Total: {formatar_reais(total_geral)} (+ frete {formatar_reais(frete_geral)})")

print()
print("--- Prova da eliminação de duplicação ---")
print("A conversão de reais existia em 12 lugares. Agora existe em 1.")
# Saída: (o relatório completo mostrado na seção 9 do capítulo)
