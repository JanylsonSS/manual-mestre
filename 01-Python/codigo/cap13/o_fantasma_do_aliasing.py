# ------------------------------------------------------------
# o_fantasma_do_aliasing.py
# Capítulo 01.13 — Listas parte 2: métodos, cópias e aliasing
# O que este arquivo demonstra: o bug de aliasing nascendo, o
#   diagnóstico com is/id, a cópia rasa e o limite dela (deepcopy)
# Como executar: python o_fantasma_do_aliasing.py
# ------------------------------------------------------------

import copy                      # caixa-preta até 01.20: traz deepcopy

print("--- Cena 1: o telefonema (o bug nascendo) ---")
originais = ["PED-1", "PED-2", "PED-3"]
processados = originais          # NÃO é cópia: é segunda etiqueta (01.03)

print("originais:", originais)
print("processados:", processados)

processados.append("PED-4")      # muta O OBJETO — as duas etiquetas veem
print("Após processados.append('PED-4'):")
print("originais:", originais, "  <- o \"original\" mudou!")

print()
print("--- Cena 2: o diagnóstico (id como estetoscópio) ---")
print("originais is processados:", originais is processados,
      "  -> não há duas listas, há duas etiquetas")

print()
print("--- Cena 3: a cirurgia (copy) ---")
originais = ["PED-1", "PED-2", "PED-3", "PED-4"]   # recomeço limpo
copia = originais.copy()         # lista NOVA com os mesmos itens
print("originais is copia:", copia is originais)
copia.append("PED-9")
print(f"Após copia.append('PED-9'): originais segue com {len(originais)} itens ✓")

print()
print("--- Cena 4: a pegadinha (rasa não resolve com aninhamento) ---")
lote_a = [["PED-1", 100], ["PED-2", 200]]
lote_b = lote_a.copy()           # invólucro novo, itens COMPARTILHADOS
lote_b[0].append("processado")   # mexe no item interno — que é o mesmo objeto
print("lote_a[0] após mexer só em lote_b[0]:", lote_a[0], " <- vazou!")

lote_a = [["PED-1", 100], ["PED-2", 200]]          # recomeço limpo
lote_c = copy.deepcopy(lote_a)   # invólucro E conteúdo, tudo novo
lote_c[0].append("processado")
print("Com deepcopy: lote_a[0] =", lote_a[0], "✓ intacto")

print()
print("--- Bônus: sort (muta) x sorted (devolve nova) ---")
precos = [30_000, 4_990, 12_990]
ordenados = sorted(precos)       # nova lista ordenada; precos intacto
print("sorted -> ", ordenados, "| precos preservado:", precos)
precos.sort()                    # muta no lugar e devolve None
print("após precos.sort() ->", precos)
# Saída: (as quatro cenas mostradas na seção 9 do capítulo)
