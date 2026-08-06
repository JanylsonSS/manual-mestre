#!/usr/bin/env bash
# Uma sessão de psql, cena a cena.
#
# O capítulo 05.02 é sobre a ferramenta que você vai usar todo dia. Este
# script roda as cenas de forma não interativa, para que a saída caiba no
# texto — mas o psql de verdade se usa interativo, e as meta-instruções
# (`\dt`, `\d`, `\x`) foram feitas para isso.
#
# Antes:  python codigo/laboratorio.py
#         export AURORA_URI="..."   (o script imprime)
#         export PATH="$(python codigo/laboratorio.py --bin):$PATH"
#
# Uso:    bash codigo/cap02/sessao.sh

set -u   # variável não definida é erro; NÃO usamos -e, porque várias
         # cenas dependem de um comando falhar

: "${AURORA_URI:?defina AURORA_URI — veja o cabeçalho deste arquivo}"
PASTA=$(mktemp -d)
trap 'rm -rf "$PASTA"' EXIT

titulo() { printf '\n[%s] %s\n' "$1" "$2"; }

titulo 1 "ONDE EU ESTOU"
psql "$AURORA_URI" -c '\conninfo'

titulo 2 "O CATÁLOGO, SEM ESCREVER SQL"
psql "$AURORA_URI" -c '\dt'
psql "$AURORA_URI" -c '\d produtos'

titulo 3 "A LINHA LARGA DEMAIS — \\x"
psql "$AURORA_URI" -c 'SELECT * FROM pedidos WHERE id = 1'
psql "$AURORA_URI" -x -c 'SELECT * FROM pedidos WHERE id = 1'

titulo 4 "QUANTO DEMOROU — \\timing"
psql "$AURORA_URI" -c '\timing on' -c 'SELECT count(*) FROM itens_pedido'

titulo 5 "SAÍDA PARA SCRIPT — -A -t"
echo "    padrão:"
psql "$AURORA_URI" -c 'SELECT count(*) FROM pedidos'
echo "    com -A -t (sem moldura, sem cabeçalho, sem rodapé):"
psql "$AURORA_URI" -A -t -c 'SELECT count(*) FROM pedidos'
echo "    e é isto que deixa o valor entrar numa variável do shell:"
TOTAL=$(psql "$AURORA_URI" -A -t -c 'SELECT count(*) FROM pedidos')
echo "    TOTAL=$TOTAL"

titulo 6 "O ERRO QUE PASSA DESPERCEBIDO — ON_ERROR_STOP"
cat > "$PASTA/migracao.sql" <<'SQL'
CREATE TABLE etapa_um (id integer);
INSERT INTO tabela_que_nao_existe VALUES (1);
CREATE TABLE etapa_tres (id integer);
SQL
echo "    sem ON_ERROR_STOP:"
psql "$AURORA_URI" -q -f "$PASTA/migracao.sql" > "$PASTA/saida" 2>&1
CODIGO=$?
sed 's/^/      /' "$PASTA/saida"
echo "      código de saída: $CODIGO"
psql "$AURORA_URI" -A -t -c \
  "SELECT string_agg(tablename, ', ') FROM pg_tables
   WHERE tablename LIKE 'etapa_%'" | sed 's/^/      criadas: /'

psql "$AURORA_URI" -q -c 'DROP TABLE IF EXISTS etapa_um, etapa_tres' >/dev/null
echo "    com ON_ERROR_STOP=1:"
psql "$AURORA_URI" -q -v ON_ERROR_STOP=1 -f "$PASTA/migracao.sql" \
  > "$PASTA/saida" 2>&1
CODIGO=$?
sed 's/^/      /' "$PASTA/saida"
echo "      código de saída: $CODIGO"
psql "$AURORA_URI" -A -t -c \
  "SELECT coalesce(string_agg(tablename, ', '), '(nenhuma)') FROM pg_tables
   WHERE tablename LIKE 'etapa_%'" | sed 's/^/      criadas: /'
psql "$AURORA_URI" -q -c 'DROP TABLE IF EXISTS etapa_um, etapa_tres' \
  >/dev/null 2>&1

titulo 7 "O SCRIPT INTEIRO OU NADA — -1"
psql "$AURORA_URI" -q -1 -v ON_ERROR_STOP=1 -f "$PASTA/migracao.sql" \
  > "$PASTA/saida" 2>&1
