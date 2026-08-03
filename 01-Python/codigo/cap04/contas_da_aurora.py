# ------------------------------------------------------------
# contas_da_aurora.py
# Capítulo 01.04 — Números e operadores
# O que este arquivo demonstra: frete (// e %), parcelamento com
#   centavos inteiros (dinheiro exato) e troco em cascata
# Como executar: python contas_da_aurora.py
# ------------------------------------------------------------

print("--- Conta 1: frete por caixas ---")
itens = 20
itens_por_caixa = 6

caixas_cheias = itens // itens_por_caixa   # quantas caixas completas cabem
resto = itens % itens_por_caixa            # itens que sobram fora delas

# Se sobrou item, precisamos de uma caixa a mais (aritmética de contar,
# sem float no caminho). O int(...) converte o True/False da comparação
# em 1/0 — truque honesto que o capítulo 01.08 destrincha.
caixas_total = caixas_cheias + int(resto > 0)

print("Itens:", itens, "| caixas cheias:", caixas_cheias, "| sobram:", resto)
print("Caixas a cobrar:", caixas_total)
# Saída: Caixas a cobrar: 4

print()
print("--- Conta 2: parcelamento com centavos inteiros ---")
preco_centavos = 139_990        # R$ 1.399,90 guardado na régua EXATA
parcelas = 3

parcela_base = preco_centavos // parcelas   # 46663 centavos
sobra = preco_centavos % parcelas           # 1 centavo — vai na primeira

parcela_1 = parcela_base + sobra
print("Parcela 1:", parcela_1, "| Parcelas 2 e 3:", parcela_base, "cada")
prova = parcela_1 + parcela_base + parcela_base
print("Prova:", prova, "centavos (exato!)")
# Saída: Prova: 139990 centavos (exato!)

print()
print("--- O mesmo, ingenuamente com float ---")
preco_float = 1399.90
parcela_float = preco_float / 3
print("1399.9 / 3 =", parcela_float)
print("466.63 * 3 =", 466.63 * 3, " (sumiu dinheiro!)")
# Saída: 466.63 * 3 = 1398.8899999999999  (sumiu dinheiro!)

print()
print("--- Conta 3: troco em cascata ---")
troco = 87   # em reais inteiros, para o balcão

notas_50 = troco // 50
resta = troco % 50
notas_20 = resta // 20
resta = resta % 20
notas_10 = resta // 10
resta = resta % 10

print("Troco de R$", troco, "-> 50:", notas_50, "| 20:", notas_20,
      "| 10:", notas_10, "| resta R$", resta)
# Saída: Troco de R$ 87 -> 50: 1 | 20: 1 | 10: 1 | resta R$ 7
