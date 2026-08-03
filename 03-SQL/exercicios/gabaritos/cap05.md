# Gabaritos — Capítulo 03.05

Abra somente após tentativa honesta.

## A1 — Preveja o número

| # | Consulta | Resultado | Observação |
|---|---|---|---|
| 1 | `COUNT(*) FROM produtos` | **12** | |
| 2 | `COUNT(*) FROM clientes` | **8** | |
| 3 | `COUNT(email) FROM clientes` | **7** | a Beatriz não tem e-mail |
| 4 | `COUNT(DISTINCT categoria)` | **4** | audio, video, perifericos, acessorios |
| 5 | `MIN(preco_centavos)` | **3490** | Cabo HDMI 2m |
| 6 | `SUM(quantidade)` | **38** | unidades, não itens (são 31 linhas) |
| 7 | `COUNT(*) ... status = 'devolvido'` | **0** | conjunto vazio → `COUNT` devolve zero |
| 8 | `SUM(...) ... categoria = 'moveis'` | **`NULL`** | conjunto vazio → `SUM` devolve nulo |

**Critério:** 8/8. O par 7/8 é o alvo: mesmo conjunto vazio, resultados de naturezas diferentes. O item 6 pega quem confundiu "quantas linhas de item" (31) com "quantas unidades" (38).

## A2 — Qual função?

```sql
-- 1
SELECT COUNT(*) AS produtos FROM produtos;

-- 2
SELECT COUNT(cidade) AS clientes_com_cidade FROM clientes;

-- 3
SELECT AVG(preco_centavos) / 100.0 AS preco_medio_reais,
       COUNT(*)                    AS produtos_considerados
FROM produtos WHERE ativo = 1;

-- 4
SELECT MAX(preco_centavos) / 100.0 AS maior_preco_reais FROM produtos;

-- 5
SELECT SUM(quantidade) AS unidades_vendidas FROM itens_pedido;

-- 6
SELECT MIN(data) AS primeiro_pedido, MAX(data) AS ultimo_pedido FROM pedidos;

-- 7
SELECT COUNT(DISTINCT categoria) AS categorias FROM produtos;

-- 8
SELECT SUM(quantidade * preco_unitario_centavos) / 100.0 AS faturamento_reais
FROM itens_pedido;
```

**Ponto de atenção no item 3:** o `COUNT(*)` ao lado da média não foi pedido no enunciado, e deveria ter sido — média sem tamanho de amostra é a prática que a seção 12 do capítulo desaconselha. Quem acrescentou por conta própria acertou mais que o enunciado.

**Critério:** 8/8, com o item 4 pedindo o **valor** (`MAX`), não o nome do produto — para o nome, seria `ORDER BY ... LIMIT 1` (03.04) ou uma subconsulta (03.09).

## A3 — `NULL` na agregação

1. **Falsa** — `COUNT(*)` conta **linhas**, independentemente do conteúdo. Uma linha toda nula continua sendo uma linha.
2. **Verdadeira**.
3. **Falsa** — divide por **5** (os não nulos), não por 8.
4. **Verdadeira** — se **todos** os valores da coluna forem nulos, `MIN` devolve `NULL`.
5. **Verdadeira** — nenhum valor não nulo para contar.
6. **Falsa** — devolve **`NULL`**. Só `COUNT` devolve zero em conjunto vazio.

**Critério:** 6/6 com as falsas corrigidas. Os itens 1 e 6 são os mais errados, e ambos derivam da mesma regra única do capítulo.

## A4 — Ache o erro

1. O apelido diz "total de clientes" mas conta **cidades preenchidas** → `COUNT(*) AS total_clientes`, ou renomeie para `clientes_com_cidade`. O erro está na **discordância entre o nome e o cálculo** — e é assim que números errados viajam.
2. Se não houver produtos de "livros", devolve `NULL` e o relatório mostra vazio → `COALESCE(SUM(preco_centavos), 0)`.
3. Média sem tamanho de amostra → acrescente `COUNT(*)` na mesma consulta.
4. Divide **antes** de somar, espalhando erro de ponto flutuante por parcela → `SUM(preco_centavos) / 100.0`.
5. A junção multiplica linhas: conta **itens**, não pedidos → `COUNT(DISTINCT p.id)`.
6. `nome` fora de agregação sem `GROUP BY` — o SQLite aceita e devolve um nome arbitrário; o padrão recusa → `SELECT COUNT(*) AS produtos FROM produtos`.

