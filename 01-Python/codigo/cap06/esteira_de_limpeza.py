# ------------------------------------------------------------
# esteira_de_limpeza.py
# Capítulo 01.06 — Strings — parte 2: métodos e f-strings
# O que este arquivo demonstra: split + strip + formas canônica/exibição
#   + validação isdigit + f-strings com alinhamento e reais
# Como executar: python esteira_de_limpeza.py
# ------------------------------------------------------------

linha_suja = "  PED-2026-00123 ; fone bluetooth XZ-9  ;46990; CAMPINAS "

print("--- Desmontando e limpando ---")
campos = linha_suja.split(";")          # desmonta nos ; -> lista de 4 pedaços
print("Campos crus:", campos)

# Cada campo passa pela alfândega: strip nas pontas.
codigo = campos[0].strip()
produto_bruto = campos[1].strip()
valor_texto = campos[2].strip()
cidade_bruta = campos[3].strip()

print("Código:", codigo)

# Forma canônica (comparar/contar) e forma de exibição (olhos humanos):
produto_canonico = produto_bruto.lower()
produto_exibicao = produto_bruto.title()   # limite honesto: vira "Xz-9";
# aceitamos e documentamos — códigos de modelo não são nomes próprios.
print("Produto (canônico):", produto_canonico, "| (exibição):", produto_exibicao)

# Validação antes da conversão: só converte o que é 100% dígitos.
print("Valor validado:", int(valor_texto), "centavos")
# (se valor_texto tivesse lixo, isdigit() denunciaria: )
print("É só dígitos?", valor_texto.isdigit())

cidade_canonica = cidade_bruta.lower()
cidade_exibicao = cidade_bruta.title()
print("Cidade (canônica):", cidade_canonica, "| (exibição):", cidade_exibicao)

print()
print("--- Linha de relatório formatada ---")
valor_centavos = int(valor_texto)

# Reais no formato brasileiro: f-string gera "4,699.90" (padrão americano);
# o replace triplo troca . e , de lugar usando um marcador temporário.
reais_americano = f"{valor_centavos / 100:,.2f}"          # '469.90' ou '4,699.90'
reais_brasil = reais_americano.replace(",", "@").replace(".", ",").replace("@", ".")

print(f"{codigo} | {produto_exibicao:<22} | R$ {reais_brasil:>9} | {cidade_exibicao}")
# Saída: PED-2026-00123 | Fone Bluetooth Xz-9    | R$    469,90 | Campinas
