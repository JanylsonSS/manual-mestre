# Gabaritos — Capítulo 03.06

Abra somente após tentativa honesta.

## A1 — Quantos grupos?

| # | Agrupamento | Linhas | Observação |
|---|---|---|---|
| 1 | por `categoria` | **4** | audio, video, perifericos, acessorios |
| 2 | por `status` | **3** | concluido, pendente, cancelado |
| 3 | por `cidade` | **4** | 3 cidades + o grupo `NULL` da Helena |
| 4 | por `cliente_id` em `pedidos` | **7** | o Rafael não tem pedidos, e por isso **não aparece** |
| 5 | por `ativo` | **2** | 0 e 1 |
| 6 | por `pedido_id` em `itens_pedido` | **20** | um grupo por pedido |

**Critério:** 6/6. Dois alvos: o item 3, em que o `NULL` forma grupo (quem previu 3 transferiu a intuição do `WHERE`); e o item 4, em que o Rafael **some** — agrupar a tabela `pedidos` só enxerga quem tem pedido. Trazer os oito clientes exigiria `LEFT JOIN`, que é o 03.08.

## A2 — `WHERE` ou `HAVING`?

| # | Condição | Onde | Por quê |
|---|---|---|---|
| 1 | produtos ativos | **`WHERE`** | condição de linha, sem agregação |
| 2 | categorias com > 3 produtos | **`HAVING`** | `COUNT(*)` só existe depois de agrupar |
| 3 | pedidos de 2026 | **`WHERE`** | condição de linha |
| 4 | cidades com faturamento > R$ 1.000 | **`HAVING`** | usa `SUM` |
| 5 | clientes com e-mail | **`WHERE`** | condição de linha (`email IS NOT NULL`) |
| 6 | grupos com média > R$ 200 | **`HAVING`** | usa `AVG` |
| 7 | produtos acima de R$ 300 | **`WHERE`** | condição de linha |
| 8 | categorias com ao menos um inativo | **`HAVING`** | `MIN(ativo) = 0` ou `COUNT(*) FILTER` — depende de agregação |

**Critério:** 8/8. A regra mecânica resolve todos: **tem função de agregação → `HAVING`; não tem → `WHERE`**. O item 8 é o mais difícil porque a condição em português não parece agregada, e é: "ao menos um inativo no grupo" só se sabe depois de olhar o grupo inteiro.

## A3 — Regra de ouro

1. **OK** — `categoria` agrupa, `COUNT` agrega.
2. **VIOLA** — `nome` não agrupa nem é agregado. O SQLite devolve um nome arbitrário; o padrão recusa. Correção: `MIN(nome)`, ou agrupe também por `nome` (que muda a pergunta), ou use subconsulta se quiser o nome do produto mais caro (03.09).
3. **OK** — `MAX` agrega.
4. **OK** — as duas colunas do `SELECT` estão no `GROUP BY`. (Como `nome` é único, cada grupo tem uma linha — a consulta é válida e inútil.)
5. **VIOLA** — `data` não está no `GROUP BY` nem agregada. Correção: `MAX(data)` (a mais recente do grupo) ou agrupe por `status, data`.
6. **OK** — agregação sem `GROUP BY` condensa a tabela inteira em uma linha; não há coluna solta.

**Critério:** 6/6. O item 4 é o que separa: ele **não** viola a regra, embora "pareça" errado — e o comentário sobre a consulta ser inútil demonstra que você entendeu o efeito, não só a regra.

## A4 — Traduza a pergunta

```sql
-- 1 (4 linhas)
SELECT categoria, COUNT(*) AS produtos
FROM produtos GROUP BY categoria ORDER BY produtos DESC;

-- 2 (7 linhas — o Rafael não aparece)
SELECT cliente_id, COUNT(*) AS pedidos
FROM pedidos GROUP BY cliente_id ORDER BY pedidos DESC;

-- 3
SELECT categoria, COUNT(*) AS produtos
FROM produtos GROUP BY categoria HAVING COUNT(*) > 2;

-- 4
SELECT categoria, AVG(preco_centavos) / 100.0 AS preco_medio, COUNT(*) AS produtos
FROM produtos GROUP BY categoria ORDER BY preco_medio DESC;

-- 5 (20 linhas)
SELECT pedido_id, COUNT(*) AS itens
FROM itens_pedido GROUP BY pedido_id ORDER BY itens DESC, pedido_id;

-- 6 (2 linhas: Fernanda com 5, Ana com 4)
SELECT c.nome, COUNT(*) AS pedidos
FROM clientes c JOIN pedidos p ON p.cliente_id = c.id
GROUP BY c.id, c.nome
HAVING COUNT(*) > 3
ORDER BY pedidos DESC;
```