**Critério:** 6/6. O item 6 antecipa a regra de ouro do 03.06, e o item 1 é o mais importante na prática: a consulta está sintaticamente perfeita e semanticamente mentirosa.

## AP1 — O painel de números

| # | Indicador | Resultado |
|---|---|---|
| 1 | total de clientes | **8** |
| 2 | clientes com e-mail | **7** |
| 3 | produtos ativos | **11** |
| 4 | preço médio dos ativos | **R$ 284,57** |
| 5 | mais caro / mais barato | **89900** / **3490** centavos |
| 6 | unidades vendidas | **38** |
| 7 | faturamento total | **R$ 9.887,20** |
| 8 | período | **2025-04-02** a **2026-07-25** |

**Observação sobre o item 7:** esse é o faturamento de **todos** os itens, incluindo pedidos cancelados e pendentes. O faturamento de pedidos concluídos é **R$ 8.318,40** — a diferença de R$ 1.568,80 é a razão pela qual todo indicador financeiro precisa dizer **qual conjunto** ele mede.

**Critério:** os 8 com apelido legível e o item 7 acompanhado da definição do conjunto.

## AP2 — A média honesta

| # | Consulta | Resultado | Pergunta que responde |
|---|---|---|---|
| 1 | `AVG(LENGTH(cidade))` | **7,43** | "em média, quão longo é o nome das cidades **informadas**?" |
| 2 | `SUM(LENGTH(cidade)) * 1.0 / COUNT(*)` | **6,50** | "se cada cliente sem cidade contasse como zero, qual a média?" |
| 3 | `AVG(LENGTH(COALESCE(cidade, '')))` | **6,50** | idem ao 2, escrito de forma mais explícita |

**Qual publicar:** a **(1)**, na maioria dos casos — porque "não informado" não é "cidade de tamanho zero", e tratar ausência como zero distorce a medida. Mas a resposta completa é que **nenhuma delas deve ser publicada sozinha**: o número precisa vir acompanhado de "sobre 7 dos 8 clientes". A escolha do denominador é uma decisão de negócio; omitir que a decisão foi tomada é o erro.

**Critério:** os três valores e a justificativa da escolha ancorada no **significado** da ausência, não na conveniência.

## AP3 — Conjunto vazio

```sql
SELECT SUM(preco_centavos) FROM produtos WHERE categoria = 'moveis';   -- NULL
SELECT AVG(preco_centavos) FROM produtos WHERE categoria = 'moveis';   -- NULL
SELECT MAX(preco_centavos) FROM produtos WHERE categoria = 'moveis';   -- NULL
```

**Quando corrigir com `COALESCE(..., 0)`:**

- **`SUM` — sim.** "Vendemos R$ 0,00 em móveis" é uma afirmação verdadeira e útil.
- **`AVG` — não.** "O preço médio dos móveis é R$ 0,00" é **falso**; não há móveis. O correto é preservar o `NULL` e apresentar como "sem dados".
- **`MAX` — não.** "O produto mais caro custa R$ 0,00" também é falso, pela mesma razão.

**A regra que sai daí:** substituir `NULL` por zero só é correto quando **zero é a resposta certa para "nenhum"**. Em soma, é; em média, mínimo e máximo, não é. Esse discernimento é o que separa quem aplica `COALESCE` mecanicamente de quem entende o que está publicando.

**Critério:** os três provocados, e a distinção entre os casos em que corrigir é certo e errado.

## D1 — O fechamento do mês

**(a) Julho de 2026, pedidos concluídos:**

