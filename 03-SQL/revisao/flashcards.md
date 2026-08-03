# Flashcards — Módulo 03

Tabela acumulativa: cada capítulo acrescenta seus 5 cards (IDs `MM.CC-Fn`). Compatível com importação no Anki via CSV.

| ID | Frente | Verso |
|---|---|---|
| 03.01-F1 | Quais são os quatro problemas que um banco relacional resolve e o CSV não? | **Duplicação** (um fato em vários lugares) · **integridade** (nada impede dado inválido) · **concorrência** (quem salva por último vence) · **busca** (ler tudo, sem cruzar fontes). |
| 03.01-F2 | Explique com suas palavras: o que significa SQL ser uma linguagem declarativa? | (Elaboração) Você descreve **o que** quer, não **como** buscar. O laço e o acumulador do Python somem; o otimizador do banco decide o plano de execução. |
| 03.01-F3 | Preveja: a Fernanda muda de e-mail. Quantas alterações no CSV de vendas e quantas no banco? | (Previsão) No CSV, **uma por linha de venda dela**; no banco, **uma** — a linha na tabela `clientes`. Os pedidos apontam para o `id`, nunca tiveram cópia do e-mail. |
| 03.01-F4 | Qual a diferença entre chave primária e chave estrangeira? | (Decisão) Primária **identifica** a linha unicamente na tabela; estrangeira **aponta** para a primária de outra tabela — e habilita a integridade referencial. |
| 03.01-F5 | O que é `NULL` e o que ele **não** é? | Ausência de valor. **Não** é string vazia, **não** é zero, **não** é `False`. Comparações com `=` não funcionam: use `IS NULL` (03.03). |
| 03.02-F1 | Quais as três propriedades de uma boa chave primária? | **Única**, **não nula** e **estável** (nunca muda). Daí a chave artificial (`id` inteiro sem significado de negócio) ser a prática dominante. |
| 03.02-F2 | Explique com suas palavras: o que é integridade referencial? | (Elaboração) A garantia, **imposta pelo banco**, de que toda chave estrangeira aponta para uma linha existente. Ele recusa referência inexistente e recusa apagar quem tem dependentes. |
| 03.02-F3 | Preveja: `INSERT` de um pedido com `cliente_id = 999`, que não existe. O que acontece? | (Previsão) Recusado: `FOREIGN KEY constraint failed`. Nada é gravado, nada é criado automaticamente. **No SQLite, só com `PRAGMA foreign_keys = ON`.** |
| 03.02-F4 | Numa relação um-para-muitos, de que lado mora a chave estrangeira? | (Decisão) Do lado **"muitos"** — o pedido guarda `cliente_id`. O cliente não guarda lista de pedidos: coluna não comporta lista de tamanho variável. |
| 03.02-F5 | Por que o e-mail é uma péssima chave primária, mesmo sendo único? | Pode **mudar** (toda referência mudaria junto), pode ser **desconhecido** (chave não aceita `NULL`), e é regra de negócio (que muda). Fica como atributo, com `UNIQUE` se preciso. |
| 03.03-F1 | Por que `WHERE email = NULL` devolve zero linhas, mesmo havendo nulos? | Comparação com `NULL` é **desconhecida**, nunca verdadeira, e o `WHERE` só deixa passar o verdadeiro. O operador correto é `IS NULL`. |
| 03.03-F2 | Explique com suas palavras: por que `WHERE cidade <> 'campinas'` esconde linhas? | (Elaboração) Linhas com `cidade` nula não satisfazem nem `=` nem `<>` — o banco não sabe qual é a cidade. Some das duas contagens. Correção: `OR cidade IS NULL`. |
| 03.03-F3 | Preveja: `WHERE a = 1 OR b = 2 AND c = 3`. Como o banco lê? | (Previsão) `a = 1 OR (b = 2 AND c = 3)` — **`AND` tem precedência sobre `OR`**. Use parênteses sempre que misturar os dois. |
| 03.03-F4 | Quando usar `IN` e quando usar `BETWEEN`? | (Decisão) `IN` para lista de valores discretos (`categoria IN ('audio','video')`); `BETWEEN` para faixa contínua, **inclusiva nas duas pontas** (≠ `range` do Python). |
| 03.03-F5 | Por que evitar `SELECT *` em código de produção? | Traz colunas não usadas (custo) e **quebra em silêncio** quando a tabela muda. Em exploração manual, é apropriado. |
