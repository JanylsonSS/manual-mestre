# Gabarito — Capítulo 05.01: PostgreSQL, instalação e arquitetura

Leia depois de tentar. Enunciados em [`../cap01.md`](../cap01.md).

> Toda saída abaixo é execução real, contra PostgreSQL 16.2.

## A1 — Quem faz o quê?

| # | Responsabilidade | Nível |
|---|---|---|
| 1 | isolar dois sistemas que nunca se consultam | **database** |
| 2 | guardar as linhas de pedidos | **tabela** |
| 3 | decidir quem pode apagar | **role** |
| 4 | separar vendas de RH no mesmo sistema | **schema** |
| 5 | escutar na porta 5432 | **servidor** |
| 6 | onde procurar tabela sem prefixo | **schema** (via `search_path`) |
| 7 | existir independentemente de qualquer database | **role** |
| 8 | o limite além do qual um `JOIN` não alcança | **database** |

**O par 1/4 é o que importa.** Os dois falam de separação, e a diferença é se as coisas separadas **precisam ser consultadas juntas**. Se nunca precisam, `database` — o isolamento é maior e o acidente é impossível. Se um dia alguém vai querer cruzar, `schema` — porque `JOIN` entre databases não existe, e migrar depois é caro.

**O 7 é o que surpreende.** Roles pertencem ao **servidor**, não ao database: o mesmo `aurora` pode ter permissões diferentes em três databases. Por isso `CREATE ROLE` não precisa dizer em qual database, e por isso apagar um database não apaga os roles que o usavam.

## A2 — Preveja o resultado

| # | Situação | Postgres |
|---|---|---|
| 1 | A e B alteram linhas **diferentes** | as duas seguem, sem erro |
| 2 | A altera a linha 1, B **lê** a linha 1 | B recebe o valor **antigo**, sem esperar |
| 3 | A altera a linha 1, B **altera** a linha 1 | B **espera** A decidir — sem prazo |
| 4 | o mesmo, com `lock_timeout = '300ms'` | `canceling statement due to lock timeout` |
| 5 | A **lê**, B altera a mesma linha | B segue; leitura não bloqueia escrita |
| 6 | as situações 1–3 **no SQLite** | 1 e 3 dão `database is locked`; 2 funciona |

**O contraste do 6 é o capítulo inteiro.** No SQLite, a situação **1** — duas escritas em linhas **diferentes** — já falha, porque a trava é do banco. No Postgres ela nem chega perto de um conflito.

**O 5 costuma sair errado**, porque a intuição diz que ler "segura" a linha. Não segura: o MVCC entrega uma versão antiga ao leitor e deixa o escritor seguir. É a metade menos lembrada da regra — **leitura não bloqueia escrita, e escrita não bloqueia leitura**.

## A3 — Ache o erro

**1. Senha na constante — funciona, e vaza.** A URI vai para o Git e fica no histórico mesmo depois de removida (04.16/A3.3). Correção: `os.environ["AURORA_URI"]`, e a variável definida fora do repositório.

**2. Conexão por chamada, e nunca fechada — funciona, e derruba o servidor.** Dois erros: abrir custa 4,4 ms contra 0,25 ms de uma consulta (§6.6), e a conexão **nunca é fechada** — em cem chamadas, cem processos no servidor até o limite de 100 estourar. Correção: pool (05.05), e `with psycopg.connect(...)` enquanto não houver um.

**3. Aplicação conectando como `postgres` — funciona, e não tem freio.** O superusuário ignora permissões: um `DROP TABLE` por engano acontece. Correção: um role da aplicação, com o mínimo necessário.

**4. `UPDATE` sem `lock_timeout` num endpoint — funciona, até duas requisições disputarem a mesma linha.** Aí a segunda espera **indefinidamente**, o cliente recebe timeout do navegador, e a conexão fica presa. Correção: `SET lock_timeout` na sessão da aplicação, junto com `statement_timeout`.

**5. `autovacuum` desligado — funciona por semanas, e depois o banco incha.** As versões antigas do MVCC (§6.3) deixam de ser removidas: a tabela cresce, os índices incham, e as consultas ficam lentas sem que nada tenha mudado no código. O consumo de CPU que incomodava era ele **fazendo o trabalho**. Correção: religue e, se for o caso, ajuste os parâmetros em vez de desligar.

