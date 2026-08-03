# ------------------------------------------------------------
# laudos_da_aurora.py
# Capítulo 01.08 — Booleanos, comparações e truthiness
# O que este arquivo demonstra: laudo-mestre com and, truthiness
#   dos valores de borda, curto-circuito como escudo e valor-padrão
# Como executar: python laudos_da_aurora.py
# ------------------------------------------------------------

print("--- Cena 1: laudo-mestre do código ---")
codigo = "PED-2026-00123"

# As verificações do inspetor (01.05/D1), agora combináveis.
len_ok = len(codigo) == 14
prefixo_ok = codigo.startswith("PED-")
hifens_ok = codigo[3] == "-" and codigo[8] == "-"
ano_ok = "2000" <= codigo[4:8] <= "2100"     # encadeamento nativo

print("len ok:", len_ok, "| prefixo ok:", prefixo_ok,
      "| hífens ok:", hifens_ok, "| ano ok:", ano_ok)

# O laudo-mestre: TODAS precisam passar. len_ok vem primeiro de propósito:
# se o código for curto demais, o and para nele — e as fatias das
# verificações seguintes nem executam (curto-circuito como guarda).
codigo_valido = len_ok and prefixo_ok and hifens_ok and ano_ok
print("CÓDIGO VÁLIDO?", codigo_valido)
# Saída: CÓDIGO VÁLIDO? True

print()
print("--- Cena 2: truthiness na borda ---")
# Os quatro valores que a borda do 01.07 produz de verdade:
print("bool('') =", bool(""), "| bool('0') =", bool("0"),
      "| bool(' ') =", bool(" "), "| bool('False') =", bool("False"))
# Saída: bool('') = False | bool('0') = True | bool(' ') = True | bool('False') = True
# Truthiness pergunta "é algo ou é nada?" — nunca "o que está escrito?".

print()
print("--- Cena 3: escudo e valor-padrão ---")
total_centavos = 46_990
quantidade = 0

# ESCUDO: a guarda vem primeiro; com quantidade 0, a divisão nem roda.
ticket_alto = quantidade != 0 and (total_centavos / quantidade) > 10_000
print("Ticket médio seguro (qtd=0):", ticket_alto, "(divisão nem executou)")
# Saída: Ticket médio seguro (qtd=0): False (divisão nem executou)

# VALOR-PADRÃO: or devolve o primeiro operando truthy.
nome_digitado = ""                       # o Enter direto do 01.07
nome_final = nome_digitado or "visitante"
print("Cliente sem nome vira:", repr(nome_final))
# Saída: Cliente sem nome vira: 'visitante'
