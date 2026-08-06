# Gabarito — Capítulo 05.02: `psql` e ferramentas gráficas

Leia depois de tentar. Enunciados em [`../cap02.md`](../cap02.md).

> Toda saída abaixo é execução real, contra o laboratório do módulo, PostgreSQL 16.2.

## A1 — Cliente ou servidor?

| # | Item | Onde executa |
|---|---|---|
| 1 | `SELECT count(*)` | **servidor** |
| 2 | `\dt` | **os dois** — o `psql` traduz, o servidor responde |
| 3 | `\timing on` | **só o psql** |
| 4 | `\copy ... TO 'p.csv'` | **os dois** — servidor lê, `psql` grava no seu disco |
| 5 | `COPY ... TO '/tmp/p.csv'` | **só o servidor** — inclusive a gravação |
| 6 | `\x auto` | **só o psql** |
| 7 | `\d produtos` | **os dois** |
| 8 | `\i migracao.sql` | **os dois** — o `psql` lê o arquivo do **seu** disco |

**O 8 é o que engana com mais frequência.** `\i` abre o arquivo na sua máquina e manda o conteúdo linha a linha. Um caminho que existe no servidor e não na sua máquina falha, e a mensagem fala de arquivo — o que faz muita gente procurar no lugar errado.

**E o par 4/5 é o ponto do capítulo.** Os dois "gravam um CSV". Em máquinas diferentes.

## A2 — Preveja o código de saída

| # | Comando | Código |
|---|---|---|
| 1 | `-c 'SELECT 1'` | **0** |
| 2 | `-c 'SELECT * FROM inexistente'` | **1** |
| 3 | `-f ruim.sql` | **0** |
| 4 | `-v ON_ERROR_STOP=1 -f ruim.sql` | **3** |
| 5 | servidor inalcançável | **2** |
| 6 | `-c 'SELECT 1' \| grep nada` | **1** |

Medidos:

```
consulta boa ........................ 0
servidor inalcançável ............... 2
SQL ruim com -c ..................... 1
SQL ruim com -f, sem ON_ERROR_STOP .. 0
SQL ruim com -f, com ON_ERROR_STOP .. 3
```

**O contraste 2/3 é a resposta que o exercício quer.** O mesmo erro de SQL devolve 1 com `-c` e **0** com `-f`. Não é inconsistência: com `-f`, o `psql` se comporta como uma sessão interativa, e "cheguei ao fim do arquivo" é sucesso.

**E o 6 é uma armadilha de shell, não de `psql`:**

```
  saida do cano: 1
```

O 1 é do `grep`, que não encontrou nada. O `psql` devolveu 0 e ninguém ficou sabendo. É o mesmo defeito do A3.4, e o mesmo que apareceu na primeira versão do script do capítulo (§10).

## A3 — Ache o erro

**1. `-f` sem proteção.** Erro no meio passa e o script devolve 0. Correção: `-1 -v ON_ERROR_STOP=1`.

**2. Senha na linha de comando.** Qualquer usuário da máquina lê com `ps aux`. Correção: `~/.pgpass` com permissão `0600`, ou `PGPASSWORD`. **E há um segundo defeito:** um `DELETE FROM pedidos` sem `WHERE` contra um host chamado `prod`, sem `\conninfo` antes e sem `BEGIN`.

**3. Falta `-A -t`.** O que entra na variável é a tabela desenhada:

```
  TOTAL=[ count
-------
    20
(1 row)]
```

E o teste seguinte quebra:

```
bash: line 10: [:  count
-------
```

Correção: `psql "$URI" -A -t -c '...'`.

**4. `$?` depois de um cano.** Lê o código do `tee`, que é 0. Correção: `${PIPESTATUS[0]}`, ou redirecionar para arquivo e ler `$?` na linha seguinte.

**5. `COPY` maiúsculo para um caminho do seu `/home`.** Ele grava no servidor. Se o servidor for remoto, o arquivo aparece lá — e se você for um role comum, nem isso:

```
ERROR:  permission denied to COPY to a file
DETAIL:  Only roles with privileges of the "pg_write_server_files" role
         may COPY to a file.
```

Correção: `\copy`.

**6. Este está quase certo, e falta `-1`.** Com `ON_ERROR_STOP` ele para no erro e sinaliza — mas as tabelas criadas antes do erro **ficam**:

```
com ON_ERROR_STOP=1:
  código de saída: 3
  criadas: etapa_um
```

Com `-1`:

```
  código de saída: 3
  criadas: (nenhuma)
```

## A4 — Terminal ou interface gráfica?

| # | Situação | Resposta |
|---|---|---|
| 1 | Migração por agendador | **terminal** — nenhum agendador clica |
| 2 | Banco herdado com 80 tabelas | **gráfica** — o diagrama de relações compensa |
| 3 | Conferir linha dentro de contêiner | **terminal** — não há outra coisa lá |
| 4 | Consulta com seis `JOIN` | **gráfica** para montar, terminal para rodar |
| 5 | Exportar 4 milhões de linhas | **terminal** — `\copy`, sem carregar tudo em memória |
| 6 | Mostrar plano para quem não lê `EXPLAIN` | **gráfica** |

