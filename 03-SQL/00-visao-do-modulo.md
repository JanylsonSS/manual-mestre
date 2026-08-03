# Módulo 03 — SQL

> **Fase 1 — Fundamentos** · 16 capítulos · ~45 h · Profundidade: N1 → N2 · _Gerado sob spec 3.0.0_

## Missão do módulo

Você sai deste módulo **conversando com bancos de dados relacionais** — consultando, modificando e, o que mais importa, **modelando**. É a virada mental da Fase 1: até aqui você **percorreu** dados linha a linha, dizendo ao computador *como* buscar; a partir de agora você **descreve** o que quer e deixa o banco decidir o caminho.

SQL é, junto com Python, a outra metade do trabalho de engenharia de dados. Não é uma linguagem que se aprende "por cima": ela aparece em toda vaga da área, em toda entrevista técnica, e continua sendo a ferramenta mais direta para responder perguntas sobre dados — cinquenta anos depois de inventada, e sem substituto à vista.

O laboratório é o **SQLite**: um banco completo, num arquivo só, sem servidor para instalar nem senha para configurar. Você escreve SQL de verdade desde o primeiro capítulo, e o que aprender vale para PostgreSQL, MySQL e qualquer outro — as diferenças aparecem sinalizadas quando existirem, e o módulo 05 formaliza a migração.

## A dor da Aurora e a entrega Atlas

**Dor:** *"Quantos pedidos a Fernanda fez este ano, e quanto ela gastou por categoria?"* O CSV do módulo 01 não responde. Ele tem uma linha por venda, com o nome do cliente repetido em cada uma — grafado de três jeitos diferentes. Não há como cruzar cliente com produto, o histórico se perde a cada exportação nova, e duas pessoas mexendo no arquivo ao mesmo tempo sobrescrevem uma à outra.

**Entrega Atlas:** o **schema relacional da Aurora** — clientes, produtos, pedidos e itens de pedido — modelado com diagrama ER, criado com DDL completo (tipos, chaves e constraints), populado a partir dos CSVs do módulo 01 por um script Python, e consultável por um conjunto de perguntas de negócio que o CSV nunca conseguiu responder.

## Pré-requisitos do módulo

Módulo 01 completo, com CP2 aprovado — o capítulo final carrega os dados via Python (`sqlite3`, biblioteca padrão), reaproveitando o importador com quarentena do 01.22. Módulo 02 recomendado: o banco de laboratório e os scripts `.sql` são versionados como qualquer outro arquivo, e o `.gitignore` do 02.09 já prevê `*.db`.

Nenhuma instalação de servidor é necessária. O SQLite acompanha o Python, e o capítulo 03.01 mostra como abrir o primeiro banco em menos de um minuto.

## Capítulos

| # | Capítulo | Objetivo central | Nível |
|---|---|---|---|
| 03.01 | Por que bancos relacionais existem | **Explicar** os problemas de planilhas/arquivos que o modelo relacional resolve | N1 |
| 03.02 | Tabelas, linhas e chaves | **Explicar** chaves primárias, estrangeiras e integridade referencial | N1 |
| 03.03 | `SELECT` e `WHERE` | **Escrever** consultas com filtros, operadores e `LIKE` | N1 |
| 03.04 | Ordenação, `LIMIT` e `DISTINCT` | **Escrever** consultas refinadas com aliases legíveis | N1 |
| 03.05 | Funções de agregação | **Aplicar** `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` (e o efeito do `NULL`) | N1 |
| 03.06 | `GROUP BY` e `HAVING` | **Prever** o resultado de agrupamentos e **diferenciar** `WHERE` de `HAVING` | N2 |
| 03.07 | `JOIN` — parte 1: `INNER` | **Escrever** junções entre tabelas relacionadas | N2 |
| 03.08 | `JOIN` — parte 2: `LEFT`/`RIGHT`/`FULL` | **Prever** o resultado de cada junção e **aplicar** anti-joins (`IS NULL`) | N2 |
| 03.09 | Subconsultas | **Aplicar** subqueries em `WHERE`, `FROM` e `SELECT` | N2 |
| 03.10 | CTEs (`WITH`) | **Refatorar** consultas complexas em etapas nomeadas e legíveis | N2 |
| 03.11 | `INSERT`, `UPDATE`, `DELETE` | **Executar** escrita de dados com disciplina (o `WHERE` que salva empregos) | N1 |
| 03.12 | DDL e tipos de dados | **Criar** e alterar tabelas escolhendo tipos adequados | N1 |
| 03.13 | Constraints | **Aplicar** `NOT NULL`, `UNIQUE`, `CHECK`, `FK` e **prever** violações | N2 |
| 03.14 | Índices | **Explicar** B-trees e **justificar** quando (não) indexar | N2 |
| 03.15 | Transações e ACID | **Explicar** atomicidade e **executar** `BEGIN`/`COMMIT`/`ROLLBACK` | N2 |
| 03.16 | Modelagem + mini projeto | **Projetar** o schema Aurora: diagrama ER, DDL completo e carga inicial via Python | N2 |

