# Exercícios — Capítulo 03.13: Constraints e integridade

> **Antes de tudo:** `python codigo/cap12/preparar_ddl.py`. Os exercícios de schema rodam com
> `AURORA_BANCO=dados/ddl.db`. O AP3 e o mini projeto usam o `aurora.db` — só para **ler**.

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap13.md`](gabaritos/cap13.md).

## Aquecimento

### A1 — Preveja a mensagem `[Aquecimento · ~10 min · qual restrição cai?]`

**Tarefa.** Sobre esta tabela, diga para cada comando: passa ou falha? Se falha, **escreva a mensagem** que você espera — depois compare com a real.

```sql
CREATE TABLE socios (
    id       INTEGER PRIMARY KEY,
    cpf      TEXT    NOT NULL UNIQUE,
    nome     TEXT    NOT NULL,
    idade    INTEGER CHECK (idade >= 18),
    plano    TEXT    NOT NULL CHECK (plano IN ('basico','pleno')),
    indicado INTEGER REFERENCES socios(id)
) STRICT;
```

1. `INSERT INTO socios VALUES (1,'111','Ana',30,'basico',NULL);`
2. `INSERT INTO socios VALUES (2,'111','Bia',25,'pleno',NULL);`
3. `INSERT INTO socios VALUES (3,'222','Cid',17,'basico',NULL);`
4. `INSERT INTO socios VALUES (4,'333','Dio',NULL,'basico',NULL);`
5. `INSERT INTO socios VALUES (5,'444','Eva',40,'ouro',NULL);`
6. `INSERT INTO socios VALUES (6,'555','Fla',22,NULL,NULL);`
7. `INSERT INTO socios VALUES (7,'666','Gil',33,'pleno',999);`
8. `INSERT INTO socios VALUES (8,'777','Hel','trinta','pleno',1);`

### A2 — Passa ou não passa? `[Aquecimento · ~10 min · o NULL nas restrições]`

**Tarefa.** Preveja e confirme. Para cada uma que passar, diga **qual restrição prometeu e não entregou**:

1. Três `NULL` numa coluna `UNIQUE`.
2. `NULL` numa coluna com `CHECK (x > 0)`.
3. `NULL` numa coluna `TEXT PRIMARY KEY` (sem `STRICT`).
4. `NULL` numa coluna `TEXT PRIMARY KEY` **com** `STRICT`.
5. `NULL` numa coluna `INTEGER REFERENCES pai(id)`.
6. `'Ana@x.com'` e `'ana@x.com'` numa coluna `UNIQUE`.

### A3 — Qual ação? `[Aquecimento · ~10 min · CASCADE, SET NULL ou RESTRICT]`

**Tarefa.** Para cada relação, escolha a ação de `ON DELETE` e justifique em uma linha:

1. Itens de um carrinho de compras → carrinho
2. Pedidos → cliente
3. Produtos → categoria
4. Comentários de um post → post
5. Empréstimos → exemplar de livro
6. Endereços de entrega → cliente

### A4 — A regra vai onde? `[Aquecimento · ~10 min · banco ou aplicação?]`

**Tarefa.** Classifique cada regra em **banco**, **aplicação** ou **ambos**, e diga o que acontece se ela for violada:

1. "CPF não se repete."
2. "Cliente do plano gratuito só pode ter 3 projetos."
3. "Nota de avaliação vai de 1 a 5."
4. "A promoção de inverno dá 20% até 31 de agosto."
5. "Todo pedido pertence a um cliente que existe."
6. "Senha precisa de 8 caracteres."

## Aplicação

### AP1 — Fechando os buracos `[Aplicação · ~25 min · o UNIQUE e o CHECK que não seguram]`

**Tarefa.** Este schema promete cinco regras e cumpre duas:

```sql
CREATE TABLE inscricoes (
    id       INTEGER PRIMARY KEY,
    email    TEXT UNIQUE,
    curso    TEXT CHECK (curso IN ('sql','python')),
    nivel    TEXT CHECK (nivel IN ('inicio','meio','fim')),
    turma    INTEGER,
    nota     REAL CHECK (nota BETWEEN 0 AND 10)
);
```

1. Escreva **um `INSERT` por regra** que a viole e mesmo assim passe — são cinco.
2. Para cada um, explique o mecanismo exato que permitiu.
3. Reescreva o schema fechando todos os buracos.
4. Reexecute os cinco ataques e mostre as cinco recusas.
5. **Um dos problemas do schema não é de restrição nenhuma.** Encontre-o.

### AP2 — O alcance do `CASCADE` `[Aplicação · ~20 min · o DELETE que mente]`

**Tarefa.** Recrie as quatro tabelas da Aurora com `ON DELETE CASCADE` em toda a cadeia (`clientes` → `pedidos` → `itens_pedido`) e carregue os dados do laboratório.

1. **Antes** de apagar, escreva a consulta que conta quantas linhas de **cada tabela** um `DELETE FROM clientes WHERE id = 4` removeria.
2. Execute o `DELETE` e leia a saída de linhas afetadas.
3. Compare o número exibido com o número real de linhas que sumiram.
4. Explique a diferença — e por que a conferência do 03.11 não a detecta.
5. Refaça com `RESTRICT` e descreva a diferença de experiência para quem executa.

### AP3 — A restrição tardia `[Aplicação · ~25 min · auditar, corrigir, aplicar]`

**Tarefa.** Você quer aplicar `email TEXT NOT NULL UNIQUE` na tabela `clientes` da Aurora.

1. **Audite:** quantas linhas violariam a regra hoje? Escreva a consulta que descobre — e note que são **duas** perguntas diferentes (ausentes e duplicados).
2. Liste as linhas problemáticas com nome e id.
3. Para cada uma, escreva as três saídas possíveis (preencher, excluir, adiar) e escolha uma, justificando.
4. Como não há `ADD CONSTRAINT` no SQLite (03.12), execute a migração de quatro passos numa cópia, com a restrição nova.
5. Prove que a tabela nova recusa o que a antiga aceitava.

## Desafio

### D1 — O schema blindado `[Desafio · ~50 min · tente quebrar o que você construiu]`

**Tarefa.** Pegue o schema da biblioteca do D1 do 03.12 e blinde-o com todas as restrições cabíveis — incluindo pelo menos um `CHECK` que **compare duas colunas** (a devolução não pode ser anterior à saída).

Depois escreva `ataques.sql` com **quinze** comandos que deveriam ser recusados. Sugestões para começar: e-mail duplicado; documento nulo; empréstimo sem leitor; exemplar de livro inexistente; devolução anterior à saída; ano de publicação no futuro; estado do exemplar fora do conjunto; dois exemplares com o mesmo código de patrimônio; leitor com data de cadastro em formato brasileiro.

Execute os quinze e entregue um relatório com:

- **(a)** quantos passaram na primeira rodada;
- **(b)** para cada um que passou: a regra que faltava e a restrição que a implementa;
- **(c)** **quantos dos ataques bem-sucedidos foram viabilizados pelo `NULL`** — e o que isso diz sobre o hábito de deixar colunas opcionais;
- **(d)** o schema corrigido, com os quinze sendo recusados;
- **(e)** um ataque que você **não** conseguiu bloquear com restrição nenhuma, e onde essa regra teria que morar.

**Fecho:** 5 linhas sobre por que escrever os ataques é diferente de reler o schema.

<details><summary>💡 Dica 1 (conceito)</summary>
Um `CHECK` que compara duas colunas é declarado no nível da **tabela**, depois das colunas — não dentro de uma delas. E ele precisa tratar o `NULL` explicitamente, ou a linha com devolução nula será recusada.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para (e): pense numa regra que dependa de **contagem** ("um leitor não pode ter mais de 3 empréstimos em aberto") ou de **tempo** ("não emprestar a quem tem atraso"). Restrições avaliam uma linha; essas regras precisam olhar várias.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Schema blindado → `ataques.sql` numerado com o resultado esperado em comentário → execução → tabela de resultados (ataque, passou?, restrição faltante) → schema v2 → reexecução → relatório.
</details>
