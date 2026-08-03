# Gabaritos — Capítulo 03.01

Abra somente após tentativa honesta.

## A1 — Vocabulário

1-d · 2-c · 3-f · 4-h · 5-b · 6-a · 7-e · 8-g

**Critério:** 8/8. Confundir 4 e 5 (primária × estrangeira) é o erro que mais aparece — a primária **identifica**, a estrangeira **aponta**.

## A2 — Os quatro problemas

1. **Integridade** — nada impede duas grafias do mesmo valor.
2. **Concorrência** — quem salva por último vence.
3. **Duplicação** — um fato (a cidade dela) registrado em 8 lugares.
4. **Busca** — não há como cruzar duas fontes sem trabalho manual.
5. **Integridade** — nenhuma regra impede um valor impossível.
6. **Busca** — responder exige varrer tudo.

**Critério:** 6/6. Os itens 1 e 5 são ambos integridade e vale notar a diferença de natureza: um é **inconsistência** (o mesmo valor grafado diferente), o outro é **invalidez** (um valor que não deveria existir). Os dois são resolvidos por regras no banco — o primeiro por chave estrangeira ou tabela de domínio, o segundo por `CHECK` (03.13).

## A3 — Lendo o modelo

1. `pedidos.cliente_id` → `clientes.id`.
2. Um cliente, **muitos** pedidos. Um pedido, **um** cliente — é o que a coluna única `cliente_id` garante.
3. Porque o número de produtos por pedido é **variável**. Com colunas fixas, você limita artificialmente (e se o pedido tiver quatro itens?) e desperdiça espaço quando tem um. A tabela separada permite zero, um ou mil itens — e é o padrão para toda relação "um para muitos".
4. Porque é o preço **daquela venda**, que não muda quando o produto muda de preço. Sem essa coluna, uma promoção de hoje reescreveria o faturamento do ano passado — e o balanço deixaria de fechar. É um **fato histórico**, não uma cópia redundante.
5. **Uma** — a linha na tabela `produtos`. Todos os itens de pedido continuam apontando para o mesmo `id`.

**Critério:** 5/5, com o item 4 explicado pelo conceito de "fato histórico" e não por conveniência.

## A4 — Primeiras consultas

1. Os 8 nomes, uma coluna.
2. `Fernanda Lima | campinas` e `Ana Souza | santos`.
3. `12`.
4. As 3 primeiras linhas de pedidos, com as 4 colunas (`id`, `cliente_id`, `data`, `status`).
5. Uma linha: `Beatriz Nogueira | NULL`.

**Erro esperado no item 5:** tentar `WHERE email = NULL` (ou `= ''`) e receber **zero linhas, sem erro**. É o bug silencioso do 03.03: comparação com `NULL` nunca é verdadeira. Use `IS NULL`.

**Critério:** 5/5, com a previsão escrita **antes** da execução — o exercício perde a função se você rodar primeiro.

## AP1 — Montando o laboratório

**Colunas esperadas:** `clientes` (id, nome, email, cidade, data_cadastro) · `produtos` (id, nome, categoria, preco_centavos, ativo) · `pedidos` (id, cliente_id, data, status) · `itens_pedido` (id, pedido_id, produto_id, quantidade, preco_unitario_centavos).

**Contagens:** 8 · 12 · 20 · 31.

**Item 4:** a coluna mostra `NULL` — a Beatriz não tem e-mail cadastrado. Não é `""`, não é espaço em branco: é a marca de "não sabemos".

**Item 5:** na prática, o SQLite devolve na mesma ordem nas duas execuções — e **isso não é garantia**. A ordem é consequência de como as linhas estão fisicamente guardadas, e muda quando há atualizações, exclusões, índices ou (em outros bancos) execução paralela. Depender dela é um bug adormecido: o teste passa hoje e falha em produção sem que nada no código tenha mudado. A correção é sempre explicitar `ORDER BY` (03.04).

**Critério:** as 4 tabelas exploradas e o item 5 respondido com "funcionou, mas não é garantido" — a resposta "sim, a ordem é fixa" é a que o exercício existe para corrigir.

## AP2 — CSV × banco

| Cenário | CSV | Banco | Por quê |
|---|---|---|---|
| 1. E-mail da Fernanda | 1 por linha de venda dela (dezenas) | **1** | O e-mail vive só em `clientes`; pedidos apontam para o `id` |
| 2. Renomear produto | 1 por venda do produto | **1** | O nome vive só em `produtos` |
| 3. Grafia da cidade | 1 por linha com "sorocaba" | **1** (ou zero) | Vive em `clientes`; num modelo com tabela de cidades, seria 1 sempre |
| 4. Cancelar um pedido | apagar/alterar N linhas do pedido | **1** | Muda o `status` na linha do pedido; os itens continuam intactos |

