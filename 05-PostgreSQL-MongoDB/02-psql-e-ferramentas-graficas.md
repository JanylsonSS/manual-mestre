# 05.02 — `psql` e ferramentas gráficas

> **Módulo 05 — PostgreSQL e MongoDB** · Nível: N1 · Tempo estimado: 2h · Código: `codigo/cap02/`

## 1. Objetivo

- **Executar** administração e consulta pelo `psql`, com as meta-instruções que substituem SQL.
- **Escrever** scripts que usam o `psql` e **detectam** o próprio erro.
- **Distinguir** `\copy` de `COPY`, e dizer qual roda em qual máquina.
- **Escolher** entre terminal e interface gráfica, sabendo o que cada uma cobra.

Ao final, você consegue rodar uma migração pelo terminal e provar que ela foi aplicada — ou que não foi.

---

## 2. Pré-requisitos

- [05.01 — PostgreSQL: instalação e arquitetura](01-postgresql-instalacao-e-arquitetura.md) — o servidor precisa estar de pé.
- [02.07 — Scripts de shell](../02-Git-Linux/07-scripts-de-shell.md) — a §6.5 usa variável, código de saída e redirecionamento.
- [03.15 — Transações e ACID](../03-SQL/15-transacoes-e-acid.md) — `BEGIN`, `COMMIT` e `ROLLBACK` voltam aqui, agora dentro de um arquivo `.sql`.

**Autoteste:** (1) O que `$?` guarda no shell? (2) O que faz um `ROLLBACK`? (3) Como você põe a saída de um comando dentro de uma variável?

---

## 3. Motivação

Uma migração de banco tem três comandos. O do meio falha. O script termina, o CI fica verde, e o time deploya.

```
psql:migracao.sql:2: ERROR:  relation "tabela_que_nao_existe" does not exist
LINE 1: INSERT INTO tabela_que_nao_existe VALUES (1);
                    ^
código de saída: 0
criadas: etapa_tres, etapa_um
```

**Leia a terceira linha de novo.** O erro apareceu na tela, e o `psql` devolveu **zero** — o código que todo sistema de automação lê como "deu certo". A segunda etapa não rodou, a terceira rodou, e o banco ficou num estado que ninguém projetou.

Este capítulo é sobre a ferramenta que você vai abrir todo dia pelos próximos anos. A parte que dá para aprender em quinze minutos são as meta-instruções. A parte que separa quem opera banco de quem consulta banco são as quatro linhas acima.

---

## 4. Modelo mental

**O `psql` é dois programas no mesmo executável.**

O primeiro é um **cliente SQL**: você digita `SELECT`, ele manda para o servidor e imprime a resposta. Nada além disso.

O segundo é um **programa que roda na sua máquina** e nunca chega ao servidor. Tudo que começa com barra invertida é dele: `\dt` vira uma consulta ao catálogo antes de sair; `\copy` lê e escreve arquivos **no seu disco**; `\timing` cronometra localmente.

```
    você digita              quem executa
    ───────────              ────────────
    SELECT ...               o SERVIDOR
    COPY ... TO 'arq'        o SERVIDOR (grava no disco DELE)
    \dt                      o psql traduz e o servidor responde
    \copy ... TO 'arq'       o psql (grava no disco SEU)
    \timing                  só o psql
```

**A frase que organiza o capítulo: a barra invertida marca o que fica na sua máquina.** Confundir essa fronteira é o erro mais caro do capítulo, e a §6.6 mostra a mensagem exata que ele produz.

---

## 5. Analogia

O `psql` é o **telefone** com o banco, e a barra invertida é o **bloco de anotações ao lado do telefone**.

Quando você fala, a voz vai para o outro lado. Quando você escreve no bloco, ela não vai — o bloco é seu, está na sua mesa, e nenhum interlocutor o vê.

**E a analogia acerta no ponto que a §6.6 mede:** pedir ao outro lado que anote algo no bloco *dele* é uma coisa; anotar no seu é outra. Os dois pedidos parecem iguais quando você está com pressa, e produzem arquivos em máquinas diferentes.

---

## 6. Teoria

### 6.1 Conectar, e saber onde você está

O `psql` aceita a mesma URI que o `psycopg`:

```bash
psql "postgresql://aurora:senha@localhost:5432/aurora"
psql "$AURORA_URI"
```