```sql
SELECT COUNT(DISTINCT p.id)                                  AS pedidos,
       SUM(i.quantidade * i.preco_unitario_centavos)/100.0   AS faturamento_reais,
       SUM(i.quantidade * i.preco_unitario_centavos)/100.0
           / COUNT(DISTINCT p.id)                            AS ticket_medio_reais
FROM pedidos p
JOIN itens_pedido i ON i.pedido_id = p.id
WHERE p.status = 'concluido'
  AND p.data >= '2026-07-01' AND p.data < '2026-08-01';
```

```text
pedidos | faturamento | ticket_medio
--------+-------------+-------------
      2 |      1518.6 |        759.3
```

**(b) Categoria sem vendas:** acrescentando `AND pr.categoria = 'moveis'` (com junção a `produtos`), o `SUM` devolve `NULL` e o `COUNT` devolve 0. A correção: `COALESCE(SUM(...), 0)` para o faturamento. **Atenção ao ticket médio:** ele viraria uma divisão por zero — no SQLite o resultado é `NULL`, e essa é a resposta honesta ("não há pedidos para calcular média"). Forçar `0,00` ali seria mentir.

**(c) Clientes distintos × total:**

```text
compraram | total
----------+------
        7 |     8
```

**Por que os dois importam juntos:** 7 sozinho não diz nada — pode ser ótimo (de 8 clientes) ou péssimo (de 8.000). O par revela a **taxa de conversão**: 87,5% da base já comprou. Um indicador de volume sem o universo correspondente é um número sem escala, e é exatamente o mesmo princípio da média sem tamanho de amostra.

**(d) A prova dos nove:**

```text
status    | total
----------+-------
cancelado |  199.9
concluido | 8318.4
pendente  | 1368.9
```

`199,90 + 8.318,40 + 1.368,90 = 9.887,20` — bate com o total sem filtro do AP1. A prova fechou, e o que ela garante é que **nenhum status foi esquecido** no relatório. Se houvesse um quarto status que você não previu, a soma denunciaria.

**Um detalhe que vale ouro se você somou no próprio banco:**

```sql
SELECT 199.9 + 8318.4 + 1368.9;      -- 9887.199999999999
```

O ponto flutuante do 01.04, vivo e presente. A prova dos nove feita sobre valores **já divididos por 100** pode não fechar exatamente, e a conclusão errada seria "falta um centavo em algum lugar". A forma correta é provar **em centavos inteiros**, dividindo só na apresentação:

```sql
SELECT SUM(i.quantidade * i.preco_unitario_centavos) AS total_centavos
FROM pedidos p JOIN itens_pedido i ON i.pedido_id = p.id;   -- 988720, exato
```

Se a sua prova não fechou por alguns centésimos, o defeito não estava nos dados — estava na unidade em que você provou.

**(e) `COUNT(*)` × `COUNT(DISTINCT p.id)`:** o número de **pedidos**. Com `COUNT(*)`, a consulta contaria as linhas da junção — 28 para o total de concluídos, em vez de 17. O faturamento, por sua vez, **não** mudaria: cada item precisa ser somado uma vez, e a multiplicação de linhas é justamente o que a soma quer.

**Reflexão esperada:** uma média é uma **compressão com perda**: ela substitui muitos números por um, e o que se perde é justamente a informação sobre confiabilidade. "Ticket médio de R$ 759,30" sobre 2 pedidos e sobre 2.000 pedidos são afirmações radicalmente diferentes, e a primeira não deveria orientar decisão nenhuma — mas ambas aparecem idênticas no relatório. Publicar o tamanho da amostra não é rigor acadêmico: é o mínimo para que quem lê possa julgar se o número merece confiança. E há um efeito secundário prático: a amostra torna visíveis os filtros que você aplicou. Se o painel diz "média sobre 2 pedidos" quando o mês teve 20, alguém vai perguntar o que aconteceu com os outros 18 — e essa pergunta é o que encontra o filtro errado antes de a decisão ser tomada.

**Critério de "está bom":** os cinco itens com números reais; o item (b) reconhecendo que o ticket médio **não** deve virar zero; o item (c) explicando o par pela noção de escala; a prova do item (d) fechando; e a reflexão tratando a média como compressão com perda.
