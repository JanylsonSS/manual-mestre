# ------------------------------------------------------------
# blindando_a_borda.py
# Capítulo 01.21 — Exceções
# O que este arquivo demonstra: try/except específico, raise no
#   miolo + tratamento na borda, traceback multiandar e o crime
#   do except genérico
# Como executar: python blindando_a_borda.py
# ------------------------------------------------------------

def converter_centavos(texto):
    """Converte texto em centavos. Levanta ValueError se não der."""
    return int(texto.strip())          # deixa o ValueError SUBIR (miolo não trata)


def separar_parcelas(total_centavos, parcelas):
    """Devolve (primeira, demais). Levanta ValueError se parcelas < 1."""
    if parcelas < 1:
        # RAISE: o contrato foi violado — falhar é a resposta certa.
        # Devolver -1 ou None seria pior: o chamador poderia ignorar.
        raise ValueError(f"parcelas deve ser >= 1, recebi {parcelas}")
    base = total_centavos // parcelas
    return base + total_centavos % parcelas, base


print("--- Cena 1: o que o isdigit() não cobre ---")
for bruto in ["46990", "12.3.4", "1e5", "  99  "]:
    laudo = bruto.isdigit()
    try:
        valor = converter_centavos(bruto)
        veredito = f"{valor} ✓"
    except ValueError:                 # captura ESPECÍFICA
        veredito = "recusado com ValueError ✓"
    print(f"{bruto!r:<9} -> isdigit {str(laudo):<5} | try/except: {veredito}")

print()
print("--- Cena 2: onde tratar (miolo levanta, borda trata) ---")
try:
    separar_parcelas(1_000, 0)
except ValueError as erro:             # 'as' captura o objeto com a mensagem
    print(f"separar_parcelas(1000, 0) -> ValueError capturado na borda: {erro}")

primeira, demais = separar_parcelas(1_000, 3)   # a borda "reperguntou" (aqui: corrigiu)
print(f"Borda repergunta e segue: primeira {primeira}, demais {demais}")

print()
print("--- Cena 3: o traceback de 3 andares (sem tratamento) ---")


def processar_linha(linha):
    """Andar do meio: não trata, só repassa o trabalho."""
    campos = linha.split(";")
    return int(campos[1])              # aqui o alarme nasce


def demonstrar_traceback():
    """Andar de cima: também não trata."""
    return processar_linha("PED-1;abc")


try:
    demonstrar_traceback()
except ValueError as erro:
    # Capturamos só para a demonstração não matar o script:
    print("Traceback (most recent call last):")
    print("  ... 3 andares: <module> -> demonstrar_traceback -> processar_linha")
    print(f"ValueError: {erro}")
    print("(capturado pelo except do próprio script para não matar a demonstração)")

print()
print("--- Cena 4: except genérico (o crime) vs. específico ---")


def com_generico():
    try:
        resultadoo = 10 / 2            # ERRO DE DIGITAÇÃO proposital abaixo
        return resultado               # NameError: 'resultado' não existe
    except:                            # PROIBIDO: engole tudo
        return "erro (mas qual?!)"


def com_especifico():
    try:
        resultadoo = 10 / 2
        return resultado               # o mesmo NameError...
    except ZeroDivisionError:          # ...que este except NÃO atende
        return "divisão por zero"


print("Genérico engoliu ATÉ o erro de digitação do programador: 'NameError' silenciado")
print(f"  com_generico() devolveu: {com_generico()!r}")
try:
    com_especifico()
except NameError as erro:
    print(f"Específico deixou passar o que não sabe tratar ✓ ({erro})")
# Saída: (as quatro cenas mostradas na seção 9 do capítulo)
