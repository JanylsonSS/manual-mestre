-- ------------------------------------------------------------
-- schema.sql
-- Capítulo 03.16 — Modelagem e mini projeto
-- O schema da Aurora reconstruído do zero, com TUDO que o módulo
--   ensinou do 03.12 ao 03.15. Cada linha é uma decisão.
-- Como executar:
--   python codigo/cap16/criar_aurora_v2.py
-- ------------------------------------------------------------

-- Ordem de remoção: FILHO antes de PAI (03.13 §10).
-- A ordem de criação, mais abaixo, é a inversa.
DROP TABLE IF EXISTS itens_pedido;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS categorias;

-- ------------------------------------------------------------
-- categorias — tabela NOVA em relação ao schema do 03.01.
-- Por quê: no original, 'categoria' era texto solto em produtos.
-- Texto solto aceita 'audio', 'Audio' e 'áudio' como três coisas
-- diferentes, e um GROUP BY devolve três linhas (03.06).
-- ------------------------------------------------------------
CREATE TABLE categorias (
    id    INTEGER PRIMARY KEY,
    nome  TEXT NOT NULL UNIQUE COLLATE NOCASE   -- NOCASE: 03.13/A2.6
) STRICT;

-- ------------------------------------------------------------
-- clientes
-- ------------------------------------------------------------
CREATE TABLE clientes (
    id             INTEGER PRIMARY KEY,
    nome           TEXT NOT NULL CHECK (LENGTH(TRIM(nome)) > 0),
    -- UNIQUE sem NOT NULL: e-mail é opcional no cadastro de balcão,
    -- e vários NULL convivem numa coluna única (03.13 §6.2).
    -- A decisão está documentada no relatório, não é esquecimento.
    email          TEXT UNIQUE COLLATE NOCASE,
    cidade         TEXT,
    -- Data em TEXT ISO: ordem alfabética = ordem cronológica (03.12).
    data_cadastro  TEXT NOT NULL CHECK (data_cadastro LIKE '____-__-__')
) STRICT;

-- ------------------------------------------------------------
-- produtos
-- ------------------------------------------------------------
CREATE TABLE produtos (
    id              INTEGER PRIMARY KEY,
    nome            TEXT    NOT NULL CHECK (LENGTH(TRIM(nome)) > 0),
    categoria_id    INTEGER NOT NULL,
    -- Dinheiro em centavos INTEIROS: 0.1 + 0.2 <> 0.3 (03.12 §6.5).
    -- O sufixo no nome diz a unidade e evita a soma errada.
    preco_centavos  INTEGER NOT NULL CHECK (preco_centavos > 0),
    -- Booleano é INTEGER 0/1; DEFAULT 1 = nasce à venda.
    ativo           INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    -- RESTRICT: apagar uma categoria com produtos é recusado (03.13).
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE RESTRICT
) STRICT;

-- ------------------------------------------------------------
-- pedidos
-- ------------------------------------------------------------
CREATE TABLE pedidos (
    id          INTEGER PRIMARY KEY,
    cliente_id  INTEGER NOT NULL,
    data        TEXT    NOT NULL CHECK (data LIKE '____-__-__'),
    -- CHECK de conjunto fechado + NOT NULL: sem os dois, NULL passa
    -- e a coluna aceita um quarto estado não previsto (03.13 §6.4).
    status      TEXT    NOT NULL
                CHECK (status IN ('pendente', 'concluido', 'cancelado')),
    -- RESTRICT: histórico financeiro não some com um cadastro.
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT
) STRICT;

-- ------------------------------------------------------------
-- itens_pedido
-- ------------------------------------------------------------
CREATE TABLE itens_pedido (
    id                      INTEGER PRIMARY KEY,
    pedido_id               INTEGER NOT NULL,
    produto_id              INTEGER NOT NULL,
    quantidade              INTEGER NOT NULL CHECK (quantidade > 0),
    -- Preço COPIADO no momento da venda: se o produto subir amanhã,
    -- o pedido de hoje continua valendo o que valeu hoje (03.02).
    preco_unitario_centavos INTEGER NOT NULL CHECK (preco_unitario_centavos > 0),
    -- CASCADE aqui, e só aqui: o item não existe sem o pedido.
    FOREIGN KEY (pedido_id)  REFERENCES pedidos(id)  ON DELETE CASCADE,
    -- RESTRICT no produto: apagar produto vendido destruiria histórico.
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE RESTRICT,
    -- O mesmo produto duas vezes no mesmo pedido é erro de negócio.
    -- Regra que NÃO cabe numa coluna só (03.13/AP1).
    UNIQUE (pedido_id, produto_id)
) STRICT;

-- ------------------------------------------------------------
-- ÍNDICES (03.14) — só os que uma consulta real justifica.
-- Não há índice em 'status' nem em 'ativo': poucos valores
-- distintos, ganho medido próximo de zero e custo permanente.
-- ------------------------------------------------------------

-- Coluna de chave estrangeira do lado FILHO. O SQLite não a indexa
-- sozinho, e sem ela o ON DELETE CASCADE varre a tabela inteira a
-- cada DELETE de pedido (03.13 §13).
CREATE INDEX idx_itens_pedido ON itens_pedido(pedido_id);

-- Idem, e serve ao painel "pedidos de um cliente".
CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id, data);

-- Filtro frequente do catálogo por categoria.
CREATE INDEX idx_produtos_categoria ON produtos(categoria_id);
