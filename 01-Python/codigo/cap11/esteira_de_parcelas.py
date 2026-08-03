# ------------------------------------------------------------
# esteira_de_parcelas.py
# Capítulo 01.11 — Laço for e range
# O que este arquivo demonstra: for sobre range (tabela 2x-12x),
#   for sobre string (varredura com contadores) e range repetidor
# Como executar: python esteira_de_parcelas.py
# ------------------------------------------------------------

preco_centavos = 139_990          # R$ 1.399,90 na régua exata (01.04)

print("--- Tabela de parcelamento: Fone Bluetooth (R$ 1.399,90) ---")
# range(2, 13): parcelas de 2 a 12 — fim exclusivo, como toda régua da casa.
for parcelas in range(2, 13):
    parcela_base = preco_centavos // parcelas          # centavos, sempre
    # Exibição em reais só na borda (pacto do 01.04/01.06):
    reais = f"{parcela_base / 100:,.2f}"
    reais = reais.replace(",", "@").replace(".", ",").replace("@", ".")
    print(f"{parcelas:>2}x de R$ {reais:>9}")
# Saída: 11 linhas, de " 2x de R$    699,95" a "12x de R$    116,65"

print()
print("--- Varredura do código: PED-2026-00123 ---")
codigo = "PED-2026-00123"

# Contadores com condição — a senha do 01.10, sem andaime:
digitos = 0
letras = 0
hifens = 0
for caractere in codigo:          # a esteira serve caractere a caractere
    if "0" <= caractere <= "9":
        digitos += 1
    elif "A" <= caractere <= "Z":
        letras += 1
    elif caractere == "-":
        hifens += 1

print(f"Dígitos: {digitos} | Letras: {letras} | Hífens: {hifens}")
# Saída: Dígitos: 9 | Letras: 3 | Hífens: 2

print()
print("--- Etiquetas da caixa (range como repetidor) ---")
caixas_total = 4                  # o resultado do frete do 01.04
for numero in range(1, caixas_total + 1):   # 1..4: o +1 paga o fim exclusivo
    print(f"[Caixa {numero} de {caixas_total}]", end=" ")
print()
# Saída: [Caixa 1 de 4] [Caixa 2 de 4] [Caixa 3 de 4] [Caixa 4 de 4]
