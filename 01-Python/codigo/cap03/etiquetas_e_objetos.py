# ------------------------------------------------------------
# etiquetas_e_objetos.py
# Capítulo 01.03 — Variáveis, objetos e referências
# O que este arquivo demonstra: atribuição = amarrar etiqueta em objeto;
#   inspeção com type(), id() e is
# Como executar: python etiquetas_e_objetos.py
# ------------------------------------------------------------

print("--- Ato 1: duas etiquetas, um objeto ---")
a = 100        # cria/localiza o objeto 100 e amarra a etiqueta 'a'
b = a          # amarra a etiqueta 'b' NO MESMO objeto — nada é copiado

# id() revela a identidade; se as etiquetas estão no mesmo objeto, os ids coincidem
print("id de a:", id(a), "| id de b:", id(b), " (iguais!)")
print("a is b:", a is b)
# Saída: a is b: True

print()
print("--- Ato 2: reatribuição desamarra só uma ---")
a = 200        # 'a' desamarra do 100 e amarra no objeto novo 200
print("a agora:", a, "| b continua:", b)
# Saída: a agora: 200 | b continua: 100
print("a is b:", a is b)
# Saída: a is b: False

print()
print("--- Ato 3: etiquetas não têm tipo, objetos têm ---")
quantidade = 42
print("type antes:", type(quantidade))
# Saída: type antes: <class 'int'>
quantidade = "quarenta e dois"   # a MESMA etiqueta, amarrada num objeto str
print("type depois:", type(quantidade))
# Saída: type depois: <class 'str'>
