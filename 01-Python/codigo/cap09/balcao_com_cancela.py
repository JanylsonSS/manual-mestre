# ------------------------------------------------------------
# balcao_com_cancela.py
# Capítulo 01.09 — Condicionais
# O que este arquivo demonstra: guardas na borda (validar-cedo),
#   cadeia de faixas de frete e ifs independentes para benefícios
# Como executar: python balcao_com_cancela.py
# ------------------------------------------------------------

print("=== Balcão Aurora v2 — agora com cancela ===")

# --- Borda com esteira (01.07) ---
valor_texto = input("Valor do produto (ex.: 1399,90): ")
valor_limpo = valor_texto.strip().replace("R$", "").strip()
valor_limpo = valor_limpo.replace(".", "").replace(",", ".")
valor_ok = valor_limpo.replace(".", "", 1).isdigit()

# --- GUARDA 1: valor. Caso de erro sai cedo, com eco e instrução. ---
if not valor_ok:
    print()
    print(f"[X] Valor não reconhecido: {valor_texto!r}")
    print("    Formato esperado: 1399,90 (ou R$ 1.399,90)")
    print("    Atendimento encerrado — rode de novo e tente outra vez.")
    # Sem 'while' (01.10) nem 'return' (01.18), encerrar educadamente
    # é a saída disponível — e já é infinitamente melhor que o traceback.
else:
    valor_centavos = int(float(valor_limpo) * 100)

    parcelas_texto = input("Número de parcelas (1 a 12): ").strip()

    # --- GUARDA 2: parcelas (formato) --- GUARDA 3: parcelas (faixa) ---
    if not parcelas_texto.isdigit():
        print(f"[X] Parcelas não reconhecidas: {parcelas_texto!r} (digite um número)")
    elif not (1 <= int(parcelas_texto) <= 12):
        print(f"[X] Fora da faixa: {parcelas_texto}x (aceitamos de 1 a 12)")
    else:
        # --- CAMINHO FELIZ, plano: as cancelas ficaram para trás ---
        parcelas = int(parcelas_texto)

        # CADEIA de faixas: da mais exigente para a mais frouxa.
        if valor_centavos >= 29_900:
            frete_centavos = 0
            faixa_frete = "grátis"
        elif valor_centavos >= 10_000:
            frete_centavos = 990
            faixa_frete = "com desconto"
        else:
            frete_centavos = 1_990
            faixa_frete = "cheio"

        # IFS INDEPENDENTES: benefícios que coexistem (não é escolha).
        brindes = ""
        if parcelas == 1:
            brindes = brindes + " [5% à vista]"
        if valor_centavos >= 50_000:
            brindes = brindes + " [embalagem presente]"

        total = valor_centavos + frete_centavos
        parcela_base = total // parcelas
        parcela_1 = parcela_base + total % parcelas

        reais_total = f"{total / 100:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")
        reais_p1 = f"{parcela_1 / 100:,.2f}".replace(",", "@").replace(".", ",").replace("@", ".")

        print()
        print(f"Frete: {faixa_frete}  |  Benefícios:{brindes or ' nenhum'}")
        print(f"Total: R$ {reais_total}  |  1ª parcela: R$ {reais_p1} de {parcelas}x")
        print("=" * 44)

# Saída: (os dois caminhos demonstrados na seção 9 do capítulo)
