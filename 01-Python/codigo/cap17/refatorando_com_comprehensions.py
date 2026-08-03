# ------------------------------------------------------------
# refatorando_com_comprehensions.py
# Capítulo 01.17 — Compreensões
# O que este arquivo demonstra: as três formas (lista, dict, set),
#   a tradução laço->comprehension e o caso em que NÃO se deve dobrar
# Como executar: python refatorando_com_comprehensions.py
# ------------------------------------------------------------

textos = ["46990", "abc", "12990", "", "34900"]
registros = [
    ("PED-1", "Fone Bluetooth", 46_990, "Campinas"),
    ("PED-2", "Mouse Sem Fio", 8_990, " santos "),
    ("PED-3", "Teclado Mecânico", 34_900, "CAMPINAS"),
    ("PED-4", "Cabo HDMI", 9_890, "Sorocaba"),
    ("PED-5", "Webcam HD", 47_890, "São Paulo"),
]

print("--- Antes e depois: 4 refatorações ---")

# 1. TRANSFORMAR + FILTRAR (era: lista vazia + for + if + append)
centavos = [int(t) for t in textos if t.isdigit()]
print("1. Transformar (textos -> centavos): 4 linhas -> 1")
print("  ", centavos)

# 2. FILTRAR sem transformar
rejeitados = [t for t in textos if not t.isdigit()]
print("2. Filtrar (rejeitados): 4 linhas -> 1")
print("  ", rejeitados)

# 3. SET comprehension: dedupe + canônica numa linha (01.16)
cidades = {r[3].strip().lower() for r in registros}
print("3. Dedupe de cidades (set comprehension): 4 linhas -> 1")
print("  ", sorted(cidades))     # sorted para exibir (conjunto não tem ordem)

# 4. DICT comprehension com desempacotamento (01.14 + 01.15)
indice = {codigo: (produto, valor) for codigo, produto, valor, cidade in registros}
print("4. Índice codigo->registro (dict comprehension): 3 linhas -> 1")
print("   PED-2:", indice["PED-2"])

print()
print("--- A que NÃO deve virar comprehension ---")

# VERSÃO COMPRIMIDA (cabe numa linha... e não deveria):
linhas_ruim = [f"{c} | {p:<18} | R$ {v / 100:>8.2f} | {cid.strip().title()}"
               for c, p, v, cid in registros if v > 9_000 and cid.strip().lower() != "sorocaba"]

# VERSÃO LAÇO (mais linhas, nomes intermediários, lógica visível):
linhas_boa = []
for codigo, produto, valor, cidade in registros:
    cidade_canonica = cidade.strip().lower()
    if valor <= 9_000 or cidade_canonica == "sorocaba":
        continue                          # filtro explícito e nomeado
    reais = f"{valor / 100:>8.2f}"
    linhas_boa.append(f"{codigo} | {produto:<18} | R$ {reais} | {cidade.strip().title()}")

print(f"Versão comprimida (ilegível, {len(linhas_ruim[0]) + 60} caracteres) vs. laço com nomes:")
print("o laço venceu — e o motivo está comentado no arquivo.")
# CRITÉRIO: a comprimida tem 2 condições, 1 formatação e 1 desempacotamento
# na mesma linha — quem lê precisa DECODIFICAR. O laço nomeia a canônica,
# separa o filtro e deixa a formatação respirar. Legibilidade vence.
print(f"(as duas produzem o mesmo: {linhas_ruim == linhas_boa})")

print()
print("--- Contagem final ---")
print("14 linhas viraram 4. E uma permaneceu laço, de propósito.")
# Saída: (o relatório completo mostrado na seção 9 do capítulo)
