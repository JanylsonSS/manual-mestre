-- ------------------------------------------------------------
-- tipos.sql
-- Capítulo 03.12 — DDL e tipos de dados
-- O que este arquivo demonstra: afinidade de tipos, o que o
--   SQLite aceita calado, e como STRICT devolve o rigor
-- Como executar (cria um banco novo, descartável):
--   python codigo/cap12/preparar_ddl.py
--   AURORA_BANCO=dados/ddl.db python codigo/sql.py \
--       codigo/cap12/tipos.sql
-- ------------------------------------------------------------

-- [0] O próprio arquivo aplica a lição da §6.7: com DROP IF EXISTS
--     no topo, ele é REEXECUTÁVEL. Sem isto, a segunda execução
--     morreria em "table teste_tipos already exists".
DROP TABLE IF EXISTS teste_tipos;
DROP TABLE IF EXISTS inventado;
DROP TABLE IF EXISTS rigorosa;
DROP TABLE IF EXISTS dec;
DROP TABLE IF EXISTS decimais;

-- [1] Uma tabela declarada com os três tipos principais.
CREATE TABLE teste_tipos (
    a INTEGER,
    b TEXT,
    c REAL
);

-- [2] Agora o teste: valores do tipo ERRADO em cada coluna.
--     Nenhum erro. O SQLite guarda o que recebeu.
INSERT INTO teste_tipos VALUES ('abacaxi', 42, 'x');

-- [3] typeof() revela o que foi REALMENTE gravado, célula a
--     célula. O tipo da coluna era uma preferência, não uma lei.
SELECT a, typeof(a) AS tipo_a,
       b, typeof(b) AS tipo_b,
       c, typeof(c) AS tipo_c
FROM teste_tipos;

-- [4] Mas a preferência age quando o valor é CONVERSÍVEL:
--     o texto '42' vira o inteiro 42 na coluna INTEGER.
INSERT INTO teste_tipos VALUES ('42', '42', '3.5');

SELECT a, typeof(a) AS tipo_a,
       b, typeof(b) AS tipo_b,
       c, typeof(c) AS tipo_c
FROM teste_tipos;

-- [5] O limite da permissividade: um tipo INVENTADO é aceito,
--     e o (3) do VARCHAR(3) não limita coisa alguma.
CREATE TABLE inventado (x BANANA, y VARCHAR(3));
INSERT INTO inventado VALUES (1, 'texto muito maior que tres');
SELECT x, typeof(x) AS tipo_x, LENGTH(y) AS tamanho FROM inventado;

-- [6] STRICT (SQLite 3.37+) devolve o rigor. A tabela é criada
--     normalmente; a diferença aparece na hora de gravar.
CREATE TABLE rigorosa (a INTEGER NOT NULL, b TEXT NOT NULL) STRICT;

-- [7] E STRICT também recusa tipo inventado — compare com [5],
--     onde BANANA passou. Este comando FALHA de propósito;
--     está comentado para o arquivo seguir até o fim. Rode à mão:
--     CREATE TABLE ruim (x BANANA) STRICT;
--     -> Erro de SQL: unknown datatype for ruim.x: "BANANA"

-- [7] Dinheiro: por que centavos inteiros, e não REAL.
--     A terceira coluna responde por que 0.1+0.2 nao "é" 0.3.
SELECT 0.1 + 0.2   AS soma_real,
       10 + 20     AS soma_inteira,
       0.1 + 0.2 = 0.3 AS sao_iguais;

-- [8] NUMERIC(10,2) é aceito, e a precisão declarada é IGNORADA:
--     19.999 entra inteiro. A declaração não protege nada.
CREATE TABLE dec (v NUMERIC(10,2));
INSERT INTO dec VALUES (19.999);
SELECT v, typeof(v) AS tipo FROM dec;

-- [9] Datas e booleanos não têm tipo próprio no SQLite.
--     Data é TEXTO no formato ISO; booleano é INTEGER 0/1.
SELECT date('now')          AS hoje,
       typeof(date('now'))  AS tipo_data,
       (1 = 1)              AS verdadeiro,
       typeof(1 = 1)        AS tipo_bool;

-- [10] ALTER TABLE: o que existe no SQLite.
ALTER TABLE teste_tipos ADD COLUMN d TEXT DEFAULT 'novo';
SELECT * FROM teste_tipos;

ALTER TABLE dec RENAME TO decimais;
ALTER TABLE decimais RENAME COLUMN v TO valor;
SELECT sql FROM sqlite_master WHERE name = 'decimais';

-- [11] IF NOT EXISTS / IF EXISTS tornam o script REEXECUTÁVEL.
CREATE TABLE IF NOT EXISTS decimais (valor TEXT);
DROP TABLE IF EXISTS inexistente;

-- [12] O que NÃO existe no SQLite: mudar o tipo de uma coluna.
--      "ALTER TABLE t ALTER COLUMN a TEXT" devolve
--      'near "ALTER": syntax error'. Não é falta de suporte a uma
--      sintaxe: é a operação inteira que não existe aqui. O
--      caminho é criar a tabela nova, copiar, apagar, renomear.

-- [13] A ÚLTIMA CENA: gravar texto numa coluna INTEGER de uma
--      tabela STRICT. Comparado com [2], que passou calado.
--      Este comando FALHA de propósito — é o fim do arquivo,
--      porque o executor para no primeiro erro.
INSERT INTO rigorosa VALUES ('abacaxi', 'ok');
