# Exercícios — Capítulo 03.09: Subconsultas

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap09.md`](gabaritos/cap09.md).

## Aquecimento

### A1 — Onde vai a subconsulta? `[Aquecimento · ~10 min · WHERE, FROM ou SELECT?]`

**Tarefa.** Para cada pergunta, diga em qual posição a subconsulta entraria:

1. Produtos acima do preço médio.
2. Média dos totais por pedido (ticket médio).
3. Cada cliente com o número de pedidos ao lado.
4. Clientes que têm pelo menos um pedido cancelado.
5. A categoria com o maior faturamento total.
6. Cada produto com o total de unidades vendidas ao lado.

### A2 — Correlacionada? `[Aquecimento · ~10 min · quantas execuções?]`

**Tarefa.** Sobre 12 produtos e 8 clientes, diga se cada subconsulta é correlacionada e quantas vezes roda:

1. `WHERE preco_centavos > (SELECT AVG(preco_centavos) FROM produtos)`
2. `WHERE preco_centavos = (SELECT MAX(preco_centavos) FROM produtos WHERE categoria = pr.categoria)`
3. `WHERE id IN (SELECT cliente_id FROM pedidos)`
4. `WHERE EXISTS (SELECT 1 FROM pedidos p WHERE p.cliente_id = c.id)`
5. `SELECT (SELECT COUNT(*) FROM pedidos p WHERE p.cliente_id = c.id) FROM clientes c`
6. `FROM (SELECT categoria, COUNT(*) FROM produtos GROUP BY categoria)`

### A3 — `IN`, `EXISTS` ou escalar? `[Aquecimento · ~10 min · qual operador]`

**Tarefa.** Para cada situação, diga qual construção usar e por quê:

1. Comparar com a média geral.
2. Verificar se o cliente tem algum pedido.
3. Filtrar por uma lista de identificadores vinda de outra tabela.
4. Verificar que o cliente **não** tem nenhum pedido.
5. Comparar com o maior valor da própria categoria.
6. Filtrar produtos que **não** estão numa lista que pode ter nulos.

### A4 — Ache o bug `[Aquecimento · ~10 min · problemas de subconsulta]`

**Tarefa.** Cada consulta tem um problema. Identifique e corrija:

1. `SELECT nome FROM produtos WHERE id NOT IN (SELECT produto_id FROM itens_pedido WHERE quantidade > 1);`
2. `SELECT nome FROM clientes WHERE id = (SELECT cliente_id FROM pedidos);`
3. `SELECT nome FROM produtos WHERE preco_centavos > (SELECT preco_centavos FROM produtos);`
4. `SELECT AVG(total) FROM (SELECT SUM(quantidade) AS total FROM itens_pedido GROUP BY pedido_id);` *(em PostgreSQL)*
5. `SELECT c.nome FROM clientes c WHERE EXISTS (SELECT 1 FROM pedidos p);`
6. `SELECT categoria, (SELECT nome FROM produtos WHERE categoria = pr.categoria) FROM produtos pr GROUP BY categoria;`

## Aplicação

### AP1 — As três posições `[Aplicação · ~25 min · a mesma pergunta, três formas]`

**Tarefa.** A pergunta é *"cada cliente com o número de pedidos"*. Escreva-a: (1) com subquery no `SELECT`; (2) com `JOIN` + `GROUP BY`; (3) com subquery no `FROM` e `JOIN`. Para cada uma: registre o resultado, diga se preserva clientes sem pedidos, e classifique a subconsulta (correlacionada ou não). Ao final, escolha qual publicaria.

### AP2 — `NOT IN` × `NOT EXISTS` `[Aplicação · ~20 min · a armadilha medida]`

**Tarefa.** (1) Escreva "produtos nunca vendidos" com `NOT IN` e registre; (2) escreva com `NOT EXISTS` e registre; (3) provoque a armadilha acrescentando um `NULL` à lista (`UNION SELECT NULL`) e registre as duas versões de novo; (4) explique o mecanismo com a lógica de três valores; (5) escreva a terceira forma — anti-join com `LEFT JOIN` — e compare as três.

### AP3 — Subquery × `JOIN` `[Aplicação · ~25 min · cinco perguntas, duas formas]`

**Tarefa.** Escreva cada pergunta das duas formas (subconsulta e `JOIN`), registre os dois resultados e justifique qual publicaria: (1) clientes que compraram áudio; (2) produtos nunca vendidos; (3) cada cliente com total gasto; (4) pedidos acima do ticket médio; (5) clientes com mais de 3 pedidos. Anote os casos em que uma das formas **não** funciona.

## Desafio

### D1 — O painel de destaques `[Desafio · ~50 min · perguntas que exigem aninhamento]`

**Tarefa.** Produza cinco consultas que só se resolvem com subconsulta:

- **(a)** produtos acima da média de preço **da sua própria categoria** (não da média geral);
- **(b)** o produto mais caro de cada categoria, **com o nome**;
- **(c)** clientes que gastaram acima da média de gasto dos clientes;
- **(d)** clientes que compraram **todos** os produtos de alguma categoria — ou, se nenhum, demonstre que a consulta está correta devolvendo vazio;
- **(e)** o pedido de maior valor de cada cliente.

Para cada uma: identifique se a subconsulta é correlacionada, diga quantas vezes ela roda, e escreva a versão com `JOIN` quando existir.

**Fecho:** 5 linhas sobre quando o aninhamento ajuda a legibilidade e quando a prejudica.

<details><summary>💡 Dica 1 (conceito)</summary>
No item (a), a correlação é a mesma do "mais caro de cada categoria": `AVG(...) FROM produtos WHERE categoria = pr.categoria`.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
No item (d), "comprou todos" se escreve como "não existe produto da categoria que ele não tenha comprado" — `NOT EXISTS` dentro de `NOT EXISTS`. É difícil de propósito.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Cada item: pergunta → SQL → correlacionada? quantas execuções? → versão com JOIN (ou "não existe") → reflexão.
</details>
