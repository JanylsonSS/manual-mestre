# ------------------------------------------------------------
# pedidos_em_json.py
# Capítulo 01.23 — JSON em Python
# O que este arquivo demonstra: dump/load, navegação segura em
#   estruturas aninhadas, perdas da ida e volta e configuração
# Como executar: python pedidos_em_json.py
# ------------------------------------------------------------

import json
from pathlib import Path

PASTA_DADOS = Path(__file__).parent / "dados"
ARQUIVO_PEDIDO = PASTA_DADOS / "pedido.json"
ARQUIVO_CATALOGO = PASTA_DADOS / "catalogo.json"
ARQUIVO_CONFIG = PASTA_DADOS / "config.json"


def formatar_reais(centavos):
    """Converte centavos no formato monetário brasileiro."""
    texto = f"{centavos / 100:,.2f}"
    return texto.replace(",", "@").replace(".", ",").replace("@", ".")


def total_dos_itens(pedido):
    """Soma quantidade x valor de cada item do pedido."""
    total = 0
    for item in pedido.get("itens", []):        # get com [] : lista vazia se faltar
        total += item["quantidade"] * item["valor_centavos"]
    return total


print("--- Cena 1: gravar e ler de volta ---")
pedido = {
    "codigo": "PED-2026-00123",
    "cliente": {
        "nome": "Ana Souza",
        "endereco": {"cidade": "Campinas", "cep": "13010-000"},
    },
    "itens": [
        {"produto": "Fone Bluetooth", "quantidade": 1, "valor_centavos": 46_990},
        {"produto": "Cabo HDMI", "quantidade": 2, "valor_centavos": 9_890},
    ],
    "pago": True,
    "observacao": None,
}

PASTA_DADOS.mkdir(exist_ok=True)                # cria a pasta se não existir
with open(ARQUIVO_PEDIDO, "w", encoding="utf-8") as arquivo:
    # ensure_ascii=False: acentos legíveis | indent=2: humano lê o arquivo
    json.dump(pedido, arquivo, ensure_ascii=False, indent=2)
print(f"Gravado em dados/{ARQUIVO_PEDIDO.name} (com acentos legíveis e indentação)")

with open(ARQUIVO_PEDIDO, encoding="utf-8") as arquivo:
    lido = json.load(arquivo)
print(f"Lido de volta: {lido['codigo']} | cliente: {lido['cliente']['nome']} "
      f"| {len(lido['itens'])} itens")

print()
print("--- Cena 2: navegação segura ---")
print("Cidade (acesso direto):", lido["cliente"]["endereco"]["cidade"])

pedido_incompleto = {"codigo": "PED-9"}         # sem cliente, como uma API pode devolver
cidade = pedido_incompleto.get("cliente", {}).get("endereco", {}).get("cidade", "")
print(f"Cidade de pedido sem cliente (get encadeado): {cidade!r} (sem explodir) ✓")
print("Total dos itens:", "R$", formatar_reais(total_dos_itens(lido)))

print()
print("--- Cena 3: o que se perde na viagem ---")
com_tupla = {"itens": ("fone", "cabo"), 1: "chave numérica"}
volta = json.loads(json.dumps(com_tupla))
print(f"Original: itens é tuple? {isinstance(com_tupla['itens'], tuple)} "
      f" | Volta: itens é tuple? {isinstance(volta['itens'], tuple)} (virou list)")
print(f"Chave int 1 volta como: {list(volta.keys())[1]!r} (str)")

try:
    json.dumps({"cidades": {"campinas", "santos"}})     # conjunto não embarca
except TypeError as erro:
    print(f"set não embarca: {erro} ✓ (capturado)")

print()
print("--- Cena 4: catálogo com vários pedidos ---")
catalogo = [
    pedido,
    {"codigo": "PED-2026-00124", "cliente": {"nome": "Bruno Lima",
     "endereco": {"cidade": "Santos", "cep": "11010-000"}},
     "itens": [{"produto": "Mouse Sem Fio", "quantidade": 1, "valor_centavos": 8_990}],
     "pago": False, "observacao": "entrega expressa"},
    {"codigo": "PED-2026-00125", "cliente": {"nome": "Carla Dias",
     "endereco": {"cidade": "Campinas", "cep": "13020-000"}},
     "itens": [{"produto": "Teclado Mecânico", "quantidade": 1, "valor_centavos": 34_900},
               {"produto": "Mousepad", "quantidade": 1, "valor_centavos": 4_990}],
     "pago": True, "observacao": None},
]

with open(ARQUIVO_CATALOGO, "w", encoding="utf-8") as arquivo:
    json.dump(catalogo, arquivo, ensure_ascii=False, indent=2)

total_geral = 0
cidades = set()
for p in catalogo:
    total_geral += total_dos_itens(p)
    cidades.add(p["cliente"]["endereco"]["cidade"])
print(f"{len(catalogo)} pedidos | total geral R$ {formatar_reais(total_geral)} "
      f"| cidades: {sorted(cidades)}")

# Configuração em arquivo — o princípio que o 06.12 formaliza
config = {"cidades_atendidas": ["campinas", "santos", "sao paulo"],
          "frete_gratis_a_partir_de_centavos": 29_900,
          "parcelas_maximas": 12}
with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as arquivo:
    json.dump(config, arquivo, ensure_ascii=False, indent=2)

with open(ARQUIVO_CONFIG, encoding="utf-8") as arquivo:
    config_lida = json.load(arquivo)
print(f"Configuração lida de config.json: {len(config_lida['cidades_atendidas'])} cidades "
      f"atendidas, frete grátis a partir de R$ "
      f"{formatar_reais(config_lida['frete_gratis_a_partir_de_centavos'])}")
# Saída: (as quatro cenas mostradas na seção 9 do capítulo)
