# ------------------------------------------------------------
# registros_da_aurora.py
# Capítulo 01.14 — Tuplas e desempacotamento
# O que este arquivo demonstra: pedidos como registros (tuplas),
#   desempacotamento no laço, troca sem auxiliar e a sutileza do
#   campo mutável dentro de tupla imutável
# Como executar: python registros_da_aurora.py
# ------------------------------------------------------------

print("--- Registros: lista de tuplas ---")
# Coleção MUTÁVEL (cresce) de registros IMUTÁVEIS (não se alteram):
pedidos = [
    ("PED-2026-00123", "Fone Bluetooth", 46_990, "Campinas"),
    ("PED-2026-00124", "Mouse Sem Fio", 8_990, "Santos"),
    ("PED-2026-00125", "Teclado Mecânico", 34_900, "Campinas"),
]

total_lote = 0
de_campinas = 0
# Desempacotamento no laço: nomes em vez de campos[0], campos[1]...
for numero, pedido in enumerate(pedidos, start=1):
    codigo, produto, valor, cidade = pedido      # 4 etiquetas de uma vez
    total_lote += valor
    if cidade.lower() == "campinas":
        de_campinas += 1
    reais = f"{valor / 100:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
    print(f"{numero}. {codigo} | {produto:<16} | R$ {reais:>8} | {cidade}")

print()
print("--- Desempacotamento em ação ---")
a, b = 10, 20                    # a vírgula cria a tupla; o lado esquerdo desempacota
antes = (a, b)
a, b = b, a                      # troca sem variável auxiliar
print(f"Troca sem auxiliar: antes {antes} -> depois {(a, b)}")

resultado = divmod(87, 50)       # devolve TUPLA (quociente, resto) — 01.04
print("divmod(87, 50) devolveu a tupla:", resultado)

print()
print("--- A tupla protege (e o teste de sabotagem prova) ---")
# A linha abaixo, se descomentada, levanta:
#   TypeError: 'tuple' object does not support item assignment
# pedidos[0][2] = 1
print("Tentativa de alterar o valor do pedido 1: TypeError capturado no comentário ✓")

reais_lote = f"{total_lote / 100:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
print(f"Total do lote: R$ {reais_lote} | Campinas: {de_campinas}")

print()
print("--- A sutileza: tupla com lista dentro ---")
registro = ("PED-9", [100, 200])
# registro[1] = []   -> TypeError: não posso TROCAR o campo...
registro[1].append(999)          # ...mas posso mutar o objeto que ele aponta
print(registro, "<- a lista interna aceitou append")
# Saída: ('PED-9', [100, 200, 999]) <- a lista interna aceitou append
