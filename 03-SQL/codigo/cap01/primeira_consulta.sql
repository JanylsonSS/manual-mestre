-- ------------------------------------------------------------
-- primeira_consulta.sql
-- Capítulo 03.01 — Por que bancos relacionais existem
-- O que este arquivo demonstra: a pergunta que o CSV não respondia
--   "quanto a Fernanda gastou por categoria?"
-- Como executar: python codigo/sql.py codigo/cap01/primeira_consulta.sql
--
-- NÃO tente entender ainda. Junções vêm no 03.07, agregação no 03.05
-- e agrupamento no 03.06. Rode, veja o resultado, e volte aqui depois.
-- ------------------------------------------------------------

SELECT pr.categoria,
       COUNT(*)                                                 AS itens,
       SUM(ip.quantidade * ip.preco_unitario_centavos) / 100.0   AS total_reais
FROM clientes c
JOIN pedidos p       ON p.cliente_id = c.id
JOIN itens_pedido ip ON ip.pedido_id = p.id
JOIN produtos pr     ON pr.id = ip.produto_id
WHERE c.nome = 'Fernanda Lima'
  AND p.status = 'concluido'
GROUP BY pr.categoria
ORDER BY total_reais DESC;
