# Exercícios — Capítulo 03.07: `JOIN` — parte 1: `INNER`

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap07.md`](gabaritos/cap07.md).

## Aquecimento

### A1 — Quantas linhas? `[Aquecimento · ~10 min · preveja antes de rodar]`

**Tarefa.** **Escreva a previsão antes de executar.** Tabelas: `clientes` 8 · `produtos` 12 · `pedidos` 20 · `itens_pedido` 31.

1. `FROM produtos, itens_pedido`
2. `FROM pedidos p JOIN itens_pedido i ON i.pedido_id = p.id`
3. `FROM produtos pr JOIN itens_pedido i ON i.produto_id = pr.id`
4. `FROM clientes c JOIN pedidos p ON p.cliente_id = c.id WHERE p.status = 'concluido'`
5. `FROM clientes, produtos`
6. As quatro tabelas encadeadas com `JOIN`

### A2 — Escreva o `ON` `[Aquecimento · ~10 min · a condição de ligação]`

**Tarefa.** Para cada par de tabelas, escreva a condição de junção:

1. `clientes` e `pedidos`
2. `pedidos` e `itens_pedido`
3. `itens_pedido` e `produtos`
4. `clientes` e `itens_pedido` (indireto — quantas tabelas são necessárias?)
5. Duas cópias de `clientes` (clientes da mesma cidade — como se escreve?)
6. `produtos` e `pedidos` (indireto)

### A3 — Ache o cartesiano `[Aquecimento · ~10 min · quais travam?]`

**Tarefa.** Quais consultas produzem produto cartesiano? Para as que produzem, aponte o que falta:

1. `SELECT * FROM clientes, pedidos WHERE clientes.id = pedidos.cliente_id;`
2. `SELECT * FROM clientes, pedidos;`
3. `SELECT * FROM clientes c JOIN pedidos p ON c.id > 0;`
4. `SELECT * FROM clientes c JOIN pedidos p ON p.cliente_id = c.id JOIN itens_pedido i ON i.pedido_id = p.id;`
5. `SELECT * FROM clientes c JOIN pedidos p ON p.cliente_id = c.id JOIN produtos pr ON pr.ativo = 1;`

### A4 — Traduza a pergunta `[Aquecimento · ~10 min · atravessando tabelas]`

**Tarefa.** Escreva a consulta para cada pergunta:

1. Nome do cliente e data de cada pedido.
2. Nome do produto e quantidade de cada item do pedido 1.
3. Todos os produtos comprados pela Ana Souza.
4. Cidade do cliente e nome do produto, para cada item vendido.
5. Pedidos concluídos com o nome do cliente, ordenados por data.
6. Categorias de produto que a Fernanda comprou (sem repetição).

## Aplicação

### AP1 — O extrato do cliente `[Aplicação · ~25 min · quatro tabelas]`

**Tarefa.** Construa o extrato de compras de um cliente: (1) escreva a consulta com as quatro tabelas, trazendo produto, quantidade, preço unitário, valor da linha e data; (2) **preveja** quantas linhas terá para a Fernanda e para a Ana **antes** de rodar; (3) execute e compare; (4) explique a divergência, se houver; (5) adapte para receber o `id` do cliente em vez do nome.

### AP2 — Prevendo a granularidade `[Aplicação · ~20 min · cinco junções]`

**Tarefa.** Para cada junção abaixo, escreva a previsão, execute e explique: (1) `clientes` + `pedidos`; (2) `pedidos` + `itens_pedido`; (3) `clientes` + `pedidos` + `itens_pedido`; (4) as quatro tabelas; (5) `produtos` + `itens_pedido`. Ao final, enuncie com suas palavras a regra que prevê o resultado.

### AP3 — A soma dobrada `[Aplicação · ~25 min · reproduzindo o bug]`

**Tarefa.** O laboratório não tem duas tabelas filhas do mesmo pai — crie o cenário: (1) crie uma tabela `pagamentos(id, pedido_id, valor_centavos)` num banco de teste (`AURORA_BANCO=teste.db`) e insira **2 pagamentos** para um pedido que já tem **2 itens**; (2) escreva a consulta que junta pedido + itens + pagamentos e some os dois; (3) compare com as somas corretas, calculadas separadamente; (4) explique o fator de inflação de cada uma; (5) escreva a versão correta usando duas consultas separadas.

## Desafio

### D1 — O relatório de vendas completo `[Desafio · ~50 min · a consulta que atravessa o modelo]`

**Tarefa.** Produza um relatório com uma linha por **item vendido**, contendo: nome do cliente, cidade, data do pedido, status, nome do produto, categoria, quantidade, preço unitário e valor total da linha — tudo com apelidos legíveis. Depois:

- **(a)** preveja o número de linhas **antes** de rodar e confira;
- **(b)** filtre para pedidos concluídos e explique se o filtro vai no `ON` ou no `WHERE` (e se faz diferença num `INNER JOIN`);
- **(c)** acrescente uma agregação que conte **pedidos** e outra que conte **itens**, na mesma consulta, e explique por que precisam de tratamentos diferentes;
- **(d)** escreva deliberadamente a versão com produto cartesiano e compare o número de linhas;
- **(e)** identifique qual índice tornaria essa consulta mais rápida em escala, e justifique.

**Fecho:** 5 linhas sobre por que "prever o número de linhas" é a habilidade central deste capítulo.

<details><summary>💡 Dica 1 (conceito)</summary>
Para o item (a): a tabela mais fina da junção define o resultado. Qual é ela, e quantas linhas tem depois do filtro?
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
No item (b), num `INNER JOIN` o filtro no `ON` e no `WHERE` dão o mesmo resultado — e isso **muda** no 03.08. Registre a observação; ela vai ser cobrada.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Consulta base com 4 JOINs e apelidos → previsão e conferência → filtro de status → as duas contagens (`COUNT(*)` e `COUNT(DISTINCT)`) → a versão cartesiana → o índice na FK → reflexão.
</details>
