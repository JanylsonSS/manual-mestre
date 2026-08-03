# Gabaritos — Capítulo 03.02

Abra somente após tentativa honesta.

## A1 — Serve como chave primária?

| # | Candidata | Serve? | Por quê |
|---|---|---|---|
| 1 | `email` | **Não** | Muda; pode ser desconhecido (`NULL` não é permitido); é regra de negócio |
| 2 | `id` autonumerado | **Sim** | Único, não nulo, estável — e sem significado, por isso permanente |
| 3 | `cpf` | **Não** | Estrangeiro pode não ter; há casos de duplicidade e correção; é dado sensível replicado em toda FK |
| 4 | `nome_completo` | **Não** | Nem único nem estável (casamento, correção de grafia) |
| 5 | `codigo_barras` | **Não** (como PK) | Produto pode não ter; o código pode ser reaproveitado pelo fabricante. Vira atributo com `UNIQUE` |
| 6 | `numero_pedido` do sistema | **Sim** | É uma chave artificial com outro nome: gerado internamente, sequencial, imutável |
| 7 | `data_cadastro` | **Não** | Duas pessoas se cadastram no mesmo instante |
| 8 | (`pedido_id`, `produto_id`) | **Depende** | Serve como chave **composta** se um produto aparece uma vez por pedido; se puder aparecer duas (embalagens diferentes), não serve |

**Critério:** 8/8 com justificativa. O item 8 é o mais interessante: chave composta é legítima, e a decisão depende de uma **regra de negócio** que o enunciado não dá — reconhecer isso vale mais que escolher um lado.

## A2 — Qual erro?

1. **Dá certo** — o cliente 3 existe e o id 99 está livre.
2. **`UNIQUE constraint failed: pedidos.id`** — o id 1 já existe.
3. **Dá certo** — `email` aceita `NULL` (não é `NOT NULL`).
4. **`NOT NULL constraint failed: clientes.nome`**.
5. **Dá certo** — o Rafael (id 7) não tem pedidos.
6. **`FOREIGN KEY constraint failed`** — a Ana (id 2) tem 4 pedidos.

**Critério:** 6/6. O contraste entre 3 e 4 é o ponto: `NULL` é permitido onde a coluna aceita, e proibido onde não aceita — a regra é declarada, não adivinhada. O contraste entre 5 e 6 mostra que a integridade referencial só bloqueia quando há **dependentes de fato**.

## A3 — De que lado mora a chave estrangeira?

1. `livros.autor_id` (do lado "muitos" — mas veja o item 4 e o desafio: se um livro tem vários autores, muda)
2. `funcionarios.departamento_id`
3. `comentarios.postagem_id`
4. **Nenhum dos dois** — é muitos-para-muitos; exige `matriculas(turma_id, aluno_id)`
5. `itens_pedido.pedido_id` **e** `itens_pedido.produto_id` — duas FKs na mesma tabela

**Critério:** 5/5. O item 4 é o que o exercício existe para pegar: quando os dois lados são "muitos", nenhuma coluna resolve — falta uma tabela.

## A4 — Lendo o schema

**Comandos e respostas:**

1. `SELECT COUNT(*) FROM sqlite_master WHERE type='table'` → **4**
2. `SELECT name, "notnull" FROM pragma_table_info('itens_pedido')` → obrigatórias: `pedido_id`, `produto_id`, `quantidade`, `preco_unitario_centavos` (o `id` aparece com `notnull=0` — veja a observação)
3. `SELECT name FROM pragma_table_info('produtos') WHERE pk=1` → **`id`**
4. `SELECT "table" FROM pragma_foreign_key_list('itens_pedido')` → **`pedidos`** e **`produtos`**
5. `SELECT COUNT(*) FROM pragma_foreign_key_list('clientes')` → **0**; `clientes` não aponta para ninguém

**Observação que confunde (item 2):** a coluna `id` aparece como `notnull = 0`, e mesmo assim não aceita `NULL`. É uma peculiaridade do SQLite: `INTEGER PRIMARY KEY` é um apelido para o identificador interno da linha, e a obrigatoriedade vem de ser chave primária, não da marcação `NOT NULL`. Em PostgreSQL, a chave primária aparece explicitamente como `NOT NULL`.

**Critério:** 5/5 respondidas **sem** abrir o arquivo — é a habilidade que o exercício treina.

## AP1 — As quatro recusas

**Mensagens exatas:**

```text
Erro de SQL: FOREIGN KEY constraint failed
Erro de SQL: UNIQUE constraint failed: clientes.id
Erro de SQL: NOT NULL constraint failed: clientes.nome
Erro de SQL: FOREIGN KEY constraint failed
```

**O que a mensagem informa além do tipo:** nas duas do meio, a **tabela e a coluna** exatas (`clientes.id`, `clientes.nome`) — diagnóstico completo sem investigação. As de chave estrangeira são as menos informativas do SQLite: não dizem qual FK falhou, o que incomoda em tabelas com várias. Em PostgreSQL a mensagem nomeia a constraint e o valor recusado, e é um dos motivos práticos de o dialeto de produção ser mais confortável para depurar.

**Critério:** as quatro provocadas de verdade, com a mensagem copiada literalmente, e o laboratório recriado ao final.

## AP2 — Lendo um banco desconhecido

**Consultas de referência:**

```sql
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;
SELECT name, type, "notnull", pk FROM pragma_table_info('clientes');
SELECT "table", "from", "to" FROM pragma_foreign_key_list('pedidos');
```

