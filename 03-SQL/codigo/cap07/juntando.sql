-- ------------------------------------------------------------
-- juntando.sql
-- Capítulo 03.07 — JOIN parte 1: INNER
-- O que este arquivo demonstra: o produto cartesiano, a junção
--   correta, a ambiguidade de coluna e o encadeamento de 4 tabelas
-- Como executar: python codigo/sql.py codigo/cap07/juntando.sql
-- ------------------------------------------------------------

-- [1] O PRODUTO CARTESIANO: todos os pares possíveis -> 8 x 20 = 160
--     Com tabelas grandes, isto trava a consulta.
SELECT COUNT(*) AS pares_possiveis FROM clientes, pedidos;

-- [2] A mesma coisa, disfarçada: um ON sempre verdadeiro
SELECT COUNT(*) AS tambem_cartesiano
FROM clientes c JOIN pedidos p ON 1 = 1;

-- [3] A junção CORRETA: o ON descarta 140 pares sem sentido -> 20
SELECT COUNT(*) AS linhas FROM clientes c
JOIN pedidos p ON p.cliente_id = c.id;

-- [4] Os dados: a Fernanda aparece 5 vezes (tem 5 pedidos).
--     Não é duplicação — é uma linha por PEDIDO.
SELECT c.nome, p.id AS pedido, p.data
FROM clientes c
JOIN pedidos p ON p.cliente_id = c.id
ORDER BY p.id
LIMIT 5;

-- [5] Qualificar é obrigatório: 'id' existe nas duas tabelas
--     Sem o apelido: "ambiguous column name: id"
SELECT c.id AS cliente_id, p.id AS pedido_id, c.nome
FROM clientes c
JOIN pedidos p ON p.cliente_id = c.id
LIMIT 3;

-- [6] QUATRO tabelas: leia como um caminho —
--     clientes, com seus pedidos, com seus itens, com os produtos
SELECT c.nome AS cliente, p.id AS pedido,
       pr.nome AS produto, i.quantidade
FROM clientes c
JOIN pedidos p      ON p.cliente_id = c.id
JOIN itens_pedido i ON i.pedido_id  = p.id
JOIN produtos pr    ON pr.id        = i.produto_id
ORDER BY p.id, pr.nome
LIMIT 5;

-- [7] A GRANULARIDADE: 31 = número de ITENS, não de pedidos (20)
--     A tabela mais fina da junção define o resultado.
SELECT COUNT(*) AS linhas_do_resultado
FROM clientes c
JOIN pedidos p      ON p.cliente_id = c.id
JOIN itens_pedido i ON i.pedido_id  = p.id
JOIN produtos pr    ON pr.id        = i.produto_id;

-- [8] A pergunta que atravessa as quatro tabelas:
--     "quais produtos a Fernanda comprou?"
SELECT pr.nome AS produto, i.quantidade, p.data
FROM clientes c
JOIN pedidos p      ON p.cliente_id = c.id
JOIN itens_pedido i ON i.pedido_id  = p.id
JOIN produtos pr    ON pr.id        = i.produto_id
WHERE c.nome = 'Fernanda Lima'
ORDER BY p.data, pr.nome;
