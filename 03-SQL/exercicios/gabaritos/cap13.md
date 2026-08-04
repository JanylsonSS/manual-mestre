# Gabarito — Capítulo 03.13: Constraints e integridade

Leia depois de tentar. Enunciados em [`../cap13.md`](../cap13.md).

> Toda mensagem de erro abaixo é saída real do SQLite 3.37.2, copiada da execução.

## A1 — Preveja a mensagem

| # | Resultado | Mensagem |
|---|---|---|
| 1 | **passa** | — |
| 2 | falha | `UNIQUE constraint failed: socios.cpf` |
| 3 | falha | `CHECK constraint failed: idade >= 18` |
| 4 | **passa** | — (veja abaixo) |
| 5 | falha | `CHECK constraint failed: plano IN ('basico','pleno')` |
| 6 | falha | `NOT NULL constraint failed: socios.plano` |
| 7 | falha | `FOREIGN KEY constraint failed` |
| 8 | falha | `cannot store TEXT value in INTEGER column socios.idade` |

Ao final, a tabela tem **duas** linhas: Ana e Dio.

**O item 4 é o ponto do exercício.** `idade = NULL` numa coluna com `CHECK (idade >= 18)`
**passa**. `NULL >= 18` é desconhecido, e `CHECK` só recusa o comprovadamente falso. A tabela
promete "só maiores de idade" e aceita um sócio de idade desconhecida — que, para efeito de
qualquer relatório, é indistinguível de quem não informou por não poder informar.

**O item 8 é o único que não é restrição.** A mensagem vem do `STRICT` (03.12), não de uma
constraint: é o tipo sendo recusado antes que qualquer `CHECK` opine. Note a ordem das
verificações — se `idade` fosse `'trinta'` numa tabela **sem** `STRICT`, o valor entraria como
texto e o `CHECK (idade >= 18)` compararia texto com número, com resultado que ninguém deveria
depender.

**Sobre o item 7:** a chave estrangeira aponta para a **própria tabela** (`indicado` referencia
`socios(id)`). É uma auto-referência, comum em hierarquias — quem indicou quem, chefe de um
funcionário, categoria pai de uma categoria. As regras são idênticas: o id 999 não existe,
recusado.

## A2 — Passa ou não passa?

| # | Resultado | O que prometeu e não entregou |
|---|---|---|
| 1 | **passa** | `UNIQUE` — `NULL = NULL` é desconhecido, logo nunca é duplicata |
| 2 | **passa** | `CHECK` — `NULL > 0` é desconhecido, e `CHECK` só recusa o falso |
| 3 | **passa** | `PRIMARY KEY` — furo histórico do SQLite em chave não-inteira |
| 4 | falha | nada: `STRICT` fecha o furo (`NOT NULL constraint failed`) |
| 5 | **passa** | nada: `NULL` numa FK é **legítimo** — veja abaixo |
| 6 | **passa** | nada: são valores diferentes — veja abaixo |

**O item 5 não é um buraco, e confundi-lo com um é o erro comum.** Uma chave estrangeira nula
significa "não aponta para ninguém", e isso costuma ser correto: um produto sem categoria, um
funcionário sem chefe, um sócio sem quem o indicasse. A chave estrangeira exige que o valor
**exista** quando há valor; ela não exige que haja valor. Quem quer relação obrigatória escreve
`NOT NULL REFERENCES ...` — os dois, de novo.

**O item 6 é a diferença entre um buraco e uma decisão.** `'Ana@x.com'` e `'ana@x.com'` são
strings distintas, e o `UNIQUE` está funcionando corretamente ao aceitar as duas. O problema é
de **regra de negócio**: e-mail não diferencia maiúsculas, e o banco não sabe disso a menos que
você conte:

```sql
CREATE TABLE m2 (e TEXT UNIQUE COLLATE NOCASE);
INSERT INTO m2 VALUES ('Ana@x.com');
INSERT INTO m2 VALUES ('ana@x.com');
-> Erro de SQL: UNIQUE constraint failed: m2.e
```

`COLLATE NOCASE` muda a regra de comparação da coluna. A alternativa — normalizar para
minúsculas antes de gravar — resolve igual e tem a vantagem de deixar o dado consistente para
quem lê. Nos dois casos, a decisão é sua; **o padrão do banco é o literal**.