E a primeira instrução a decorar responde "onde eu caí?":

```
You are connected to database "postgres" as user "postgres" via socket in
"/tmp/aurora-pgdata" at port "5432".
```

Quatro dados numa linha: **database**, **role**, **como** (soquete ou TCP) e **porta**. São exatamente os níveis do 05.01/§6.2, e `\conninfo` é o que você roda antes de qualquer comando destrutivo — porque a pergunta "estou em produção?" tem resposta.

### 6.2 O catálogo sem escrever SQL

`\dt` lista tabelas:

```
            List of relations
 Schema |     Name     | Type  |  Owner
--------+--------------+-------+----------
 public | clientes     | table | postgres
 public | itens_pedido | table | postgres
 public | pedidos      | table | postgres
 public | produtos     | table | postgres
(4 rows)
```

`\d produtos` descreve uma tabela — e devolve mais do que as colunas:

```
                  Table "public.produtos"
     Column     |  Type   | Collation | Nullable | Default
----------------+---------+-----------+----------+---------
 id             | integer |           | not null |
 nome           | text    |           | not null |
 categoria      | text    |           | not null |
 preco_centavos | integer |           | not null |
 ativo          | boolean |           | not null | true
Indexes:
    "produtos_pkey" PRIMARY KEY, btree (id)
Check constraints:
    "produtos_preco_centavos_check" CHECK (preco_centavos >= 0)
Referenced by:
    TABLE "itens_pedido" CONSTRAINT "itens_pedido_produto_id_fkey"
      FOREIGN KEY (produto_id) REFERENCES produtos(id)
```

As três últimas seções são o que você não veria consultando `information_schema.columns`: os **índices**, as **restrições** e — a mais útil — **quem aponta para esta tabela**. `Referenced by` responde "posso apagar esta linha?" antes de você tentar.

O conjunto que cobre 90% do uso:

| Instrução | O que lista |
|---|---|
| `\l` | databases |
| `\c nome` | troca de database |
| `\dt` | tabelas |
| `\d nome` | uma tabela em detalhe |
| `\di` | índices |
| `\du` | roles |
| `\dn` | schemas |
| `\df` | funções |
| `\?` | as meta-instruções |
| `\h COMANDO` | a sintaxe SQL de um comando |

`\h UPDATE` é o que evita abrir o navegador: ele imprime a sintaxe completa do comando, da versão que você está usando.

### 6.3 Quando a linha não cabe

Uma tabela larga vira ilegível no terminal. `\x` transpõe:

```
 id | cliente_id |    data    | status
----+------------+------------+--------
  1 |          1 | 2026-06-02 | pago
(1 row)
```

```
-[ RECORD 1 ]----------
id         | 1
cliente_id | 1
data       | 2026-06-02
status     | pago
```

Com quatro colunas a diferença é estética. Com trinta, é a diferença entre ler e não ler. **`\x auto`** deixa o `psql` decidir: modo normal quando cabe, transposto quando não cabe — e é a linha que quase todo mundo põe no `.psqlrc`.

### 6.4 Cronometrar

```
Timing is on.
 count
-------
    31
(1 row)

Time: 0.708 ms
```

`\timing on` mede **ida, execução e volta**. Não é o tempo do plano de execução (isso é `EXPLAIN ANALYZE`, do 05.11) — é o tempo que você esperou. Para comparar duas formas de escrever a mesma consulta, é a medida honesta, porque inclui o que o cliente paga.

### 6.5 O `psql` dentro de um script

Por padrão o `psql` desenha uma moldura para humanos. Um script não quer moldura:

```
    padrão:
 count
-------
    20
(1 row)

    com -A -t (sem moldura, sem cabeçalho, sem rodapé):
20
```

`-A` desliga o alinhamento e `-t` desliga cabeçalho e rodapé (*tuples only*). O que sobra é o valor:

```bash
TOTAL=$(psql "$AURORA_URI" -A -t -c 'SELECT count(*) FROM pedidos')
```

```
    TOTAL=20
```

Some `--csv` a esse conjunto e você tem um exportador de uma linha.

### 6.6 `\copy` e `COPY`: a fronteira

Os dois comandos escrevem um arquivo. Rodando como superusuário, no laboratório, os dois funcionam e parecem iguais:

```
COPY 12
    as três primeiras linhas do arquivo:
      id,nome,categoria,preco_centavos
      1,Fone Bluetooth XZ-9,audio,46990
      2,Mouse Sem Fio,perifericos,8990
    e o mesmo comando com COPY (maiúsculo, sem a barra):
      COPY 12
```

**Aqui o laboratório engana**, e vale saber por quê: o servidor e o cliente estão na mesma máquina, e o usuário é superusuário. Repita com um role comum — o que você vai ter no trabalho:

```
      COPY:   ERROR:  permission denied to COPY to a file
      COPY:   DETAIL:  Only roles with privileges of the
                       "pg_write_server_files" role may COPY to a file.
      \copy:  COPY 12
```

**`COPY` grava no disco do servidor**, e por isso exige um privilégio que quase ninguém tem — um role qualquer poderia escrever onde quisesse na máquina do banco. **`\copy` grava no seu disco**, com as suas permissões de usuário do sistema, e por isso não exige nada.

Num servidor remoto a diferença deixa de ser sutil: `COPY ... TO '/tmp/dados.csv'` cria o arquivo **numa máquina onde você talvez não tenha acesso**, e `\copy` cria na sua.

### 6.7 Autocommit, e o que ele esconde

O `psql` confirma cada comando sozinho:

```
o UPDATE acima já está gravado — o psql abre e fecha a transação
```

Isso vale para o comando avulso. Dentro de um bloco, o `BEGIN` manda:

```
preço depois do BEGIN..ROLLBACK: 46990
```

O `UPDATE` para zero desapareceu — estava dentro de uma transação que terminou em `ROLLBACK`. **A regra: sem `BEGIN`, cada comando é uma transação; com `BEGIN`, você decide onde ela acaba.**

`\set AUTOCOMMIT off` inverte o padrão, e é o que operadores experientes fazem antes de mexer em produção: nada é gravado até você digitar `COMMIT`.

### 6.8 O erro que passa e o erro que para

Um arquivo com três comandos, o do meio quebrado. Sem proteção:

```
psql:migracao.sql:2: ERROR:  relation "tabela_que_nao_existe" does not exist
código de saída: 0
criadas: etapa_tres, etapa_um
```

Com `ON_ERROR_STOP=1`:

```
psql:migracao.sql:2: ERROR:  relation "tabela_que_nao_existe" does not exist
código de saída: 3
criadas: etapa_um
```

**O código de saída virou 3, e isso resolve o problema do CI.** Mas repare no que sobrou: `etapa_um` foi criada e as outras não. **A migração ficou pela metade.** O banco está num estado que não é nem o antigo nem o novo, e o próximo `deploy` vai encontrar uma tabela que ele acha que não existe.

A opção que fecha o buraco é `-1`:

```
psql:migracao.sql:2: ERROR:  relation "tabela_que_nao_existe" does not exist
código de saída: 3
criadas: (nenhuma)
```

`-1` embrulha o arquivo inteiro numa transação. Deu erro, nada é gravado. **A dupla `-1 -v ON_ERROR_STOP=1` é o que você quer em qualquer script de migração**, e a segunda sem a primeira é uma armadilha silenciosa.

---

## 7. Funcionamento interno

Os códigos de saída do `psql`, medidos:

```
consulta boa ........................ 0
servidor inalcançável ............... 2
SQL ruim com -c ..................... 1
SQL ruim com -f, sem ON_ERROR_STOP .. 0
SQL ruim com -f, com ON_ERROR_STOP .. 3
```

**As duas linhas do meio explicam a §3.** Com `-c`, um erro de SQL devolve **1** — o `psql` tinha um comando e ele falhou. Com `-f`, o `psql` entende que está lendo um roteiro interativo: reporta o erro, segue para a próxima linha e termina dizendo que **chegou ao fim do arquivo**, que é o que o zero significa.

Não é defeito: é o comportamento de um interpretador de sessão. `ON_ERROR_STOP` é o que diz "aqui não é uma sessão, é um script" — e aí o 3 aparece.

**Decore os quatro:** 0 sucesso, 1 erro de SQL, 2 problema de conexão, 3 parada por `ON_ERROR_STOP`.

---

## 8. Visualização do fluxo

