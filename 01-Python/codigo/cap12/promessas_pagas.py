# ------------------------------------------------------------
# promessas_pagas.py
# Capítulo 01.12 — Listas — parte 1
# O que este arquivo demonstra: a máquina de troco e a tabela de
#   vendas refatoradas com listas — acumular, filtrar, transformar
# Como executar: python promessas_pagas.py
# ------------------------------------------------------------

print("--- Máquina de troco v2: 6 degraus viram 3 linhas ---")
notas = [50, 20, 10, 5, 2, 1]        # a política de notas MORA em dados agora
troco = 87
resta = troco

partes = []                           # acumulador de coleção: nasce vazio, fora
for nota in notas:                    # a esteira percorre a política
    quantas = resta // nota           # a lógica de UM degrau (01.04), intacta
    resta = resta % nota
    if quantas > 0:                   # filtro: só notas usadas entram no recibo
        partes.append(f"{quantas}x R${nota}")

print(f"Troco de R$ {troco}: " + ", ".join(partes))   # join costura a lista

# Prova dos nove com o padrão transformar+acumular na forma compacta:
prova = 0
for parte in partes:
    quantas_texto = parte.split("x R$")[0]            # split devolve lista!
    valor_texto = parte.split("x R$")[1]
    prova += int(quantas_texto) * int(valor_texto)
print(f"Prova dos nove: {prova} " + ("✓" if prova == troco else "✗ DIVERGIU"))

print()
print("--- Tabela de vendas v2: 3 blocos viram 1 laço ---")
linhas_sujas = [                      # as 3 variáveis do 01.06 viram UMA lista
    "  PED-2026-00123 ; fone bluetooth XZ-9  ;46990; CAMPINAS ",
    "PED-2026-00124;  mouse sem fio ;8990;santos",
    " PED-2026-00125 ;TECLADO MECÂNICO; 34900 ;  Campinas",
]

total_lote = 0                        # acumulador numérico
de_campinas = 0                       # contador com filtro
for numero, linha in enumerate(linhas_sujas, start=1):
    campos = linha.split(";")         # a caixa-preta do 01.06, aberta: lista!
    codigo = campos[0].strip()
    produto = campos[1].strip().title()
    valor_centavos = int(campos[2].strip())
    cidade = campos[3].strip()
    cidade_canonica = cidade.lower()  # canônica p/ contar (01.06)

    total_lote += valor_centavos
    if cidade_canonica == "campinas":
        de_campinas += 1

    reais = f"{valor_centavos / 100:,.2f}"
    reais = reais.replace(",", "@").replace(".", ",").replace("@", ".")
    print(f"{numero:>2}. {codigo} | {produto:<22} | R$ {reais:>9} | {cidade.title()}")

reais_lote = f"{total_lote / 100:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
print(f"Total do lote: R$ {reais_lote} | Pedidos de Campinas: {de_campinas}")
# Saída: (as duas tabelas mostradas na seção 9 do capítulo)
