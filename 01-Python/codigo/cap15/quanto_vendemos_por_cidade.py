# ------------------------------------------------------------
# quanto_vendemos_por_cidade.py
# Capítulo 01.15 — Dicionários
# O que este arquivo demonstra: chave->acumulador (contar e somar),
#   agrupamento com setdefault e índice por chave — a dor original
#   da Aurora, respondida
# Como executar: python quanto_vendemos_por_cidade.py
# ------------------------------------------------------------

# Registros do 01.14: lista (mutável) de tuplas (imutáveis)
pedidos = [
    ("PED-2026-00123", "Fone Bluetooth", 46_990, "Campinas"),
    ("PED-2026-00124", "Mouse Sem Fio", 8_990, " santos "),
    ("PED-2026-00125", "Teclado Mecânico", 34_900, "CAMPINAS"),
    ("PED-2026-00126", "Cabo HDMI", 9_890, "Santos"),
    ("PED-2026-00127", "Webcam HD", 47_890, "campinas"),
    ("PED-2026-00128", "Headset Gamer", 34_900, "São Paulo"),
]

print("--- A pergunta da gestora (primeiro dia do módulo) ---")
print("Quanto vendemos por cidade?")
print()

totais = {}       # chave -> soma em centavos
contagem = {}     # chave -> quantos pedidos

for codigo, produto, valor, cidade in pedidos:
    # CANÔNICA obrigatória (01.06): sem ela, "Campinas" e "campinas"
    # viram DUAS caixas — comente esta linha e rode para ver o estrago.
    chave = cidade.strip().lower()

    # O padrão do capítulo: o get(chave, 0) resolve a inicialização
    totais[chave] = totais.get(chave, 0) + valor
    contagem[chave] = contagem.get(chave, 0) + 1

# Percurso com .items(): cada volta entrega uma TUPLA (chave, valor)
for chave, total in totais.items():
    reais = f"{total / 100:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
    plural = "pedidos" if contagem[chave] > 1 else "pedido "
    print(f"{chave:<11} | {contagem[chave]} {plural} | R$ {reais:>10}")

# Campeã sem key= (04.02): acumulador de máximo, padrão do 01.12
cidade_campea = ""
maior_total = 0
for chave, total in totais.items():
    if total > maior_total:
        maior_total = total
        cidade_campea = chave
reais_campea = f"{maior_total / 100:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
print(f"\nCampeã: {cidade_campea} com R$ {reais_campea}")

print()
print("--- Agrupamento: quais pedidos de cada cidade ---")
por_cidade = {}
for codigo, produto, valor, cidade in pedidos:
    chave = cidade.strip().lower()
    # setdefault GARANTE a lista e a devolve, para o append alimentar
    por_cidade.setdefault(chave, []).append(codigo)

for chave, codigos in por_cidade.items():
    print(f"{chave}: " + ", ".join(codigos))

print()
print("--- Índice por código (busca direta) ---")
indice = {}
for codigo, produto, valor, cidade in pedidos:
    indice[codigo] = (produto, valor, cidade)     # chave -> registro

print("Consulta PED-2026-00125:", indice["PED-2026-00125"])
# get com padrão: consulta que pode falhar sem quebrar o programa
print("Consulta PED-9999:", indice.get("PED-9999", "não encontrado (get com padrão) ✓"))
# Saída: (o relatório completo mostrado na seção 9 do capítulo)
