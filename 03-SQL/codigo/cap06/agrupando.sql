-- ------------------------------------------------------------
-- agrupando.sql
-- Capítulo 03.06 — GROUP BY e HAVING
-- O que este arquivo demonstra: agrupamento, o NULL como grupo,
--   a diferença WHERE x HAVING e a dor da Aurora respondida
-- Como executar: python codigo/sql.py codigo/cap06/agrupando.sql
-- ------------------------------------------------------------

-- [1] O sort | uniq -c do 02.04, declarativo
SELECT cidade, COUNT(*) AS clientes
FROM clientes
GROUP BY cidade
ORDER BY clientes DESC;

-- [2] O NULL forma SEU PRÓPRIO grupo (≠ do WHERE, onde ele some)
--     A quarta linha acima é a Helena. Para excluí-la, seja explícito:
SELECT cidade, COUNT(*) AS clientes
FROM clientes
WHERE cidade IS NOT NULL
GROUP BY cidade;

-- [3] WHERE: descarta LINHAS antes de agrupar
--     "considerando só produtos caros, quantos por categoria?"
SELECT categoria, COUNT(*) AS qtd
FROM produtos
WHERE preco_centavos > 30000
GROUP BY categoria;

-- [4] HAVING: descarta GRUPOS depois de agregar
--     "quais categorias têm MÉDIA acima de R$ 300?"
--     Note: audio aparece com 4 (não 2) — o grupo inteiro passou
SELECT categoria, COUNT(*) AS qtd, AVG(preco_centavos) / 100.0 AS media
FROM produtos
GROUP BY categoria
HAVING AVG(preco_centavos) > 30000;

-- [5] Os dois juntos, na ordem de execução:
--     WHERE (linhas) -> GROUP BY -> HAVING (grupos) -> ORDER BY
SELECT categoria, COUNT(*) AS qtd, AVG(preco_centavos) / 100.0 AS media
FROM produtos
WHERE ativo = 1
GROUP BY categoria
HAVING COUNT(*) >= 3
ORDER BY qtd DESC;

-- [6] Agrupar por DUAS colunas: o grupo é a combinação
SELECT categoria, ativo, COUNT(*) AS qtd
FROM produtos
GROUP BY categoria, ativo
ORDER BY categoria, ativo;

-- [7] A DOR DA AURORA, respondida: faturamento por cidade
--     COUNT(DISTINCT p.id) porque a junção repete o pedido por item (03.05)
SELECT c.cidade,
       COUNT(DISTINCT p.id)                                  AS pedidos,
       SUM(i.quantidade * i.preco_unitario_centavos) / 100.0 AS faturamento_reais
FROM clientes c
JOIN pedidos p       ON p.cliente_id = c.id
JOIN itens_pedido i  ON i.pedido_id  = p.id
WHERE p.status = 'concluido'
GROUP BY c.cidade
ORDER BY faturamento_reais DESC;
