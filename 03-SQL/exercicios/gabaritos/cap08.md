# Gabaritos — Capítulo 03.08

Abra somente após tentativa honesta.

## A1 — Quantas linhas?

| # | Junção | Linhas | Por quê |
|---|---|---|---|
| 1 | `clientes JOIN pedidos` | **20** | uma por pedido; o Rafael some |
| 2 | `clientes LEFT JOIN pedidos` | **21** | os 20 + **uma** linha do Rafael com nulos |
| 3 | `produtos JOIN itens` | **31** | uma por item; o Mousepad some |
| 4 | `produtos LEFT JOIN itens` | **32** | os 31 + **uma** do Mousepad |
| 5 | `LEFT ... WHERE p.id IS NULL` | **1** | o anti-join: só o Rafael |
| 6 | `LEFT ... WHERE p.status = 'cancelado'` | **1** | o `WHERE` matou o `LEFT`; sobra só o pedido cancelado |

**Critério:** 6/6. A regra dos itens 2 e 4: o `LEFT JOIN` acrescenta **exatamente uma** linha por registro sem par. E o item 6 é o alvo — quem previu 2 (esperando o Rafael preservado) encontrou a armadilha.

## A2 — Qual junção?

| # | Pergunta | Junção |
|---|---|---|
| 1 | pedidos com nome do cliente | **`INNER`** — todo pedido tem cliente |
| 2 | todos os clientes e quantos pedidos | **`LEFT`** |
| 3 | produtos nunca vendidos | **anti-join** |
| 4 | itens com nome do produto | **`INNER`** — todo item tem produto |
| 5 | todas as categorias e faturamento | **`LEFT`** (partindo de produtos) |
| 6 | clientes sem e-mail | **nenhuma** — é `WHERE email IS NULL` numa tabela só |
| 7 | todos os produtos com unidades vendidas | **`LEFT`** |
| 8 | pedidos sem nenhum item | **anti-join** |

**Critério:** 8/8. O item 6 é a pegadinha: "sem e-mail" parece anti-join pela redação, e é apenas um filtro — o `NULL` já está nos dados, não precisa ser fabricado por junção. Distinguir os dois casos é o que o exercício treina.

## A3 — `ON` ou `WHERE`?

| # | Condição | Onde | Por quê |
|---|---|---|---|
| 1 | `c.cidade = 'campinas'` | **`WHERE`** | é sobre a **esquerda**; filtrar a esquerda é legítimo e não afeta a preservação |
| 2 | `p.status = 'concluido'` | **`ON`** | sobre a direita — no `WHERE` mataria o `LEFT` |
| 3 | `p.id IS NULL` | **`WHERE`** | é o **anti-join**; precisa agir depois da montagem |
| 4 | `p.data >= '2026-01-01'` | **`ON`** | sobre a direita |
| 5 | `c.email IS NOT NULL` | **`WHERE`** | sobre a esquerda |
| 6 | `p.status <> 'cancelado'` | **`ON`** | sobre a direita — e note que a negação também descartaria os nulos (03.03) |

**A regra completa:** condição sobre a **esquerda** → `WHERE` (você quer mesmo filtrar aqueles clientes). Condição sobre a **direita** → `ON`. Exceção única: o `IS NULL` do anti-join → `WHERE`.

**Critério:** 6/6 com a distinção esquerda/direita explicitada. Muita gente decora "condição vai no `ON`" e passa a pôr o filtro de cidade ali também — o que funciona, mas comunica a intenção errada.

## A4 — Ache o bug

1. `COUNT(*)` conta a linha fabricada → o Rafael apareceria com **1**. Correção: **`COUNT(p.id)`**.
2. `p.status` **aceita nulos** na tabela original; se houvesse um pedido com status nulo, ele entraria como se fosse ausência. Correção: **`WHERE p.id IS NULL`** (chave primária).
3. `SUM` de conjunto vazio devolve `NULL` (03.05) → células vazias. Correção: **`COALESCE(SUM(i.quantidade), 0)`**.
4. Filtro sobre a direita no `WHERE` → matou o `LEFT`. Correção: mover para o `ON` com `AND`.
5. As tabelas estão **invertidas**: partindo de `itens_pedido`, o `LEFT` preserva itens, não produtos — e `i.id` nunca é nulo ali. Correção: **`FROM produtos pr LEFT JOIN itens_pedido i ... WHERE i.id IS NULL`**.
6. O `JOIN` (inner) depois do `LEFT` **descarta** as linhas preservadas: o Rafael tem `p.id` nulo, e nenhum item casa com nulo. Correção: **`LEFT JOIN itens_pedido`** também.

**Critério:** 6/6. Os itens 5 e 6 são os mais difíceis: o 5 exige perceber que o lado preservado é o **esquerdo**, e o 6 mostra que um `INNER` depois de um `LEFT` anula o efeito da preservação.

