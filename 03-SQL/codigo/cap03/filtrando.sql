-- ------------------------------------------------------------
-- filtrando.sql
-- Capítulo 03.03 — SELECT e WHERE
-- O que este arquivo demonstra: os operadores de filtro, o LIKE,
--   a precedência de AND/OR e as duas armadilhas do NULL
-- Como executar: python codigo/sql.py codigo/cap03/filtrando.sql
-- ------------------------------------------------------------

-- [1] Projeção: escolher colunas (evite SELECT * em produção)
SELECT nome, cidade FROM clientes WHERE cidade = 'campinas';

-- [2] Faixa: BETWEEN é inclusivo nas DUAS pontas (≠ range do 01.11)
--     R$ 100,00 a R$ 300,00 — em centavos, a disciplina do 01.04
SELECT nome, preco_centavos FROM produtos
WHERE preco_centavos BETWEEN 10000 AND 30000;

-- [3] Lista: IN é o OR encadeado, legível a partir de dois valores
SELECT nome, categoria FROM produtos
WHERE categoria IN ('audio', 'video');

-- [4] Texto: % = qualquer sequência · _ = exatamente um caractere
SELECT nome FROM produtos WHERE nome LIKE '%Sem Fio%';

-- [5] No SQLite, LIKE ignora maiúsculas em ASCII (dialeto!)
--     Mas NÃO ignora acento: 'mecânico' não acha 'Mecanico'
SELECT nome FROM produtos WHERE nome LIKE '%sem fio%';

-- [6] ARMADILHA 1: comparar com NULL nunca é verdadeiro
--     -> 0 linhas, SEM erro. A Beatriz existe e não aparece.
SELECT nome FROM clientes WHERE email = NULL;

-- [7] A forma correta
SELECT nome FROM clientes WHERE email IS NULL;

-- [8] ARMADILHA 2: negação EXCLUI os NULL
--     -> 4 linhas. A Helena (cidade NULL) sumiu.
SELECT nome, cidade FROM clientes WHERE cidade <> 'campinas';

-- [9] A correção: dizer explicitamente o que fazer com o desconhecido
SELECT nome, cidade FROM clientes
WHERE cidade <> 'campinas' OR cidade IS NULL;

-- [10] Precedência: AND antes de OR. Sem parênteses, lê-se
--      "campinas OU (santos E deste ano)" -> 3 linhas, duas de 2025
SELECT nome, cidade, data_cadastro FROM clientes
WHERE cidade = 'campinas' OR cidade = 'santos'
  AND data_cadastro >= '2026-01-01';

-- [11] Com parênteses: a intenção real -> 1 linha
SELECT nome, cidade, data_cadastro FROM clientes
WHERE (cidade = 'campinas' OR cidade = 'santos')
  AND data_cadastro >= '2026-01-01';
