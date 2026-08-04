# Gabaritos — Capítulo 03.07

Abra somente após tentativa honesta.

## A1 — Quantas linhas?

| # | Junção | Linhas | Por quê |
|---|---|---|---|
| 1 | `produtos, itens_pedido` | **372** | 12 × 31 — cartesiano |
| 2 | `pedidos JOIN itens_pedido` | **31** | uma por item |
| 3 | `produtos JOIN itens_pedido` | **31** | uma por item (todo item tem 1 produto) |
| 4 | `clientes JOIN pedidos` + concluídos | **17** | uma por pedido concluído |
| 5 | `clientes, produtos` | **96** | 8 × 12 — cartesiano |
| 6 | as quatro encadeadas | **31** | a tabela mais fina define |

**Critério:** 6/6. O item 3 é o que confirma a regra: juntar `produtos` (12 linhas) com `itens_pedido` (31) dá **31**, não 372 — porque cada item casa com **um** produto. O resultado nunca é maior que a tabela mais fina quando a ligação é FK→PK.

## A2 — Escreva o `ON`

```sql
-- 1
ON p.cliente_id = c.id

-- 2
ON i.pedido_id = p.id

-- 3
ON pr.id = i.produto_id

-- 4 — indireto: exige TRÊS tabelas (clientes → pedidos → itens_pedido)
FROM clientes c
JOIN pedidos p      ON p.cliente_id = c.id
JOIN itens_pedido i ON i.pedido_id  = p.id

-- 5 — auto-junção: a mesma tabela duas vezes, com apelidos diferentes
FROM clientes a
JOIN clientes b ON b.cidade = a.cidade AND b.id <> a.id

-- 6 — indireto: produtos → itens_pedido → pedidos
FROM produtos pr
JOIN itens_pedido i ON i.produto_id = pr.id
JOIN pedidos p      ON p.id         = i.pedido_id
```

**Ponto de atenção nos itens 4 e 6:** não existe ligação **direta** entre `clientes` e `itens_pedido`, nem entre `produtos` e `pedidos` — e isso não é uma falha do modelo, é a consequência de ele estar normalizado. O caminho passa pela tabela do meio, e reconhecer isso é ler o diagrama corretamente.

**Item 5 — a auto-junção:** a mesma tabela aparece duas vezes com apelidos distintos, como se fossem duas tabelas. O `AND b.id <> a.id` evita parear cada cliente consigo mesmo. É a primeira aparição de uma técnica que o 03.09 aprofunda.

**Critério:** 6/6, com os itens 4 e 6 reconhecidos como indiretos.

## A3 — Ache o cartesiano

1. **Não** — a condição está no `WHERE`, e o resultado é equivalente ao `INNER JOIN` (sintaxe antiga). 20 linhas.
2. **SIM** — sem condição nenhuma. 160 linhas.
3. **SIM, disfarçado** — `c.id > 0` é verdadeiro para todos; nada é descartado. 160 linhas.
4. **Não** — 2 `JOIN`, 2 `ON`, ambos corretos. 31 linhas.
5. **SIM, parcial** — o segundo `ON` não liga `produtos` a nada; ele **filtra**. Cada linha da junção anterior (20) se combina com os 11 produtos ativos → **220 linhas**.

**Critério:** 5/5. O item 5 é o mais importante: a condição do `ON` é sintaticamente válida e semanticamente errada — ela não relaciona as tabelas, e o resultado é um cartesiano parcial. A verificação mecânica (contar `JOIN` e `ON`) **não pega** este caso; o que pega é ler cada `ON` e confirmar que ele **compara colunas das duas tabelas**.

## A4 — Traduza a pergunta

```sql
-- 1
SELECT c.nome AS cliente, p.data
FROM clientes c JOIN pedidos p ON p.cliente_id = c.id
ORDER BY p.data;

-- 2
SELECT pr.nome AS produto, i.quantidade
FROM itens_pedido i JOIN produtos pr ON pr.id = i.produto_id
WHERE i.pedido_id = 1;

-- 3
SELECT pr.nome AS produto, i.quantidade, p.data
FROM clientes c
JOIN pedidos p      ON p.cliente_id = c.id
JOIN itens_pedido i ON i.pedido_id  = p.id
JOIN produtos pr    ON pr.id        = i.produto_id
WHERE c.nome = 'Ana Souza'
ORDER BY p.data;

-- 4
SELECT c.cidade, pr.nome AS produto, i.quantidade
FROM clientes c
JOIN pedidos p      ON p.cliente_id = c.id
JOIN itens_pedido i ON i.pedido_id  = p.id
JOIN produtos pr    ON pr.id        = i.produto_id;

-- 5
SELECT c.nome AS cliente, p.id AS pedido, p.data
FROM clientes c JOIN pedidos p ON p.cliente_id = c.id
WHERE p.status = 'concluido'
ORDER BY p.data, p.id;

-- 6
SELECT DISTINCT pr.categoria
FROM clientes c
JOIN pedidos p      ON p.cliente_id = c.id
JOIN itens_pedido i ON i.pedido_id  = p.id
JOIN produtos pr    ON pr.id        = i.produto_id
WHERE c.nome = 'Fernanda Lima'
ORDER BY pr.categoria;
```

