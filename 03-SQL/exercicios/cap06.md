# Exercícios — Capítulo 03.06: `GROUP BY` e `HAVING`

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap06.md`](gabaritos/cap06.md).

## Aquecimento

### A1 — Quantos grupos? `[Aquecimento · ~10 min · preveja as linhas]`

**Tarefa.** **Escreva a previsão antes de executar.** Quantas linhas cada agrupamento devolve?

1. `SELECT categoria, COUNT(*) FROM produtos GROUP BY categoria;`
2. `SELECT status, COUNT(*) FROM pedidos GROUP BY status;`
3. `SELECT cidade, COUNT(*) FROM clientes GROUP BY cidade;`
4. `SELECT cliente_id, COUNT(*) FROM pedidos GROUP BY cliente_id;`
5. `SELECT ativo, COUNT(*) FROM produtos GROUP BY ativo;`
6. `SELECT pedido_id, COUNT(*) FROM itens_pedido GROUP BY pedido_id;`

### A2 — `WHERE` ou `HAVING`? `[Aquecimento · ~10 min · onde vai a condição?]`

**Tarefa.** Para cada condição, diga se vai no `WHERE` ou no `HAVING` — e por quê:

1. Apenas produtos ativos.
2. Apenas categorias com mais de 3 produtos.
3. Apenas pedidos de 2026.
4. Apenas cidades cujo faturamento passa de R$ 1.000.
5. Apenas clientes com e-mail cadastrado.
6. Apenas grupos cuja média de preço passa de R$ 200.
7. Apenas produtos acima de R$ 300.
8. Apenas categorias que têm ao menos um produto inativo.

### A3 — Regra de ouro `[Aquecimento · ~10 min · quais violam?]`

**Tarefa.** Quais consultas violam a regra de ouro? Para as que violam, diga o que fazer:

1. `SELECT categoria, COUNT(*) FROM produtos GROUP BY categoria;`
2. `SELECT categoria, nome FROM produtos GROUP BY categoria;`
3. `SELECT categoria, MAX(preco_centavos) FROM produtos GROUP BY categoria;`
4. `SELECT cidade, nome, COUNT(*) FROM clientes GROUP BY cidade, nome;`
5. `SELECT status, data, COUNT(*) FROM pedidos GROUP BY status;`
6. `SELECT COUNT(*) FROM produtos;`

### A4 — Traduza a pergunta `[Aquecimento · ~10 min · escreva a consulta]`

**Tarefa.** Escreva a consulta para cada pergunta:

1. Quantos produtos há por categoria?
2. Quantos pedidos cada cliente fez?
3. Quais categorias têm mais de 2 produtos?
4. Qual o preço médio por categoria, do maior para o menor?
5. Quantos itens tem cada pedido?
6. Quais clientes fizeram mais de 3 pedidos?

## Aplicação

### AP1 — O painel agrupado `[Aplicação · ~25 min · seis agrupamentos]`

**Tarefa.** Produza, cada um com apelidos e ordenação explícita: (1) clientes por cidade; (2) produtos por categoria, com preço médio; (3) pedidos por status, ordenados por quantidade; (4) itens por pedido, mostrando os 5 pedidos com mais itens; (5) unidades vendidas por produto; (6) faturamento por categoria de produto. Registre o resultado de cada um.

### AP2 — `WHERE` × `HAVING` lado a lado `[Aplicação · ~20 min · a mesma pergunta, duas formas]`

**Tarefa.** Sobre `produtos`, com o limiar de R$ 200: (1) escreva a versão com `WHERE` e registre; (2) escreva a versão com `HAVING` sobre a média e registre; (3) explique em duas linhas **qual pergunta** cada uma responde; (4) identifique uma categoria que aparece nas duas com **números diferentes** e explique; (5) escreva uma terceira consulta que use as duas cláusulas juntas.

### AP3 — O grupo `NULL` `[Aplicação · ~20 min · três destinos]`

**Tarefa.** Encontre três agrupamentos do laboratório em que um grupo `NULL` aparece (ou apareceria se houvesse nulos). Para cada um, produza **três** versões: (a) deixando o grupo `NULL` aparecer; (b) excluindo-o com `WHERE ... IS NOT NULL`; (c) rotulando-o com `COALESCE(coluna, 'não informado')`. Diga qual publicaria em cada caso e por quê.

## Desafio

### D1 — O painel de vendas `[Desafio · ~50 min · o primeiro gráfico de qualquer dashboard]`

**Tarefa.** Produza cinco agrupamentos que formariam o painel de vendas da Aurora:

- **(a)** faturamento e número de pedidos **por cidade**, considerando só pedidos concluídos;
- **(b)** faturamento **por categoria de produto**;
- **(c)** número de pedidos **por status**, com o percentual sobre o total;
- **(d)** clientes **por cidade** com pelo menos 2 clientes, usando `HAVING`;
- **(e)** **ticket médio por cidade** — e explique por que ele não é a média das médias.

Para cada um: escreva a pergunta em português **antes** do SQL, e diga se algum grupo `NULL` aparece e o que você decidiu fazer com ele.

**Fecho:** 5 linhas comparando a versão SQL com o `relatorio_aurora.py` do 01.25 — o que ficou melhor, e o que o Python ainda fazia que o SQL não faz.

<details><summary>💡 Dica 1 (conceito)</summary>
Para o percentual do item (c), você precisa do total geral dentro de uma consulta agrupada — use uma subconsulta escalar: `COUNT(*) * 100.0 / (SELECT COUNT(*) FROM pedidos)`.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Ticket médio por cidade = faturamento da cidade ÷ **pedidos** da cidade. Cuidado: `AVG` sobre os itens daria a média por **item**, que é outra coisa.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Cada item: pergunta em português → SQL com `AS` → resultado → decisão sobre o grupo `NULL`. No fecho, compare linhas de código, legibilidade e o que o Python fazia a mais (quarentena, validação).
</details>
