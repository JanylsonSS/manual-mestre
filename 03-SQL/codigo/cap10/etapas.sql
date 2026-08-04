-- ------------------------------------------------------------
-- etapas.sql
-- Capítulo 03.10 — CTEs (WITH)
-- O que este arquivo demonstra: a mesma consulta antes e depois,
--   o encadeamento de etapas, o reuso e a CTE recursiva
-- Como executar: python codigo/sql.py codigo/cap10/etapas.sql
-- ------------------------------------------------------------

-- [1] ANTES (03.09): subconsulta no FROM — leitura de dentro pra fora
SELECT AVG(total_pedido) / 100.0 AS ticket_medio, COUNT(*) AS pedidos
FROM (
    SELECT p.id, SUM(i.quantidade * i.preco_unitario_centavos) AS total_pedido
    FROM pedidos p JOIN itens_pedido i ON i.pedido_id = p.id
    WHERE p.status = 'concluido'
    GROUP BY p.id
) AS totais;

-- [2] DEPOIS: a etapa ganhou NOME e a leitura virou de cima pra baixo.
--     Mesmo resultado — 489.3176... — a CTE não muda o que a consulta faz.
WITH totais_por_pedido AS (
    SELECT p.id AS pedido_id,
           SUM(i.quantidade * i.preco_unitario_centavos) AS total_centavos
    FROM pedidos p
    JOIN itens_pedido i ON i.pedido_id = p.id
    WHERE p.status = 'concluido'
    GROUP BY p.id
)
SELECT AVG(total_centavos) / 100.0 AS ticket_medio,
       COUNT(*)                    AS pedidos
FROM totais_por_pedido;

-- [3] ENCADEAMENTO: WITH aparece UMA vez; as demais vêm por VÍRGULA.
--     Leia como um roteiro: por pedido -> por cliente -> vs. média
WITH totais_por_pedido AS (
    SELECT p.id AS pedido_id, p.cliente_id,
           SUM(i.quantidade * i.preco_unitario_centavos) AS total_centavos
    FROM pedidos p
    JOIN itens_pedido i ON i.pedido_id = p.id
    WHERE p.status = 'concluido'
    GROUP BY p.id, p.cliente_id
),
gasto_por_cliente AS (
    SELECT cliente_id,
           SUM(total_centavos) AS gasto_centavos,
           COUNT(*)            AS pedidos
    FROM totais_por_pedido            -- usa a CTE anterior
    GROUP BY cliente_id
),
media_geral AS (
    SELECT AVG(gasto_centavos) AS media FROM gasto_por_cliente
)
SELECT c.nome,
       g.pedidos,
       g.gasto_centavos / 100.0 AS gasto,
       ROUND(g.gasto_centavos - (SELECT media FROM media_geral), 0) / 100.0
           AS acima_da_media
FROM gasto_por_cliente g
JOIN clientes c ON c.id = g.cliente_id
ORDER BY gasto DESC;

-- [4] REUSO: a CTE 'gasto' é usada DUAS vezes — no FROM e no percentual.
--     Com tabela derivada, o bloco teria que ser escrito duas vezes.
WITH gasto AS (
    SELECT p.cliente_id, SUM(i.quantidade * i.preco_unitario_centavos) AS total
    FROM pedidos p JOIN itens_pedido i ON i.pedido_id = p.id
    WHERE p.status = 'concluido'
    GROUP BY p.cliente_id
)
SELECT c.nome,
       g.total / 100.0 AS gasto,
       ROUND(g.total * 100.0 / (SELECT SUM(total) FROM gasto), 1) AS pct_do_total
FROM gasto g
JOIN clientes c ON c.id = g.cliente_id
ORDER BY gasto DESC;

-- [5] A SOLUÇÃO do problema do 03.07: cada tabela filha agregada na
--     SUA CTE, reduzida a uma linha por pedido ANTES de juntar ao pai.
--     Com uma segunda filha, acrescenta-se outra CTE — nada multiplica.
WITH itens AS (
    SELECT pedido_id,
           SUM(quantidade * preco_unitario_centavos) AS total_itens,
           COUNT(*)                                  AS qtd_itens
    FROM itens_pedido
    GROUP BY pedido_id
)
SELECT p.id, p.status, i.qtd_itens, i.total_itens / 100.0 AS valor
FROM pedidos p
JOIN itens i ON i.pedido_id = p.id
ORDER BY valor DESC
LIMIT 4;

-- [6] RECURSIVA: caso base UNION ALL passo. Sem condição de parada,
--     não termina. Uso real: hierarquias (módulo 10).
WITH RECURSIVE contagem(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM contagem WHERE n < 5
)
SELECT n FROM contagem;