**Critério:** 6/6, com apelidos em todas as tabelas e colunas qualificadas. O item 6 exige o `DISTINCT` porque a junção repete a categoria uma vez por item.

## AP1 — O extrato do cliente

```sql
SELECT pr.nome                                       AS produto,
       i.quantidade,
       i.preco_unitario_centavos / 100.0             AS preco_unit_reais,
       i.quantidade * i.preco_unitario_centavos / 100.0 AS total_linha_reais,
       p.data
FROM clientes c
JOIN pedidos p      ON p.cliente_id = c.id
JOIN itens_pedido i ON i.pedido_id  = p.id
JOIN produtos pr    ON pr.id        = i.produto_id
WHERE c.nome = 'Fernanda Lima'
ORDER BY p.data, pr.nome;
```

**Contagens:** Fernanda **8** itens (5 pedidos), Ana **5** itens (4 pedidos).

**Item 4 — a divergência:** a Fernanda tem 5 pedidos e 8 itens; a Ana, 4 pedidos e 5 itens. O extrato tem uma linha por **item**, não por pedido — se você previu 5 e 4, previu pedidos. É a granularidade novamente.

**Item 5 — por `id`:** `WHERE c.id = 1`. Preferível num sistema real: o `id` é único e estável, o nome não é (dois clientes homônimos quebrariam a consulta em silêncio, trazendo os itens dos dois).

**Critério:** as duas previsões escritas antes, e a divergência explicada por granularidade — não por erro de contagem.

## AP2 — Prevendo a granularidade

| # | Junção | Linhas | Explicação |
|---|---|---|---|
| 1 | clientes + pedidos | **20** | uma por pedido |
| 2 | pedidos + itens | **31** | uma por item |
| 3 | clientes + pedidos + itens | **31** | a mais fina continua sendo itens |
| 4 | as quatro | **31** | `produtos` não multiplica (1 por item) |
| 5 | produtos + itens | **31** | idem |

**A regra, enunciada:** numa cadeia de junções por FK→PK, o número de linhas do resultado é o da **tabela mais fina** da cadeia — aquela cujas linhas são as mais numerosas e específicas. Acrescentar uma tabela do lado "um" (como `produtos` para `itens`) **não** aumenta o resultado; acrescentar uma do lado "muitos" (como `itens` para `pedidos`) aumenta.

**Critério:** as cinco previsões e a regra enunciada com palavras próprias.

## AP3 — A soma dobrada

**Cenário criado:** o pedido 1 tem **2 itens** e recebe **2 pagamentos**.

```sql
CREATE TABLE pagamentos (
    id             INTEGER PRIMARY KEY,
    pedido_id      INTEGER NOT NULL,
    valor_centavos INTEGER NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);
INSERT INTO pagamentos VALUES (1, 1, 27000), (2, 1, 26970);
```

**As somas corretas (separadas):**

```text
total_itens | total_pago
------------+-----------
      53970 |      53970
```

**A junção das duas filhas:**

```sql
SELECT COUNT(*) FROM pedidos p
JOIN itens_pedido i ON i.pedido_id = p.id
JOIN pagamentos g   ON g.pedido_id = p.id
WHERE p.id = 1;
```

```text
linhas
------
     4
```

2 itens × 2 pagamentos = **4 linhas**. E as somas:

```text
itens_inflado | pago_inflado
--------------+-------------
       107940 |       107940
```

**Item 4 — os fatores de inflação:** a soma dos itens foi multiplicada por **2** (o número de pagamentos), e a soma dos pagamentos, também por **2** (o número de itens). Neste caso os fatores coincidem porque os dois lados têm 2 linhas; com 3 itens e 2 pagamentos, a soma dos itens dobraria e a dos pagamentos triplicaria — **fatores diferentes**, o que torna o erro ainda mais difícil de reconhecer.

**Item 5 — a versão correta:**

