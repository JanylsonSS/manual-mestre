# Exercícios — Capítulo 03.10: CTEs (`WITH`)

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap10.md`](gabaritos/cap10.md).

## Aquecimento

### A1 — Leia a CTE `[Aquecimento · ~10 min · o que cada etapa produz?]`

**Tarefa.** Para cada consulta, descreva **em português** o que a CTE produz e o que a consulta final faz:

1. `WITH ativos AS (SELECT * FROM produtos WHERE ativo = 1) SELECT COUNT(*) FROM ativos;`
2. `WITH por_cat AS (SELECT categoria, COUNT(*) AS n FROM produtos GROUP BY categoria) SELECT * FROM por_cat WHERE n > 2;`
3. `WITH tot AS (SELECT pedido_id, SUM(quantidade) AS q FROM itens_pedido GROUP BY pedido_id) SELECT AVG(q) FROM tot;`
4. `WITH a AS (SELECT id FROM clientes WHERE cidade = 'campinas'), b AS (SELECT cliente_id FROM pedidos) SELECT COUNT(*) FROM a JOIN b ON b.cliente_id = a.id;`
5. `WITH RECURSIVE n(x) AS (SELECT 1 UNION ALL SELECT x*2 FROM n WHERE x < 100) SELECT x FROM n;`

### A2 — CTE ou não? `[Aquecimento · ~10 min · melhora ou piora?]`

**Tarefa.** Para cada consulta, decida se reescrever com CTE melhora, piora ou é indiferente — e justifique:

1. `SELECT nome FROM clientes WHERE cidade = 'campinas';`
2. Uma consulta que agrega por pedido, depois por cliente, depois compara com a média.
3. `SELECT COUNT(*) FROM produtos;`
4. Uma consulta que usa o mesmo total geral em três colunas diferentes.
5. Uma junção de duas tabelas com filtro.
6. Uma consulta que agrega itens **e** pagamentos do mesmo pedido.

### A3 — Ache o erro `[Aquecimento · ~10 min · `WITH` defeituoso]`

**Tarefa.** Cada consulta tem um problema. Identifique e corrija:

1. `WITH a AS (SELECT 1 AS x) WITH b AS (SELECT 2 AS y) SELECT * FROM a;`
2. `WITH media AS (SELECT AVG(preco_centavos) AS m FROM produtos) SELECT nome FROM produtos WHERE preco_centavos > media;`
3. `WITH a AS (SELECT * FROM b), b AS (SELECT * FROM produtos) SELECT * FROM a;`
4. `WITH totais AS (SELECT pedido_id, SUM(quantidade) FROM itens_pedido GROUP BY pedido_id) SELECT pedido_id, soma FROM totais;`
5. `WITH RECURSIVE n(x) AS (SELECT 1 UNION ALL SELECT x+1 FROM n) SELECT x FROM n;`
6. `WITH cte AS (SELECT * FROM produtos); SELECT * FROM cte;`

### A4 — Nomeie a etapa `[Aquecimento · ~10 min · o nome revela a abstração]`

**Tarefa.** Para cada bloco, proponha um nome de CTE — e diga se o bloco **merece** ser uma CTE:

1. `SELECT pedido_id, SUM(quantidade * preco_unitario_centavos) FROM itens_pedido GROUP BY pedido_id`
2. `SELECT * FROM produtos WHERE ativo = 1`
3. `SELECT cliente_id, COUNT(*) FROM pedidos WHERE status = 'concluido' GROUP BY cliente_id`
4. `SELECT AVG(preco_centavos) FROM produtos`
5. `SELECT id FROM clientes WHERE id > 0`
6. `SELECT categoria, MAX(preco_centavos) FROM produtos GROUP BY categoria`

## Aplicação

### AP1 — Refatorando `[Aplicação · ~25 min · aninhado → nomeado]`

**Tarefa.** Reescreva com CTEs três consultas aninhadas do módulo: (1) o ticket médio do 03.09; (2) o produto mais caro de cada categoria (03.09); (3) clientes acima da média de gasto (03.09/D1c). Para cada uma: **antes** de reescrever, liste os passos em português; depois, confirme que o resultado é idêntico; e diga se a versão com CTE ficou melhor.

### AP2 — O reuso `[Aplicação · ~20 min · a mesma etapa duas vezes]`

**Tarefa.** Escreva três consultas em que a mesma CTE é usada **duas ou mais** vezes: (1) gasto por cliente e o percentual do total; (2) faturamento por categoria e a diferença para a categoria líder; (3) pedidos por cliente e quantos estão acima da média de pedidos. Para cada uma, escreva também a versão sem CTE e conte quantas linhas de texto foram duplicadas.

### AP3 — As duas filhas `[Aplicação · ~25 min · fechando o 03.07]`

**Tarefa.** Recrie a tabela `pagamentos` do 03.07/AP3 num banco de teste e: (1) reproduza a soma dobrada com uma junção só; (2) escreva a versão correta com duas CTEs; (3) confirme que os totais batem com as somas calculadas separadamente; (4) acrescente `LEFT JOIN` e `COALESCE` para preservar pedidos sem pagamento; (5) explique em três linhas por que a CTE resolve o problema na raiz.

## Desafio

### D1 — O painel executivo `[Desafio · ~50 min · uma consulta que outra pessoa mantém]`

**Tarefa.** Construa, com CTEs, um painel de clientes contendo: nome, cidade, número de pedidos concluídos, valor total gasto, ticket médio do cliente, percentual do faturamento total, e a diferença entre o gasto dele e a média geral.

- **(a)** mínimo de **três** CTEs encadeadas, cada uma com nome que descreve o que produz;
- **(b)** todos os clientes aparecem, inclusive quem nunca comprou (03.08);
- **(c)** nenhuma soma inflada por multiplicação de linhas (03.07);
- **(d)** escreva a **mesma** consulta sem CTEs, com aninhamento, e compare lado a lado;
- **(e)** peça a alguém — ou ao seu eu de amanhã — para ler as duas e dizer o que cada uma faz, cronometrando.

**Fecho:** 5 linhas sobre por que legibilidade em SQL é critério de engenharia e não de estética.

<details><summary>💡 Dica 1 (conceito)</summary>
Estrutura sugerida: `totais_por_pedido` → `resumo_por_cliente` → `totais_gerais`, e a consulta final juntando `clientes` (com `LEFT JOIN`) ao resumo.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para o item (b), a última junção precisa partir de `clientes` com `LEFT JOIN` ao resumo — e `COALESCE` em todas as agregações.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`WITH etapa1 AS (...), etapa2 AS (...), etapa3 AS (...) SELECT ... FROM clientes c LEFT JOIN etapa2 ...` → versão aninhada → comparação cronometrada → reflexão.
</details>
