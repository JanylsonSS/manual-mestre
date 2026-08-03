# ------------------------------------------------------------
# balcao_parcelamento.py
# Capítulo 01.07 — Entrada e saída
# O que este arquivo demonstra: input + esteira da borda (limpar,
#   validar, converter) + parcelamento em centavos + saída formatada
# Como executar: python balcao_parcelamento.py
# ------------------------------------------------------------

print("=== Balcão Aurora — consulta de parcelamento ===")

# --- Entrada 1: o valor (aceita "R$ 1.399,90", "1399,90", "1399") ---
valor_texto = input("Valor do produto (ex.: 1399,90): ")

# Alfândega do 01.06: tirar R$, espaços e o ponto de milhar; vírgula vira ponto.
valor_texto = valor_texto.strip().replace("R$", "").strip()
valor_texto = valor_texto.replace(".", "").replace(",", ".")

# Laudo antes da conversão: float aceita 1 ponto — validamos removendo-o.
# (Defesa honesta e limitada: "12.3.4" ainda derrubaria o float; o caso
#  está documentado e espera as exceções do 01.21.)
eh_numero = valor_texto.replace(".", "", 1).isdigit()
print("Valor reconhecido?", eh_numero)

valor_centavos = int(float(valor_texto) * 100)   # p/ a régua EXATA (01.04)

# --- Entrada 2: as parcelas (int puro, laudo direto) ---
parcelas_texto = input("Número de parcelas (2 a 12): ").strip()
print("Parcelas reconhecidas?", parcelas_texto.isdigit())
parcelas = int(parcelas_texto)

# --- Eco: confirmar o que foi entendido ANTES de responder ---
reais_eco = f"{valor_centavos / 100:,.2f}"
reais_eco = reais_eco.replace(",", "@").replace(".", ",").replace("@", ".")
print()
print(f"Entendi: R$ {reais_eco} em {parcelas}x.")
print("-" * 32)

# --- O parcelador do 01.04, intacto: centavos, sobra na primeira ---
parcela_base = valor_centavos // parcelas
sobra = valor_centavos % parcelas
parcela_1 = parcela_base + sobra

reais_parcela_1 = f"{parcela_1 / 100:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
reais_parcela_n = f"{parcela_base / 100:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")

print(f"Parcela 1:  R$ {reais_parcela_1}")
print(f"Parcelas 2 a {parcelas}:  R$ {reais_parcela_n}")

# Prova dos nove exibida — o balcão confere na frente do cliente.
total_prova = parcela_1 + parcela_base * (parcelas - 1)
reais_prova = f"{total_prova / 100:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
print(f"Total conferido: R$ {reais_prova}")
print("=" * 32)

# Saída: (a conversa completa mostrada na seção 9 do capítulo)