## AP1 — O painel completo

| Relatório | `INNER` | `LEFT` | Quem aparece só no `LEFT` |
|---|---|---|---|
| 1. clientes e pedidos | 7 linhas | **8** | Rafael Torres (0) |
| 2. produtos e unidades | 11 linhas | **12** | Mousepad Grande (0) |
| 3. categorias e faturamento | 4 linhas | **4** | ninguém — toda categoria tem venda |

**Qual publicar:** o `LEFT`, nos casos 1 e 2. O motivo não é completude por completude — é que **a linha com zero é frequentemente a mais acionável do relatório**. Um cliente cadastrado que nunca comprou é alguém para a equipe de vendas procurar; um produto encalhado é decisão de estoque. O `INNER` esconde exatamente as informações que exigem ação.

**Observação sobre o item 3:** as duas versões coincidem, e isso **não** significa que o `LEFT` era desnecessário — significa que hoje não há categoria sem venda. No dia em que houver, a versão `INNER` a esconderá em silêncio.

**Critério:** as três comparações com contagens, e a justificativa da escolha pela **acionabilidade** da linha zero.

## AP2 — A família de anti-joins

```sql
-- 1. clientes sem pedidos -> 1 (Rafael)
SELECT c.nome FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id WHERE p.id IS NULL;

-- 2. produtos sem vendas -> 1 (Mousepad)
SELECT pr.nome FROM produtos pr
LEFT JOIN itens_pedido i ON i.produto_id = pr.id WHERE i.id IS NULL;

-- 3. pedidos sem itens -> 0
SELECT p.id FROM pedidos p
LEFT JOIN itens_pedido i ON i.pedido_id = p.id WHERE i.id IS NULL;

-- 4. categorias sem produtos ativos -> 0
SELECT DISTINCT pr.categoria FROM produtos pr
WHERE pr.categoria NOT IN (SELECT categoria FROM produtos WHERE ativo = 1);
```

**A prova de completude:**

| # | Anti-join | Positiva | Soma | Total |
|---|---|---|---|---|
| 1 | 1 | 7 | **8** | 8 clientes ✓ |
| 2 | 1 | 11 | **12** | 12 produtos ✓ |
| 3 | 0 | 20 | **20** | 20 pedidos ✓ |
| 4 | 0 | 4 | **4** | 4 categorias ✓ |

**Ponto de atenção nos itens 3 e 4:** o anti-join devolveu **zero linhas**, e isso é uma **resposta**, não uma falha. "Nenhum pedido está sem itens" é informação de qualidade de dados — e é justamente o tipo de verificação que se roda periodicamente para detectar corrupção. Um anti-join que **passa a devolver linhas** é um alerta.

**Critério:** os quatro escritos, a chave primária identificada em cada, e a tabela de completude fechando nos quatro casos.

## AP3 — `ON` × `WHERE` medido

| Condição | No `ON` | No `WHERE` | Quem some |
|---|---|---|---|
| `p.status = 'concluido'` | 8 clientes | **7** | Rafael |
| `p.data >= '2026-01-01'` | 8 clientes | **7** | Rafael (e quem não comprou em 2026) |
| `p.status = 'cancelado'` | 8 clientes | **1** | todos, menos a Ana |

**Item 3 — qual responde "todos os clientes, com seus pedidos de 2026":** a versão com a condição no **`ON`**. A versão `WHERE` responde outra pergunta: "os clientes que fizeram pedidos em 2026, com esses pedidos" — o que exclui quem não comprou no período, e a exclusão é silenciosa.

**A regra, enunciada:** num `LEFT JOIN`, o `ON` decide **quais pares se formam** e a preservação acontece depois dele; o `WHERE` age sobre o resultado montado, e qualquer condição que a linha preservada não satisfaça (o que inclui **toda** comparação com o `NULL` fabricado) a elimina. Por isso condição sobre a direita pertence ao `ON`.

**Critério:** os três pares medidos, e a regra enunciada em termos de **quando** cada cláusula age.

## D1 — O relatório que não perde ninguém

**(a) O painel — e um bug escondido no caminho.**

A tentação é escrever assim:

```sql
SELECT c.nome,
       COUNT(p.id)                                              AS pedidos,
       COALESCE(SUM(i.quantidade * i.preco_unitario_centavos), 0) / 100.0 AS total_gasto,
       COALESCE(MAX(p.data), 'nunca')                           AS ultima_compra
FROM clientes c
LEFT JOIN pedidos p      ON p.cliente_id = c.id
LEFT JOIN itens_pedido i ON i.pedido_id  = p.id
GROUP BY c.id, c.nome;
```

E o resultado sai **errado na coluna de pedidos**:

```text
nome             | errado | certo
-----------------+--------+------
Carlos Menezes   |      6 |     3
Fernanda Lima    |      8 |     5
Ana Souza        |      5 |     4
Rafael Torres    |      0 |     0
```

