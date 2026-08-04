-- ------------------------------------------------------------
-- restricoes.sql
-- Capítulo 03.13 — Constraints e integridade
-- O que este arquivo demonstra: as cinco restrições, os buracos
--   que o NULL abre em duas delas, e as ações de chave estrangeira
-- Como executar:
--   python codigo/cap12/preparar_ddl.py
--   AURORA_BANCO=dados/ddl.db python codigo/sql.py \
--       codigo/cap13/restricoes.sql
-- ------------------------------------------------------------

DROP TABLE IF EXISTS filho_casc;
DROP TABLE IF EXISTS filho_null;
DROP TABLE IF EXISTS filho_rest;
DROP TABLE IF EXISTS filho_bug;
DROP TABLE IF EXISTS pai;
DROP TABLE IF EXISTS assinaturas;
DROP TABLE IF EXISTS avaliacoes;
DROP TABLE IF EXISTS chave_texto;

-- [1] UNIQUE promete "não se repete". Veja o que ele deixa passar.
CREATE TABLE assinaturas (
    id    INTEGER PRIMARY KEY,
    email TEXT UNIQUE
);

INSERT INTO assinaturas (email) VALUES ('ana@aurora.com'), (NULL), (NULL), (NULL);

-- [2] QUATRO linhas. Três NULLs numa coluna UNIQUE, sem reclamação:
--     NULL nunca é IGUAL a NULL, então nunca é DUPLICADO (03.03).
SELECT COUNT(*) AS linhas, COUNT(email) AS emails_preenchidos
FROM assinaturas;

-- [3] Com valor de verdade, aí sim o UNIQUE age. Comando comentado
--     porque falharia no meio; rode à mão para ver:
--     INSERT INTO assinaturas (email) VALUES ('ana@aurora.com');
--     -> Erro de SQL: UNIQUE constraint failed: assinaturas.email

-- [4] CHECK: a restrição que valida FAIXA e CONJUNTO — o que
--     STRICT (03.12) não faz.
CREATE TABLE avaliacoes (
    id     INTEGER PRIMARY KEY,
    nota   INTEGER NOT NULL CHECK (nota BETWEEN 1 AND 5),
    status TEXT             CHECK (status IN ('publicada', 'oculta'))
) STRICT;

-- [5] O MESMO buraco do UNIQUE, agora no CHECK: status NULL passa.
--     A condição NULL IN (...) é DESCONHECIDA, e o CHECK só recusa
--     o que é comprovadamente FALSO.
INSERT INTO avaliacoes VALUES (1, 5, NULL);
SELECT id, nota, status FROM avaliacoes;

-- [6] Os dois que o CHECK pega. Comentados pelo mesmo motivo de [3]:
--     INSERT INTO avaliacoes VALUES (2, 47, 'publicada');
--     -> Erro de SQL: CHECK constraint failed: nota BETWEEN 1 AND 5
--     INSERT INTO avaliacoes VALUES (3, 5, 'rascunho');
--     -> Erro de SQL: CHECK constraint failed: status IN (...)

-- [7] A chave primária de TEXTO aceita NULL — um furo histórico do
--     SQLite. Com STRICT, ou com NOT NULL explícito, ele fecha.
CREATE TABLE chave_texto (id TEXT PRIMARY KEY, x TEXT);
INSERT INTO chave_texto VALUES (NULL, 'chave primaria nula');
SELECT id, x FROM chave_texto;

-- [8] As três ações de ON DELETE, lado a lado.
CREATE TABLE pai (id INTEGER PRIMARY KEY, nome TEXT NOT NULL);

CREATE TABLE filho_casc (
    id     INTEGER PRIMARY KEY,
    pai_id INTEGER REFERENCES pai(id) ON DELETE CASCADE
);
CREATE TABLE filho_null (
    id     INTEGER PRIMARY KEY,
    pai_id INTEGER REFERENCES pai(id) ON DELETE SET NULL
);
CREATE TABLE filho_rest (
    id     INTEGER PRIMARY KEY,
    pai_id INTEGER REFERENCES pai(id) ON DELETE RESTRICT
);

INSERT INTO pai VALUES (1, 'a'), (2, 'b'), (3, 'c');
INSERT INTO filho_casc VALUES (10, 1);
INSERT INTO filho_null VALUES (20, 2);
INSERT INTO filho_rest VALUES (30, 3);

-- [9] CASCADE: apagar o pai APAGA o filho junto.
DELETE FROM pai WHERE id = 1;
SELECT COUNT(*) AS filhos_cascade_restantes FROM filho_casc;

-- [10] SET NULL: o filho sobrevive, órfão e declarado como tal.
DELETE FROM pai WHERE id = 2;
SELECT id, pai_id FROM filho_null;

-- [11] RESTRICT: o pai não vai a lugar nenhum. Comentado:
--      DELETE FROM pai WHERE id = 3;
--      -> Erro de SQL: FOREIGN KEY constraint failed

-- [12] A CONTRADIÇÃO QUE SÓ APARECE NO DELETE: SET NULL numa
--      coluna NOT NULL. A tabela é criada, o INSERT funciona, e
--      a bomba só estoura quando alguém apaga o pai — o que pode
--      levar anos. Esta é a última cena: FALHA de propósito.
CREATE TABLE filho_bug (
    id     INTEGER PRIMARY KEY,
    pai_id INTEGER NOT NULL REFERENCES pai(id) ON DELETE SET NULL
);
INSERT INTO pai VALUES (4, 'd');
INSERT INTO filho_bug VALUES (40, 4);
DELETE FROM pai WHERE id = 4;
