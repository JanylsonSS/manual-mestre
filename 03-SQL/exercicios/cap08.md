# Exercícios — Capítulo 03.08: `JOIN` — parte 2: `LEFT`/`RIGHT`/`FULL`

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap08.md`](gabaritos/cap08.md).

## Aquecimento

### A1 — Quantas linhas? `[Aquecimento · ~10 min · INNER × LEFT]`

**Tarefa.** **Escreva a previsão antes de executar.** Lembre: 8 clientes (1 sem pedidos), 12 produtos (1 sem vendas), 20 pedidos, 31 itens.

1. `clientes c JOIN pedidos p ON p.cliente_id = c.id`
2. `clientes c LEFT JOIN pedidos p ON p.cliente_id = c.id`
3. `produtos pr JOIN itens_pedido i ON i.produto_id = pr.id`
4. `produtos pr LEFT JOIN itens_pedido i ON i.produto_id = pr.id`
5. `clientes c LEFT JOIN pedidos p ON p.cliente_id = c.id WHERE p.id IS NULL`
6. `clientes c LEFT JOIN pedidos p ON p.cliente_id = c.id WHERE p.status = 'cancelado'`

### A2 — Qual junção? `[Aquecimento · ~10 min · a pergunta decide]`

**Tarefa.** Para cada pergunta, diga se usa `INNER`, `LEFT` ou anti-join:

1. Listar os pedidos com o nome do cliente.
2. Listar todos os clientes e quantos pedidos cada um fez.
3. Descobrir quais produtos nunca foram vendidos.
4. Listar os itens de pedido com o nome do produto.
5. Listar todas as categorias e o faturamento de cada uma (mesmo as sem venda).
6. Descobrir quais clientes não têm e-mail cadastrado.
7. Listar todos os produtos com o total de unidades vendidas.
8. Descobrir quais pedidos não têm nenhum item.

### A3 — `ON` ou `WHERE`? `[Aquecimento · ~10 min · num LEFT JOIN]`

**Tarefa.** Numa consulta `clientes c LEFT JOIN pedidos p ON p.cliente_id = c.id`, onde vai cada condição — e por quê?

1. `c.cidade = 'campinas'`
2. `p.status = 'concluido'`
3. `p.id IS NULL`
4. `p.data >= '2026-01-01'`
5. `c.email IS NOT NULL`
6. `p.status <> 'cancelado'`

### A4 — Ache o bug `[Aquecimento · ~10 min · junção externa]`

**Tarefa.** Cada consulta tem um problema. Identifique e corrija:

1. `SELECT c.nome, COUNT(*) FROM clientes c LEFT JOIN pedidos p ON p.cliente_id = c.id GROUP BY c.id;`
2. `SELECT c.nome FROM clientes c LEFT JOIN pedidos p ON p.cliente_id = c.id WHERE p.status IS NULL;` *(intenção: quem nunca comprou)*
3. `SELECT c.nome, SUM(i.quantidade) FROM clientes c LEFT JOIN pedidos p ON p.cliente_id = c.id LEFT JOIN itens_pedido i ON i.pedido_id = p.id GROUP BY c.id;` *(o relatório mostra células vazias)*
4. `SELECT c.nome, COUNT(p.id) FROM clientes c LEFT JOIN pedidos p ON p.cliente_id = c.id WHERE p.data >= '2026-01-01' GROUP BY c.id;`
5. `SELECT pr.nome FROM itens_pedido i LEFT JOIN produtos pr ON pr.id = i.produto_id WHERE i.id IS NULL;` *(intenção: produtos nunca vendidos)*
6. `SELECT c.nome, p.id FROM clientes c LEFT JOIN pedidos p ON p.cliente_id = c.id JOIN itens_pedido i ON i.pedido_id = p.id;` *(intenção: preservar todos os clientes)*

## Aplicação

### AP1 — O painel completo `[Aplicação · ~25 min · comparando as contagens]`

**Tarefa.** Refaça três relatórios do módulo trocando `INNER` por `LEFT` e compare: (1) clientes e número de pedidos; (2) produtos e unidades vendidas; (3) categorias e faturamento. Para cada um: registre a contagem de linhas nas duas versões, identifique **quem** aparece só na versão `LEFT`, e diga qual das duas você publicaria e por quê.

### AP2 — A família de anti-joins `[Aplicação · ~20 min · perguntas pela ausência]`

**Tarefa.** Escreva quatro anti-joins: (1) clientes sem pedidos; (2) produtos sem vendas; (3) pedidos sem itens; (4) categorias sem produtos ativos. Para cada um: identifique a chave primária testada, execute, e **confira a completude** — a contagem do anti-join mais a contagem da versão positiva deve dar o total da tabela.

### AP3 — `ON` × `WHERE` medido `[Aplicação · ~25 min · três cenários]`

**Tarefa.** Para três condições diferentes (status, data e valor), escreva as duas versões — condição no `ON` e no `WHERE` — e registre: (1) o número de linhas de cada uma; (2) quem some na versão `WHERE`; (3) qual das duas responde à pergunta "todos os clientes, com seus pedidos de 2026". Ao final, enuncie a regra com suas palavras.

## Desafio

### D1 — O relatório que não perde ninguém `[Desafio · ~50 min · auditoria de cobertura]`

**Tarefa.** Produza um painel de clientes que **nunca** perde uma linha:

- **(a)** todos os clientes com número de pedidos, total gasto e data da última compra — quem nunca comprou aparece com 0, R$ 0,00 e "nunca";
- **(b)** escreva a versão errada (filtro no `WHERE`) e mostre quantas linhas ela perde;
- **(c)** construa os **três** anti-joins do laboratório — clientes sem pedidos, produtos sem vendas, categorias sem produtos ativos;
- **(d)** escreva uma consulta de conciliação que, para cada cliente, mostre quantos pedidos tem em cada status (zeros onde não houver);
- **(e)** explique por que `COUNT(*)`, `SUM` e `MAX` precisam de tratamentos diferentes na linha preservada.

**Fecho:** 5 linhas sobre por que "o relatório perdeu linhas" é mais perigoso que "o relatório deu erro".

<details><summary>💡 Dica 1 (conceito)</summary>
Para o item (a), "nunca" na data: `COALESCE(MAX(p.data), 'nunca')` — o `MAX` de um conjunto vazio devolve `NULL` (03.05).
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
No item (d), três contagens condicionais na mesma consulta: `COUNT(CASE WHEN p.status = 'concluido' THEN 1 END)` — o `CASE` sem `ELSE` devolve `NULL`, que o `COUNT` ignora.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
LEFT JOIN + GROUP BY → COALESCE em cada agregação → versão errada com WHERE → os três anti-joins → a conciliação com CASE → a explicação por função → reflexão.
</details>