**Ponto de atenção no item 6:** o `GROUP BY c.id, c.nome` agrupa pelas **duas** colunas, e não só pelo nome. O motivo é a regra de ouro combinada com a boa prática: agrupar pelo `id` garante que dois clientes homônimos não sejam fundidos, e incluir `c.nome` no `GROUP BY` satisfaz o padrão SQL. Agrupar só por `nome` funcionaria hoje e fundiria dois "João Silva" amanhã.

**Critério:** 6/6, com o item 4 acompanhado do `COUNT` (média com tamanho de amostra, 03.05) e o item 6 agrupando por `id`.

## AP1 — O painel agrupado

**Resultados de referência:**

| # | Indicador | Resultado |
|---|---|---|
| 1 | clientes por cidade | campinas 3 · santos 2 · sorocaba 2 · `NULL` 1 |
| 2 | produtos e preço médio por categoria | video R$ 549,45 (2) · audio R$ 341,95 (4) · perifericos R$ 209,45 (2) · acessorios R$ 73,65 (4) |
| 3 | pedidos por status | concluido 17 · pendente 2 · cancelado 1 |
| 4 | top 5 pedidos com mais itens | todos com **2** itens — há empate geral |
| 5 | unidades por produto | Cabo HDMI 6 · Fone 5 · Mouse 5 · Caixa de Som 4 · ... |
| 6 | faturamento por categoria (concluídos) | audio R$ 3.975,20 · video R$ 2.197,80 · perifericos R$ 1.436,50 · acessorios R$ 708,90 |

**Ponto de atenção no item 4:** todos os pedidos com mais itens têm exatamente 2, e há empate entre vários. Sem critério de desempate no `ORDER BY`, o "top 5" é arbitrário — é o problema do 03.04 reaparecendo sobre um resultado agrupado. Acrescente `, pedido_id`.

**Critério:** os seis com apelidos e ordenação; o empate do item 4 percebido.

## AP2 — `WHERE` × `HAVING` lado a lado

```sql
-- (1) WHERE: produtos acima de R$ 200, contados por categoria
SELECT categoria, COUNT(*) AS qtd
FROM produtos WHERE preco_centavos > 20000 GROUP BY categoria ORDER BY categoria;
```

```text
categoria   | qtd
------------+----
audio       |   3
perifericos |   1
video       |   1
```

```sql
-- (2) HAVING: categorias cuja MÉDIA passa de R$ 200
SELECT categoria, COUNT(*) AS qtd, AVG(preco_centavos) / 100.0 AS media
FROM produtos GROUP BY categoria HAVING AVG(preco_centavos) > 20000 ORDER BY categoria;
```

```text
categoria   | qtd | media
------------+-----+-------
audio       |   4 | 341.95
perifericos |   2 | 209.45
video       |   2 | 549.45
```

**(3) Qual pergunta cada uma responde:** a primeira, *"quantos produtos caros cada categoria tem?"*; a segunda, *"quais categorias são caras em média?"*.

**(4) A categoria com números diferentes:** todas as três. `audio` aparece com **3** na primeira (só os caros) e **4** na segunda (o grupo inteiro passou no critério de média). `perifericos` com 1 e 2; `video` com 1 e 2. E o mais revelador: `acessorios` **não aparece em nenhuma das duas** — não tem produto acima de R$ 200 nem média acima disso.

**(5) As duas juntas:**

```sql
SELECT categoria, COUNT(*) AS qtd, AVG(preco_centavos) / 100.0 AS media
FROM produtos
WHERE ativo = 1
GROUP BY categoria
HAVING AVG(preco_centavos) > 20000;
```

**Critério:** os dois resultados registrados, a distinção das perguntas em (3), e pelo menos uma categoria com números divergentes explicada.

## AP3 — O grupo `NULL`

**Onde ele aparece hoje:** `GROUP BY cidade` em `clientes` (a Helena). Nas demais colunas do laboratório não há nulos — os outros dois casos exigem imaginar (ou provocar) o cenário.

**As três versões:**

```sql
-- (a) deixando aparecer
SELECT cidade, COUNT(*) AS clientes FROM clientes GROUP BY cidade;

-- (b) excluindo
SELECT cidade, COUNT(*) AS clientes FROM clientes
WHERE cidade IS NOT NULL GROUP BY cidade;

-- (c) rotulando
SELECT COALESCE(cidade, 'não informada') AS cidade, COUNT(*) AS clientes
FROM clientes GROUP BY COALESCE(cidade, 'não informada');
```