```mermaid
flowchart TD
    A["você digita algo"] --> B{"começa com barra?"}
    B -- "não" --> C["texto vai para o SERVIDOR"]
    B -- "sim" --> D{"qual barra?"}
    D -- "\\dt, \\d, \\du" --> E["psql traduz para SQL<br/>e manda ao servidor"]
    D -- "\\copy" --> F["psql lê/escreve<br/>no SEU disco"]
    D -- "\\timing, \\x, \\set" --> G["fica só no psql"]
    C --> H{"deu erro?"}
    E --> H
    H -- "não" --> I["resultado na tela"]
    H -- "sim, e é -f sem<br/>ON_ERROR_STOP" --> J["segue para o<br/>próximo comando<br/>saída = 0"]
    H -- "sim, e há<br/>ON_ERROR_STOP" --> K["para agora<br/>saída = 3"]
```

**Como ler:** siga de cima para baixo. A primeira bifurcação é a fronteira da §4 — barra invertida decide se o texto sai da sua máquina. A parte de baixo é a da §6.8: o mesmo erro produz dois destinos, e o que muda entre eles é uma opção de linha de comando.

---

## 9. Aplicação prática

**Aurora, situação real.** O time precisa aplicar uma migração em produção pela madrugada, sem ninguém olhando. O script tem cinco comandos e é chamado por um agendador que só sabe ler código de saída.

A primeira versão:

```bash
psql "$AURORA_URI" -f migracao.sql
```

Ela erra duas vezes: não para no erro e não desfaz o que já fez. A versão que sobrevive:

```bash
set -euo pipefail
psql "$AURORA_URI" -v ON_ERROR_STOP=1 -1 -f migracao.sql
```

E a conferência que vai junto, porque "não deu erro" e "está correto" são coisas diferentes:

```bash
ANTES=$(psql "$AURORA_URI" -A -t -c 'SELECT count(*) FROM pedidos')
psql "$AURORA_URI" -v ON_ERROR_STOP=1 -1 -f migracao.sql
DEPOIS=$(psql "$AURORA_URI" -A -t -c 'SELECT count(*) FROM pedidos')
[ "$ANTES" = "$DEPOIS" ] || echo "AVISO: a contagem mudou ($ANTES -> $DEPOIS)"
```

**E a interface gráfica?** DBeaver e pgAdmin são bons para explorar um schema que você não conhece, montar uma consulta com muitos `JOIN` e olhar um plano de execução desenhado. São ruins para o que este capítulo faz: nenhum agendador clica em botão.

Há um custo que quase ninguém conta. **A interface gráfica abre uma transação para navegar e às vezes esquece de fechá-la.** No 05.01/§6.3 você viu que o MVCC guarda versões antigas enquanto houver transação aberta — uma janela do DBeaver esquecida numa aba `idle in transaction` impede o `autovacuum` de limpar, e o banco incha sem que ninguém tenha rodado nada.

---

## 10. Código comentado

O arquivo `codigo/cap02/sessao.sh` roda todas as cenas. A parte que vale ler linha a linha é a cena 6, porque ela contém a pegadinha que quase entrou neste capítulo como afirmação errada:

```bash
psql "$AURORA_URI" -q -f "$PASTA/migracao.sql" > "$PASTA/saida" 2>&1
CODIGO=$?                       # o código do psql, e de mais ninguém
sed 's/^/      /' "$PASTA/saida"
echo "      código de saída: $CODIGO"
```

**A primeira versão deste script fazia `psql ... | sed` e depois lia `$?`.** Num cano, `$?` é o código do **último** comando — o `sed`, que sempre devolve zero. O script relatava "código de saída: 0" para todos os casos, inclusive os que falhavam de verdade.

A correção é guardar a saída num arquivo e ler `$?` na linha seguinte. Quando o cano é inevitável, o instrumento é `${PIPESTATUS[0]}` no `bash`.

**O motivo de isto estar no capítulo:** o defeito produzia exatamente o número que a §3 usa para assustar você. Se ninguém tivesse conferido, o manual estaria certo por acidente — e a explicação, errada.

---

## 11. Erros comuns

