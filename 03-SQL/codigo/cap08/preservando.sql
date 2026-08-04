-- ------------------------------------------------------------
-- preservando.sql
-- Capítulo 03.08 — JOIN parte 2: LEFT/RIGHT/FULL
-- O que este arquivo demonstra: o desaparecimento no INNER, a
--   preservação no LEFT, os anti-joins e a armadilha do WHERE
-- Como executar: python codigo/sql.py codigo/cap08/preservando.sql
-- ------------------------------------------------------------

-- [1] INNER: 7 clientes de 8. O Rafael some, SEM AVISO.
SELECT COUNT(DISTINCT c.id) AS clientes_no_inner
FROM clientes c JOIN pedidos p ON p.cliente_id = c.id;

-- [2] LEFT: os 8 aparecem. Note COUNT(p.id), não COUNT(*) —
--     a linha do Rafael existe, mas p.id nela é NULL (03.05)
SELECT c.nome, COUNT(p.id) AS pedidos
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
GROUP BY c.id, c.nome
ORDER BY pedidos, c.nome;

-- [3] O NULL FABRICADO pela junção: não existe pedido com id nulo
SELECT c.nome, p.id AS pedido, p.data
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
WHERE c.nome = 'Rafael Torres';

-- [4] ANTI-JOIN: "quem nunca comprou?"
--     Teste IS NULL na CHAVE PRIMÁRIA — coluna que nunca é nula
SELECT c.nome AS nunca_comprou
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
WHERE p.id IS NULL;

-- [5] ANTI-JOIN: "quais produtos estão encalhados?"
SELECT pr.nome AS nunca_vendido
FROM produtos pr
LEFT JOIN itens_pedido i ON i.produto_id = pr.id
WHERE i.id IS NULL;

-- [6] A ARMADILHA: filtro no WHERE mata o LEFT.
--     NULL = 'concluido' é DESCONHECIDO -> o Rafael é descartado
--     -> 7 clientes. O LEFT virou INNER, sem aviso.
SELECT COUNT(DISTINCT c.id) AS clientes_com_where
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
WHERE p.status = 'concluido';

-- [7] A CORREÇÃO: a condição faz parte da LIGAÇÃO -> 8 clientes
SELECT COUNT(DISTINCT c.id) AS clientes_com_on
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
                   AND p.status = 'concluido';

-- [8] O relatório correto: todos os clientes, com os concluídos
SELECT c.nome, COUNT(p.id) AS pedidos_concluidos
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
                   AND p.status = 'concluido'
GROUP BY c.id, c.nome
ORDER BY pedidos_concluidos, c.nome;
