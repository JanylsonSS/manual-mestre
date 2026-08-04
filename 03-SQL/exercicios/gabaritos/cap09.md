# Gabaritos — Capítulo 03.09

Abra somente após tentativa honesta.

## A1 — Onde vai a subconsulta?

| # | Pergunta | Posição | Forma |
|---|---|---|---|
| 1 | acima do preço médio | **`WHERE`** | escalar |
| 2 | ticket médio | **`FROM`** | tabela derivada (agrega o agregado) |
| 3 | cliente com nº de pedidos | **`SELECT`** (ou `LEFT JOIN` + `GROUP BY`) | escalar correlacionada |
| 4 | clientes com pedido cancelado | **`WHERE`** | `IN` ou `EXISTS` |
| 5 | categoria de maior faturamento | **`FROM`** + `ORDER BY ... LIMIT 1` | derivada |
| 6 | produto com unidades vendidas | **`SELECT`** (ou `LEFT JOIN` + `GROUP BY`) | escalar correlacionada |

**Critério:** 6/6. Os itens 2 e 5 são os que exigem `FROM`: sempre que a pergunta pede **agregar um resultado já agregado**, é tabela derivada. Os itens 3 e 6 aceitam as duas formas — e reconhecer isso vale mais que escolher uma.

## A2 — Correlacionada?

| # | Correlacionada? | Execuções |
|---|---|---|
| 1 | **Não** | 1 |
| 2 | **Sim** (`pr.categoria`) | até 12 |
| 3 | **Não** | 1 |
| 4 | **Sim** (`c.id`) | até 8 |
| 5 | **Sim** (`c.id`) | até 8 |
| 6 | **Não** | 1 |

**Critério:** 6/6. O teste é mecânico: **a subconsulta menciona um apelido da consulta externa?** Se sim, correlacionada. E a ressalva honesta que vale acrescentar: "até 8 execuções" é a leitura ingênua — o otimizador frequentemente reescreve `EXISTS` correlacionado como semi-junção, e o custo real fica próximo ao de um `JOIN`.

## A3 — `IN`, `EXISTS` ou escalar?

1. **Escalar** — `> (SELECT AVG(...))`; a comparação é com um número.
2. **`EXISTS`** — a pergunta é sim/não; não precisa dos dados do pedido.
3. **`IN`** — comparação com uma lista de valores.
4. **`NOT EXISTS`** — negação de existência; imune a nulos.
5. **Escalar correlacionada** — `= (SELECT MAX(...) WHERE categoria = pr.categoria)`.
6. **`NOT EXISTS`** — justamente porque a lista pode ter nulos; `NOT IN` zeraria o resultado.

**Critério:** 6/6, com os itens 4 e 6 escolhendo `NOT EXISTS` pelo motivo certo (imunidade a `NULL`), não por preferência.

## A4 — Ache o bug

1. **`NOT IN` com subconsulta filtrada** — o filtro `quantidade > 1` não introduz nulos aqui, mas a construção é frágil e a semântica está errada: ela devolve produtos que nunca foram vendidos **em quantidade maior que 1**, o que não é "nunca vendidos". Correção: `NOT EXISTS` com a condição correta.
2. **Escalar com várias linhas** — `= (SELECT cliente_id FROM pedidos)` devolve 20 linhas. Correção: **`IN`**.
3. **Compara a coluna consigo mesma** sem agregação — a subconsulta devolve 12 linhas. Correção: `> (SELECT AVG(preco_centavos) FROM produtos)`.
4. **Tabela derivada sem apelido** — PostgreSQL e MySQL exigem. Correção: `) AS totais`.
5. **`EXISTS` sem correlação** — `SELECT 1 FROM pedidos p` é verdadeiro se **existir qualquer pedido**, então traz **todos** os clientes. Falta `WHERE p.cliente_id = c.id`.
6. **Viola a regra de ouro e a subconsulta devolve várias linhas** — `SELECT nome FROM produtos WHERE categoria = pr.categoria` traz vários nomes. Correção: `MIN(nome)` ou a subconsulta correlacionada com `MAX(preco)` do item [9] do capítulo.

**Critério:** 6/6. O item 5 é o mais instrutivo: um `EXISTS` **sem correlação** é quase sempre um bug, porque ele responde uma pergunta global ("existe algum pedido?") quando a intenção era por linha.

## AP1 — As três posições

