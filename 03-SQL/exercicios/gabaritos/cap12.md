# Gabarito — Capítulo 03.12: DDL e tipos de dados

Leia depois de tentar. Enunciados em [`../cap12.md`](../cap12.md).

> Toda saída abaixo veio de execução real contra `dados/ddl.db` no SQLite 3.37.2.

## A1 — Preveja o `typeof`

```
i    | t    | r    | b    | n
-----+------+------+------+--------
real | text | real | text | integer
null | null | real | text | text
```

| Célula | Valor inserido | Coluna | Resultado | Por quê |
|---|---|---|---|---|
| `i` (1ª) | `'3.7'` | `INTEGER` | **`real`** | ver abaixo |
| `t` (1ª) | `99` | `TEXT` | `text` | afinidade `TEXT` converte número em texto |
| `r` (1ª) | `'2.5'` | `REAL` | `real` | conversível |
| `b` (1ª) | `'oi'` | `BLOB` | **`text`** | ver abaixo |
| `n` (1ª) | `'10'` | `NUMERIC` | `integer` | `NUMERIC` prefere inteiro quando não há fração |
| `i`,`t` (2ª) | `NULL` | — | `null` | `NULL` é um dos cinco tipos |
| `r` (2ª) | `7` | `REAL` | `real` | inteiro vira real na afinidade `REAL` |
| `n` (2ª) | `'abc'` | `NUMERIC` | `text` | inconversível: guarda como veio |

**As duas células que contrariam a previsão:**

**`'3.7'` numa coluna `INTEGER` vira `real`, não `integer`.** A afinidade `INTEGER` converte para
número — mas só converte para *inteiro* se a conversão for **sem perda**. `3.7` não é inteiro,
então o resultado é `real`. A regra completa da afinidade numérica: *converte para inteiro se
couber exatamente; senão para real; senão guarda como texto*. Três saídas possíveis para a
mesma coluna, decididas valor a valor.

**`'oi'` numa coluna `BLOB` vira `text`.** `BLOB` é a única declaração **sem afinidade** — ela
não tenta converter nada, guarda exatamente o que recebeu. E o que recebeu foi uma string, cujo
tipo é `text`. Consequência: declarar `BLOB` não faz o valor virar binário; para gravar um
binário de verdade é preciso enviá-lo como tal (`X'6F69'` em SQL, ou `bytes` pelo driver
Python).

## A2 — Escolha o tipo

| Campo | Tipo | `NOT NULL`? | Justificativa |
|---|---|---|---|
| CPF | `TEXT` | sim | **nunca `INTEGER`**: zeros à esquerda somem, e ninguém soma CPFs |
| Frete | `INTEGER` (centavos) | sim, `DEFAULT 0` | é dinheiro |
| Data/hora do pedido | `TEXT` ISO | sim | `'YYYY-MM-DD HH:MM:SS'` ordena corretamente |
| Aceita e-mails? | `INTEGER` 0/1 | sim, `DEFAULT 0` | ver abaixo |
| Quantidade em estoque | `INTEGER` | sim, `DEFAULT 0` | contagem é inteira; `NULL` não é o mesmo que zero |
| Descrição longa | `TEXT` | não | ausência de descrição é informação legítima |
| Percentual de desconto | `INTEGER` | sim, `DEFAULT 0` | guarde em pontos-base ou inteiro; `CHECK` entre 0 e 100 no 03.13 |
| Foto do produto | `TEXT` (caminho/URL) | não | ver abaixo |

**CPF é o caso que mais se erra.** `INTEGER` destrói `012.345.678-90` — o zero inicial
desaparece e não volta. A regra: **um identificador não é um número só porque é escrito com
dígitos.** Vale para CEP, telefone, código de barras, número de nota fiscal.

**O `DEFAULT 0` em "aceita e-mails" não é detalhe técnico.** Consentimento ausente é
consentimento **negado** — o padrão precisa ser o mais conservador, porque a coluna vai ser lida
por um sistema que dispara e-mails. Um `DEFAULT 1` transformaria um esquecimento de cadastro
numa violação de LGPD.