| # | Erro | Sintoma | Correção |
|---|---|---|---|
| 1 | `-f` sem `ON_ERROR_STOP` | CI verde, banco quebrado | `-v ON_ERROR_STOP=1` |
| 2 | `ON_ERROR_STOP` sem `-1` | migração aplicada pela metade | some `-1` |
| 3 | `COPY` no lugar de `\copy` | `permission denied to COPY to a file` | barra invertida |
| 4 | `COPY` funcionando e gravando no lugar errado | arquivo "sumiu" | ele está no servidor |
| 5 | Ler `$?` depois de um cano | código de saída sempre 0 | arquivo, ou `${PIPESTATUS[0]}` |
| 6 | Esquecer a barra em `\d` | `syntax error at or near "d"` | é meta-instrução, não SQL |
| 7 | GUI aberta em `idle in transaction` | banco inchando sem uso | feche a aba, ou `COMMIT` |
| 8 | `psql` sem `\conninfo` antes de um `DELETE` | rodou em produção | `\conninfo` primeiro |

**O 2 é o mais caro**, porque parece resolvido: você adicionou a proteção, o CI passou a falhar corretamente, e ninguém percebeu que o banco fica num estado intermediário a cada falha.

---

## 12. Boas práticas

**Um `.psqlrc` que economiza uma hora por semana:**

```
\set QUIET 1
\x auto
\timing on
\set ON_ERROR_ROLLBACK interactive
\set HISTSIZE 5000
\pset null '(null)'
\unset QUIET
```

A linha de `null` é a mais subestimada: sem ela, `NULL` e string vazia aparecem idênticos na tela, e você depura pela tarde inteira uma diferença que não existe.

**Em script, sempre `-1 -v ON_ERROR_STOP=1`.** Sem exceção — inclusive nos scripts que "só leem", porque eles crescem.

**Nunca `-c` com uma string montada por concatenação.** É a mesma vulnerabilidade do 05.04, na versão shell.

**A senha vai no `~/.pggpass`** (permissão `0600`) ou na variável `PGPASSWORD`, nunca na linha de comando — o `ps` mostra a linha de comando de qualquer processo para qualquer usuário da máquina.

---

## 13. Performance

O `\timing` mede o que você espera, e o número de referência do laboratório:

```
 count
-------
    31
(1 row)

Time: 0.708 ms
```

**Sub-milissegundo, e isso já inclui a rede local.** Compare com o 05.01/§6.5: abrir uma conexão custou 4,4 ms. Uma consulta que roda em 0,7 ms atrás de uma conexão de 4,4 ms é uma conta em que a abertura pesa seis vezes mais que o trabalho.

**A consequência para o dia a dia:** um script de shell que roda `psql` cinco vezes seguidas paga cinco conexões. Se os cinco comandos couberem num arquivo, um `psql -f` paga uma. Em automação que roda a cada minuto, a diferença aparece.

**E o contraponto:** o `\timing` não separa o tempo do servidor do tempo da rede. Quando os dois estão em máquinas diferentes, um número que piorou pode ser plano de execução (05.11) ou latência — e a ferramenta que distingue é `EXPLAIN ANALYZE`, que reporta só o lado do servidor.

---

## 14. Mercado

`psql` aparece em vaga como requisito implícito: "experiência com PostgreSQL" quer dizer que você abre um terminal e resolve. Ninguém escreve "saber `\d`" numa vaga, e todo mundo espera.

**Onde ele aparece de verdade no trabalho:** dentro de um contêiner em produção, onde não há interface gráfica; dentro de um script de deploy; e no meio de um incidente, quando alguém precisa saber o que a tabela tem **agora**.

**O que a interface gráfica ganha:** explorar um banco herdado sem documentação, e mostrar um plano de execução para quem não lê `EXPLAIN`. DBeaver é o mais comum por ser gratuito e falar com vários bancos; pgAdmin vem com o instalador oficial.

**O que o mercado cobra em entrevista** não é a lista de meta-instruções — é a §6.8. "Como você garante que uma migração não fica pela metade?" é uma pergunta de arquitetura disfarçada de pergunta de ferramenta.

---

## 15. Entrevistas

**P1. Qual a diferença entre `COPY` e `\copy`?**
`COPY` roda no servidor e grava no disco dele, exigindo privilégio de `pg_write_server_files`; `\copy` roda no cliente e grava no seu disco, com as suas permissões de sistema. Num servidor remoto, os dois criam arquivos em máquinas diferentes.

**P2. Um script com `psql -f` teve erro e o CI passou. Por quê?**
Sem `ON_ERROR_STOP`, o `psql` trata o arquivo como uma sessão: reporta o erro, continua, e devolve 0 ao chegar ao fim. A correção é `-v ON_ERROR_STOP=1`, e `-1` junto para não deixar a migração pela metade.

