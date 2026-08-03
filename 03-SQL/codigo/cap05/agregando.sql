-- ------------------------------------------------------------
-- agregando.sql
-- Capítulo 03.05 — Funções de agregação
-- O que este arquivo demonstra: as cinco funções, o efeito do NULL
--   em cada uma, a armadilha do conjunto vazio e o faturamento real
-- Como executar: python codigo/sql.py codigo/cap05/agregando.sql
-- ------------------------------------------------------------

-- [1] As cinco de uma vez: 12 produtos viram UMA linha
SELECT COUNT(*)            AS qtd,
       SUM(preco_centavos) AS soma,
       AVG(preco_centavos) AS media,
       MIN(preco_centavos) AS minimo,
       MAX(preco_centavos) AS maximo
FROM produtos;

-- [2] As contagens que DISCORDAM — e todas estão certas
--     COUNT(*) conta LINHAS; COUNT(col) conta VALORES não nulos
SELECT COUNT(*)               AS linhas,      -- 8
       COUNT(cidade)          AS com_cidade,  -- 7 (Helena não tem)
       COUNT(email)           AS com_email,   -- 7 (Beatriz não tem)
       COUNT(DISTINCT cidade) AS cidades      -- 3 (o NULL não conta)
FROM clientes;

-- [3] A ferramenta que sai daí: contar nulos numa tacada
SELECT COUNT(*) - COUNT(cidade) AS cidades_nulas FROM clientes;

-- [4] A média muda de DENOMINADOR conforme o NULL
--     AVG divide por 7 (não nulos); a forma manual divide por 8
SELECT AVG(LENGTH(cidade))                  AS media_real,
       SUM(LENGTH(cidade)) * 1.0 / COUNT(*) AS media_forcada
FROM clientes;

-- [5] ARMADILHA: conjunto vazio -> COUNT devolve 0, SUM devolve NULL
SELECT SUM(preco_centavos) AS soma, COUNT(*) AS qtd
FROM produtos WHERE categoria = 'inexistente';

-- [6] A correção: COALESCE é o "get com padrão" do 01.15, em SQL
SELECT COALESCE(SUM(preco_centavos), 0) AS soma_segura
FROM produtos WHERE categoria = 'inexistente';

-- [7] Agregar EXPRESSÃO: multiplica linha a linha, soma depois.
--     Divide por 100 só no FIM — exatidão em centavos (01.04)
SELECT SUM(quantidade * preco_unitario_centavos) / 100.0 AS total_geral_reais
FROM itens_pedido;

-- [8] O faturamento real: o WHERE age ANTES de agregar.
--     COUNT(DISTINCT p.id) porque a junção repete o pedido por item
SELECT COUNT(DISTINCT p.id)                                AS pedidos,
       SUM(i.quantidade * i.preco_unitario_centavos)/100.0 AS faturamento_reais
FROM pedidos p
JOIN itens_pedido i ON i.pedido_id = p.id
WHERE p.status = 'concluido';
