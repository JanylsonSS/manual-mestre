-- ------------------------------------------------------------
-- aninhando.sql
-- Capítulo 03.09 — Subconsultas
-- O que este arquivo demonstra: subquery escalar, IN, EXISTS,
--   tabela derivada, a armadilha do NOT IN e a dívida do 03.04
-- Como executar: python codigo/sql.py codigo/cap09/aninhando.sql
-- ------------------------------------------------------------

-- [1] ESCALAR no WHERE: a média é calculada UMA vez, não fica no código
SELECT nome, preco_centavos / 100.0 AS preco
FROM produtos
WHERE preco_centavos > (SELECT AVG(preco_centavos) FROM produtos)
ORDER BY preco_centavos DESC;

-- [2] LISTA com IN: quem teve pedido cancelado
SELECT nome FROM clientes
WHERE id IN (SELECT cliente_id FROM pedidos WHERE status = 'cancelado');

-- [3] NOT IN funciona AQUI porque produto_id é NOT NULL -> 1 linha
SELECT nome AS nunca_vendido FROM produtos
WHERE id NOT IN (SELECT produto_id FROM itens_pedido);

-- [4] A ARMADILHA: um único NULL na lista -> ZERO linhas, sem erro.
--     id NOT IN (1,2,NULL) vira "id<>1 AND id<>2 AND id<>NULL",
--     e a última comparação é DESCONHECIDA (03.03)
SELECT COUNT(*) AS resultado_zerado FROM produtos
WHERE id NOT IN (SELECT produto_id FROM itens_pedido UNION SELECT NULL);

-- [5] NOT EXISTS: a forma SEGURA — não compara valores, logo
--     é imune a NULL. O SELECT 1 é convenção: o valor não é usado.
SELECT c.nome AS nunca_comprou FROM clientes c
WHERE NOT EXISTS (SELECT 1 FROM pedidos p WHERE p.cliente_id = c.id);

-- [6] EXISTS não multiplica linhas: cada cliente aparece UMA vez,
--     mesmo tendo comprado vários itens de áudio (com JOIN
--     precisaria de DISTINCT)
SELECT c.nome FROM clientes c
WHERE EXISTS (
    SELECT 1 FROM pedidos p
    JOIN itens_pedido i ON i.pedido_id = p.id
    JOIN produtos pr    ON pr.id = i.produto_id
    WHERE p.cliente_id = c.id AND pr.categoria = 'audio'
);

-- [7] TABELA DERIVADA: agregar o que já foi agregado.
--     De dentro para fora: soma por pedido -> média entre pedidos
SELECT AVG(total_pedido) / 100.0 AS ticket_medio,
       COUNT(*)                  AS pedidos
FROM (
    SELECT p.id, SUM(i.quantidade * i.preco_unitario_centavos) AS total_pedido
    FROM pedidos p
    JOIN itens_pedido i ON i.pedido_id = p.id
    WHERE p.status = 'concluido'
    GROUP BY p.id
) AS totais;

-- [8] Subquery no SELECT: cada uma é INDEPENDENTE, então duas
--     tabelas filhas não se multiplicam (o problema do 03.07)
SELECT c.nome,
       (SELECT COUNT(*)    FROM pedidos p WHERE p.cliente_id = c.id) AS pedidos,
       (SELECT MAX(p.data) FROM pedidos p WHERE p.cliente_id = c.id) AS ultima
FROM clientes c
ORDER BY pedidos DESC;

-- [9] A DÍVIDA DO 03.04: o produto mais caro de CADA categoria.
--     Correlacionada: "o maior preço da SUA PRÓPRIA categoria"
SELECT pr.categoria, pr.nome, pr.preco_centavos / 100.0 AS preco
FROM produtos pr
WHERE pr.preco_centavos = (
    SELECT MAX(preco_centavos) FROM produtos WHERE categoria = pr.categoria
)
ORDER BY pr.categoria;