**A foto é uma decisão de arquitetura disfarçada de escolha de tipo.** `BLOB` guardaria a imagem
dentro do banco: backups inflam, consultas ficam pesadas, e servir a imagem passa pelo banco.
`TEXT` com o caminho ou URL mantém o banco leve e delega o armazenamento a quem é bom nisso. A
prática usual é `TEXT`; `BLOB` se justifica para arquivos pequenos que precisam da mesma
garantia transacional dos dados.

## A3 — Leia o `CREATE`

**(1) `pagamentos` — 4 problemas.** `id` sem `PRIMARY KEY` (não há identificador único, e o
`INTEGER PRIMARY KEY` que preencheria sozinho não existe); `valor FLOAT` é dinheiro em ponto
flutuante; `data VARCHAR(10)` — o `(10)` não limita e o nome não diz o formato; **nenhum
`NOT NULL`**, então um pagamento sem valor é aceito.

**(2) `cupons` — 4 problemas.** `codigo` deveria ser `PRIMARY KEY` ou ao menos `UNIQUE`
(03.13) — dois cupons com o mesmo código é um bug de negócio; `desconto REAL` volta ao problema
do dinheiro; `DATETIME` tem afinidade `NUMERIC`, o que é **pior que `TEXT`** para datas ISO,
porque números e textos podem conviver na mesma coluna; `BOOLEAN` funciona mas mente sobre o
que é (`INTEGER` 0/1).

**(3) `enderecos` — 2 problemas.** `CHAR(8)` para CEP não limita a 8 nada; e `cliente_id` não
tem `FOREIGN KEY` nem `NOT NULL` — um endereço sem dono. O `numero TEXT` está **certo**, e é a
pegadinha: número de endereço tem `123-A`, `s/n`, `12 fundos`. Se você marcou como erro,
inverteu o critério — é o mesmo raciocínio do CPF.

**(4) `logs` — 4 problemas.** `quando NUMERIC` para timestamp permite mistura de formatos;
`VARCHAR(50)` para mensagem de log é um limite fictício sobre um campo que quer ser longo;
`BANANA` é aceito calado; e não há `PRIMARY KEY`.

**(5) `estoque` — 2 problemas, e o segundo é sutil.** `quantidade REAL` para uma contagem —
`2.9999` unidades em estoque. E `DEFAULT NULL`, que é **pior que não ter `DEFAULT`**: declara
explicitamente que a ausência de estoque é `NULL`, e `NULL` não é zero. Toda soma vai ignorar
essas linhas (03.05), todo `WHERE quantidade < 10` vai omiti-las (03.03), e o relatório de
reposição não vai listar justamente os produtos zerados. `INTEGER NOT NULL DEFAULT 0` diz a
verdade.

## A4 — Existe ou não?

| # | Comando | Resultado |
|---|---|---|
| 1 | `ADD COLUMN` | **aceito** |
| 2 | `RENAME COLUMN` | **aceito** (desde 3.25) |
| 3 | `DROP COLUMN` | **aceito** (desde 3.35) |
| 4 | `ADD CONSTRAINT` | `Erro de SQL: near "CONSTRAINT": syntax error` |
| 5 | `TRUNCATE TABLE` | `Erro de SQL: near "TRUNCATE": syntax error` |
| 6 | `CREATE ... STRICT` | **aceito** (desde 3.37) |

**Os itens 2, 3 e 6 dependem da versão** — e é por isso que `preparar_ddl.py` imprime a versão
do SQLite. Se você está numa 3.30, o item 3 falha, e a conclusão correta não é "não existe" e
sim "não existe aqui". A pergunta "a partir de que versão?" é sempre parte da resposta.

**O item 4 é o que ensina.** Não há como acrescentar uma `CHECK` ou `UNIQUE` a uma tabela que já
existe: a restrição precisa estar no `CREATE TABLE`. Acrescentá-la depois exige... os quatro
passos do AP3. **A restrição esquecida na criação custa uma migração inteira** — mais um argumento
para pensar o schema antes.

**O item 5:** `TRUNCATE` não existe no SQLite. O equivalente é `DELETE FROM t` sem `WHERE`, que
o SQLite otimiza internamente para algo parecido.

## AP1 — A tabela de avaliações

