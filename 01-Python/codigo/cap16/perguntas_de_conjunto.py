# ------------------------------------------------------------
# perguntas_de_conjunto.py
# Capítulo 01.16 — Conjuntos
# O que este arquivo demonstra: deduplicação, pertinência e as
#   operações de conjunto respondendo perguntas de negócio
# Como executar: python perguntas_de_conjunto.py
# ------------------------------------------------------------

# Registros com cliente: (codigo, cliente, produto, valor, cidade)
pedidos = [
    ("PED-1", "Ana", "Fone Bluetooth", 46_990, "Campinas"),
    ("PED-2", "Bruno", "Mouse Sem Fio", 8_990, " campinas "),
    ("PED-3", "Carla", "Teclado Mecânico", 34_900, "CAMPINAS"),
    ("PED-4", "Carla", "Cabo HDMI", 9_890, "Santos"),
    ("PED-5", "Diego", "Teclado Mecânico", 34_900, "santos"),
    ("PED-6", "Ana", "Webcam HD", 47_890, "Campinas"),
    ("PED-7", "Elisa", "Mouse Sem Fio", 8_990, "São Paulo"),
    ("PED-8", "Bruno", "Cabo HDMI", 9_890, "Sorocaba"),
]

print("--- Pergunta 1: quantas cidades distintas atendemos? ---")
cidades = set()                       # conjunto vazio: set(), nunca {}
for codigo, cliente, produto, valor, cidade in pedidos:
    cidades.add(cidade.strip().lower())     # canônica antes de entrar (01.15)
# sorted() devolve LISTA ordenada — o idioma para exibir conjunto
print(f"{len(cidades)} cidades: " + ", ".join(sorted(cidades)))

print()
print("--- Pergunta 2: quem compra em mais de uma cidade? ---")
# Dicionário cujo VALOR é conjunto: as duas estruturas do lote juntas
clientes_por_cidade = {}
for codigo, cliente, produto, valor, cidade in pedidos:
    chave = cidade.strip().lower()
    clientes_por_cidade.setdefault(chave, set()).add(cliente.lower())

campinas = clientes_por_cidade["campinas"]
santos = clientes_por_cidade["santos"]
print("Clientes de Campinas:", sorted(campinas))
print("Clientes de Santos:  ", sorted(santos))
print("Compraram nas DUAS (interseção):", sorted(campinas & santos))
print("Exclusivos de Campinas (diferença):", sorted(campinas - santos))
print("Base total (união):", len(campinas | santos), "clientes")

print()
print("--- Pergunta 3: produtos vendidos em Campinas mas nunca em Santos ---")
produtos_campinas = set()
produtos_santos = set()
for codigo, cliente, produto, valor, cidade in pedidos:
    chave = cidade.strip().lower()
    if chave == "campinas":
        produtos_campinas.add(produto)
    elif chave == "santos":
        produtos_santos.add(produto)
print(sorted(produtos_campinas - produtos_santos))

print()
print("--- Bônus: dedupe em uma linha e o custo de não usar conjunto ---")
lista_bruta = ["Campinas", " campinas ", "CAMPINAS", "Santos", "santos",
               "São Paulo", "Sorocaba", "campinas"]
lista_cidades = []
for c in lista_bruta:                 # canônica (a comprehension chega em 01.17)
    lista_cidades.append(c.strip().lower())
unicas = set(lista_cidades)           # UMA chamada faz o que 5 linhas faziam
print(f"Lista com {len(lista_cidades)} cidades -> set -> {len(unicas)} únicas (uma chamada)")
# Saída: (o relatório completo mostrado na seção 9 do capítulo)
