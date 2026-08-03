# Exercícios — Capítulo 03.02: Tabelas, linhas e chaves

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap02.md`](gabaritos/cap02.md).

## Aquecimento

### A1 — Serve como chave primária? `[Aquecimento · ~10 min · aprove ou reprove]`

**Tarefa.** Para cada candidata, decida se serve como chave primária e **justifique** em uma linha:

1. `email` numa tabela de clientes
2. `id` inteiro autonumerado
3. `cpf` numa tabela de pessoas
4. `nome_completo` numa tabela de clientes
5. `codigo_barras` numa tabela de produtos
6. `numero_pedido` gerado pelo próprio sistema, sequencial e imutável
7. `data_cadastro` numa tabela de clientes
8. A combinação (`pedido_id`, `produto_id`) numa tabela de itens

### A2 — Qual erro? `[Aquecimento · ~10 min · a mensagem do banco]`

**Tarefa.** Para cada operação sobre o laboratório, diga se dá certo ou qual mensagem de erro aparece:

1. `INSERT INTO pedidos VALUES (99, 3, '2026-08-01', 'concluido');`
2. `INSERT INTO pedidos VALUES (1, 3, '2026-08-01', 'concluido');`
3. `INSERT INTO clientes VALUES (99, 'Novo', NULL, 'santos', '2026-08-01');`
4. `INSERT INTO clientes VALUES (99, NULL, 'n@a.com', 'santos', '2026-08-01');`
5. `DELETE FROM clientes WHERE id = 7;`
6. `DELETE FROM clientes WHERE id = 2;`

### A3 — De que lado mora a chave estrangeira? `[Aquecimento · ~10 min · um para muitos]`

**Tarefa.** Para cada relação, diga em qual tabela fica a chave estrangeira e como ela se chamaria:

1. Um autor escreve muitos livros.
2. Um departamento tem muitos funcionários.
3. Uma postagem tem muitos comentários.
4. Uma turma tem muitos alunos, e um aluno cursa muitas turmas.
5. Um pedido tem muitos itens, e cada item se refere a um produto.

### A4 — Lendo o schema `[Aquecimento · ~10 min · só com consulta]`

**Tarefa.** Responda usando **apenas** consultas ao schema (`sqlite_master`, `pragma_table_info`, `pragma_foreign_key_list`), sem abrir o arquivo do laboratório:

1. Quantas tabelas o banco tem?
2. Quais colunas de `itens_pedido` são obrigatórias?
3. Qual é a chave primária de `produtos`?
4. Para quais tabelas `itens_pedido` aponta?
5. A tabela `clientes` aponta para alguma outra?

## Aplicação

### AP1 — As quatro recusas `[Aplicação · ~20 min · o banco defendendo]`

**Tarefa.** Provoque, uma a uma, as quatro violações e registre a mensagem **exata**: (1) chave estrangeira inexistente; (2) chave primária duplicada; (3) coluna `NOT NULL` vazia; (4) exclusão de linha com dependentes. Para cada uma, escreva em uma linha: qual regra foi violada, e o que a mensagem informa além do tipo do erro. Ao final, recrie o laboratório.

### AP2 — Lendo um banco desconhecido `[Aplicação · ~20 min · engenharia reversa]`

**Tarefa.** Imagine que você acabou de chegar num projeto e recebeu apenas o arquivo `aurora.db`. Usando **somente** consultas ao schema, produza um documento de uma página com: (1) a lista de tabelas; (2) para cada uma, as colunas com tipo e obrigatoriedade; (3) o diagrama das ligações; (4) três frases descrevendo o que o sistema faz, deduzidas do modelo. Compare depois com a seção 6 do capítulo 03.01.

### AP3 — A lista na coluna `[Aplicação · ~20 min · corrigindo um modelo]`

**Tarefa.** Um sistema guarda assim:

```text
clientes(id, nome, pedidos_ids)
   1 | Fernanda Lima | "1,2,5,9,13"
```

(1) Liste **quatro** problemas concretos desse desenho; (2) mostre como responder "quantos pedidos a Fernanda fez" nos dois modelos; (3) mostre por que `LIKE '%,5,%'` falha; (4) proponha a correção e diga onde fica a chave estrangeira.

## Desafio

### D1 — O modelo da biblioteca `[Desafio · ~45 min · as três relações]`

**Tarefa.** Uma biblioteca precisa controlar: **livros** (título, ISBN, ano), **exemplares** físicos (o mesmo livro pode ter 5 cópias), **leitores**, **empréstimos** e **autores** (um livro pode ter vários autores; um autor, vários livros).

- **(a)** Proponha as tabelas com colunas e tipos;
- **(b)** marque a chave primária de cada uma e **justifique** por que não usou ISBN nem CPF;
- **(c)** declare todas as chaves estrangeiras e diga de que lado cada uma mora;
- **(d)** identifique qual relação é **muitos-para-muitos** e mostre a tabela intermediária;
- **(e)** para cada FK, decida o comportamento `ON DELETE` e justifique em uma linha;
- **(f)** escreva o `CREATE TABLE` de **duas** delas e execute no laboratório (use `AURORA_BANCO=biblioteca.db`), provando que as restrições funcionam com uma inserção inválida.

**Fecho:** 5 linhas sobre por que "exemplar" precisa ser uma tabela separada de "livro".

<details><summary>💡 Dica 1 (conceito)</summary>
Todo substantivo do enunciado é candidato a tabela. A pergunta que revela a relação é "quantos X para cada Y, e quantos Y para cada X?" — se a resposta for "muitos" dos dois lados, falta uma tabela no meio.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
"O mesmo livro pode ter 5 cópias" é a frase-chave: o que se empresta é o **exemplar**, não o livro. O empréstimo aponta para exemplar.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Tabelas e colunas → PKs com justificativa → FKs com o lado → a tabela de ligação autores↔livros → ON DELETE de cada uma → dois CREATE TABLE executados → a inserção que falha.
</details>