| Coluna | Declarado | O que o SQLite faz | Absurdo que entra | Escolha |
|---|---|---|---|---|
| `produto_id` | `INTEGER` | afinidade numérica, aceita nulo | `NULL` — avaliação sem produto | `INTEGER NOT NULL` + FK |
| `nota` | `REAL` | aceita fração | `4.7`, `-3`, `1000` | `INTEGER NOT NULL` (+ `CHECK` no 03.13) |
| `comentario` | `VARCHAR(500)` | afinidade `TEXT`, sem limite | 50 000 caracteres | `TEXT` (opcional de propósito) |
| `data` | `DATETIME` | afinidade **`NUMERIC`** | `1721`, `'ontem'`, `'12/07/26'` | `TEXT NOT NULL` ISO |
| `verificada` | `BOOLEAN` | afinidade `NUMERIC` | `7`, `'talvez'` | `INTEGER NOT NULL DEFAULT 0` |
| `id` | `INTEGER PRIMARY KEY` | correto | — | manter |

**As três recusas provadas na versão `STRICT`:**

```
INSERT INTO avaliacoes VALUES (1, 1, 'cinco', NULL, '2026-08-04', 0);
-> Erro de SQL: cannot store TEXT value in INTEGER column avaliacoes.nota

INSERT INTO avaliacoes (id, nota, data) VALUES (2, 5, '2026-08-04');
-> Erro de SQL: NOT NULL constraint failed: avaliacoes.produto_id

INSERT INTO avaliacoes VALUES (3, 1, 5, NULL, '2026-08-04', 'talvez');
-> Erro de SQL: cannot store TEXT value in INTEGER column avaliacoes.verificada
```

**O que `STRICT` ainda NÃO pega, e é a parte importante do exercício:** `nota = 47` passa. É um
inteiro, e a coluna aceita inteiros. `STRICT` garante o **tipo**, não a **faixa** — e faixa é
assunto de `CHECK`, no próximo capítulo. Quem concluiu que `STRICT` resolveu o problema das
notas ainda tem uma tabela que aceita nota 47.

## AP2 — A auditoria

**A consulta que revela a bagunça:**

```sql
SELECT typeof(valor) AS tipo, COUNT(*) AS quantas
FROM importado GROUP BY typeof(valor);
```

**As linhas com `''` onde deveria haver `NULL`:**

```sql
SELECT COUNT(*) FROM importado WHERE valor = '';
```

E o fato que torna isso uma armadilha: `SELECT typeof('') , '' IS NULL, LENGTH('')` devolve
`text | 0 | 0`. **String vazia é `text`, tem comprimento 0 e NÃO é `NULL`.** Uma coluna
"limpa" com `WHERE valor IS NOT NULL` continua cheia de vazios; um `COUNT(valor)` conta os
vazios como preenchidos. É a diferença entre "não sei" e "sei que é nada", e importações
malfeitas confundem as duas o tempo todo.

**As datas fora do padrão ISO:**

```sql
SELECT data FROM importado WHERE data NOT LIKE '____-__-__';
```

E a prova de que o formato importa:

```
'12/07/2026' < '20/06/2026'  ->  1   (verdadeiro, e CRONOLOGICAMENTE ERRADO)
'2026-07-12' < '2026-06-20'  ->  0   (falso, e cronologicamente CERTO)
```

12 de julho vem **depois** de 20 de junho. No formato brasileiro, a comparação de texto diz o
contrário, porque compara o `1` de `12` com o `2` de `20` e para ali. Todo `ORDER BY data`,
todo `WHERE data < ...`, todo relatório "dos últimos 30 dias" fica errado — **sem dar erro**.

**Por que o `SUM(valor)` está errado.** Com os valores `10`, `20`, `'abc'`, `''`, `NULL` e
`'30'` numa coluna sem tipo declarado:

```
soma | cnt_valor | cnt_tudo
-----+-----------+---------
60.0 |         5 |        6
```

Três fatos numa linha. **A soma deu 60** — o `'30'` foi convertido e entrou, mas `'abc'` e `''`
valeram **zero** em vez de causar erro. **`COUNT(valor)` deu 5 e `COUNT(*)` deu 6** — só o
`NULL` foi descartado; a string vazia foi contada como valor presente (03.05). E a soma saiu
como `60.0`, um **real**, porque a conversão de texto para número produz real: o tipo do
resultado mudou por causa de uma linha suja.