**6. Pasta de dados dentro do repositório — pode nem funcionar.** Além de ser dado gerado (que não se versiona), o servidor precisa criar um **soquete Unix** ali, e pastas sincronizadas (OneDrive, Dropbox) e alguns sistemas de arquivos recusam. Foi exatamente o erro que apareceu ao montar o laboratório deste módulo:

```
OSError: [Errno 95] Operation not supported
```

**A leitura do lote:** os seis "funcionam" em desenvolvimento, com um usuário e dez linhas. Todos falham em produção, e três deles (2, 4, 5) falham **só sob carga** — que é o pior momento para descobrir.

## A4 — SQLite ou Postgres?

| # | Cenário | Resposta |
|---|---|---|
| 1 | anotações num app de celular | **SQLite** |
| 2 | site com 200 pedidos/min | **Postgres** |
| 3 | testes automatizados de uma API | **os dois** — ver abaixo |
| 4 | relatório que 3 analistas atualizam | **Postgres** |
| 5 | script que guarda resultado local | **SQLite** |
| 6 | cadastro de clientes, 40 funcionários | **Postgres** |

**O 3 é o que ensina.** SQLite em memória deixa a suíte de testes muito mais rápida — e **testa outro banco**. Diferenças de tipo (03.12), de concorrência e de SQL específico passam despercebidas, e o defeito aparece em produção.

A prática recomendada hoje é **testar contra o mesmo banco de produção**, subindo um Postgres descartável (Docker, ou o `pgserver` deste módulo). O ganho de velocidade do SQLite não compensa a classe de defeito que ele esconde.

**E o 6 tem uma nuance:** quarenta funcionários não são 200 pedidos por minuto, e um SQLite aguentaria o volume. O que decide não é o volume — é que **várias pessoas escrevem ao mesmo tempo**, e é preciso saber quem pode ver o quê.

## AP1 — O laboratório

As consultas ao catálogo:

```sql
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'clientes';
SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint WHERE contype = 'f';
SELECT relname, pg_size_pretty(pg_total_relation_size(oid)) FROM pg_class WHERE relkind = 'r';
```

**A pergunta que fecha — o tipo de `criado_em`:**

```
('criado_em', 'timestamp with time zone')

valor lido em Python:
datetime.datetime(2026, 8, 6, 9, 36, 11, 286265,
                  tzinfo=zoneinfo.ZoneInfo(key='America/Sao_Paulo'))
```

**O `psycopg` devolveu um `datetime` consciente** (04.18), com `tzinfo` preenchido. No SQLite, a mesma coluna seria **texto** — e viraria um `datetime` ingênuo, ou uma string, conforme quem lesse.

**Por que importa:** o 04.18 mostrou que cinco das oito formas comuns de obter um `datetime` produzem valores ingênuos, e que um ingênuo circulando é a origem de erros silenciosos. O `timestamptz` do Postgres **fecha essa porta na fronteira do banco**: o que sai de lá tem endereço.

E note o nome do tipo: `timestamp with time zone` **não guarda o fuso**. Ele guarda o instante em UTC e converte na leitura, usando o fuso da sessão. É por isso que o valor chegou em `America/Sao_Paulo` — e é a mesma regra do 04.18: **guarde instantes, mostre leituras**.

## AP2 — Duas conexões

A parte que o capítulo não mostra é a situação 4, e ela é a mais instrutiva:

```
B esperou 403 ms e conseguiu; valor final para B: 222
depois do rollback de B, o valor no banco: 111 (o de A)
```

**B esperou, A fez `commit`, e B seguiu** — não recebeu erro. E o valor que B viu depois foi **222**, o dele: ao ganhar a trava, o Postgres fez B **reler** a linha na versão recém-confirmada por A e aplicar o `UPDATE` em cima dela.

**É isso que impede o *lost update*** que o 03.15 demonstrou: B não sobrescreveu cegamente o que leu antes; ele trabalhou sobre o resultado de A.

**A pergunta que separa** — o que B vê depois do `commit` de A:

- **Numa consulta nova**, fora de transação: o valor **novo**. É o nível `READ COMMITTED`, padrão do Postgres: cada comando enxerga o que já foi confirmado.
- **Dentro de uma transação aberta antes**, no nível `REPEATABLE READ`: o valor **antigo**, ainda. A transação inteira enxerga o banco como ele era quando ela começou.