```sql
-- (1) Subquery no SELECT — correlacionada; PRESERVA clientes sem pedidos
SELECT c.nome,
       (SELECT COUNT(*) FROM pedidos p WHERE p.cliente_id = c.id) AS pedidos
FROM clientes c ORDER BY pedidos DESC;

-- (2) JOIN + GROUP BY — com LEFT preserva; com INNER perde o Rafael
SELECT c.nome, COUNT(p.id) AS pedidos
FROM clientes c LEFT JOIN pedidos p ON p.cliente_id = c.id
GROUP BY c.id, c.nome ORDER BY pedidos DESC;

-- (3) Tabela derivada + JOIN — não correlacionada; agrega UMA vez
SELECT c.nome, COALESCE(t.pedidos, 0) AS pedidos
FROM clientes c
LEFT JOIN (SELECT cliente_id, COUNT(*) AS pedidos FROM pedidos GROUP BY cliente_id) AS t
       ON t.cliente_id = c.id
ORDER BY pedidos DESC;
```

**As três devolvem 8 linhas**, com o Rafael em 0 — desde que a (2) use `LEFT`.

**Qual publicar:** a **(3)** quando o volume for grande, porque a agregação acontece **uma vez** para todos os clientes, em vez de uma vez por cliente. A **(1)** é a mais legível quando há **duas ou mais** métricas de tabelas filhas diferentes, porque cada subconsulta é independente e não se multiplicam (03.07). A **(2)** é a mais idiomática para uma métrica só. Não há vencedora absoluta — e reconhecer isso é a resposta.

**Critério:** as três executadas, a preservação verificada em cada, e a escolha justificada por **contexto**, não por preferência.

## AP2 — `NOT IN` × `NOT EXISTS`

| Versão | Sem `NULL` na lista | Com `NULL` na lista |
|---|---|---|
| `NOT IN` | **1** (Mousepad) | **0** ← quebrou |
| `NOT EXISTS` | **1** | **1** ← imune |
| `LEFT JOIN ... IS NULL` | **1** | **1** ← imune |

**Item 4 — o mecanismo:** `id NOT IN (1, 2, ..., NULL)` expande para `id <> 1 AND id <> 2 AND ... AND id <> NULL`. A última comparação é **desconhecida** (03.03), e uma conjunção que contém desconhecido nunca é verdadeira — no máximo desconhecida. Como o `WHERE` só deixa passar o verdadeiro, **nenhuma** linha sobrevive.

**Item 5 — as três formas:**

```sql
-- NOT IN: frágil
SELECT nome FROM produtos WHERE id NOT IN (SELECT produto_id FROM itens_pedido);

-- NOT EXISTS: seguro e expressivo
SELECT nome FROM produtos pr
WHERE NOT EXISTS (SELECT 1 FROM itens_pedido i WHERE i.produto_id = pr.id);

-- Anti-join: seguro, mas exige escolher a coluna certa para o IS NULL
SELECT pr.nome FROM produtos pr
LEFT JOIN itens_pedido i ON i.produto_id = pr.id WHERE i.id IS NULL;
```

**Comparação:** `NOT EXISTS` é a mais segura **e** a mais legível — ela diz literalmente "não existe". O anti-join é igualmente correto e depende de o autor lembrar de testar a chave primária. O `NOT IN` só é seguro quando a coluna é comprovadamente `NOT NULL`, e essa garantia pode desaparecer numa migração futura.

**Critério:** a tabela com os seis valores, e o mecanismo explicado com "desconhecido", não com "vazio".

## AP3 — Subquery × `JOIN`

| # | Pergunta | Subconsulta | `JOIN` | Qual publicar |
|---|---|---|---|---|
| 1 | compraram áudio | `EXISTS` → 6 | `JOIN` + `DISTINCT` → 6 | **`EXISTS`** — não multiplica, dispensa `DISTINCT` |
| 2 | nunca vendidos | `NOT EXISTS` → 1 | anti-join → 1 | **`NOT EXISTS`** — expressa a intenção |
| 3 | total gasto por cliente | subquery no `SELECT` → 8 | `LEFT JOIN` + `GROUP BY` → 8 | **`JOIN`** — uma agregação só |
| 4 | pedidos acima do ticket médio | escalar + derivada | **não existe** versão só com `JOIN` | subconsulta |
| 5 | clientes com > 3 pedidos | `WHERE (SELECT COUNT...) > 3` → 2 | `GROUP BY` + `HAVING` → 2 | **`JOIN`** — `HAVING` é o idioma |

**Os casos em que uma forma não funciona:** o item 4. Comparar cada pedido com uma **média calculada sobre agregações** exige uma tabela derivada — não há junção que produza esse número sem subconsulta.

**Critério:** os cinco pares executados, e o item 4 identificado como exclusivo de subconsulta.

## D1 — O painel de destaques

**(a) Acima da média da própria categoria** — correlacionada, **até 12 execuções**:

```sql
SELECT pr.categoria, pr.nome, pr.preco_centavos / 100.0 AS preco
FROM produtos pr
WHERE pr.preco_centavos > (
    SELECT AVG(preco_centavos) FROM produtos WHERE categoria = pr.categoria
)
ORDER BY pr.categoria;
```

```text
categoria   | nome                  | preco
------------+-----------------------+------
acessorios  | Hub USB-C 6 portas    | 129.9
acessorios  | Suporte para Notebook |  79.9
audio       | Fone Bluetooth XZ-9   | 469.9
audio       | Microfone Condensador | 459.0
perifericos | Teclado Mecanico K2   | 329.0
video       | Monitor 24 polegadas  | 899.0
```

Seis produtos. Compare com a média **geral** (5 produtos, item [1] do capítulo): são conjuntos diferentes, e o "Suporte para Notebook" (R$ 79,90) só aparece aqui — barato no catálogo, caro entre os acessórios.

**(b) O mais caro de cada categoria** — ver o comando [9] do capítulo. Correlacionada, até 12 execuções. Versão com `JOIN`: existe, via tabela derivada com `MAX` por categoria.

**(c) Clientes acima da média de gasto** — **3 clientes**:

```text
nome             | gasto
-----------------+-------
Carlos Menezes   | 2528.4
Fernanda Lima    | 1812.2
Beatriz Nogueira | 1798.0
```

Exige **duas** camadas: agregar por cliente, depois tirar a média entre clientes — e usar essa média no `HAVING`. É o caso do item 4 do AP3: não há versão sem subconsulta.

**(d) Clientes que compraram todos os produtos de alguma categoria** — **3 resultados**:

```text
nome           | categoria
---------------+------------
Carlos Menezes | video
Helena Prado   | perifericos
Juliana Castro | perifericos
```

A construção é `NOT EXISTS` dentro de `NOT EXISTS` — a **divisão relacional**:

```sql
SELECT DISTINCT c.nome, cat.categoria
FROM clientes c
CROSS JOIN (SELECT DISTINCT categoria FROM produtos) cat
WHERE NOT EXISTS (
    SELECT 1 FROM produtos pr
    WHERE pr.categoria = cat.categoria
      AND NOT EXISTS (
          SELECT 1 FROM pedidos p
          JOIN itens_pedido i ON i.pedido_id = p.id
          WHERE p.cliente_id = c.id AND i.produto_id = pr.id
      )
);
```

**A leitura:** *"não existe produto desta categoria que este cliente não tenha comprado"*. A dupla negação é a única forma de expressar "todos" em SQL — não há quantificador universal. É reconhecidamente difícil, e vale saber que o padrão tem nome: **divisão relacional**.

**(e) Pedido de maior valor de cada cliente** — **8 linhas para 7 clientes**:

```text
nome             | pedido | valor
-----------------+--------+-------
Carlos Menezes   |     19 | 1099.7
Beatriz Nogueira |      4 |  899.0
Beatriz Nogueira |     18 |  899.0    ← EMPATE
Helena Prado     |     16 |  563.7
...
```

**O empate é o achado do exercício:** a Beatriz tem **dois** pedidos de R$ 899,00, e os dois aparecem. Isso não é bug — é a consequência de comparar por igualdade com o máximo. Se a pergunta exige **um** por cliente, é preciso um critério de desempate, e a ferramenta limpa para isso é a função de janela (`ROW_NUMBER`), que o módulo 04 apresenta. Reconhecer o empate e nomear a limitação vale mais que escondê-lo com `LIMIT`.

**Reflexão esperada:** o aninhamento ajuda quando cada nível responde a uma **pergunta com nome** — "a média da categoria", "o total por pedido" — e o leitor consegue enunciar o que a subconsulta devolve sem decifrá-la. Ele prejudica quando os níveis passam a existir por conveniência de escrita: três `SELECT` dentro de parênteses, sem nome, com a lógica de fora dependendo de detalhes de dentro. O sintoma é prático: se para entender a linha 1 você precisa ler até a linha 20 e voltar, a consulta está mal estruturada. E há um limite duro — a subconsulta **não pode ser reaproveitada**: se o mesmo cálculo aparece duas vezes, ele é escrito duas vezes, e as duas cópias divergem na primeira manutenção. É exatamente esse conjunto de problemas que as CTEs do 03.10 resolvem, dando nome a cada etapa e permitindo reuso.

**Critério de "está bom":** as cinco consultas funcionando; cada uma classificada quanto à correlação; o item (d) com a dupla negação (ou o reconhecimento honesto de que não conseguiu, com a tentativa registrada); e o item (e) **com o empate identificado** — quem entregou 7 linhas escondeu o problema em vez de resolvê-lo.