O total é menor que o real e ninguém percebe, **porque um número sempre aparece**. Uma soma que
falhasse seria um presente; uma soma que responde 60 quando a verdade é outra é o que faz
alguém perder a tarde procurando o erro na planilha.

## AP3 — Mudando o tipo

```
total em REAL:  243.57999999999998   (6 linhas)
```

Os quatro passos:

```sql
BEGIN;
CREATE TABLE precos_novo (
    id             INTEGER PRIMARY KEY,
    valor_centavos INTEGER NOT NULL
) STRICT;
INSERT INTO precos_novo
    SELECT id, CAST(ROUND(valor * 100) AS INTEGER) FROM precos;
DROP TABLE precos;
ALTER TABLE precos_novo RENAME TO precos;
COMMIT;
```

```
valor_centavos: 1999, 10, 20, 8990, 349, 12990
total_centavos: 24358  ->  R$ 243,58
```

**A comparação:** `243.57999999999998` contra `243.58`. **O total em centavos é o correto** — e
o outro não está "quase certo": ele é um número que não existe em dinheiro. Some mais mil linhas
e o erro cresce de forma imprevisível, ora para cima, ora para baixo.

**O `ROUND` não é opcional, e aqui está a prova:**

```
19.99 * 100                      ->  1998.9999999999998
CAST(19.99 * 100 AS INTEGER)     ->  1998
CAST(ROUND(19.99 * 100) AS INT)  ->  1999
```

**`CAST` trunca.** Sem `ROUND`, a migração transformaria R$ 19,99 em 1998 centavos — perdendo
um centavo por linha, silenciosamente, em toda a base. É o erro perfeito: roda sem falhar, o
resultado parece plausível, e a diferença só aparece na conciliação contábil meses depois.

**Por que dentro de `BEGIN`/`COMMIT`.** Entre o `DROP TABLE precos` e o `RENAME`, a tabela
`precos` **não existe**. Uma falha nesse intervalo — queda de energia, erro de digitação no
comando seguinte — deixaria o banco sem a tabela e com os dados numa tabela de nome temporário.
A transação torna os quatro passos um só: ou todos acontecem, ou nenhum. É o assunto do 03.15,
e este é o caso em que ele deixa de ser teoria.

## D1 — O schema da biblioteca

```sql
DROP TABLE IF EXISTS emprestimos;
DROP TABLE IF EXISTS exemplares;
DROP TABLE IF EXISTS leitores;
DROP TABLE IF EXISTS livros;

CREATE TABLE livros (
    id      INTEGER PRIMARY KEY,
    isbn    TEXT    NOT NULL,          -- TEXT: tem hifens e digito X
    titulo  TEXT    NOT NULL,
    autor   TEXT    NOT NULL,
    ano     INTEGER                     -- opcional: obras antigas sem data
) STRICT;

CREATE TABLE exemplares (
    id        INTEGER PRIMARY KEY,
    livro_id  INTEGER NOT NULL,
    codigo    TEXT    NOT NULL,         -- patrimonio; TEXT pelo mesmo motivo do CPF
    estado    TEXT    NOT NULL DEFAULT 'bom',
    FOREIGN KEY (livro_id) REFERENCES livros(id)
) STRICT;

CREATE TABLE leitores (
    id         INTEGER PRIMARY KEY,
    nome       TEXT NOT NULL,
    documento  TEXT NOT NULL,
    cadastro   TEXT NOT NULL            -- ISO 'YYYY-MM-DD'
) STRICT;

CREATE TABLE emprestimos (
    id              INTEGER PRIMARY KEY,
    exemplar_id     INTEGER NOT NULL,   -- o EXEMPLAR, nao o livro
    leitor_id       INTEGER NOT NULL,
    data_saida      TEXT    NOT NULL,
    data_prevista   TEXT    NOT NULL,
    data_devolucao  TEXT,               -- NULL = em aberto; ver decisao (c)
    FOREIGN KEY (exemplar_id) REFERENCES exemplares(id),
    FOREIGN KEY (leitor_id)   REFERENCES leitores(id)
) STRICT;
```

**(b) As três decisões de modelagem.**

