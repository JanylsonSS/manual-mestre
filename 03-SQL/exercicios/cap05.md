# Exercícios — Capítulo 03.05: Funções de agregação

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap05.md`](gabaritos/cap05.md).

## Aquecimento

### A1 — Preveja o número `[Aquecimento · ~10 min · qual o resultado?]`

**Tarefa.** **Escreva a previsão antes de executar.**

1. `SELECT COUNT(*) FROM produtos;`
2. `SELECT COUNT(*) FROM clientes;`
3. `SELECT COUNT(email) FROM clientes;`
4. `SELECT COUNT(DISTINCT categoria) FROM produtos;`
5. `SELECT MIN(preco_centavos) FROM produtos;`
6. `SELECT SUM(quantidade) FROM itens_pedido;`
7. `SELECT COUNT(*) FROM pedidos WHERE status = 'devolvido';`
8. `SELECT SUM(preco_centavos) FROM produtos WHERE categoria = 'moveis';`

### A2 — Qual função? `[Aquecimento · ~10 min · a pergunta certa]`

**Tarefa.** Escreva a consulta para cada pergunta de negócio:

1. Quantos produtos existem no catálogo?
2. Quantos clientes informaram cidade?
3. Qual o preço médio dos produtos ativos?
4. Qual o produto mais caro (o valor, não o nome)?
5. Quantas unidades foram vendidas ao todo?
6. Qual a data do primeiro e do último pedido?
7. Quantas categorias distintas existem?
8. Qual o faturamento total, em reais, de todos os itens?

### A3 — `NULL` na agregação `[Aquecimento · ~10 min · entra ou não?]`

**Tarefa.** Para cada afirmação, diga se é verdadeira ou falsa e corrija as falsas:

1. `COUNT(*)` ignora linhas em que todas as colunas são nulas.
2. `SUM` de uma coluna com 3 nulos e 5 valores soma os 5.
3. `AVG` de uma coluna com 3 nulos e 5 valores divide por 8.
4. `MIN` pode devolver `NULL` mesmo havendo linhas na tabela.
5. `COUNT(coluna)` devolve 0 quando a coluna é toda nula.
6. `SUM` de conjunto vazio devolve 0.

### A4 — Ache o erro `[Aquecimento · ~10 min · o que está errado?]`

**Tarefa.** Cada consulta tem um problema. Identifique e corrija:

1. `SELECT COUNT(cidade) AS total_clientes FROM clientes;`
2. `SELECT SUM(preco_centavos) AS total FROM produtos WHERE categoria = 'livros';` *(alimenta um relatório)*
3. `SELECT AVG(preco_centavos) FROM produtos;` *(o relatório publica só a média)*
4. `SELECT SUM(preco_centavos / 100.0) AS total_reais FROM produtos;`
5. `SELECT COUNT(*) AS pedidos FROM pedidos p JOIN itens_pedido i ON i.pedido_id = p.id;`
6. `SELECT nome, COUNT(*) FROM produtos;` *(a intenção era contar produtos)*

## Aplicação

### AP1 — O painel de números `[Aplicação · ~20 min · oito indicadores]`

**Tarefa.** Produza, cada um com sua consulta e apelido legível: (1) total de clientes; (2) clientes com e-mail; (3) total de produtos ativos; (4) preço médio dos ativos; (5) produto mais caro e mais barato; (6) total de unidades vendidas; (7) faturamento total em reais; (8) período coberto pelos pedidos (primeira e última data). Registre o resultado de cada um.

### AP2 — A média honesta `[Aplicação · ~20 min · três denominadores]`

**Tarefa.** Sobre a coluna `cidade` de `clientes`: (1) calcule `AVG(LENGTH(cidade))`; (2) calcule a mesma média dividindo pelo total de linhas; (3) calcule tratando ausência como texto vazio (`COALESCE`). Para cada uma: qual pergunta de negócio ela responde? Ao final, escolha qual publicaria num relatório e justifique.

### AP3 — Conjunto vazio `[Aplicação · ~20 min · o NULL do SUM]`

**Tarefa.** Provoque o `NULL` em três cenários diferentes: (1) `SUM` com filtro que não casa nada; (2) `AVG` idem; (3) `MAX` idem. Para cada um: registre o resultado, corrija com `COALESCE` **quando for correto corrigir**, e explique em uma linha os casos em que substituir por zero seria **errado**.

## Desafio

### D1 — O fechamento do mês `[Desafio · ~45 min · um relatório que não pode errar]`

**Tarefa.** Produza o fechamento de **julho de 2026** da Aurora:

- **(a)** número de pedidos, faturamento e ticket médio, considerando **apenas** pedidos concluídos;
- **(b)** os mesmos três números para uma categoria **sem vendas no período** — garanta que o relatório mostre `0,00`, não vazio;
- **(c)** quantos clientes distintos compraram e quantos clientes existem no total — explique por que os dois números importam juntos;
- **(d)** a **prova dos nove** do 01.25: some o faturamento por status e verifique que bate com o total sem filtro;
- **(e)** identifique **um** número do seu relatório que mudaria se você usasse `COUNT(*)` em vez de `COUNT(DISTINCT ...)`, e explique.

**Fecho:** 5 linhas sobre por que um relatório deve publicar o tamanho da amostra junto com toda média.

<details><summary>💡 Dica 1 (conceito)</summary>
Filtrar julho de 2026 com datas em texto `AAAA-MM-DD`: `WHERE data >= '2026-07-01' AND data < '2026-08-01'` — mais seguro que `LIKE '2026-07%'` e capaz de usar índice.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para o item (d), rode uma consulta por status e some à mão; depois compare com a consulta sem `WHERE`. Se não bater, provavelmente há status que você não previu.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Consulta dos três números → a mesma com categoria vazia + `COALESCE` → clientes distintos vs. total → a prova por status → a análise `COUNT(*)` vs `COUNT(DISTINCT)` → reflexão.
</details>
