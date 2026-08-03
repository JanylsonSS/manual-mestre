# ------------------------------------------------------------
# sombras.py
# Capítulo 01.03 — Variáveis, objetos e referências
# O que este arquivo demonstra: bancada do exercício AP3 — dois
#   sombreamentos de nomes embutidos causando erros "estranhos".
#   Missão: rodar, diagnosticar com hipótese e consertar (renomeando).
# Como executar: python sombras.py
# ------------------------------------------------------------

print("Relatório rápido da Aurora")

# Um estagiário apressado guardou o tipo do relatório numa variável...
type = "consolidado mensal"
print("Tipo do relatório:", type)

# ...e o id do último pedido em outra.
id = 88412
print("Último pedido:", id)

# Mais abaixo, alguém tenta usar os instrumentos do capítulo:
quantidade = 42
print("Inspecionando quantidade:", type(quantidade))
print("Identidade do objeto:", id(quantidade))

# Saída (com os defeitos): imprime as 3 primeiras linhas e quebra com
# TypeError: 'str' object is not callable  — por quê? conserte os DOIS.