**Observação esperada:** o cenário 4 revela algo além da contagem — no banco, cancelar **não apaga**. O pedido continua existindo com `status = 'cancelado'`, preservando o histórico. No CSV, a tendência é apagar as linhas, e a informação "houve um cancelamento" desaparece.

**Critério:** as 4 linhas com o raciocínio, e a percepção do padrão: **quantas cópias do fato existem** é o que determina o custo da mudança.

## AP3 — Traduzindo perguntas

| # | Tabelas | Ligação |
|---|---|---|
| 1 | `clientes` | nenhuma — agrupa por `cidade` |
| 2 | `produtos` + `itens_pedido` | `itens_pedido.produto_id = produtos.id` |
| 3 | `clientes` + `pedidos` + `itens_pedido` | cliente → pedido → itens |
| 4 | `produtos` + `itens_pedido` | produtos **sem** correspondência em itens (anti-join, 03.08) |
| 5 | `pedidos` + `itens_pedido` | soma por pedido, depois média das somas |
| 6 | `clientes` + `pedidos` + `itens_pedido` + `produtos` | as quatro, filtrando `categoria = 'audio'` |

**Ponto de atenção:** os itens 4 e 5 são de natureza diferente dos outros. O 4 pergunta pela **ausência** (o que não tem correspondência), e não se resolve com uma junção comum. O 5 exige **duas etapas** — somar dentro de cada pedido, depois calcular a média entre pedidos —, que é exatamente o que as CTEs do 03.10 tornam legível.

**Critério:** 6/6 com as ligações corretas; reconhecer que 4 e 5 são "diferentes" vale ponto extra, mesmo sem saber ainda como resolvê-los.

## D1 — O caso da planilha

**Cinco problemas (referência):**

| # | Problema | Exemplo concreto |
|---|---|---|
| 1 | E-mail do aluno repetido em cada matrícula | Aluno com 5 matrículas muda de e-mail → 5 alterações; esquecer uma cria duas verdades |
| 2 | E-mail do professor repetido em cada matrícula de cada curso dele | Professor com 3 turmas de 40 alunos → 120 cópias do mesmo e-mail |
| 3 | Nome do curso escrito à mão | "Python Basico", "Python Básico" e "python basico" viram três cursos nos relatórios |
| 4 | Nenhuma regra sobre a nota | Nota 150 ou -3 entram sem reclamação |
| 5 | Um professor por curso, fixo na linha | Curso com dois professores não cabe no modelo; trocar de professor reescreve o histórico |

**Proposta (item b):**

```text
   alunos              matriculas              cursos            professores
   ------              ----------              ------            -----------
   id  ◄───────────── aluno_id                 id  ◄───────┐     id  ◄────┐
   nome               curso_id ─────────────►  nome        │     nome     │
   email              nota                     professor_id ─────────────┘  email
                      data_matricula
```

**Como resolve (item d):** 1 e 2 → cada e-mail vive numa linha só; 3 → o curso é escolhido por `id`, grafia impossível de divergir; 4 → `CHECK (nota BETWEEN 0 AND 10)` no banco (03.13); 5 → o professor sai da matrícula e vai para o curso, e trocar de professor é uma alteração numa linha.

**O problema não resolvido (item e) — respostas aceitáveis:**

- **Curso com vários professores.** O modelo acima ainda permite só um (`professor_id` em `cursos`). Resolver exige uma tabela de ligação `curso_professores` — a relação **muitos para muitos**, que o 03.16 formaliza.
- **Histórico de nota.** Se a nota for corrigida, o valor anterior se perde. Resolver exige uma tabela de histórico ou versionamento — e é decisão de negócio, não técnica.
- **O mesmo curso em semestres diferentes.** "Python Básico 2026.1" e "2026.2" são o mesmo curso ou dois? O modelo não decide — falta o conceito de **turma**, que é a resposta correta.

**Reflexão esperada:** juntar tudo numa tabela é tentador porque a **primeira** operação fica mais simples: uma linha por evento, nada a cruzar, dá para abrir e ler. O custo aparece depois, e é assimétrico — escrever segue simples e **manter** fica impossível. Cada fato duplicado é uma oportunidade de divergência, e divergências não avisam: elas aparecem como números errados num relatório meses depois. O modelo relacional troca conveniência imediata por garantia permanente, e é essa a troca que o 03.16 vai ensinar a fazer conscientemente — inclusive quando **não** vale a pena (há casos legítimos de tabela desnormalizada, e o módulo 10 os apresenta).

**Critério de "está bom":** cinco problemas com exemplos concretos (não genéricos); diagrama com as ligações corretas; o item (e) identificando uma limitação **real** da própria proposta — quem não acha nenhuma não olhou o suficiente.
