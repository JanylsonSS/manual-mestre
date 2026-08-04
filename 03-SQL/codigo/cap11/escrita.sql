-- ------------------------------------------------------------
-- escrita.sql
-- Capítulo 03.11 — INSERT, UPDATE, DELETE
-- O que este arquivo demonstra: as três formas de escrita, o
--   WHERE que salva empregos, e a rede de segurança da transação
-- Como executar (NUNCA no banco bom — veja o cabeçalho abaixo):
--   python codigo/cap11/preparar_rascunho.py
--   AURORA_BANCO=dados/rascunho.db python codigo/sql.py \
--       codigo/cap11/escrita.sql
-- ------------------------------------------------------------

-- [1] INSERT com colunas NOMEADAS. Sem a lista de colunas, a ordem
--     dos VALUES vira contrato invisível — quebra ao alterar a tabela.
INSERT INTO clientes (nome, email, cidade, data_cadastro)
VALUES ('Otavio Ramos', 'otavio@exemplo.com', 'jundiai', '2026-08-04');

-- [2] INSERT de várias linhas: um comando, três linhas.
--     Note a terceira: email NULL é permitido, cidade também.
INSERT INTO clientes (nome, email, cidade, data_cadastro) VALUES
    ('Priscila Nunes', 'priscila@exemplo.com', 'campinas', '2026-08-04'),
    ('Tadeu Moraes',   'tadeu@exemplo.com',    'santos',   '2026-08-04'),
    ('Vera Lucia',     NULL,                    NULL,      '2026-08-04');

-- [3] O que a coluna DEFAULT faz: produtos.ativo tem DEFAULT 1.
--     Omitir a coluna não é o mesmo que passar NULL nela.
INSERT INTO produtos (nome, categoria, preco_centavos)
VALUES ('Suporte de Monitor', 'acessorios', 18900);

SELECT id, nome, ativo FROM produtos WHERE nome = 'Suporte de Monitor';

-- [4] O SELECT DE ENSAIO. Antes de qualquer UPDATE, rode o WHERE
--     como SELECT. É a diferença entre 1 linha e a tabela inteira.
SELECT id, nome, preco_centavos
FROM produtos
WHERE categoria = 'acessorios' AND ativo = 1;

-- [5] O UPDATE com o MESMO WHERE do ensaio. Reajuste de 10%.
UPDATE produtos
SET preco_centavos = CAST(preco_centavos * 1.10 AS INTEGER)
WHERE categoria = 'acessorios' AND ativo = 1;

-- [6] A CONFERÊNCIA depois da escrita: o número de linhas afetadas
--     tem que bater com o número de linhas do ensaio.
SELECT COUNT(*) AS acessorios_ativos
FROM produtos
WHERE categoria = 'acessorios' AND ativo = 1;

-- [7] UPDATE com subconsulta: desativa produtos que nunca venderam.
--     NOT EXISTS, não NOT IN — a lição do 03.09 vale na escrita.
UPDATE produtos
SET ativo = 0
WHERE NOT EXISTS (
    SELECT 1 FROM itens_pedido i WHERE i.produto_id = produtos.id
);

SELECT id, nome FROM produtos WHERE ativo = 0;

-- [8] DELETE com WHERE. Remove só os clientes de teste criados aqui.
DELETE FROM clientes WHERE data_cadastro = '2026-08-04';

-- [9] A REDE DE SEGURANÇA: transação explícita (03.15).
--     BEGIN abre, ROLLBACK desfaz TUDO desde o BEGIN.
BEGIN;
UPDATE produtos SET preco_centavos = 1;      -- o desastre
SELECT COUNT(*) AS a_um_centavo FROM produtos WHERE preco_centavos = 1;
ROLLBACK;

-- [10] Depois do ROLLBACK, o desastre não aconteceu.
SELECT COUNT(*) AS a_um_centavo FROM produtos WHERE preco_centavos = 1;

-- [11] A INTEGRIDADE REFERENCIAL SEGURA A MÃO. Apagar um cliente que
--      tem pedidos é RECUSADO: a chave estrangeira (03.13) protege.
--      Este comando FALHA de propósito, e é o último do arquivo:
--      o executor para no primeiro erro, e essa é a última cena.
DELETE FROM clientes WHERE id = 1;
