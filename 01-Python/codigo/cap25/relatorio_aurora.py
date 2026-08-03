# ------------------------------------------------------------
# relatorio_aurora.py
# Capítulo 01.25 — PEP 8 + mini projeto do módulo
# O que este arquivo demonstra: o Relatório de Vendas Aurora v0 —
#   importação com quarentena, agregações, relatório formatado e
#   três saídas gravadas (txt, csv, json)
# Como executar: python relatorio_aurora.py
# ------------------------------------------------------------

import csv
import json
from datetime import datetime
from pathlib import Path

PASTA = Path(__file__).parent
ARQUIVO_CONFIG = PASTA / "config.json"
PASTA_SAIDA = PASTA / "saida"

CONFIG_PADRAO = {
    "arquivo_vendas": "dados/vendas.csv",
    "separador": ";",
    "cidades_atendidas": ["campinas", "santos", "sao paulo", "sorocaba"],
    "top_produtos": 5,
}


def carregar_config(caminho):
    """Lê a configuração; devolve os padrões se o arquivo não existir."""
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            return {**CONFIG_PADRAO, **json.load(arquivo)}
    except FileNotFoundError:
        return CONFIG_PADRAO


def formatar_reais(centavos):
    """Converte centavos (int) no formato monetário brasileiro."""
    texto = f"{centavos / 100:,.2f}"
    return texto.replace(",", "@").replace(".", ",").replace("@", ".")


def processar_linha(linha):
    """Valida e converte uma linha do CSV. Levanta ValueError se inválida."""
    if linha.get("cidade") is None or linha.get("valor_centavos") is None:
        presentes = len([valor for valor in linha.values() if valor is not None])
        raise ValueError(f"esperava 4 colunas, veio {presentes}")
    cidade = linha["cidade"].strip()
    if not cidade:
        raise ValueError("cidade obrigatória")
    valor = int(linha["valor_centavos"].strip())
    return (linha["codigo"].strip(), linha["produto"].strip(), valor, cidade)


def classificar_erro(mensagem):
    """Devolve o tipo de rejeição a partir da mensagem do erro."""
    if "colunas" in mensagem:
        return "CAMPOS_FALTANDO"
    if "cidade" in mensagem:
        return "CIDADE_VAZIA"
    return "VALOR_INVALIDO"


def importar(caminho, separador):
    """Lê o CSV e devolve (registros, quarentena, total_lido)."""
    registros = []
    quarentena = []
    total_lido = 0
    with open(caminho, encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=separador)
        for numero, linha in enumerate(leitor, start=2):
            total_lido += 1
            try:
                registros.append(processar_linha(linha))
            except ValueError as erro:
                mensagem = str(erro)
                quarentena.append((numero, classificar_erro(mensagem), mensagem))
    return registros, quarentena, total_lido


def agregar(registros):
    """Devolve as agregações por cidade e por produto (chave -> acumulador)."""
    por_cidade = {}
    contagem_cidade = {}
    por_produto = {}
    contagem_produto = {}
    for _codigo, produto, valor, cidade in registros:
        chave_cidade = cidade.strip().lower()
        por_cidade[chave_cidade] = por_cidade.get(chave_cidade, 0) + valor
        contagem_cidade[chave_cidade] = contagem_cidade.get(chave_cidade, 0) + 1
        por_produto[produto] = por_produto.get(produto, 0) + valor
        contagem_produto[produto] = contagem_produto.get(produto, 0) + 1
    return por_cidade, contagem_cidade, por_produto, contagem_produto


def cidade_campea(por_cidade):
    """Devolve (cidade, total) da cidade com maior faturamento."""
    campea = ""
    maior = 0
    for cidade, total in por_cidade.items():
        if total > maior:
            maior = total
            campea = cidade
    return campea, maior


