-- ------------------------------------------------------------
-- chaves_e_integridade.sql
-- Capítulo 03.02 — Tabelas, linhas e chaves
-- O que este arquivo demonstra: leitura de estrutura e as quatro
--   recusas do banco (FK, PK duplicada, NOT NULL, DELETE com filhos)
-- Como executar: python codigo/sql.py codigo/cap02/chaves_e_integridade.sql
--
-- ATENÇÃO: os comandos 4 a 7 FALHAM de propósito. O erro é o resultado
-- esperado — leia a mensagem, ela diz qual regra foi violada e onde.
-- O executor para no primeiro erro; rode cada um separadamente para
-- ver os quatro:
--   python codigo/sql.py "INSERT INTO pedidos VALUES (99, 999, '2026-08-01', 'concluido')"
-- ------------------------------------------------------------

-- [1] Que tabelas existem neste banco?
SELECT name FROM sqlite_master WHERE type = 'table' ORDER BY name;

-- [2] Como a tabela pedidos é feita? (pk=1 marca a chave primária)
SELECT name, type, "notnull", pk FROM pragma_table_info('pedidos');

-- [3] Para onde as chaves estrangeiras de itens_pedido apontam?
SELECT "table" AS tabela_destino, "from" AS coluna_origem, "to" AS coluna_destino
FROM pragma_foreign_key_list('itens_pedido');

-- [4] FALHA: cliente 999 não existe
--     -> FOREIGN KEY constraint failed
INSERT INTO pedidos VALUES (99, 999, '2026-08-01', 'concluido');

-- [5] FALHA: o id 1 já é da Fernanda
--     -> UNIQUE constraint failed: clientes.id
INSERT INTO clientes VALUES (1, 'Outro', 'x@x.com', 'campinas', '2026-01-01');

-- [6] FALHA: nome é NOT NULL
--     -> NOT NULL constraint failed: clientes.nome
INSERT INTO clientes VALUES (99, NULL, 'x@x.com', 'campinas', '2026-01-01');

-- [7] FALHA: a Fernanda tem 5 pedidos apontando para ela
--     -> FOREIGN KEY constraint failed
DELETE FROM clientes WHERE id = 1;