## A3 — Qual ação?

| # | Ação | Justificativa |
|---|---|---|
| 1 | Itens do carrinho → carrinho | `CASCADE` | o item não tem existência própria; carrinho apagado, itens vão junto |
| 2 | Pedidos → cliente | **`RESTRICT`** | histórico financeiro; apagar o cadastro não pode apagar as vendas |
| 3 | Produtos → categoria | `SET NULL` | um produto sem categoria continua sendo um produto |
| 4 | Comentários → post | `CASCADE` | comentário sem post não significa nada |
| 5 | Empréstimos → exemplar | **`RESTRICT`** | é registro histórico; e um exemplar emprestado não deveria sumir |
| 6 | Endereços → cliente | **depende** | veja abaixo |

**O item 6 é o interessante, porque a resposta muda com o negócio.** Um endereço de cadastro
(`CASCADE`) some com o cliente sem prejuízo. Mas o endereço **de entrega de um pedido** é parte
do registro fiscal daquela venda: onde a mercadoria foi entregue faz parte da nota. Se as duas
coisas moram na mesma tabela, você tem um problema de modelagem antes de ter um de restrição —
e a solução usual é copiar o endereço para dentro do pedido no momento da compra, pelo mesmo
motivo que `itens_pedido` guarda `preco_unitario_centavos` (03.02).

**O padrão dos itens 2 e 5:** sempre que a palavra "histórico" aparece na descrição, a resposta
tende a `RESTRICT`. Recusar é reversível — você conversa e decide depois. `CASCADE` não é.

## A4 — A regra vai onde?

| # | Regra | Onde | Se violada |
|---|---|---|---|
| 1 | CPF não se repete | **banco** (+app) | dois cadastros da mesma pessoa; corrupção difícil de desfazer |
| 2 | Plano gratuito, 3 projetos | **aplicação** | limite comercial; muda com frequência, e um a mais não corrompe nada |
| 3 | Nota de 1 a 5 | **banco** (+app) | gráficos e médias quebram; `CHECK` |
| 4 | Promoção até 31/08 | **aplicação** | é uma campanha, não uma invariante |
| 5 | Pedido pertence a cliente existente | **banco** | órfão; a FK existe exatamente para isso |
| 6 | Senha com 8 caracteres | **aplicação** | ver abaixo |

**O critério que organiza a tabela:** *se essa regra for violada, dá para consertar depois?* O
item 2 sim — desativa-se um projeto. O item 1 não — dois cadastros duplicados já geraram
pedidos, faturas e histórico, e fundi-los é um projeto.

**O item 6 tem uma razão específica para não ir ao banco:** a senha nunca deveria chegar ao
banco em texto. O que se grava é o *hash*, que tem comprimento fixo independentemente da senha
— um `CHECK (LENGTH(senha) >= 8)` estaria validando o tamanho do hash, o que não significa nada.
A regra tem que ser aplicada **antes** do hash, e portanto na aplicação. É um caso em que a
resposta "banco" revela desconhecimento de como o dado chega lá.

**O "(+app)" dos itens 1 e 3** não é redundância: a restrição no banco garante a invariante, e a
validação na aplicação existe para dar ao usuário uma mensagem em português em vez de
`UNIQUE constraint failed: clientes.cpf`. Papéis diferentes, ambos necessários.

## AP1 — Fechando os buracos

**Os cinco `INSERT` que violam e passam** (executados; cinco de seis entraram):

```sql
INSERT INTO inscricoes VALUES (1, NULL, 'sql', 'meio', 1, 7.0);       -- passa
INSERT INTO inscricoes VALUES (2, NULL, 'sql', 'meio', 1, 7.0);       -- passa: 2 NULL no UNIQUE
INSERT INTO inscricoes VALUES (3, 'a@x.com', NULL, 'meio', 1, 7.0);   -- passa: curso NULL
INSERT INTO inscricoes VALUES (4, 'b@x.com', 'sql', NULL, 1, 7.0);    -- passa: nivel NULL
INSERT INTO inscricoes VALUES (5, 'c@x.com', 'sql', 'meio', NULL, NULL); -- passa: turma e nota NULL
```

