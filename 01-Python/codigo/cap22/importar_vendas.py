# ------------------------------------------------------------
# importar_vendas.py
# Capítulo 01.22 — Arquivos: texto e CSV
# O que este arquivo demonstra: leitura de CSV com DictReader,
#   quarentena por linha, agregação e gravação de dois arquivos
# Como executar: python importar_vendas.py
# ------------------------------------------------------------

import csv
from pathlib import Path

PASTA_DADOS = Path(__file__).parent / "dados"    # caminho relativo AO SCRIPT
ARQUIVO_ENTRADA = PASTA_DADOS / "vendas.csv"
ARQUIVO_RELATORIO = PASTA_DADOS / "relatorio_vendas.txt"
ARQUIVO_QUARENTENA = PASTA_DADOS / "quarentena.csv"


def formatar_reais(centavos):
    """Converte centavos no formato monetário brasileiro."""
    texto = f"{centavos / 100:,.2f}"
    return texto.replace(",", "@").replace(".", ",").replace("@", ".")


def processar_linha(linha):
    """Valida e converte uma linha do CSV. Levanta ValueError se inválida."""
    # DictReader entrega dicionário; colunas ausentes vêm como None
    if linha.get("cidade") is None or linha.get("valor_centavos") is None:
        presentes = len([v for v in linha.values() if v is not None])
        raise ValueError(f"esperava 4 colunas, veio {presentes}")
    cidade = linha["cidade"].strip()
    if not cidade:                                # truthiness (01.08)
        raise ValueError("cidade obrigatória")
    valor = int(linha["valor_centavos"].strip())  # ValueError se não numérico
    return (linha["codigo"].strip(), linha["produto"].strip(), valor, cidade)


def classificar_erro(mensagem):
    """Devolve o tipo de rejeição a partir da mensagem do erro."""
    if "colunas" in mensagem:
        return "CAMPOS_FALTANDO"
    if "cidade" in mensagem:
        return "CIDADE_VAZIA"
    return "VALOR_INVALIDO"


def importar(caminho):
    """Lê o CSV e devolve (registros, quarentena, total_lido)."""
    registros = []
    quarentena = []
    total_lido = 0

    with open(caminho, encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        # enumerate com start=2: a linha 1 do arquivo é o cabeçalho
        for numero, linha in enumerate(leitor, start=2):
            total_lido += 1
            try:
                registros.append(processar_linha(linha))
            except ValueError as erro:
                mensagem = str(erro)
                quarentena.append((numero, classificar_erro(mensagem), mensagem))
    return registros, quarentena, total_lido


def agregar_por_cidade(registros):
    """Devolve (totais, contagem) por cidade canônica (01.15)."""
    totais = {}
    contagem = {}
    for codigo, produto, valor, cidade in registros:
        chave = cidade.strip().lower()
        totais[chave] = totais.get(chave, 0) + valor
        contagem[chave] = contagem.get(chave, 0) + 1
    return totais, contagem


def main():
    """Importa, agrega, imprime e grava os resultados."""
    print(f"=== Importação: dados/{ARQUIVO_ENTRADA.name} ===")
    try:
        registros, quarentena, lidas = importar(ARQUIVO_ENTRADA)
    except FileNotFoundError:
        # A defesa do 01.21: mensagem clara em vez de traceback
        print(f"[X] Arquivo não encontrado: {ARQUIVO_ENTRADA}")
        print("    Verifique se o export do sistema foi salvo na pasta dados/.")
        return

    print(f"Lidas: {lidas} | Válidas: {len(registros)} | Rejeitadas: {len(quarentena)}")

    print("\n--- Quarentena ---")
    for numero, tipo, mensagem in quarentena:
        print(f"Linha {numero:>2} | {tipo:<16} | {mensagem}")

    totais, contagem = agregar_por_cidade(registros)
    print("\n--- Vendas por cidade (chave->acumulador, 01.15) ---")
    linhas_relatorio = []
    for cidade, total in totais.items():
        plural = "pedidos" if contagem[cidade] > 1 else "pedido "
        linha = f"{cidade:<11} | {contagem[cidade]} {plural} | R$ {formatar_reais(total):>10}"
        print(linha)
        linhas_relatorio.append(linha)

    total_geral = sum(totais.values())     # sum: embutida útil (01.12)
    print(f"\nTotal geral: R$ {formatar_reais(total_geral)}")

    # --- Gravação 1: relatório em texto ---
    with open(ARQUIVO_RELATORIO, "w", encoding="utf-8") as saida:
        saida.write("RELATÓRIO DE VENDAS — AURORA\n")
        saida.write("=" * 44 + "\n")
        for linha in linhas_relatorio:
            saida.write(linha + "\n")      # write NÃO adiciona quebra de linha
        saida.write(f"\nTotal geral: R$ {formatar_reais(total_geral)}\n")
    print(f"Relatório gravado em: dados/{ARQUIVO_RELATORIO.name}")

    # --- Gravação 2: quarentena em CSV ---
    with open(ARQUIVO_QUARENTENA, "w", encoding="utf-8", newline="") as saida:
        escritor = csv.DictWriter(saida, fieldnames=["linha", "tipo", "mensagem"],
                                  delimiter=";")
        escritor.writeheader()
        for numero, tipo, mensagem in quarentena:
            escritor.writerow({"linha": numero, "tipo": tipo, "mensagem": mensagem})
    print(f"Rejeitados gravados em: dados/{ARQUIVO_QUARENTENA.name}")


if __name__ == "__main__":
    main()