## Objetivos detalhados por capítulo

**03.01 — Por que bancos relacionais existem**
- **Explicar** os quatro problemas que planilhas e CSVs não resolvem: duplicação, integridade, concorrência e busca.
- **Descrever** o modelo relacional como conjunto de tabelas ligadas por valores, não por posição.
- **Preparar** o laboratório SQLite e executar a primeira consulta em menos de um minuto.
- **Reconhecer** o que é SQL (linguagem) e o que é o banco (implementação) — a distinção do 01.01, em outro domínio.

**03.02 — Tabelas, linhas e chaves**
- **Explicar** tabela, linha, coluna e tipo — e a diferença entre um registro e uma linha de CSV.
- **Distinguir** chave primária de chave estrangeira, e **justificar** por que identificadores não são nomes.
- **Explicar** integridade referencial: o banco recusando dados que apontam para o nada.
- **Ler** um diagrama de relacionamento e traduzir "um para muitos" em duas tabelas.

**03.03 — `SELECT` e `WHERE`**
- **Escrever** consultas com projeção de colunas e filtros com `=`, `<>`, `>`, `<`, `BETWEEN`, `IN`.
- **Aplicar** `LIKE` com `%` e `_`, e **prever** o efeito da sensibilidade a maiúsculas.
- **Combinar** condições com `AND`, `OR` e `NOT`, respeitando a precedência (a lição do 01.08).
- **Tratar** `NULL` corretamente: `IS NULL` em vez de `= NULL`, e por quê.

**03.04 — Ordenação, `LIMIT` e `DISTINCT`**
- **Ordenar** com `ORDER BY` (múltiplas colunas, `ASC`/`DESC`) e **prever** o lugar do `NULL`.
- **Limitar** resultados com `LIMIT` e `OFFSET` — e o cuidado com paginação sem ordenação estável.
- **Eliminar** repetições com `DISTINCT`, entendendo que ele age sobre a **linha inteira**.
- **Nomear** colunas e expressões com `AS`, escrevendo consultas que outra pessoa lê sem esforço.

**03.05 — Funções de agregação**
- **Aplicar** `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` sobre colunas e expressões.
- **Prever** o efeito do `NULL` em cada uma — e a diferença entre `COUNT(*)` e `COUNT(coluna)`.
- **Combinar** agregação com filtro, entendendo que o `WHERE` age **antes** de agregar.
- **Formatar** valores monetários em centavos inteiros (a disciplina do 01.04, agora no banco).

**03.06 — `GROUP BY` e `HAVING`**
- **Prever** o resultado de um agrupamento antes de executar a consulta.
- **Diferenciar** `WHERE` (filtra linhas, antes) de `HAVING` (filtra grupos, depois).
- **Explicar** a regra de ouro: toda coluna do `SELECT` está no `GROUP BY` ou dentro de uma agregação.
- **Reconhecer** que este é o `chave → acumulador` do 01.15 e o `sort | uniq -c` do 02.04, declarativos.

**03.07 — `JOIN` — parte 1: `INNER`**
- **Escrever** junções entre duas e três tabelas com `INNER JOIN ... ON`.
- **Explicar** o que o `ON` compara e por que ele não é um filtro de linhas comum.
- **Prever** o número de linhas do resultado — e reconhecer o produto cartesiano acidental.
- **Aplicar** aliases de tabela para consultas legíveis, sem ambiguidade de coluna.

**03.08 — `JOIN` — parte 2: `LEFT`/`RIGHT`/`FULL`**
- **Prever** o resultado de cada tipo de junção sobre os mesmos dados.
- **Aplicar** `LEFT JOIN` para perguntas do tipo "todos os clientes, tenham comprado ou não".
- **Construir** anti-joins com `LEFT JOIN ... WHERE ... IS NULL` — "quem nunca comprou".
- **Diagnosticar** o erro clássico: o filtro no `WHERE` que transforma um `LEFT JOIN` em `INNER`.

**03.09 — Subconsultas**
- **Aplicar** subqueries em `WHERE` (com `IN`, `EXISTS`, comparação escalar).
- **Usar** subquery em `FROM` (tabela derivada) e em `SELECT` (valor calculado por linha).
- **Diferenciar** subquery correlacionada de não correlacionada, e o custo de cada uma.
- **Decidir** entre subquery e `JOIN` — quando cada uma comunica melhor a intenção.

**03.10 — CTEs (`WITH`)**
- **Refatorar** consultas aninhadas em etapas nomeadas com `WITH`.
- **Justificar** a legibilidade como critério de engenharia, não de estética (a PEP 8 do 01.25, em SQL).
- **Encadear** múltiplas CTEs, construindo o raciocínio de cima para baixo.
- **Reconhecer** os limites: CTE não é variável, e nem toda consulta melhora ao ser quebrada.