**P3. Por que uma janela de DBeaver aberta pode inchar o banco?**
Se a ferramenta deixa uma transação aberta (`idle in transaction`), o MVCC precisa manter as versões antigas de linha que aquela transação ainda poderia enxergar, e o `autovacuum` não consegue removê-las.

**P4. Como você põe o resultado de uma consulta numa variável de shell?**
`VAR=$(psql "$URI" -A -t -c 'SELECT ...')` — `-A` tira o alinhamento e `-t` tira cabeçalho e rodapé.

---

## 16. Exercícios guiados

Enunciados completos em [`exercicios/cap02.md`](exercicios/cap02.md); gabaritos em [`exercicios/gabaritos/cap02.md`](exercicios/gabaritos/cap02.md).

**Aquecimento (4):** classificar comandos entre cliente e servidor; prever códigos de saída; achar o erro em seis trechos de script; escolher terminal ou interface gráfica.

**Aplicação (3):** montar um `.psqlrc` e justificar cada linha; escrever um exportador de CSV que funcione como usuário comum; transformar uma migração ingênua numa segura e provar as duas.

**Desafio (1):** um script de aplicação de migrações com registro do que já rodou.

**Mini projeto (1):** um verificador de saúde do banco, feito só de `psql` e shell.

---

## 17. Desafios

O desafio D1 pede o esqueleto do que o Alembic (05.10) faz: uma tabela de controle, um diretório de arquivos `.sql` numerados, e a decisão de aplicar apenas o que falta.

**O ponto difícil não é o laço.** É decidir se o registro de "esta migração rodou" entra na mesma transação da migração. Se entrar, uma falha desfaz as duas coisas juntas e o estado fica coerente. Se não entrar, existe um instante em que uma das duas está gravada e a outra não — e o script precisa saber o que fazer quando reencontrar esse estado.

---

## 18. Mini projeto

**Verificador de saúde**, em `bash` e `psql`, sem Python.

Ele reporta: versão e tempo de atividade; conexões por estado; conexões `idle in transaction` há mais de um minuto; as cinco maiores tabelas; e a idade da transação mais antiga.

**Requisito que muda o desenho:** o script devolve código de saída diferente de zero quando encontra um problema, para que um agendador consiga usá-lo. Isso obriga você a decidir o que é problema — e essa decisão é o exercício.

---

## 19. Revisão

**O que fica:**

1. Barra invertida marca o que roda na sua máquina; o resto vai ao servidor.
2. `\conninfo` antes de qualquer comando destrutivo.
3. `\d tabela` mostra índices, restrições e quem referencia — mais do que as colunas.
4. `-A -t` transforma o `psql` em fonte de dados para o shell.
5. `-f` sem `ON_ERROR_STOP` devolve 0 mesmo com erro.
6. `ON_ERROR_STOP` sem `-1` deixa a migração pela metade.
7. `COPY` grava no servidor; `\copy` grava no cliente.
8. Interface gráfica esquecida em transação aberta impede o `autovacuum`.

**Repetição espaçada:** D+1 refaça a cena 6 de cabeça; D+7 escreva o `.psqlrc` sem consultar; D+30 explique a P2 em voz alta; D+90 releia a §7 antes do 05.10.

---

## 20. Checklist

- [ ] Conecto e confirmo onde estou com `\conninfo`.
- [ ] Descrevo uma tabela e leio a seção `Referenced by`.
- [ ] Ligo `\x auto` e digo por que ele importa.
- [ ] Ponho o resultado de uma consulta numa variável de shell.
- [ ] Explico por que `-f` sem proteção devolve 0.
- [ ] Escrevo uma migração que não fica pela metade.
- [ ] Digo em que máquina cada arquivo de `COPY` e `\copy` aparece.
- [ ] Reconheço `idle in transaction` como problema, e explico o motivo.

---

## 21. Próximo capítulo

[05.03 — Tipos avançados do Postgres](03-tipos-avancados.md) sai da ferramenta e vai para o que o Postgres guarda que o SQLite não guardava: `JSONB`, arrays, `UUID` e uma família de tipos de data e hora que resolve o problema do 04.18 dentro do banco.

O `\d` deste capítulo volta lá o tempo todo — é como você vai conferir que o tipo que pediu foi o tipo que ficou.
