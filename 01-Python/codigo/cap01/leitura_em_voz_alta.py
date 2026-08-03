# ------------------------------------------------------------
# leitura_em_voz_alta.py
# Capítulo 01.01 — O que é Python e por que ele domina
# O que este arquivo demonstra: código Python se lê como texto —
#   este é o exercício de previsão da seção 4, executável
# Como executar: python leitura_em_voz_alta.py
# ------------------------------------------------------------

# Uma lista de cidades com repetições (a sintaxe de listas é o capítulo 01.12 —
# por ora, leia como o que parece ser: uma coleção entre colchetes).
cidades = ["Campinas", "Santos", "Campinas", "São Paulo", "Campinas"]

# .count(...) conta quantas vezes o valor aparece na lista.
contagem = cidades.count("Campinas")

print(contagem)
# Saída: 3