**Três frases dedutíveis (referência):** o sistema registra **clientes** com cidade e data de cadastro · cada cliente faz **pedidos** com data e status, o que indica um ciclo de vida (pendente → concluído → cancelado) · cada pedido tem **itens** que guardam quantidade e o **preço no momento da venda**, o que revela que preços mudam e o histórico precisa ser preservado.

**Ponto de atenção:** a terceira frase é a mais valiosa e a que exige interpretação — a existência de `preco_unitario_centavos` em `itens_pedido`, **duplicando** aparentemente o preço de `produtos`, só faz sentido se o preço variar no tempo. Schemas contam decisões de negócio a quem sabe ler.

**Critério:** o documento produzido sem abrir o arquivo; as três frases interpretando o modelo, não descrevendo colunas.

## AP3 — A lista na coluna

**Quatro problemas:**

1. **Sem integridade** — nada garante que o pedido 13 exista; o banco não consegue verificar texto.
2. **Consulta por texto** — filtrar exige `LIKE`, que é lento e não usa índice de forma útil.
3. **Sem agregação** — contar, somar ou juntar exige quebrar a string em código de aplicação.
4. **Limite de tamanho e escrita concorrente** — acrescentar um pedido exige ler, alterar a string e regravar; duas escritas simultâneas perdem uma.

**Item 2 — a comparação:**

```sql
-- Modelo errado: impossível em SQL puro; exige quebrar a string fora do banco
-- Modelo correto:
SELECT COUNT(*) FROM pedidos WHERE cliente_id = 1;
```

**Item 3 — por que `LIKE '%,5,%'` falha:** ele casa com `"15"` e `"25"` (a substring `,5,` não existe em `"1,15,2"`, mas `%5%` casaria; e mesmo com vírgulas, `"...,5,..."` não encontra o `5` quando ele é o **primeiro** ou o **último** da lista, porque falta a vírgula de um dos lados). Corrigir exige remendos como concatenar vírgulas nas pontas — sintoma claro de que o modelo está errado.

**Item 4 — correção:** remover a coluna `pedidos_ids`; a chave estrangeira `cliente_id` mora em `pedidos`, do lado "muitos". A lista deixa de ser guardada e passa a ser **consultada**.

**Critério:** os quatro problemas, com o item 3 demonstrando um caso concreto de falha do `LIKE`.

## D1 — O modelo da biblioteca

**Tabelas de referência:**

```text
   autores            livros_autores          livros              exemplares
   -------            --------------          ------              ----------
   id  ◄───────────── autor_id                id  ◄────────────── livro_id
   nome               livro_id ─────────────► titulo              id  ◄──────┐
                                              isbn                codigo     │
                                              ano                 estado     │
                                                                             │
   leitores                        emprestimos                               │
   --------                        -----------                               │
   id  ◄──────────────────────────  leitor_id                                │
   nome                             exemplar_id ────────────────────────────┘
   email                            data_emprestimo
                                    data_devolucao
```

**(b) PKs:** todas artificiais (`id` inteiro). **ISBN não serve** porque livros antigos não têm, edições diferentes compartilham problemas de padronização, e é dado externo (regra de terceiros pode mudar). **CPF não serve** pelos mesmos motivos do A1: opcional para estrangeiros, sensível, e replicá-lo em toda FK espalha dado pessoal pelo banco.

**(d) Muitos-para-muitos:** `livros ↔ autores`, resolvida por `livros_autores(livro_id, autor_id)`. Note que `livros ↔ exemplares` **não** é muitos-para-muitos: um exemplar pertence a um único livro.

**(e) `ON DELETE` de referência:**

| FK | Comportamento | Por quê |
|---|---|---|
| `exemplares.livro_id` | `RESTRICT` | Apagar um livro com exemplares no acervo é erro de operação |
| `livros_autores.*` | `CASCADE` | A ligação não existe sem os dois lados; é ligação pura |
| `emprestimos.exemplar_id` | `RESTRICT` | Apagar exemplar emprestado esconderia um item fora da biblioteca |
| `emprestimos.leitor_id` | `RESTRICT` | Histórico de empréstimo é registro; anonimizar, não apagar (a pegadinha da seção 15) |

**(f) Prova esperada:** um `INSERT` de empréstimo com `exemplar_id` inexistente devolvendo `FOREIGN KEY constraint failed`.

**Reflexão esperada (por que "exemplar" é tabela separada):** porque **livro** e **exemplar** são coisas de naturezas diferentes. Livro é a obra — título, ISBN, ano, autores —, e existe uma vez, independentemente de quantas cópias a biblioteca tenha. Exemplar é o objeto físico na prateleira, com estado de conservação, código de tombo e histórico próprio de empréstimos. Juntá-los numa tabela só forçaria uma escolha ruim: ou repetir título, ISBN e ano em cada cópia (o problema de duplicação do 03.01, com todas as consequências), ou perder a capacidade de saber **qual** cópia está com quem. E a prova de que a separação é correta está na pergunta que só o modelo separado responde: *"o livro está disponível?"* — que significa "existe algum exemplar sem empréstimo em aberto", uma pergunta sobre exemplares, não sobre o livro.

**Critério de "está bom":** a distinção livro/exemplar identificada sem dica; a tabela de ligação `livros_autores` presente; o `ON DELETE` de cada FK justificado (e não todos iguais); os dois `CREATE TABLE` executados de verdade, com a inserção inválida recusada.