1. **O empréstimo aponta para o exemplar, não para o livro.** Quem sai pela porta é o objeto
   físico. Se apontasse para `livros`, seria impossível saber qual das quatro cópias está com
   quem — e impossível emprestar duas cópias do mesmo título ao mesmo tempo sem ambiguidade.
2. **`ano` é opcional; `isbn` não.** Obras antigas e edições artesanais têm data incerta.
   Forçar `NOT NULL` num campo que às vezes não existe produz o pior resultado possível:
   alguém preenche `0` ou `1900` para o cadastro passar, e o dado falso é pior que o ausente.
3. **`estado` com `DEFAULT 'bom'`.** Um exemplar novo entra em bom estado; o padrão evita que
   toda inserção tenha que declarar o que já se sabe, e `NOT NULL` impede que fique indefinido.

**(c) A decisão considerada de duas formas: `data_devolucao NULL` × coluna `status`.**

*Forma A — `data_devolucao` nula enquanto está fora.* Uma coluna a menos, e a informação já está
lá: se é nula, está emprestado. **Custo:** toda consulta de empréstimos em aberto vira
`WHERE data_devolucao IS NULL`, e um `NOT IN` sobre essa coluna devolve zero linhas sem avisar
(03.09). O `NULL` passa a significar duas coisas — "ainda não devolveu" e "não sabemos" — e
nada no schema distingue as duas.

*Forma B — coluna `status TEXT NOT NULL` com `'aberto'`/`'devolvido'`/`'perdido'`.* Explícita,
e comporta o terceiro caso, que a forma A não comporta: um exemplar perdido nunca terá data de
devolução, e na forma A ele é indistinguível de um empréstimo em aberto.

**O critério do desempate: existe um terceiro estado?** Se o domínio tem só dois estados, a
forma A é suficiente e mais enxuta. Numa biblioteca real existe "perdido", e provavelmente
"renovado" — então a forma B. **A pergunta que decide não é sobre elegância; é sobre quantos
estados o negócio tem** — e essa é uma pergunta para o cliente, não para o modelador.

**(d) As três perguntas ao cliente.** Um leitor pode ter mais de um empréstimo em aberto — há
limite? Um exemplar perdido some do acervo ou vira um estado? A multa por atraso é calculada
aqui ou em outro sistema? Cada uma muda o schema.

**(e) O teste de recusas.** Insira: um exemplar com `livro_id` inexistente (`FOREIGN KEY
constraint failed`); um empréstimo sem `leitor_id` (`NOT NULL constraint failed`); um `ano` como
texto numa tabela `STRICT` (`cannot store TEXT value in INTEGER column`). Um schema que você
não tentou quebrar é um schema que você não testou.

**O fecho.** Uma consulta errada afeta uma resposta; um schema errado afeta todos os dados
gravados a partir dele. A consulta se reescreve em cinco minutos e a mudança termina ali. O
schema, depois de dois anos e cinco sistemas lendo dele, exige migração, janela de manutenção,
coordenação entre times e um plano de reversão. **A assimetria não é de dificuldade técnica, é
de alcance** — e é por isso que a hora de fazer as perguntas do item (d) é antes do primeiro
`CREATE TABLE`, quando elas custam uma conversa, e não depois, quando custam um projeto.

---

## Erros mais comuns

1. **Prever `integer` para `'3.7'` numa coluna `INTEGER`.** Vira `real` — a conversão para
   inteiro só ocorre se for sem perda.
2. **Achar que `BLOB` converte para binário.** É a única declaração sem afinidade.
3. **Guardar CPF, CEP ou telefone como `INTEGER`.** Zeros à esquerda somem.
4. **`DEFAULT NULL` numa coluna de contagem.** `NULL` não é zero, e some das somas.
5. **Confundir `''` com `NULL`.** São coisas diferentes, e `IS NOT NULL` não filtra vazios.
6. **`CAST` sem `ROUND` ao converter dinheiro.** `CAST` trunca: 19,99 vira 1998 centavos.
7. **Migrar em quatro passos sem transação.** Entre o `DROP` e o `RENAME` a tabela não existe.
8. **Achar que `STRICT` valida faixa.** Ele garante tipo; `nota = 47` continua passando.
