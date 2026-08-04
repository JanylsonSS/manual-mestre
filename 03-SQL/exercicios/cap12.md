# Exercícios — Capítulo 03.12: DDL e tipos de dados

> **Antes de tudo:** `python codigo/cap12/preparar_ddl.py`. Todo exercício roda com
> `AURORA_BANCO=dados/ddl.db`, num banco vazio que é seu para destruir.

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap12.md`](gabaritos/cap12.md).

## Aquecimento

### A1 — Preveja o `typeof` `[Aquecimento · ~10 min · o que fica gravado?]`

**Tarefa.** Crie a tabela e, **antes de executar**, escreva o `typeof()` de cada célula:

```sql
CREATE TABLE a1 (i INTEGER, t TEXT, r REAL, b BLOB, n NUMERIC);
INSERT INTO a1 VALUES ('3.7', 99,   '2.5', 'oi',  '10');
INSERT INTO a1 VALUES (NULL,  NULL, 7,     '3.7', 'abc');
```

Confira com `SELECT typeof(i), typeof(t), typeof(r), typeof(b), typeof(n) FROM a1;`.
**Duas células vão contrariar a previsão da maioria** — descubra quais e explique.

### A2 — Escolha o tipo `[Aquecimento · ~10 min · e justifique]`

**Tarefa.** Para cada campo, escolha o tipo SQLite e diga se é `NOT NULL`:

1. CPF de um cliente
2. Valor de um frete
3. Data e hora de um pedido
4. "O cliente aceita receber e-mails?"
5. Quantidade de itens no estoque
6. Descrição longa de um produto
7. Percentual de desconto (0 a 100)
8. Foto do produto

### A3 — Leia o `CREATE` `[Aquecimento · ~10 min · quantos problemas?]`

**Tarefa.** Cada definição tem de 1 a 4 problemas. Encontre todos:

```sql
-- (1)
CREATE TABLE pagamentos (id INTEGER, valor FLOAT, data VARCHAR(10));

-- (2)
CREATE TABLE cupons (codigo TEXT, desconto REAL, valido_ate DATETIME, usado BOOLEAN);

-- (3)
CREATE TABLE enderecos (id INTEGER PRIMARY KEY, cliente_id INTEGER, cep CHAR(8), numero TEXT);

-- (4)
CREATE TABLE logs (quando NUMERIC, mensagem VARCHAR(50), nivel BANANA);

-- (5)
CREATE TABLE estoque (produto_id INTEGER PRIMARY KEY, quantidade REAL DEFAULT NULL);
```

### A4 — Existe ou não? `[Aquecimento · ~10 min · o que o SQLite aceita]`

**Tarefa.** Preveja se o SQLite aceita, e confirme executando:

1. `ALTER TABLE t ADD COLUMN z TEXT;`
2. `ALTER TABLE t RENAME COLUMN a TO aa;`
3. `ALTER TABLE t DROP COLUMN c;`
4. `ALTER TABLE t ADD CONSTRAINT ck CHECK (aa > 0);`
5. `TRUNCATE TABLE t;`
6. `CREATE TABLE x (i INT) STRICT;`

## Aplicação

### AP1 — A tabela de avaliações `[Aplicação · ~25 min · do rascunho às decisões]`

**Tarefa.** Parta da versão ruim da §9 do capítulo. Para **cada** uma das seis colunas, escreva: (a) que tipo estava declarado; (b) o que o SQLite realmente faz com ele; (c) que valor absurdo consegue entrar; (d) sua escolha e o motivo.

Depois crie a versão `STRICT` e **prove** que ela recusa três dos absurdos que a primeira aceitava — com a mensagem de erro de cada um.

### AP2 — A auditoria `[Aplicação · ~20 min · tipos misturados]`

**Tarefa.** Crie uma tabela sem `STRICT` e insira 8 linhas simulando dados vindos de uma importação malfeita: alguns números como texto, algumas datas em `DD/MM/YYYY`, alguns campos vazios como `''` em vez de `NULL`.

Depois escreva as consultas de auditoria que um analista rodaria ao receber essa tabela:

1. quantas linhas de cada `typeof()` existem em cada coluna;
2. quais linhas têm `''` onde deveria haver `NULL`;
3. quais datas não estão no formato ISO;
4. o que `SELECT SUM(valor)` devolve nessa bagunça — e por que o número está errado.

### AP3 — Mudando o tipo `[Aplicação · ~25 min · os quatro passos]`

**Tarefa.** Uma tabela guarda preços em `REAL` (reais com centavos) e precisa passar a guardar centavos em `INTEGER`. Execute a migração completa:

1. crie a tabela com 6 linhas em `REAL`, incluindo valores como `19.99` e `0.1`;
2. **antes** de migrar, some tudo e anote o resultado;
3. execute os quatro passos dentro de `BEGIN`/`COMMIT`, convertendo os valores;
4. some de novo e compare;
5. explique a diferença, se houver, e diga qual dos dois totais é o correto.

## Desafio

### D1 — O schema da biblioteca `[Desafio · ~50 min · um schema com as decisões escritas]`

**Tarefa.** Projete e crie o schema de uma biblioteca: **livros**, **exemplares** (um livro tem vários), **leitores** e **empréstimos**. Todas as tabelas `STRICT`, script reexecutável, ordem de criação respeitando as dependências.

Entregue junto um `decisoes.md` com:

- **(a)** para cada coluna: o tipo, se é `NOT NULL`, e **por quê** — uma linha por coluna;
- **(b)** as três decisões de modelagem que você tomou (por exemplo: o empréstimo aponta para o livro ou para o exemplar? a data de devolução é nula enquanto o livro está fora?);
- **(c)** **uma decisão que você considerou de duas formas** — escreva as duas, e o critério que desempatou;
- **(d)** três perguntas que você faria ao cliente antes de dar o schema por pronto;
- **(e)** um teste: insira dados que **deveriam** ser recusados e mostre que são.

**Fecho:** 5 linhas sobre por que um schema é mais difícil de mudar que uma consulta — e o que isso implica para a pressa.

<details><summary>💡 Dica 1 (conceito)</summary>
A pergunta de (b) sobre livro × exemplar é a que estrutura tudo: quem é emprestado é o objeto físico, não o título. Um livro tem ISBN; um exemplar tem um código de patrimônio.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
"Data de devolução nula enquanto está emprestado" é conveniente e tem custo: toda consulta de empréstimos em aberto passa a depender de `IS NULL` (03.03), e um `NULL` inesperado se propaga (03.09). A alternativa é uma coluna `status`. Não há resposta única — o que se avalia é o critério.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`livros(id, isbn, titulo, autor, ano)` → `exemplares(id, livro_id, codigo, estado)` → `leitores(id, nome, documento, cadastro)` → `emprestimos(id, exemplar_id, leitor_id, data_saida, data_prevista, data_devolucao)`. Crie nessa ordem: pai antes de filho.
</details>
