-- ------------------------------------------------------------
-- organizando.sql
-- Capítulo 03.04 — Ordenação, LIMIT e DISTINCT
-- O que este arquivo demonstra: ORDER BY com desempate, a posição
--   do NULL, paginação estável, o alcance do DISTINCT e o AS
-- Como executar: python codigo/sql.py codigo/cap04/organizando.sql
-- ------------------------------------------------------------

-- [1] Duas colunas: a segunda é o critério de DESEMPATE
SELECT nome, categoria, preco_centavos FROM produtos
ORDER BY categoria ASC, preco_centavos DESC
LIMIT 6;

-- [2] Onde o NULL para? SQLite e PostgreSQL: primeiro no ASC.
--     Portável em qualquer banco: ORDER BY (cidade IS NULL), cidade
SELECT nome, cidade FROM clientes ORDER BY cidade;

-- [3] O AS dá nome à expressão — e o apelido vale no ORDER BY,
--     porque ele roda DEPOIS do SELECT
SELECT nome AS produto, preco_centavos / 100.0 AS preco_reais
FROM produtos
ORDER BY preco_reais DESC
LIMIT 3;

-- [4] Paginação CONFIÁVEL: ordenada por coluna única
SELECT nome FROM produtos ORDER BY nome LIMIT 3 OFFSET 3;

-- [5] Paginação FRÁGIL: 'categoria' repete, a ordem interna é
--     arbitraria — o mesmo produto pode cair em duas paginas
SELECT nome, categoria FROM produtos ORDER BY categoria LIMIT 3 OFFSET 3;

-- [6] A correção: desempate por uma coluna ÚNICA (a chave primária)
SELECT nome, categoria FROM produtos ORDER BY categoria, id LIMIT 3 OFFSET 3;

-- [7] DISTINCT: o NULL conta como UM valor (≠ do WHERE, onde
--     NULL = NULL é desconhecido — são perguntas diferentes)
SELECT DISTINCT cidade FROM clientes;

-- [8] ARMADILHA: DISTINCT age sobre a LINHA INTEIRA.
--     Cada nome é único -> 8 linhas, nada é eliminado.
SELECT DISTINCT cidade, nome FROM clientes;
