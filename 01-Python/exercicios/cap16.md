# Exercícios — Capítulo 01.16: Conjuntos

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap16.md`](gabaritos/cap16.md).

## Aquecimento

### A1 — Previsão `[Aquecimento · ~10 min · unicidade e restrições]`

**Tarefa.** Preveja resultado ou erro exato:

1. `len({"a", "b", "a", "c"})`
2. `type({})`
3. `type(set())`
4. `set("aaa")`
5. `set("aurora")`
6. `{"a", "b"}[0]`
7. `"a" in {"a", "b"}`
8. `{1, 2} | {2, 3}`

### A2 — As quatro operações `[Aquecimento · ~10 min · à mão]`

**Tarefa.** Com `A = {"ana", "bruno", "carla"}` e `B = {"carla", "diego"}`, calcule **à mão** (depois confira): `A | B` · `A & B` · `A - B` · `B - A` · `A ^ B` · `A.isdisjoint(B)`.

### A3 — Qual estrutura? `[Aquecimento · ~5 min · o quarteto]`

**Tarefa.** lista, tupla, dicionário ou conjunto?

1. Os pedidos do dia, em ordem de chegada.
2. Quanto vendemos por cidade.
3. As UFs válidas para validação.
4. Um registro de venda (código, produto, valor).
5. Os clientes distintos que já compraram.
6. O histórico de preços de um produto.
7. A busca "este código já foi processado?".
8. Cliente → total gasto.

### A4 — Itens válidos `[Aquecimento · ~5 min · unhashable]`

**Tarefa.** Quais podem entrar num conjunto? `"ana"` · `42` · `("ana", 30)` · `["ana"]` · `{"a": 1}` · `("ana", ["x"])`.

## Aplicação

### AP1 — A base de clientes `[Aplicação · ~20 min · dicionário de conjuntos]`

**Tarefa.** Do lote com clientes, monte `cidade → conjunto de clientes` e responda: (a) quantos clientes distintos no total; (b) quem comprou em Campinas E Santos; (c) quem comprou só em Campinas; (d) quantos clientes têm Sorocaba ou São Paulo. Todas as saídas com `sorted()`.

### AP2 — Validação por lista branca `[Aplicação · ~20 min · qualidade de dados]`

**Tarefa.** Defina `CIDADES_VALIDAS = {"campinas", "santos", "sao paulo"}` e `PRODUTOS_VALIDOS` (3 itens). Percorra um lote com sujeira e produza: o conjunto de cidades **inválidas** encontradas (diferença!), o de produtos inválidos, e um relatório de qualidade com contagens.

<details><summary>💡 Dica 1 (conceito)</summary>
Cidades encontradas − cidades válidas = as inválidas. Uma operação, não um laço de comparação.
</details>

### AP3 — Dedupe preservando ordem `[Aplicação · ~20 min · o padrão da idempotência]`

**Tarefa.** Dada uma lista com duplicatas em ordem específica, produza: (a) `list(set(lista))` e (b) a versão com "já vistos" preservando a ordem. Imprima as duas lado a lado e explique em 3 linhas quando cada uma serve.

## Desafio

### D1 — Reconciliação de bases `[Desafio · ~45 min · conjuntos em produção]`

**Tarefa.** Duas listas de códigos (fornecedor e sistema), com sobreposição parcial, duplicatas e sujeira. Produza o relatório: (a) únicos em cada base; (b) conferem (interseção); (c) faltantes (fornecedor − sistema); (d) surpresas (sistema − fornecedor); (e) veredito de igualdade. Fecho: 5 linhas sobre custo/legibilidade com listas puras e onde isso reaparece na vida real.

<details><summary>💡 Dica 1 (conceito)</summary>
Mapeie cada item do relatório para uma operação ANTES de codar.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Canonize (strip/upper) antes: um espaço faz um código sumir da interseção — e o relatório mente.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
listas cruas → conjuntos canonizados → 4 operações → relatório com sorted() → veredito → reflexão.
</details>
