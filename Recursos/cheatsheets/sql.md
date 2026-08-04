# Cheatsheet — SQL

Referência de consulta rápida do módulo 03. Dialeto: SQLite (diferenças relevantes anotadas).

## Consultar

```sql
SELECT col1, col2 AS apelido FROM tabela WHERE cond ORDER BY col DESC LIMIT 10;

WHERE preco BETWEEN 100 AND 500        -- inclusivo nas duas pontas
WHERE categoria IN ('audio','video')
WHERE nome LIKE 'Mou%'                 -- % qualquer coisa · _ um caractere
WHERE email IS NULL                    -- NUNCA "= NULL"
SELECT DISTINCT cidade FROM clientes;
```

## `NULL` — a tabela que resolve metade dos erros

| Operação | Com `NULL` |
|---|---|
| `= NULL` | nunca verdadeiro → use `IS NULL` |
| `SUM`, `AVG`, `MIN`, `MAX` | **ignoram** os nulos |
| `COUNT(*)` / `COUNT(col)` | conta linhas / conta **não nulos** |
| `GROUP BY` | agrupa todos os nulos **numa linha** |
| `NOT IN (... NULL ...)` | **zero linhas** → use `NOT EXISTS` |
| `UNIQUE` | aceita **vários** nulos |
| `CHECK` | `NULL` **atravessa** |

## Agregar

```sql
SELECT categoria, COUNT(*) AS n, SUM(preco_centavos) AS total
FROM produtos
WHERE ativo = 1                        -- filtra LINHAS, antes
GROUP BY categoria
HAVING COUNT(*) > 2                    -- filtra GRUPOS, depois
ORDER BY total DESC;
```

## Juntar

```sql
FROM pedidos p JOIN itens_pedido i ON i.pedido_id = p.id       -- so quem casa
FROM clientes c LEFT JOIN pedidos p ON p.cliente_id = c.id     -- todos da esquerda

-- anti-join: quem NAO tem correspondencia
FROM clientes c LEFT JOIN pedidos p ON p.cliente_id = c.id
WHERE p.id IS NULL

-- num LEFT JOIN: COUNT(p.id), nao COUNT(*)
-- com DOIS JOIN: COUNT(DISTINCT p.id)
```

## Compor

```sql
WHERE preco > (SELECT AVG(preco) FROM produtos)     -- roda UMA vez
WHERE EXISTS (SELECT 1 FROM itens i WHERE i.produto_id = p.id)   -- por linha

WITH etapa1 AS (
    SELECT ...
),                                     -- WITH uma vez; o resto por VIRGULA
etapa2 AS (
    SELECT ... FROM etapa1
)
SELECT ... FROM etapa2;
```

## Escrever — o procedimento de 5 passos

```sql
-- 1. rascunho   2. ENSAIO com o WHERE exato   3. BEGIN
SELECT id, nome FROM produtos WHERE categoria = 'audio' AND ativo = 1;  -- 4 linhas

BEGIN;
UPDATE produtos SET preco_centavos = CAST(ROUND(preco_centavos * 1.10) AS INTEGER)
WHERE categoria = 'audio' AND ativo = 1;     -- 4. WHERE COPIADO do ensaio
-- 5. conferir: "Linhas afetadas: 4" tem que bater com o ensaio
COMMIT;                                       -- ou ROLLBACK

INSERT INTO t (col1, col2) VALUES (?, ?);     -- SEMPRE nomeie as colunas
DELETE FROM t WHERE id = ?;                   -- remove a LINHA inteira
```

## Estruturar

```sql
CREATE TABLE pedidos (
    id         INTEGER PRIMARY KEY,               -- preenchido sozinho
    cliente_id INTEGER NOT NULL,
    data       TEXT    NOT NULL CHECK (data LIKE '____-__-__'),
    status     TEXT    NOT NULL CHECK (status IN ('pendente','concluido')),
    total_centavos INTEGER NOT NULL CHECK (total_centavos > 0),
    ativo      INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0,1)),
    nome       TEXT    NOT NULL CHECK (LENGTH(TRIM(nome)) > 0),  -- '' nao e NULL
    email      TEXT    NOT NULL UNIQUE COLLATE NOCASE,           -- os DOIS
    UNIQUE (cliente_id, data),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT
) STRICT;                                        -- 3.37+: garante TIPO, nao faixa

ALTER TABLE t ADD COLUMN c TEXT DEFAULT 'x';
ALTER TABLE t RENAME COLUMN a TO b;
ALTER TABLE t DROP COLUMN c;
-- NAO EXISTE ALTER COLUMN: criar nova, copiar, DROP, RENAME (em transacao)
```