**O 5 é o que muita gente erra.** A interface gráfica traz o resultado para a memória antes de exportar, e 4 milhões de linhas derrubam a ferramenta ou a máquina. `\copy` transmite em fluxo e não guarda nada.

**E o 4 admite as duas**, o que é uma resposta legítima: montar visualmente e depois colar no terminal é fluxo comum de quem trabalha com bancos grandes.

## AP1 — Seu `.psqlrc`

```
\set QUIET 1
\x auto
\timing on
\pset null '(null)'
\set ON_ERROR_ROLLBACK interactive
\set HISTSIZE 5000
\unset QUIET
```

**Linha a linha:** `QUIET` cala as confirmações durante a leitura do arquivo; `\x auto` transpõe só quando a linha não cabe; `\timing` mede sem você pedir; `\pset null` distingue `NULL` de string vazia — e a diferença aparece na hora:

```
 email
--------
 (null)
(1 row)
```

`ON_ERROR_ROLLBACK interactive` cria um `SAVEPOINT` invisível por comando, para que um erro de digitação no meio de uma transação longa não derrube a transação inteira. O `interactive` limita isso à sessão interativa, sem afetar scripts.

**A pergunta que fecha, e ela tem duas partes.**

O `\timing on` polui a saída de qualquer script que use `-A -t`:

```
Timing is on.
20
Time: 0.727 ms
```

Três linhas onde o script esperava uma. E a correção intuitiva **não resolve**:

```
\set QUIET 1
\timing on
```

```
20
Time: 0.888 ms
```

`QUIET` calou o "Timing is on." e não calou o "Time:". **A correção certa é o script não ler o `.psqlrc`:**

```bash
psql -X "$AURORA_URI" -A -t -c 'SELECT count(*) FROM pedidos'
```

```
20
```

**Regra: `-X` em todo `psql` dentro de script.** O `.psqlrc` é do seu terminal, e um script que depende do arquivo de configuração pessoal de quem o roda vai se comportar diferente em cada máquina.

## AP2 — Exportador que funciona para todo mundo

```bash
#!/usr/bin/env bash
set -uo pipefail

PERMITIDAS="clientes produtos pedidos itens_pedido"
TABELA=${1:?uso: exportar.sh <tabela>}

case " $PERMITIDAS " in
  *" $TABELA "*) ;;
  *) echo "tabela não permitida: $TABELA" >&2; exit 64 ;;
esac

EXISTE=$(psql -X "$AURORA_URI" -A -t \
  -c "SELECT to_regclass('$TABELA') IS NOT NULL")
[ "$EXISTE" = "t" ] || { echo "tabela não existe: $TABELA" >&2; exit 65; }

psql -X "$AURORA_URI" -v ON_ERROR_STOP=1 \
  -c "\\copy $TABELA TO '$TABELA.csv' WITH CSV HEADER"
```

**Três decisões merecem defesa.**

A **lista branca antes da consulta**: `$TABELA` entra numa string SQL, e sem a lista isso é injection pela via do shell. A conferência de existência com `to_regclass` vem **depois** da lista, e não no lugar dela.

```
=== to_regclass de tabela inexistente ===
t
```

O **`\copy` e não `COPY`**: o requisito era funcionar sem superusuário. Provado com um role comum:

```
COPY:   ERROR:  permission denied to COPY to a file
\copy:  COPY 12
```

O **`-X`**: pelo motivo do AP1.

Os códigos 64 e 65 vêm do `sysexits.h` (`EX_USAGE` e `EX_DATAERR`) e distinguem "você pediu errado" de "o banco não tem isso" — informação que um agendador consegue usar.

## AP3 — A migração segura

As três execuções, medidas:

| Forma | Código | Objetos depois |
|---|---|---|
| sem proteção | **0** | `etapa_tres, etapa_um` |
| `ON_ERROR_STOP=1` | **3** | `etapa_um` |
| `-1 -v ON_ERROR_STOP=1` | **3** | `(nenhuma)` |

**A pergunta que separa: quando a segunda forma é pior que a primeira?**

Quando o arquivo contém um comando que **não pode rodar dentro de uma transação**, e por isso a terceira forma está indisponível. Os casos reais no PostgreSQL:

- `CREATE INDEX CONCURRENTLY` — existe justamente para não travar a tabela, e recusa transação explícita.
- `VACUUM`.
- `CREATE DATABASE` e `DROP DATABASE`.
- `ALTER TYPE ... ADD VALUE` em versões anteriores à 12.

