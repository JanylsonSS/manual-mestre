# Exercícios — Capítulo 01.23: JSON em Python

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap23.md`](gabaritos/cap23.md).

## Aquecimento

### A1 — Correspondência de tipos `[Aquecimento · ~10 min · a viagem]`

**Tarefa.** Para cada valor Python: o que vira em JSON e como volta?

1. `{"a": 1}`
2. `[1, 2, 3]`
3. `("a", "b")`
4. `True`
5. `None`
6. `{"cidades"}` (conjunto)
7. `46990`
8. `{1: "um"}`

### A2 — JSON válido? `[Aquecimento · ~10 min · a rigidez do formato]`

**Tarefa.** Quais são JSON válido? Para os inválidos, aponte o erro:

1. `{"nome": "Ana", "ativo": true}`
2. `{'nome': 'Ana'}`
3. `{"nome": "Ana", "ativo": True}`
4. `{"itens": [1, 2, 3,]}`
5. `{"obs": null}`
6. `{"nome": "Ana"} // comentário`

### A3 — Navegação `[Aquecimento · ~10 min · aninhamento]`

**Tarefa.** Dado:

```python
dados = {"pedido": {"codigo": "PED-1",
                    "cliente": {"nome": "Ana"},
                    "itens": [{"produto": "Fone", "qtd": 2}]}}
```

Resultado ou erro de:

1. `dados["pedido"]["codigo"]`
2. `dados["pedido"]["cliente"]["email"]`
3. `dados["pedido"].get("cliente", {}).get("email", "sem e-mail")`
4. `dados["pedido"]["itens"][0]["produto"]`
5. `dados.get("cliente", {}).get("nome", "?")`

### A4 — CSV ou JSON? `[Aquecimento · ~5 min · o critério]`

**Tarefa.** Escolha e justifique: (1) export diário de 50 mil vendas; (2) pedido com itens e cliente; (3) configuração do sistema; (4) resposta de uma API de CEP; (5) planilha para o time comercial; (6) catálogo de produtos com atributos variáveis por categoria.

## Aplicação

### AP1 — Ida e volta `[Aplicação · ~20 min · o que sobrevive]`

**Tarefa.** Monte um dicionário com **todos** os tipos da tabela (incluindo tupla e chave numérica), grave, leia de volta, e produza um relatório campo a campo: `campo | tipo antes | tipo depois | idêntico?`.

### AP2 — O catálogo `[Aplicação · ~25 min · navegação em lista de aninhados]`

**Tarefa.** Leia o `catalogo.json` gerado pelo capítulo (ou crie um com 5 pedidos) e produza: total por cidade, o produto mais vendido (por quantidade), e a lista de códigos não pagos. Navegue com segurança nos campos opcionais.

### AP3 — Configuração externa `[Aplicação · ~20 min · o princípio do 06.12]`

**Tarefa.** Mova as constantes da sua biblioteca (`CIDADE_SEDE`, faixas de frete, `PARCELAS_MAXIMAS`) para `config.json`; escreva `carregar_config(caminho)` com tratamento de arquivo ausente e padrões sensatos. Prove que mudar o JSON muda o comportamento sem tocar no código.

## Desafio

### D1 — O conversor bidirecional `[Desafio · ~50 min · CSV ⇄ JSON]`

**Tarefa.** `csv_para_json(caminho_csv, caminho_json)` (agrupando por cidade, com totais) e `json_para_csv(caminho_json, caminho_csv)` (achatando de volta). Teste de ida e volta comparando os conjuntos de registros (ordenados por código). Documente em 5 linhas o que se perde em cada direção.

<details><summary>💡 Dica 1 (conceito)</summary>
Agrupar é `setdefault(cidade, []).append(pedido)` — o que o JSON representa bem e o CSV não.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Ordene por código antes de comparar: ordem não é o que você está testando.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
DictReader → agrupar → json.dump; json.load → percorrer grupos → DictWriter → comparar.
</details>
