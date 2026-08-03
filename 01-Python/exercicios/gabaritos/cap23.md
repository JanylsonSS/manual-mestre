# Gabaritos — Capítulo 01.23

Abra somente após tentativa honesta.

## A1 — Correspondência de tipos

1. objeto `{"a": 1}` → `dict` · 2. array → `list` · 3. array (**perde a tupla**) → `list` · 4. `true` → `bool` · 5. `null` → `None` · 6. **`TypeError`** (set não embarca) · 7. number → `int` · 8. `{"1": "um"}` (**chave vira string**) → `dict` com chave `str`.

**Critério:** 8/8; os itens 3, 6 e 8 são as três armadilhas do capítulo.

## A2 — JSON válido?

1. ✓ · 2. ✗ aspas simples (JSON exige duplas) · 3. ✗ `True` com maiúscula (JSON usa `true`) · 4. ✗ vírgula sobrando antes do `]` · 5. ✓ · 6. ✗ JSON não tem comentários.

**Critério:** 6/6 com os erros nomeados.

## A3 — Navegação

1. `"PED-1"` · 2. **`KeyError: 'email'`** · 3. `"sem e-mail"` (get encadeado com padrão) · 4. `"Fone"` (índice em lista dentro de dicionário) · 5. `"?"` — atenção: `dados` não tem chave "cliente" no topo (ela está dentro de "pedido"), então o get devolve `{}` e depois o padrão.

**Critério:** 5/5; o item 5 testa a leitura atenta da estrutura.

## A4 — CSV ou JSON?

1. **CSV** (tabular, volume — e, adiante, Parquet) · 2. **JSON** (aninhado) · 3. **JSON** (chaves nomeadas, tipos) · 4. **JSON** (é o que a API devolve) · 5. **CSV** (abre em planilha) · 6. **JSON** (atributos variáveis por categoria não cabem em colunas fixas).

**Critério:** 6/6 com justificativa de uma linha.

## AP1 — Ida e volta

Relatório esperado (linhas-chave): `tupla | tuple | list | ✗`; `chave_int | int | str | ✗`; `texto | str | str | ✓`; `numero | int | int | ✓`; `decimal | float | float | ✓ (com ressalva de precisão)`; `booleano | bool | bool | ✓`; `nulo | NoneType | NoneType | ✓`.

**Erro esperado:** incluir um `set` no dicionário e o programa quebrar na gravação — o que é o **aprendizado**: converta antes (`list(...)`) e anote a perda de unicidade.
**Critério:** relatório campo a campo com as duas divergências identificadas.

## AP2 — O catálogo

Com o catálogo do capítulo: total por cidade → Campinas (pedido 1: 66.770 + pedido 3: 39.890) e Santos (8.990); produto mais vendido por quantidade → Cabo HDMI (2 unidades); não pagos → `PED-2026-00124`.

**Erro esperado:** somar `valor_centavos` sem multiplicar pela quantidade — o total do item é `qtd × valor`.
**Critério:** 3 respostas corretas; navegação com `get` onde o campo é opcional (`observacao`).

## AP3 — Configuração externa

Referência:

```python
def carregar_config(caminho):
    """Lê a config; devolve padrões se o arquivo não existir."""
    padroes = {"cidades_atendidas": ["campinas"], "frete_gratis_a_partir_de_centavos": 29_900,
               "parcelas_maximas": 12}
    try:
        with open(caminho, encoding="utf-8") as arquivo:
            return {**padroes, **json.load(arquivo)}   # arquivo sobrepõe padrões
    except FileNotFoundError:
        return padroes
```

**Prova esperada:** mudar `frete_gratis_a_partir_de_centavos` para 24_900 no JSON e ver `calcular_frete(25_000, "santos")` passar de 990 para 0 — **sem editar `.py`**.
**Critério:** função com tratamento de ausência; prova executada e registrada.

## D1 — O conversor bidirecional

**Estrutura de referência:** CSV → dicionário `cidade → {"total": N, "pedidos": [...]}` → `json.dump`; JSON → percorrer cidades e pedidos → `DictWriter` com as colunas originais.

**O que se perde (a reflexão pedida):** de CSV para JSON não se perde nada (só se ganha estrutura) — mas se **inventa** hierarquia que o original não tinha (a cidade vira nível, e o total vira dado derivado que pode dessincronizar). De JSON para CSV perde-se a hierarquia e os campos derivados: o total por cidade não cabe na linha do pedido (ou é repetido em todas as linhas, criando redundância). "Achatar" é sempre escolher o que descartar.

**Erros esperados:** gravar o total por cidade em cada linha do CSV sem avisar (redundância silenciosa); comparar arquivos byte a byte em vez de comparar conjuntos de registros ordenados.
**Critério de "está bom":** as duas funções operando; ida e volta preservando o conjunto de registros; reflexão cobrindo a perda **e** a invenção de estrutura.
