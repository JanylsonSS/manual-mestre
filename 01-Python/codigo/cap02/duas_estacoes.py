# ------------------------------------------------------------
# duas_estacoes.py
# Capítulo 01.02 — Como o Python executa seu código
# O que este arquivo demonstra: erros de execução acontecem NO MEIO
#   do programa (linhas anteriores já rodaram) — e tracebacks dão endereço
# Como executar: python duas_estacoes.py
#   (o erro na última linha é PROPOSITAL — o capítulo manda consertá-lo)
# ------------------------------------------------------------

print("Etapa 1: pedido recebido")
print("Etapa 2: pedido validado")

total = 250

# A linha abaixo tem um nome digitado errado DE PROPÓSITO ("totaal").
# Missão do Experimento 2: ler o traceback e consertar só o necessário.
print(total)

print("Etapa 3: total calculado")
print("Fim do programa.")

# Saída (com o erro proposital):
# Etapa 1: pedido recebido
# Etapa 2: pedido validado
# Traceback (most recent call last):
#   ...line 17... NameError: name 'totaal' is not defined. Did you mean: 'total'?