**O mecanismo é o mesmo nos cinco:** a coluna não tem `NOT NULL`, e nem `UNIQUE` nem `CHECK`
opinam sobre `NULL`. Cinco regras prometidas, cinco atravessadas pela mesma porta.

**Um bônus que a execução revelou.** O sexto ataque planejado — `nota = 'nove'` — foi
**recusado**:

```
Erro de SQL: CHECK constraint failed: nota BETWEEN 0 AND 10
```

E não pelo motivo que se imagina. A tabela não é `STRICT`, então o texto entraria pela
afinidade; quem barrou foi o **`CHECK`**, porque no SQLite qualquer texto ordena **depois** de
qualquer número. Confira:

```
'nove' BETWEEN 0 AND 10  ->  0        'nove' > 10  ->  1
'5'    BETWEEN 0 AND 10  ->  0
```

Note o segundo: **`'5'` também é recusado.** Um `CHECK` numérico acaba barrando todo valor de
texto — inclusive o que "parece" um número válido. Isso soa como uma proteção de brinde, e é
uma armadilha: a regra que você escreveu para validar **faixa** está recusando por **tipo**, e
a mensagem de erro fala da faixa. Quem receber `CHECK constraint failed: nota BETWEEN 0 AND 10`
ao enviar `'5'` vai procurar o problema no lugar errado. **`STRICT` é que faz o trabalho do
tipo; o `CHECK` faz o da faixa** — e misturar os dois produz diagnósticos enganosos.

**O schema corrigido:**

```sql
CREATE TABLE inscricoes (
    id     INTEGER PRIMARY KEY,
    email  TEXT    NOT NULL UNIQUE COLLATE NOCASE,
    curso  TEXT    NOT NULL CHECK (curso IN ('sql', 'python')),
    nivel  TEXT    NOT NULL CHECK (nivel IN ('inicio', 'meio', 'fim')),
    turma  INTEGER NOT NULL,
    nota   INTEGER CHECK (nota BETWEEN 0 AND 100),  -- ver item 5
    UNIQUE (email, curso)                            -- ver item 5
) STRICT;
```

**Item 5 — o que não era problema de restrição.** Duas coisas:

**`nota REAL`.** Nota é um problema de **tipo**, não de constraint (03.12). Em `REAL`, duas
notas "iguais" a 7,5 podem não ser iguais na comparação, e a média de uma turma carrega o erro
de ponto flutuante. A conversão para inteiro — em décimos ou centésimos, como o dinheiro —
resolve na raiz. Nenhum `CHECK` conserta isso.

**A regra que nenhuma coluna expressa.** "Uma inscrição por pessoa por curso" não é sobre
`email` nem sobre `curso` isoladamente: é sobre o **par**. `UNIQUE(email, curso)` resolve, e
quem procurou o erro coluna a coluna não o encontra. **Nem toda regra cabe numa coluna** — e a
que não cabe é a que mais escapa da revisão.

## AP2 — O alcance do `CASCADE`

**A contagem antecipada, para o cliente 4 (Carlos Menezes):**

```
clientes | pedidos | itens
---------+---------+------
       1 |       3 |     6
```

**Dez linhas** serão removidas ao todo.

**O que o comando exibe:**

```
DELETE FROM clientes WHERE id = 4;
OK. Linhas afetadas: 1
```

**Um.** O contador informa quantas linhas o **comando** atingiu diretamente — as nove removidas
pelo cascateamento não entram na conta.

**Por que a conferência do 03.11 não detecta.** Aquele procedimento compara linhas do ensaio com
linhas afetadas, e aqui os dois números batem perfeitamente: o ensaio (`SELECT ... WHERE id = 4`)
devolve 1, o comando afeta 1. **A conferência passa, e nove linhas de histórico sumiram.** É a
limitação exata do procedimento, e conhecê-la é mais útil que o procedimento em si: ele valida o
alcance do `WHERE`, não o alcance do efeito.

**A correção do procedimento para tabelas com `CASCADE`:** o ensaio precisa contar os
descendentes, não a linha. A consulta da etapa 1 deste exercício **é** o ensaio correto.

**Com `RESTRICT`:**

```
Erro de SQL: FOREIGN KEY constraint failed
```