Nesses arquivos, `-1` devolve `ERROR: CREATE INDEX CONCURRENTLY cannot run inside a transaction block`, e você fica com a segunda forma — com a obrigação de escrever cada comando de modo que rodar duas vezes não quebre (`IF NOT EXISTS`, `ON CONFLICT DO NOTHING`).

**A resposta boa não é "use sempre `-1`".** É: use `-1` quando puder, e quando não puder, torne cada comando repetível.

## D1 — O aplicador de migrações

O esqueleto:

```bash
psql -X "$URI" -v ON_ERROR_STOP=1 -c "
  CREATE TABLE IF NOT EXISTS schema_migrations (
      versao      text PRIMARY KEY,
      aplicada_em timestamptz NOT NULL DEFAULT now())"

for arquivo in migracoes/*.sql; do
  versao=$(basename "$arquivo" .sql)
  ja=$(psql -X "$URI" -A -t \
       -c "SELECT count(*) FROM schema_migrations WHERE versao = '$versao'")
  [ "$ja" = "1" ] && continue
  psql -X "$URI" -1 -v ON_ERROR_STOP=1 \
    -c "\\i $arquivo" \
    -c "INSERT INTO schema_migrations (versao) VALUES ('$versao')" || exit 1
done
```

**1. O registro entra na mesma transação?**

**Sim, e é o que o código acima faz** — os dois `-c` dentro do mesmo `-1` formam uma transação só. O argumento a favor: falhou, nada aconteceu, e o estado do banco continua descrevível por `schema_migrations`.

O argumento **contra**, que é real: migrações com `CREATE INDEX CONCURRENTLY` não cabem em transação (AP3), e aí a atomicidade é impossível. O Alembic (05.10) vive com isso e por padrão coloca o registro na mesma transação, deixando o caso especial para quem o escreve.

**2. O arquivo mudou depois de aplicado.**

O script acima **não percebe** — ele compara nomes. A defesa é guardar o `hash` do conteúdo:

```sql
ALTER TABLE schema_migrations ADD COLUMN soma text;
```

e recusar rodar quando o `sha256` do arquivo divergir do gravado. **A resposta madura inclui o motivo:** editar uma migração já aplicada significa que o banco de desenvolvimento e o de produção divergiram em silêncio, e uma falha barulhenta agora é melhor que a descoberta em produção.

**3. Dois processos ao mesmo tempo.**

Sem proteção, os dois leem "não aplicada", os dois aplicam, e o segundo falha no meio — deixando o estado que a pergunta 1 tentava evitar.

A defesa é uma trava consultiva:

```
=== pg_try_advisory_lock ===
t|t
```

```bash
TRAVOU=$(psql -X "$URI" -A -t -c "SELECT pg_try_advisory_lock(72401)")
[ "$TRAVOU" = "t" ] || { echo "outra migração em andamento" >&2; exit 75; }
```

`pg_try_advisory_lock` devolve imediatamente `f` se outro já tem a trava, em vez de esperar. A trava é do **servidor**, o que a torna correta mesmo com os dois processos em máquinas diferentes — o que um arquivo de trava local não resolveria.

A trava precisa ser mantida pela **mesma conexão** durante toda a aplicação; com um `psql` por comando, cada chamada abre e fecha a conexão e a trava é liberada. A implementação correta usa um único `psql` alimentado por `stdin`, ou muda para Python.

## MP — Verificador de saúde

O núcleo, com as consultas que respondem cada item:

```bash
psql -X "$URI" -A -t <<'SQL'
SELECT version();
SELECT now() - pg_postmaster_start_time();
SELECT state, count(*) FROM pg_stat_activity GROUP BY state;
SELECT count(*) FROM pg_stat_activity
 WHERE state = 'idle in transaction'
   AND now() - state_change > interval '1 minute';
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
  FROM pg_stat_user_tables ORDER BY pg_total_relation_size(relid) DESC LIMIT 5;
SELECT coalesce(max(now() - xact_start)::text, '(nenhuma)')
  FROM pg_stat_activity WHERE xact_start IS NOT NULL;
SQL
```

A última, rodada num banco parado:

```
00:00:00
```

**A pergunta que fecha — os limites, e por que eles são discutíveis.**

Uma escolha defensável para o laboratório:

| Sinal | Limite | Motivo |
|---|---|---|
| `idle in transaction` | 1 minuto | acima disso é conexão esquecida, não trabalho |
| conexões em uso | 80% do `max_connections` | margem para o administrador entrar |
| transação mais antiga | 5 minutos | é o que segura o `autovacuum` |
| maior tabela | crescimento de 20% em uma semana | inchaço, e não uso |

**E o que muda num banco dez vezes maior:** o limite de `idle in transaction` **encurta**, não alonga. Com mais escrita por segundo, um minuto de transação aberta acumula muito mais versão morta — e o mesmo minuto que era tolerável passa a ser o motivo de o disco encher.

O limite de conexões, ao contrário, deixa de ser útil: em banco grande há pool na frente, e o número que interessa passa a ser o do pool, não o do servidor.