**Por quê:** o segundo `LEFT JOIN` (itens) multiplicou as linhas — cada pedido aparece uma vez por item, exatamente como no 03.07. O `COUNT(p.id)` do capítulo resolve o problema do `LEFT JOIN` (não contar a linha fabricada) e **não** resolve o da multiplicação. É preciso o `COUNT(DISTINCT p.id)`, que junta as duas lições.

**A versão correta:**

```sql
SELECT c.nome,
       COUNT(DISTINCT p.id)                                     AS pedidos,
       COALESCE(SUM(i.quantidade * i.preco_unitario_centavos), 0) / 100.0 AS total_gasto,
       COALESCE(MAX(p.data), 'nunca')                           AS ultima_compra
FROM clientes c
LEFT JOIN pedidos p      ON p.cliente_id = c.id
LEFT JOIN itens_pedido i ON i.pedido_id  = p.id
GROUP BY c.id, c.nome
ORDER BY total_gasto DESC;
```

```text
nome             | pedidos | total_gasto | ultima_compra
-----------------+---------+-------------+--------------
Carlos Menezes   |       3 |      2528.4 | 2026-07-20
Fernanda Lima    |       5 |      1812.2 | 2026-05-19
Beatriz Nogueira |       2 |      1798.0 | 2026-07-12
Ana Souza        |       4 |      1188.5 | 2026-07-25
Helena Prado     |       2 |       982.6 | 2026-06-21
Diego Alves      |       2 |       838.8 | 2026-06-15
Juliana Castro   |       2 |       738.7 | 2026-07-04
Rafael Torres    |       0 |         0.0 | nunca
```

Repare no Rafael: **0 pedidos, R$ 0,00 e "nunca"** — as três agregações tratadas corretamente, cada uma com uma técnica diferente.

**(b) A versão errada:** acrescentando `WHERE p.status = 'concluido'`, o resultado cai de 8 para **7 linhas** — o Rafael some. Uma palavra, um cliente inteiro fora do relatório.

**(c) Os três anti-joins:** ver AP2 — 1 cliente, 1 produto, 0 categorias.

**(d) A conciliação por status:**

```sql
SELECT c.nome,
       COUNT(CASE WHEN p.status = 'concluido' THEN 1 END) AS concluidos,
       COUNT(CASE WHEN p.status = 'pendente'  THEN 1 END) AS pendentes,
       COUNT(CASE WHEN p.status = 'cancelado' THEN 1 END) AS cancelados
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
GROUP BY c.id, c.nome
ORDER BY c.nome;
```

O `CASE` sem `ELSE` devolve `NULL` quando a condição falha, e o `COUNT` ignora nulos (03.05) — é o idioma padrão para contagens condicionais.

**(e) Por que cada função precisa de tratamento diferente:**

| Função | Problema na linha preservada | Solução |
|---|---|---|
| `COUNT(*)` | conta a linha fabricada → daria 1 | `COUNT(coluna_da_direita)` |
| `COUNT(coluna)` | correto para o `LEFT`, **inflado** se houver segundo `JOIN` | `COUNT(DISTINCT chave)` |
| `SUM` / `AVG` | ignoram nulos → devolvem `NULL`, não 0 | `COALESCE(SUM(...), 0)` |
| `MAX` / `MIN` | idem → `NULL` | `COALESCE(MAX(...), 'nunca')` — e note que aqui o `NULL` **não** vira zero, vira um rótulo |

A raiz é única: as três lições do módulo se encontram nesta consulta — o `NULL` fabricado pelo `LEFT JOIN` (03.08), o comportamento das agregações diante do `NULL` (03.05), e a multiplicação de linhas pela junção (03.07).

**Reflexão esperada:** um relatório que **dá erro** é um relatório que ninguém usa — o problema é visível, alguém investiga, e o dano é o tempo perdido. Um relatório que **perde linhas** é usado normalmente: os números parecem plausíveis, ninguém desconfia, e as decisões são tomadas sobre uma base incompleta. A diferença de gravidade está em quem detecta: no primeiro caso, o sistema; no segundo, apenas alguém que conheça o número esperado — e essa pessoa frequentemente não existe. Some-se que a ausência é silenciosa por natureza: o Rafael não aparece no relatório e **também não aparece em lugar nenhum dizendo que não apareceu**. É por isso que a auditoria de completude (a soma anti-join + positiva = total) não é preciosismo: ela é o único mecanismo que transforma uma ausência invisível num número conferível.

**Critério de "está bom":** o painel com as três agregações corretas (incluindo o `COUNT(DISTINCT)` — quem usou `COUNT(p.id)` e não conferiu contra o número real de pedidos entregou um relatório errado); a versão (b) com a perda medida; os três anti-joins; a conciliação com `CASE`; e a tabela do item (e) identificando que a causa é a mesma nos quatro casos.