A diferença de experiência é enorme e vale a reflexão pedida. Com `CASCADE`, quem executa vê
sucesso e segue o dia; a descoberta vem semanas depois, de outra pessoa, olhando um relatório
com um buraco. Com `RESTRICT`, quem executa vê o erro **na hora**, com o contexto todo na
cabeça, e decide o que fazer. **Uma falha imediata é mais barata que um sucesso silencioso
errado** — e é por isso que `RESTRICT` é a escolha padrão quando há dúvida.

## AP3 — A restrição tardia

**1. A auditoria — e são duas perguntas, não uma:**

```sql
SELECT
  (SELECT COUNT(*) FROM clientes WHERE email IS NULL) AS ausentes,
  (SELECT COUNT(*) FROM (
      SELECT email FROM clientes
      WHERE email IS NOT NULL
      GROUP BY email HAVING COUNT(*) > 1
  )) AS duplicados;
```

```
ausentes | duplicados
---------+-----------
       1 |          0
```

**Uma violação: `NOT NULL`. Nenhuma de `UNIQUE`.** Repare no `WHERE email IS NOT NULL` dentro da
subconsulta de duplicados. Sem ele, a auditoria mente — comprovado com três nulos numa tabela
de teste:

```
SELECT e, COUNT(*) FROM g GROUP BY e;        ->  NULL | 3   e   a | 1
duplicados SEM o filtro  ->  1               duplicados COM o filtro  ->  0
```

**`GROUP BY` agrupa os nulos numa linha só** (03.06), enquanto `UNIQUE` nunca os considera
iguais. Duas operações, duas regras opostas para o mesmo `NULL` — e a auditoria escrita sem
cuidado acusa uma duplicata de e-mail que não existe, fazendo alguém procurar um problema
inexistente antes de chegar ao real.

**2. A linha problemática:** id 3, **Beatriz Nogueira**, `email` nulo — plantada no laboratório
desde o 03.01, justamente para chegar até aqui.

**3. As três saídas.**

- **Preencher** com algo como `beatriz@invalido.local`: a restrição passa e o dado vira mentira.
  Alguém vai disparar e-mail para lá, e o relatório de alcance de campanha vai contá-la como
  contatável.
- **Excluir** a cliente: ela tem um pedido concluído de R$ 899,00 — apagar destrói faturamento
  real, e a chave estrangeira recusaria de qualquer forma.
- **Adiar**: aplicar `UNIQUE` agora e `NOT NULL` quando o dado for obtido.

**A escolha justificada: adiar o `NOT NULL`, aplicar o `UNIQUE` já.** As duas regras têm
situações diferentes — `UNIQUE` não é violado por ninguém hoje e pode entrar sem custo; o
`NOT NULL` tem uma violação real que exige uma ação de negócio: alguém precisa ligar para a
Beatriz. Separar as duas é o que permite ganhar metade da proteção hoje em vez de nenhuma.

**4. A migração de quatro passos** (03.12), numa cópia:

```sql
BEGIN;
CREATE TABLE clientes_novo (
    id            INTEGER PRIMARY KEY,
    nome          TEXT NOT NULL,
    email         TEXT UNIQUE COLLATE NOCASE,   -- UNIQUE sim, NOT NULL ainda nao
    cidade        TEXT,
    data_cadastro TEXT NOT NULL
) STRICT;
INSERT INTO clientes_novo SELECT id, nome, email, cidade, data_cadastro FROM clientes;
DROP TABLE clientes;
ALTER TABLE clientes_novo RENAME TO clientes;
COMMIT;
```

**Atenção ao passo 3 num banco com chaves estrangeiras:** `DROP TABLE clientes` com `pedidos`
referenciando-a é recusado, e mesmo onde passa, as FKs que apontavam para a tabela antiga
precisam ser recriadas. É a complicação que o 03.12 mencionou de passagem e que aqui tem
consequência: **migrar a tabela pai é sensivelmente mais caro que migrar uma folha.**

**5. A prova:**

```sql
INSERT INTO clientes (nome, email, data_cadastro)
VALUES ('Teste', 'ana@aurora.com', '2026-08-04');
-> Erro de SQL: UNIQUE constraint failed: clientes.email
```

A tabela antiga aceitaria; a nova recusa.

## D1 — O schema blindado