O Postgres usa `READ COMMITTED` por padrão, e é por isso que duas consultas seguidas na mesma transação **podem devolver valores diferentes**. Quem precisa de estabilidade pede `SET TRANSACTION ISOLATION LEVEL REPEATABLE READ` — e paga com mais conflitos.

## AP3 — Role e database

```sql
CREATE ROLE leitor WITH LOGIN PASSWORD 'x';
GRANT CONNECT ON DATABASE postgres TO leitor;
GRANT USAGE ON SCHEMA public TO leitor;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO leitor;
```

```
SELECT ok: 12
DELETE -> permission denied for table produtos
```

**As três permissões são necessárias, e esquecer uma dá erros diferentes** — o que confunde:

- Sem `CONNECT`: a conexão é recusada.
- Sem `USAGE` no schema: `permission denied for schema public`.
- Sem `SELECT`: `permission denied for table produtos`.

**E há uma armadilha que o exercício não pede e vale conhecer:** `GRANT ... ON ALL TABLES` vale para as tabelas que existem **naquele momento**. Uma tabela criada depois não é alcançada, e o `leitor` vai receber `permission denied` numa tabela nova sem que ninguém tenha mexido nas permissões. A correção é `ALTER DEFAULT PRIVILEGES`, que define o que vale para o que ainda vai ser criado.

## D1 — A migração

**(1) Colunas que precisam de tipo diferente.**

`data` no SQLite era `TEXT` em ISO (03.12); no Postgres vira `date`. `criado_em` vira `timestamptz`. `ativo` era `INTEGER` 0/1; vira `boolean`.

**O ganho não é estética:** com `date`, o banco recusa `'2026-13-45'` e permite `data + interval '1 month'`. Com `TEXT`, tudo passa e a aritmética é sua. É a diferença entre afinidade (03.12) e tipo rígido.

**(2) O `AUTOINCREMENT`.** Vira `GENERATED ALWAYS AS IDENTITY` (ou `serial`, mais antigo). E há um detalhe que morde: se você inserir os IDs existentes explicitamente, a **sequência não avança** — o próximo `INSERT` sem ID tenta usar o 1 e viola a chave primária. A correção é reposicionar a sequência depois da carga:

```sql
SELECT setval(pg_get_serial_sequence('pedidos', 'id'), (SELECT max(id) FROM pedidos));
```

**(3) A comparação das agregações.** Se der diferença, olhe primeiro para **divisão** e **`NULL`**. `SUM` sobre inteiros dá inteiro nos dois; mas uma média (`AVG`) sobre inteiros devolve tipos diferentes, e o arredondamento pode divergir. Se você seguiu a regra do 03.05 — **dinheiro em centavos inteiros** —, os totais batem exatamente, e é essa a prova que o exercício quer.

## MP — O painel do servidor

**A pergunta que fecha: por que `idle in transaction` merece um aviso e `idle` não?**

```
('idle in transaction', True)      ← tem transação aberta
```

Uma conexão `idle` está parada e **não segura nada**: nenhuma transação aberta, nenhuma trava, nenhuma versão de linha presa. Ela custa um processo e memória, e é isso.

Uma conexão **`idle in transaction`** está parada **com uma transação aberta**, e isso tem três consequências, em ordem crescente de gravidade:

**Ela pode estar segurando travas** — de linhas que alterou e não confirmou. Qualquer outra transação que precise daquelas linhas espera (A2.3), indefinidamente.

**Ela impede o `autovacuum` de limpar.** O MVCC precisa manter todas as versões de linha que **alguma transação aberta ainda possa enxergar** (§6.3). Uma transação aberta há uma hora congela a limpeza de tudo o que mudou nessa hora — em todo o banco, não só nas tabelas que ela tocou.

**E o efeito composto é o que derruba sistemas:** a tabela incha com versões mortas, os índices incham junto, as consultas ficam lentas, e o diagnóstico aponta para "o banco está lento" quando a causa é **uma conexão esquecida** que alguém abriu e não fechou.

**A causa mais comum** é código que abre transação e faz outra coisa no meio — uma chamada de rede, uma espera por entrada do usuário. É o mesmo erro do 04.20/§12 ("segure a trava pelo menor tempo possível"), agora com um banco no meio.

O Postgres tem um parâmetro para isso: `idle_in_transaction_session_timeout`, que encerra essas conexões automaticamente. Ligá-lo é uma das configurações mais baratas de produção.