```sql
-- Duas consultas separadas
SELECT SUM(quantidade * preco_unitario_centavos) FROM itens_pedido WHERE pedido_id = 1;
SELECT SUM(valor_centavos) FROM pagamentos WHERE pedido_id = 1;

-- Ou, numa consulta só, com subconsultas escalares (03.09):
SELECT p.id,
       (SELECT SUM(quantidade * preco_unitario_centavos)
        FROM itens_pedido WHERE pedido_id = p.id) AS total_itens,
       (SELECT SUM(valor_centavos)
        FROM pagamentos WHERE pedido_id = p.id)   AS total_pago
FROM pedidos p WHERE p.id = 1;
```

**Ponto de atenção:** se o pedido tivesse **um** pagamento só, as somas sairiam **corretas** — e o bug ficaria dormindo até o primeiro pedido parcelado. É por isso que este erro sobrevive em produção: os dados de teste raramente têm dois filhos dos dois lados.

**Critério:** o cenário criado de verdade; as 4 linhas observadas; os fatores de inflação identificados; e a percepção de que com um pagamento só o bug não apareceria.

## D1 — O relatório de vendas completo

**Consulta base:**

```sql
SELECT c.nome                                            AS cliente,
       c.cidade,
       p.data                                            AS data_pedido,
       p.status,
       pr.nome                                           AS produto,
       pr.categoria,
       i.quantidade,
       i.preco_unitario_centavos / 100.0                 AS preco_unit_reais,
       i.quantidade * i.preco_unitario_centavos / 100.0  AS total_linha_reais
FROM clientes c
JOIN pedidos p      ON p.cliente_id = c.id
JOIN itens_pedido i ON i.pedido_id  = p.id
JOIN produtos pr    ON pr.id        = i.produto_id
ORDER BY p.data, p.id, pr.nome;
```

**(a) Previsão:** **31 linhas** — uma por item, a tabela mais fina.

**(b) Com o filtro de concluídos:** **28 linhas**. E a resposta sobre `ON` × `WHERE`: **num `INNER JOIN`, dá no mesmo** — as duas formas produzem 28 linhas. A explicação: no `INNER`, um par que não satisfaz a condição é descartado, esteja ela no `ON` ou no `WHERE`. **Isso muda no `LEFT JOIN`** (03.08), onde a posição da condição decide se a linha da esquerda é preservada ou não. Registre a observação: ela é uma das pegadinhas mais frequentes do próximo capítulo.

**(c) As duas contagens:**

```sql
SELECT COUNT(DISTINCT p.id) AS pedidos, COUNT(*) AS itens
FROM clientes c
JOIN pedidos p      ON p.cliente_id = c.id
JOIN itens_pedido i ON i.pedido_id  = p.id
WHERE p.status = 'concluido';
```

```text
pedidos | itens
--------+------
     17 |    28
```

**Por que tratamentos diferentes:** o resultado da junção está na granularidade do **item**. `COUNT(*)` conta linhas desse resultado — portanto, itens. Para contar pedidos, é preciso desfazer a repetição com `DISTINCT`, porque cada pedido aparece uma vez por item que possui.

**(d) A versão cartesiana:** trocando os `JOIN ... ON` por vírgulas sem condição, o resultado seria 8 × 20 × 31 × 12 = **59.520 linhas**, contra 31. Com tabelas reais de milhões de linhas, a consulta não terminaria.

**(e) O índice:** `CREATE INDEX idx_itens_pedido_id ON itens_pedido(pedido_id)` — e o equivalente em `pedidos(cliente_id)` e `itens_pedido(produto_id)`. Justificativa: as três são colunas de **chave estrangeira**, usadas nos `ON`, e não ganham índice automaticamente (03.02). Com índice, o banco resolve cada junção por busca indexada em vez de varredura; sem, precisa construir tabelas de dispersão ou ordenar. É a otimização de maior retorno em junções (03.14 mede).

**Reflexão esperada:** prever o número de linhas é a habilidade central porque ela é a **única defesa contra uma classe inteira de erros silenciosos**. Uma junção nunca dá erro por multiplicar linhas — ela devolve um resultado plausível, com números maiores do que deveriam ser, e nada avisa. Quem escreve a consulta e depois olha o resultado não tem como saber se 28 é o número certo; quem prevê 28 **antes** e recebe 28 confirmou o modelo mental. E quando a previsão falha, a divergência aponta exatamente onde o entendimento estava errado — qual tabela multiplicou, qual condição faltou. É a mesma disciplina do "preveja antes de rodar" que o manual pede desde o 01.03, aplicada ao lugar em que ela mais rende.

**Critério de "está bom":** a previsão escrita antes; o item (b) observando que `ON` e `WHERE` coincidem no `INNER` **e** registrando que isso muda; o item (c) explicando a granularidade; o índice do item (e) justificado por ser FK sem índice automático.