```sql
CREATE TABLE emprestimos (
    id             INTEGER PRIMARY KEY,
    exemplar_id    INTEGER NOT NULL REFERENCES exemplares(id) ON DELETE RESTRICT,
    leitor_id      INTEGER NOT NULL REFERENCES leitores(id)   ON DELETE RESTRICT,
    data_saida     TEXT    NOT NULL CHECK (data_saida LIKE '____-__-__'),
    data_prevista  TEXT    NOT NULL,
    data_devolucao TEXT,
    CHECK (data_prevista >= data_saida),
    CHECK (data_devolucao IS NULL OR data_devolucao >= data_saida)
) STRICT;
```

**O `CHECK` que compara duas colunas** é declarado no nível da **tabela**, depois de todas as
colunas — dentro de uma coluna, ele não enxerga as outras. E repare no `IS NULL OR`:

```sql
-- SEM o IS NULL OR:
CREATE TABLE emp2 (saida TEXT NOT NULL, devolucao TEXT, CHECK (devolucao >= saida));
INSERT INTO emp2 VALUES ('2026-08-04', NULL);
-> OK. Linhas afetadas: 1
```

O `NULL` passa de qualquer jeito. Então o `IS NULL OR` não está ali para *permitir* o nulo — ele
já passaria. Está ali para **documentar que o nulo é intencional**, e para que a intenção
sobreviva ao dia em que alguém acrescentar `NOT NULL` à coluna. Sem o `OR`, o `CHECK` é uma
armadilha que funciona por acidente.

E a versão com o `OR` recusa o que deve recusar:

```sql
INSERT INTO emp VALUES (1, '2026-08-04', '2026-08-01');
-> Erro de SQL: CHECK constraint failed: devolucao IS NULL OR devolucao >= saida
```

**(c) Quantos ataques o `NULL` viabilizou.** Num schema sem `NOT NULL` sistemático, a proporção
costuma ficar entre metade e dois terços dos ataques bem-sucedidos. O que isso diz sobre o
hábito de deixar colunas opcionais: **"opcional" não é um estado neutro.** Toda coluna sem
`NOT NULL` é uma porta aberta em todas as outras restrições daquela coluna ao mesmo tempo — e a
decisão de deixá-la aberta costuma ser tomada por omissão, não por análise.

**(e) O ataque que restrição nenhuma bloqueia.** "Um leitor não pode ter mais de 3 empréstimos
em aberto." Um `CHECK` avalia **uma linha por vez** e não pode contar linhas de outras — a
restrição não tem como saber quantos empréstimos já existem. A regra precisa morar num
*trigger*, numa transação da aplicação que confere antes de inserir, ou num serviço que
serializa a operação. E há uma armadilha de concorrência: duas inserções simultâneas podem
ambas contar 3 e ambas inserir, resultando em 5. É o assunto do 03.15.

**O fecho.** Reler o schema verifica o que você **pensou**; escrever os ataques verifica o que
você **construiu**. A releitura é feita pela mesma cabeça que criou o schema, com os mesmos
pontos cegos — você lê `email TEXT UNIQUE` e sua mente completa "único e obrigatório", porque
era isso que você queria dizer. O ataque não completa nada: ele insere dois `NULL` e mostra o
resultado. **É a diferença entre revisar a intenção e testar o comportamento**, e é o mesmo
motivo pelo qual código sem teste parece correto para quem o escreveu.

---

## Erros mais comuns

1. **Achar que `UNIQUE` implica obrigatório.** Vários `NULL` cabem.
2. **Achar que `CHECK` cobre o `NULL`.** Não cobre; desconhecido não é falso.
3. **Tratar `NULL` numa FK como buraco.** É legítimo — significa "não aponta para ninguém".
4. **Esperar que `UNIQUE` ignore maiúsculas.** `COLLATE NOCASE` ou normalização.
5. **Procurar a regra numa coluna quando ela é sobre um par.** `UNIQUE(a, b)`.
6. **Confiar na conferência de linhas afetadas com `CASCADE`.** Ela conta o comando, não o efeito.
7. **Validar tamanho de senha no banco.** O que chega lá é o hash.
8. **`CHECK` fazendo o trabalho do tipo.** Funciona por acidente e falha em silêncio.
9. **Adicionar restrição sem auditar.** As duas perguntas — ausentes e duplicados — são distintas.