def montar_relatorio(dados):
    """Devolve o texto completo do relatório (não imprime — 01.18)."""
    linhas = []
    linhas.append("=" * 64)
    linhas.append("RELATÓRIO DE VENDAS — AURORA COMÉRCIO")
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linhas.append(f"Origem: {dados['origem']} | Gerado em: {agora}")
    linhas.append("=" * 64)

    linhas.append("\nIMPORTAÇÃO")
    linhas.append(f"  Lidas: {dados['lidas']} | Válidas: {dados['validas']} "
                  f"| Rejeitadas: {dados['rejeitadas']}")

    linhas.append("\nVENDAS POR CIDADE")
    for cidade in sorted(dados["por_cidade"]):
        total = dados["por_cidade"][cidade]
        quantidade = dados["contagem_cidade"][cidade]
        plural = "pedidos" if quantidade > 1 else "pedido "
        linhas.append(f"  {cidade:<11} | {quantidade:>2} {plural} "
                      f"| R$ {formatar_reais(total):>10}")
    linhas.append("  " + "-" * 46)
    linhas.append(f"  {'TOTAL':<11} | {dados['validas']:>2} pedidos "
                  f"| R$ {formatar_reais(dados['total_geral']):>10}")

    # Prova dos nove: hábito nascido no 01.04, agora requisito de entrega
    soma_cidades = sum(dados["por_cidade"].values())
    prova = "OK" if soma_cidades == dados["total_geral"] else "DIVERGÊNCIA"
    linhas.append(f"  Prova dos nove: {prova} (soma das cidades = total geral)")

    linhas.append(f"\nVENDAS POR PRODUTO (top {dados['top_produtos']})")
    # Ordenação por valor sem key= (que só chega em 04.02):
    # acumulador de máximo repetido sobre uma cópia do dicionário.
    restantes = dict(dados["por_produto"])
    mostrados = 0
    while restantes and mostrados < dados["top_produtos"]:
        melhor_produto = ""
        melhor_valor = 0
        for produto, total in restantes.items():
            if total > melhor_valor:
                melhor_valor = total
                melhor_produto = produto
        quantidade = dados["contagem_produto"][melhor_produto]
        linhas.append(f"  {melhor_produto:<20} | {quantidade} un "
                      f"| R$ {formatar_reais(melhor_valor):>10}")
        del restantes[melhor_produto]
        mostrados += 1

    linhas.append("\nINDICADORES")
    if dados["validas"] > 0:
        ticket = dados["total_geral"] // dados["validas"]
        linhas.append(f"  Ticket médio: R$ {formatar_reais(ticket)}")
    else:
        linhas.append("  Ticket médio: não aplicável (nenhuma venda válida)")
    campea, total_campea = cidade_campea(dados["por_cidade"])
    if campea:
        linhas.append(f"  Cidade campeã: {campea} (R$ {formatar_reais(total_campea)})")

    linhas.append(f"\nQUARENTENA ({dados['rejeitadas']} linhas)")
    for numero, tipo, mensagem in dados["quarentena"]:
        linhas.append(f"  Linha {numero:>2} | {tipo:<16} | {mensagem}")

    return "\n".join(linhas)


def gravar_saidas(texto, quarentena, resumo):
    """Grava relatório (txt), quarentena (csv) e resumo (json)."""
    PASTA_SAIDA.mkdir(exist_ok=True)

    with open(PASTA_SAIDA / "relatorio_vendas.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(texto + "\n")

    with open(PASTA_SAIDA / "quarentena.csv", "w", encoding="utf-8",
              newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=["linha", "tipo", "mensagem"],
                                  delimiter=";")
        escritor.writeheader()
        for numero, tipo, mensagem in quarentena:
            escritor.writerow({"linha": numero, "tipo": tipo, "mensagem": mensagem})

    with open(PASTA_SAIDA / "resumo.json", "w", encoding="utf-8") as arquivo:
        json.dump(resumo, arquivo, ensure_ascii=False, indent=2)


def main():
    """Ponto de entrada: importa, agrega, monta o relatório e grava."""
    config = carregar_config(ARQUIVO_CONFIG)
    caminho_vendas = PASTA / config["arquivo_vendas"]

    try:
        registros, quarentena, lidas = importar(caminho_vendas, config["separador"])
    except FileNotFoundError:
        print(f"[X] Arquivo de vendas não encontrado: {caminho_vendas}")
        print("    Ajuste 'arquivo_vendas' no config.json ou salve o export na pasta.")
        return

    por_cidade, contagem_cidade, por_produto, contagem_produto = agregar(registros)
    total_geral = sum(por_cidade.values())

    dados = {
        "origem": caminho_vendas.name,
        "lidas": lidas,
        "validas": len(registros),
        "rejeitadas": len(quarentena),
        "por_cidade": por_cidade,
        "contagem_cidade": contagem_cidade,
        "por_produto": por_produto,
        "contagem_produto": contagem_produto,
        "total_geral": total_geral,
        "quarentena": quarentena,
        "top_produtos": config["top_produtos"],
    }

    texto = montar_relatorio(dados)
    print(texto)

    resumo = {
        "origem": caminho_vendas.name,
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "funil": {"lidas": lidas, "validas": len(registros),
                  "rejeitadas": len(quarentena)},
        "total_geral_centavos": total_geral,
        "por_cidade": por_cidade,
        "por_produto": por_produto,
    }
    gravar_saidas(texto, quarentena, resumo)

    print("\nArquivos gerados:")
    print("  saida/relatorio_vendas.txt")
    print("  saida/quarentena.csv")
    print("  saida/resumo.json")
    print("=" * 64)


if __name__ == "__main__":
    main()