### Tipos — as decisões

| Guardar | Use | Por quê |
|---|---|---|
| dinheiro | `INTEGER` em centavos | `0.1 + 0.2 = 0.3` é **falso** |
| data | `TEXT` ISO `YYYY-MM-DD` | ordem alfabética = cronológica |
| booleano | `INTEGER` 0/1 | não existe tipo próprio |
| CPF, CEP, telefone | `TEXT` | zeros à esquerda somem em `INTEGER` |
| foto, arquivo | `TEXT` com o caminho | `BLOB` incha backup e consulta |

### `ON DELETE`

| Ação | Ao apagar o pai | Quando |
|---|---|---|
| `CASCADE` | apaga os filhos | filho não existe sem o pai (itens, fotos) |
| `SET NULL` | filho fica órfão | relação opcional (categoria) |
| `RESTRICT` | **recusa** | histórico (pedidos) — **na dúvida, este** |

## Índices

```sql
EXPLAIN QUERY PLAN SELECT ...;     -- PRIMEIRO comando diante de consulta lenta
-- SCAN   = varre a tabela
-- SEARCH = usa indice
-- SCAN ... USING INDEX = varre o indice, na ordem (ORDER BY de graca)

CREATE INDEX idx_tabela_coluna ON tabela(coluna);
CREATE INDEX idx_t_ab ON t(a, b);      -- serve a "a" e "a+b"; NUNCA so "b"
DROP INDEX idx_tabela_coluna;

SELECT COUNT(DISTINCT coluna) FROM t;  -- mede a seletividade ANTES de indexar
```

**Vale a pena?** Se o filtro devolve **menos de ~5%** da tabela. Medido: 13 de 500 mil → 763x;
100 mil de 500 mil → ganho zero; 62 mil (12,5%) → **51% mais lento**.
**Custo:** três índices = +66% no tempo de escrita, para sempre.
**Desliga o índice:** `UPPER(col)`, `col + 0`, `strftime(...)`, `LIKE '%algo'`.

## Transações

```sql
BEGIN;              -- reserva a escrita so no primeiro UPDATE
BEGIN IMMEDIATE;    -- reserva JA: use quando a leitura decide a escrita
COMMIT;
ROLLBACK;           -- um ERRO NAO faz isso sozinho: a transacao fica ABERTA
```

**Evitar o *lost update*** (dois leem, dois gravam, um some sem erro):

```sql
UPDATE contas SET saldo = saldo - 100 WHERE id = ?;              -- 1a escolha
UPDATE produtos SET estoque = estoque - 1 WHERE id=? AND estoque > 0;  -- + rowcount
BEGIN IMMEDIATE; SELECT ...; UPDATE ...; COMMIT;                 -- pessimista
UPDATE t SET x = ? WHERE id = ? AND x = <lido>;                  -- otimista + rowcount
```

Lote: 3 000 linhas em autocommit = 10 609 ms · lotes de 100 = 107 ms · uma transação = 5,9 ms.

## Diagnóstico rápido

| Sintoma | Investigue |
|---|---|
| consulta lenta | `EXPLAIN QUERY PLAN`; seletividade; função sobre a coluna |
| soma dobrada | junção multiplicando linhas → CTE por filha |
| `NOT IN` vazio | `NULL` na subconsulta → `NOT EXISTS` |
| `UNIQUE` com duplicatas | são `NULL`s; ou diferença de caixa; ou é sobre um **par** |
| `database is locked` | transação longa; `COMMIT` esquecido; `timeout` curto |
| `Linhas afetadas: 0` | resultado que **exige explicação** — confira o valor do filtro |
| FK "não funciona" | `PRAGMA foreign_keys = ON` (desligado por padrão) |
