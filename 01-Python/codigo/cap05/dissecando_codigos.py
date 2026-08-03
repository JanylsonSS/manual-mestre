# ------------------------------------------------------------
# dissecando_codigos.py
# Capítulo 01.05 — Strings — parte 1
# O que este arquivo demonstra: indexação, fatiamento e imutabilidade
#   sobre dados reais da Aurora (pedido, CPF, espaço fantasma)
# Como executar: python dissecando_codigos.py
# ------------------------------------------------------------

print("--- Desmontando o código de pedido ---")
codigo = "PED-2026-00123"
#         0123456789...        (régua anotada: P=0, E=1, D=2, -=3, 2=4...)

print("Código completo:", codigo, "(len =", len(codigo), ")")

prefixo = codigo[:3]       # do começo até a marca 3 (exclusiva) -> "PED"
ano = codigo[4:8]          # marcas 4..8 -> "2026"
numero = codigo[-5:]       # os últimos 5 — robusto se o prefixo mudar
print("Prefixo:", prefixo, "| Ano:", ano, "| Número:", numero)
# Saída: Prefixo: PED | Ano: 2026 | Número: 00123

print()
print("--- Mascarando o CPF ---")
cpf = "123.456.789-01"
# Mostrar apenas o final: máscara fixa + os últimos 7 caracteres (".789-01")
mascarado = "***.***" + cpf[-7:]
print("Original:", cpf)
print("Mascarado:", mascarado)
# Saída: Mascarado: ***.***.789-01

# Imutabilidade: o cpf original segue intacto — mascarar CRIOU outra string
print("Original continua:", cpf)

print()
print("--- O espaço fantasma ---")
produto_a = "Fone Bluetooth XZ-9"
produto_b = "Fone Bluetooth XZ-9 "   # espaço no fim — carga invisível
print("Produto A:", repr(produto_a), "(len =", len(produto_a), ")")
print("Produto B:", repr(produto_b), "(len =", len(produto_b), ")")
# repr() mostra a string COM as aspas e espaços visíveis — a lupa do
# depurador de textos (tratamento completo no capítulo 01.24)
print("São o mesmo texto?", produto_a == produto_b)
# Saída: São o mesmo texto? False