**Qual publicar — e o critério:** depende do que o número **serve para decidir**.

- Num relatório de **cobertura** ("onde temos clientes"), a versão **(c)** é a melhor: o dado faltante vira visível e alguém pode ir corrigi-lo. Esconder incompletude é a pior das três opções.
- Num relatório que soma **percentuais que precisam fechar 100%**, a **(c)** também — a **(b)** faria os percentuais somarem menos que o total sem explicação.
- A **(b)** só se justifica quando a pergunta é explicitamente sobre as cidades conhecidas, e o relatório **diz isso** ("entre os clientes com cidade informada").

**Critério:** as três versões executadas e a escolha justificada pelo **uso** do número, não por preferência.

## D1 — O painel de vendas

**(a) Faturamento por cidade** — *"quanto cada cidade faturou, e em quantos pedidos?"*

```text
cidade   | pedidos | faturamento_reais
---------+---------+------------------
sorocaba |       5 |            3267.1
campinas |       6 |            2711.2
santos   |       4 |            1357.5
NULL     |       2 |             982.6
```

Grupo `NULL`: presente (Helena). Decisão sugerida: rotular como "não informada" — R$ 982,60 sumindo do painel seria pior que uma linha estranha.

**(b) Faturamento por categoria** — *"quais categorias vendem mais?"*

```text
categoria   | faturamento
------------+------------
audio       |      3975.2
video       |      2197.8
perifericos |      1436.5
acessorios  |       708.9
```

Sem grupo `NULL` (toda categoria é `NOT NULL`).

**(c) Pedidos por status, com percentual:**

```sql
SELECT status,
       COUNT(*)                                                        AS qtd,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM pedidos), 1)     AS percentual
FROM pedidos GROUP BY status ORDER BY qtd DESC;
```

```text
status    | qtd | percentual
----------+-----+-----------
concluido |  17 |       85.0
pendente  |   2 |       10.0
cancelado |   1 |        5.0
```

A subconsulta escalar `(SELECT COUNT(*) FROM pedidos)` calcula o total **uma vez** e é usada em cada grupo — é a primeira aparição do assunto do 03.09.

**(d) Cidades com pelo menos 2 clientes:**

```sql
SELECT cidade, COUNT(*) AS clientes FROM clientes
GROUP BY cidade HAVING COUNT(*) >= 2 ORDER BY clientes DESC;
```

Três linhas: campinas 3, santos 2, sorocaba 2. O grupo `NULL` (1 cliente) foi eliminado **pelo `HAVING`**, não por decisão explícita — e vale notar isso: às vezes o filtro de grupo resolve o problema do nulo por acidente, o que é conveniente e não é uma decisão.

**(e) Ticket médio por cidade:**

```text
cidade   | pedidos | ticket_medio
---------+---------+-------------
sorocaba |       5 |       653.42
NULL     |       2 |        491.3
campinas |       6 |       451.87
santos   |       4 |       339.38
```

**Por que não é a média das médias:** o ticket médio de uma cidade é `faturamento da cidade ÷ pedidos da cidade`. Se você calculasse a média dos tickets de cada **pedido** e depois tirasse a média disso, cada pedido pesaria igual, independentemente do valor — e o resultado seria diferente. Média de médias só coincide com a média geral quando todos os grupos têm o mesmo tamanho, o que quase nunca acontece. É a mesma armadilha do 03.05, agora entre níveis de agregação.

E o achado de negócio: **Campinas tem mais pedidos (6) e fatura menos que Sorocaba (5)** — ticket médio de R$ 451,87 contra R$ 653,42. Nenhum dos relatórios anteriores tornava isso visível.

**Reflexão esperada:** o SQL ganha em quase tudo. Onde o `relatorio_aurora.py` tinha sessenta linhas com laço, acumulador e formatação, há oito linhas declarativas; a legibilidade é maior porque a consulta descreve **a pergunta**, não o procedimento; e o desempenho com dez milhões de linhas não tem comparação, porque o banco agrega onde os dados estão, com índices, em vez de trazer tudo para a memória do programa. O que o Python continua fazendo e o SQL não faz é a **fronteira suja**: ler um arquivo externo, validar cada linha, rejeitar as defeituosas com motivo registrado e mandar para quarentena. Agregação é trabalho do banco; **entrada de dados não confiáveis é trabalho da aplicação** — e essa divisão vai se repetir em todos os módulos seguintes.

**Critério de "está bom":** os cinco itens com a pergunta em português antes do SQL; a decisão sobre o grupo `NULL` explicitada em cada um; o item (e) explicando a média de médias; e a reflexão identificando a validação de entrada como o que o SQL **não** substitui.
