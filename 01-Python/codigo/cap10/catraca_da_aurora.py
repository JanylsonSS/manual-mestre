# ------------------------------------------------------------
# catraca_da_aurora.py
# Capítulo 01.10 — Laço while
# O que este arquivo demonstra: contagem, insistência (while True +
#   break), sentinela com acumulador — e os dois demônios, domados
# Como executar: python catraca_da_aurora.py
# ------------------------------------------------------------

print("--- Padrão 1: contagem ---")
volta = 1                        # inicializa ANTES
while volta <= 5:                # testa na catraca
    print(f"Imprimindo etiqueta {volta} de 5")
    volta += 1                   # avança DENTRO — sem esta linha: infinito
# Saída: 5 linhas, e 'volta' termina valendo 6 (o 1º valor reprovado)

print()
print("--- Padrão 3: insistência (a pendência do 01.07 morre aqui) ---")
while True:                      # o porteiro sempre aprova...
    resposta = input("Parcelas (1 a 12): ").strip()
    if resposta.isdigit() and 1 <= int(resposta) <= 12:
        parcelas = int(resposta)
        break                    # ...e a saída é explícita e visível
    print(f"[X] Inválido: {resposta!r} — digite um número de 1 a 12.")
print(f"Fechado: {parcelas}x. (Reparou? Ele INSISTIU em vez de desistir.)")

print()
print("--- Padrão 2: sentinela + acumulador ---")
total_centavos = 0               # acumulador nasce neutro, FORA do laço
entrada = input("Valor do item em centavos (ou 'fim'): ").strip().lower()
while entrada != "fim":          # a sentinela é testada antes de processar
    if entrada.isdigit():
        total_centavos += int(entrada)
        print(f"  subtotal: {total_centavos} centavos")
    else:
        print(f"  [X] ignorado: {entrada!r}")
    entrada = input("Valor do item em centavos (ou 'fim'): ").strip().lower()

reais = f"{total_centavos / 100:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
print(f"Caixa fechado: R$ {reais}")

# --- BATISMO (Experimento 2): descomente as 3 linhas, rode, Ctrl+C ---
# n = 0
# while n >= 0:                  # n só cresce: a condição nunca vira False
#     n += 1
#     print("volta infinita", n)

# --- ZERO_VOLTAS (Experimento 3): condição invertida — conserte-a ---
contagem = 1
while contagem >= 5:             # deveria ser <= : falsa de cara, 0 voltas
    print("você nunca verá esta linha")
    contagem += 1
print("(o bloco acima rodou zero vezes — silêncio é o sintoma)")

# Saída: (as conversas completas mostradas na seção 9 do capítulo)