**03.11 — `INSERT`, `UPDATE`, `DELETE`**
- **Executar** inserções com e sem lista de colunas, e inserção múltipla.
- **Aplicar** a disciplina do `WHERE`: `SELECT` antes de `UPDATE`/`DELETE`, sempre (o par listar→apagar do 02.02).
- **Prever** o efeito de um `UPDATE` sem `WHERE` — e o que fazer nos primeiros dez segundos depois.
- **Usar** `RETURNING` (onde disponível) e conferir o número de linhas afetadas.

**03.12 — DDL e tipos de dados**
- **Criar** tabelas com `CREATE TABLE`, escolhendo tipos adequados a cada coluna.
- **Explicar** os tipos fundamentais (inteiro, texto, real, data/hora, booleano) e a afinidade de tipos do SQLite.
- **Alterar** estrutura com `ALTER TABLE` e **remover** com `DROP` — e por que `DROP` merece cerimônia.
- **Decidir** entre armazenar dinheiro como inteiro de centavos ou decimal (o 01.04 volta, com consequências).

**03.13 — Constraints**
- **Aplicar** `NOT NULL`, `UNIQUE`, `CHECK`, `PRIMARY KEY` e `FOREIGN KEY`.
- **Prever** a mensagem de erro de cada violação — e ler o erro como informação, não como obstáculo.
- **Justificar** a regra que sustenta o módulo: **validação no banco não substitui, mas também não é substituída pela** validação na aplicação.
- **Configurar** o comportamento de FK em cascata, e **decidir** quando cascatear é perigoso.

**03.14 — Índices**
- **Explicar** o que é um índice B-tree, com a analogia do índice remissivo de um livro.
- **Medir** o efeito de um índice com `EXPLAIN QUERY PLAN`, antes e depois.
- **Justificar** quando **não** indexar: custo de escrita, espaço, e índices que nunca são usados.
- **Reconhecer** as colunas candidatas naturais: chaves estrangeiras e colunas de filtro frequente.

**03.15 — Transações e ACID**
- **Explicar** atomicidade com o exemplo canônico: a transferência que não pode acontecer pela metade.
- **Executar** `BEGIN`, `COMMIT` e `ROLLBACK`, observando o efeito em duas conexões.
- **Descrever** as quatro propriedades ACID em linguagem própria, sem decorar a sigla.
- **Reconhecer** o que muda em bancos com concorrência real — o gancho para o módulo 05.

**03.16 — Modelagem + mini projeto**
- **Projetar** o schema da Aurora a partir das perguntas de negócio, não das telas.
- **Aplicar** normalização até a 3ª forma normal — e **justificar** quando parar antes.
- **Construir** o diagrama ER e o DDL completo, com constraints e índices deliberados.
- **Carregar** os dados dos CSVs do módulo 01 com um script Python (`sqlite3` + o importador com quarentena do 01.22).

## Fio condutor do módulo

O módulo tem três movimentos, e cada um resolve uma limitação do anterior:

1. **Consultar** (03.01–03.10) — dos primeiros `SELECT` às CTEs, você aprende a fazer perguntas cada vez mais complexas sobre dados que já existem. O ponto de virada é o 03.07: quando o `JOIN` aparece, o modelo relacional finalmente mostra a que veio.
2. **Modificar** (03.11) — escrever é diferente de ler, e mais perigoso. Um capítulo inteiro dedicado à disciplina que evita o `UPDATE` sem `WHERE`.
3. **Modelar** (03.12–03.16) — a parte que separa quem usa banco de quem projeta banco. Tipos, constraints, índices e transações são as quatro ferramentas com que você garante que dados errados **não conseguem entrar**.

O 03.16 fecha os três: modela do zero, cria com DDL, popula com Python e responde, em SQL, a pergunta que abriu o módulo — quanto a Fernanda gastou por categoria.

## Critério de conclusão (CP2)

`Simulados/modulo-03.md`: 10 objetivas + 3 discursivas + 1 prático de ~45 min (dado um schema e um conjunto de perguntas de negócio, escrever as consultas — incluindo ao menos um `LEFT JOIN` com anti-join e uma agregação com `HAVING`). Aprovação: ≥ 8/10 e prático ≥ 3.

A entrega Atlas (schema modelado, criado e populado) é pré-requisito para o **CP3 da Fase 1**, que integra Python + SQL.

## Tempo estimado

~45 h: capítulos de 2–3 h, com prática obrigatória em consulta — SQL se aprende **escrevendo consultas que falham** e lendo a mensagem de erro, não lendo sintaxe. No ritmo de 32 h/semana, ~1,5 semana.

> 📌 **Observação sobre o banco**
> O laboratório é **SQLite** (arquivo único, zero instalação, acompanha o Python). Tudo o que você escrever aqui vale para PostgreSQL e MySQL; onde houver diferença relevante de dialeto, ela aparece em callout 📌 no próprio capítulo. O módulo 05 apresenta o PostgreSQL de verdade — com servidor, usuários e concorrência — e a migração é direta justamente porque a base é a mesma.

---

*Gerado sob spec 3.0.0*