CODIGO=$?
sed 's/^/      /' "$PASTA/saida"
echo "      código de saída: $CODIGO"
psql "$AURORA_URI" -A -t -c \
  "SELECT coalesce(string_agg(tablename, ', '), '(nenhuma)') FROM pg_tables
   WHERE tablename LIKE 'etapa_%'" | sed 's/^/      criadas: /'

titulo 8 "TIRAR DADO DO BANCO — \\copy"
psql "$AURORA_URI" -c \
  "\\copy (SELECT id, nome, categoria, preco_centavos FROM produtos
           ORDER BY id) TO '$PASTA/produtos.csv' WITH CSV HEADER"
echo "    as três primeiras linhas do arquivo:"
head -3 "$PASTA/produtos.csv" | sed 's/^/      /'
echo "    e o mesmo comando com COPY (maiúsculo, sem a barra):"
psql "$AURORA_URI" -c \
  "COPY (SELECT id FROM produtos) TO '$PASTA/servidor.csv' WITH CSV" 2>&1 |
  sed 's/^/      /'
echo "    >>> funcionou porque estamos conectados como SUPERUSUÁRIO."
echo "        Agora um role comum, que é o caso do seu trabalho:"
psql "$AURORA_URI" -q -c "DROP ROLE IF EXISTS analista" >/dev/null 2>&1
psql "$AURORA_URI" -q -c "CREATE ROLE analista WITH LOGIN"
psql "$AURORA_URI" -q -c "GRANT SELECT ON ALL TABLES IN SCHEMA public
                          TO analista"
URI_ANALISTA=${AURORA_URI/postgres:@/analista@}
psql "$URI_ANALISTA" -c \
  "COPY (SELECT id FROM produtos) TO '$PASTA/proibido.csv' WITH CSV" 2>&1 |
  head -2 | sed 's/^/      COPY:   /'
psql "$URI_ANALISTA" -c \
  "\\copy (SELECT id FROM produtos) TO '$PASTA/permitido.csv' WITH CSV" 2>&1 |
  head -2 | sed 's/^/      \\copy:  /'
psql "$AURORA_URI" -q -c "REVOKE SELECT ON ALL TABLES IN SCHEMA public
                          FROM analista" >/dev/null 2>&1
psql "$AURORA_URI" -q -c "DROP ROLE IF EXISTS analista" >/dev/null 2>&1

titulo 9 "AUTOCOMMIT: O QUE O psql FAZ SEM PEDIR"
psql "$AURORA_URI" -q -c \
  "UPDATE produtos SET preco_centavos = preco_centavos WHERE id = 1"
echo "    o UPDATE acima já está gravado — o psql abre e fecha a transação"
psql "$AURORA_URI" -q <<'SQL'
BEGIN;
UPDATE produtos SET preco_centavos = 0 WHERE id = 1;
ROLLBACK;
SQL
psql "$AURORA_URI" -A -t -c \
  'SELECT preco_centavos FROM produtos WHERE id = 1' |
  sed 's/^/    preço depois do BEGIN..ROLLBACK: /'

titulo 10 "OS CÓDIGOS DE SAÍDA QUE UM SCRIPT PRECISA CONHECER"
echo 'SELECT * FROM nada;' > "$PASTA/ruim.sql"
psql "$AURORA_URI" -q -c 'SELECT 1' >/dev/null 2>&1
echo "    consulta boa ........................ $?"
psql "postgresql://ninguem@/nao_existe?host=/tmp" -c 'SELECT 1' >/dev/null 2>&1
echo "    servidor inalcançável ............... $?"
psql "$AURORA_URI" -q -c 'SELECT * FROM nada' >/dev/null 2>&1
echo "    SQL ruim com -c ..................... $?"
psql "$AURORA_URI" -q -f "$PASTA/ruim.sql" >/dev/null 2>&1
echo "    SQL ruim com -f, sem ON_ERROR_STOP .. $?"
psql "$AURORA_URI" -q -v ON_ERROR_STOP=1 -f "$PASTA/ruim.sql" >/dev/null 2>&1
echo "    SQL ruim com -f, com ON_ERROR_STOP .. $?"
