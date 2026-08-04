# Gabarito — Capítulo 03.16: Modelagem e mini projeto

Leia depois de tentar. Enunciados em [`../cap16.md`](../cap16.md).

## A1 — 1-N ou N-N?

| # | Relação | Tipo | Onde vai a chave |
|---|---|---|---|
| 1 | Cliente ↔ pedidos | 1-N | `cliente_id` em `pedidos` |
| 2 | Pedido ↔ produtos | **N-N** | tabela do meio: `itens_pedido` |
| 3 | Produto ↔ categoria | 1-N | `categoria_id` em `produtos` |
| 4 | Aluno ↔ turmas | **N-N** | tabela do meio: `matriculas` |
| 5 | Pessoa ↔ CPF | 1-1 | mesma tabela |
| 6 | Post ↔ comentários | 1-N | `post_id` em `comentarios` |
| 7 | Ator ↔ filmes | **N-N** | tabela do meio: `elenco` |
| 8 | Funcionário ↔ chefe | 1-N | `chefe_id` em `funcionarios` |

**A regra que resolve todos: a chave vai no lado "muitos".** Um pedido pertence a um cliente, então `cliente_id` mora em `pedidos`. Se você tentar o contrário — uma coluna `pedidos` em `clientes` — precisará guardar uma lista numa célula, que é a violação da 1FN do A2.1.

**O item 8 é a auto-referência.** `chefe_id` aponta para a própria tabela, e é `NULL` para quem não tem chefe — um dos casos em que a FK nula é legítima (03.13/A2.5).

**O item 5 merece a ressalva:** 1-1 costuma virar a mesma tabela, mas nem sempre. Separa-se quando o dado é opcional para a maioria, ou quando tem regras de acesso próprias — dados sensíveis numa tabela à parte, com permissões diferentes.

## A2 — Que forma normal violou?

| # | Violação | Correção |
|---|---|---|
| 1 | **1FN** — lista numa célula | tabela `itens_pedido` |
| 2 | **2FN** — `nome_produto` depende de metade da chave | tirar; vem por junção |
| 3 | **3FN** — `cidade_do_cliente` depende de `cliente_id` | tirar; vem por junção |
| 4 | **3FN** — `nome_depto` e `telefone_depto` dependem de `depto_id` | tabela `departamentos` |
| 5 | **1FN** — grupo repetido em colunas | tabela `telefones` |
| 6 | **3FN**, e é o caso interessante | ver abaixo |

**O item 5 é a 1FN na sua forma mais disfarçada.** `telefone1, telefone2, telefone3` parece respeitar a regra — cada célula tem um valor. Mas é a mesma lista, espalhada em colunas: quem tem quatro telefones não cabe, quem tem um desperdiça duas colunas, e procurar por um número exige `WHERE telefone1 = ? OR telefone2 = ? OR telefone3 = ?`. **O teste é a pergunta "e se forem cinco?"**

**O item 6 é o que separa este exercício do A3.** `preco_atual_do_produto` viola a 3FN e a correção **não** é copiá-lo com outro nome: é decidir qual dos dois fatos você quer. Se é *quanto custa hoje*, sai da tabela e vem por junção. Se é *quanto custou naquela venda*, o nome está errado — deveria ser `preco_unitario_centavos`, e aí não é violação nenhuma. **O nome da coluna revelou a confusão.**

## A3 — Erro ou decisão?

| # | Veredito | Por quê |
|---|---|---|
| 1 | **decisão** | preço no momento da venda ≠ preço de hoje |
| 2 | **erro** | mudar a cidade do cliente desatualiza os pedidos |
| 3 | **decisão** | onde foi entregue é fato daquela entrega |
| 4 | **erro** | o nome do produto é um fato só, e mora em `produtos` |
| 5 | **depende** | ver abaixo |
| 6 | **decisão** | documento fiscal congela o que valia na emissão |

**O critério que decide todos: é o mesmo fato ou dois fatos que hoje coincidem?** Se o valor original mudar, o outro deve mudar junto (erro) ou deve permanecer (decisão)?

- Cliente muda de cidade → os pedidos antigos devem mostrar a cidade **nova**? Não faz diferença para o pedido, e a cópia só cria contradição. **Erro.**
- Cliente muda de endereço → o pedido entregue mês passado foi para o endereço **antigo**. **Decisão.**
- Produto muda de nome (correção de digitação) → todos os itens devem refletir. **Erro.**

**O item 5 é o único em que a resposta honesta é "depende", e por um motivo diferente dos outros.** `pedidos.total_centavos` é **derivável**: `SUM(quantidade * preco_unitario)` sobre os itens. Guardá-lo é cache, não histórico — e cache tem um custo específico: ele pode **divergir** da fonte. Um item alterado sem recalcular o total é suficiente, e o banco passa a conter dois números que discordam sobre o mesmo pedido.

Justifica-se quando o cálculo é caro e o relatório é frequente, e a condição para adotá-lo é ter um mecanismo que garanta a atualização — *trigger*, ou uma única função de escrita por onde tudo passa. **Sem esse mecanismo, é erro; com ele, é decisão.** É a diferença entre desnormalizar e deixar acontecer.

## A4 — Substantivos

**1. Clínica.** Entidades: `medicos`, `pacientes`, `consultas`. `consultas` é a tabela do meio de uma N-N (um médico atende vários pacientes; um paciente vê vários médicos) — **e é mais que isso**: tem atributos próprios (data, hora, status), o que a torna uma entidade de pleno direito, não só uma ligação. É o padrão mais comum em sistemas reais.

**2. Curso.** `cursos` 1-N `modulos` 1-N `aulas`, e `matriculas` como tabela do meio entre `alunos` e `cursos`. Duas hierarquias 1-N encadeadas mais uma N-N.

**3. Restaurante.** `pratos` N-N `ingredientes`, com `receitas` no meio — e a tabela do meio guarda a **quantidade** de cada ingrediente, que é o fato do encontro. Idêntico em estrutura a `itens_pedido`.

**4. Transportadora.** `veiculos`, `motoristas`, `entregas` — e `entregas` tem **duas** chaves estrangeiras, uma para cada. Não é uma N-N entre veículo e motorista: é uma entidade que referencia as duas. A pergunta que confirma: "existe uma relação direta entre veículo e motorista, fora da entrega?" Se cada motorista tiver um veículo fixo, sim, e é 1-N ou N-N à parte.

## AP1 — O schema da locadora

**1. As perguntas antes de desenhar** — e fazê-las é metade da nota:

- Um item pode ser alugado em partes, ou é indivisível? (Decide se há `quantidade`.)
- Existem **vários exemplares** do mesmo item? (É a pergunta do 03.12/D1: aluga-se o modelo ou a unidade física?)
- O que acontece com um aluguel quando o item é retirado do catálogo?
- A diária muda com o tempo? Há desconto por período?
- Um cliente pode ter quantos aluguéis em aberto?

**2 e 3. O DDL:**

```sql
CREATE TABLE categorias (
    id   INTEGER PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE COLLATE NOCASE
) STRICT;

CREATE TABLE itens (
    id                     INTEGER PRIMARY KEY,
    nome                   TEXT    NOT NULL CHECK (LENGTH(TRIM(nome)) > 0),
    categoria_id           INTEGER NOT NULL,
    valor_diaria_centavos  INTEGER NOT NULL CHECK (valor_diaria_centavos > 0),
    ativo                  INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0,1)),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE RESTRICT
) STRICT;

CREATE TABLE clientes (
    id        INTEGER PRIMARY KEY,
    nome      TEXT NOT NULL CHECK (LENGTH(TRIM(nome)) > 0),
    documento TEXT NOT NULL UNIQUE,          -- TEXT: zeros a esquerda (03.12)
    cadastro  TEXT NOT NULL CHECK (cadastro LIKE '____-__-__')
) STRICT;

CREATE TABLE alugueis (
    id                     INTEGER PRIMARY KEY,
    item_id                INTEGER NOT NULL,
    cliente_id             INTEGER NOT NULL,
    data_retirada          TEXT    NOT NULL CHECK (data_retirada LIKE '____-__-__'),
    data_prevista          TEXT    NOT NULL,
    data_devolucao         TEXT,             -- NULL = em aberto; ver (4)
    -- A DECISAO QUE VALE A NOTA:
    valor_diaria_centavos  INTEGER NOT NULL CHECK (valor_diaria_centavos > 0),
    CHECK (data_prevista >= data_retirada),
    CHECK (data_devolucao IS NULL OR data_devolucao >= data_retirada),
    FOREIGN KEY (item_id)    REFERENCES itens(id)    ON DELETE RESTRICT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT
) STRICT;

CREATE INDEX idx_alugueis_item    ON alugueis(item_id);
CREATE INDEX idx_alugueis_cliente ON alugueis(cliente_id, data_retirada);
```

**A decisão que vale a nota: `valor_diaria_centavos` aparece nas duas tabelas.** Em `itens` é *quanto custa alugar hoje*; em `alugueis` é *quanto custou naquele aluguel*. É o `preco_unitario_centavos` da Aurora com outro nome — e reconhecer o mesmo padrão num domínio diferente é o que este exercício testa. Sem a cópia, um reajuste de tabela mudaria retroativamente o valor de aluguéis já encerrados.

**Sobre `data_devolucao` nula:** é a decisão (c) do 03.12/D1, e a resposta continua dependendo de existir um terceiro estado. Se houver "item perdido" ou "em manutenção", uma coluna `status` é melhor.

**O `CHECK` de tabela precisa do `IS NULL OR`** (03.15 — o `NULL` passaria de qualquer forma; o `OR` documenta que é intencional).

**5. Os três comandos recusados** — data em formato brasileiro, diária zero, devolução anterior à retirada. Todos com a mensagem nomeando a condição violada.

## AP2 — Consertando

**1. Os problemas, por categoria:**

*Forma normal:* `produtos TEXT` guarda `"mouse:2, teclado:1"` — 1FN violada, e da pior maneira, porque a quantidade está codificada dentro de uma string. `cliente_nome`, `cliente_email` e `cliente_cidade` repetem em toda venda — 3FN.

*Tipo:* `total REAL` é dinheiro em ponto flutuante (03.12). `data` em `DD/MM/AAAA` ordena errado como texto.

*Restrição:* nenhuma. Sem `NOT NULL`, sem `CHECK`, sem `UNIQUE`, sem `STRICT`. Uma venda sem cliente, com total negativo e data `'ontem'` entra sem reclamação.

*E o que não é nenhum dos três:* `total` é derivável dos itens — o problema do A3.5, aqui sem nenhum mecanismo que o mantenha coerente.

**2 e 3.** `clientes` + `produtos` + `vendas` + `itens_venda`, com a string `"mouse:2"` desmontada em linhas durante a migração.

**5. A pergunta difícil, e ela não tem resposta técnica.** Dois `'Ana Souza'` com e-mails diferentes podem ser: duas pessoas homônimas; a mesma pessoa que trocou de e-mail; ou um erro de digitação. **O schema antigo destruiu a informação que responderia** — não havia identificador de cliente, então não há como saber.

As saídas possíveis, todas ruins: tratar como duas pessoas (arriscando duplicar quem é um só) ou como uma (arriscando fundir duas). A menos ruim é **preservar as duas e marcar para revisão humana**, com uma coluna de "possível duplicata" e a decisão tomada por quem conhece os clientes.

**E a lição que fecha o exercício:** o custo do schema ruim não é a migração difícil — é que **certas perguntas se tornam impossíveis de responder para sempre**. Nenhum SQL recupera uma informação que nunca foi guardada. É o argumento mais forte a favor de modelar antes.

## AP3 — A conferência

**1 a 4** — as quatro conferências batem entre `aurora.db` e `aurora_v2.db`:

```
contagens        8 / 12 / 20 / 31   nos dois
faturamento      831840 centavos    nos dois
por cliente      1:181220 · 2:98860 · 3:89900 · 4:252840 · 5:36890 · 6:98260 · 8:73870
nunca venderam   produto 12         nos dois
```

O faturamento por cliente é mais forte que o total: ele pega redistribuição entre clientes, que o total esconde. E note que **o cliente 7 não aparece** em nenhuma das duas listas — Rafael Torres nunca comprou, desde o 03.01. Uma lista de sete linhas onde há oito clientes é o resultado **correto** aqui (03.08), e conferir "as duas listas têm 7 linhas" é diferente de conferir "as duas listas são idênticas".

**5. O erro que passa pelos itens 1 e 2** — a parte que ensina.

**Trocar o `cliente_id` entre dois pedidos.** As contagens ficam idênticas: 20 pedidos continuam 20. O faturamento total fica idêntico: os mesmos itens, os mesmos valores, só que atribuídos ao cliente errado. **Uma migração que confere contagem e total passa com os clientes embaralhados** — e o relatório de melhores clientes fica errado sem que nada acuse.

A consulta que detecta é a do item 3: faturamento **por cliente**. Ou, mais barata:

```sql
SELECT cliente_id, COUNT(*) FROM pedidos GROUP BY cliente_id;
```

**A regra geral que sai daí: conferir agregados globais não detecta erros de atribuição.** É preciso ao menos um agregado **por grupo**. Uma variante ainda mais barata, útil como canário: `SELECT SUM(cliente_id) FROM pedidos` — 69 nos dois bancos. Não prova a correção, mas uma troca com clientes diferentes altera a soma, e custa uma consulta.

## D1 — O projeto do módulo

**Os três requisitos, e o que cada um ensina.**

**Fotos — a ordem importa.**

```sql
CREATE TABLE fotos_produto (
    id         INTEGER PRIMARY KEY,
    produto_id INTEGER NOT NULL,
    caminho    TEXT    NOT NULL,          -- TEXT, nao BLOB (03.12/A2.8)
    posicao    INTEGER NOT NULL CHECK (posicao > 0),
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE,
    UNIQUE (produto_id, posicao)
) STRICT;
```

`CASCADE` aqui é correto — foto não existe sem produto. E `UNIQUE(produto_id, posicao)` impede duas fotos disputando o mesmo lugar.

**Sobre "a principal":** `posicao = 1` resolve com o que já existe. Uma coluna `principal INTEGER` exigiria a regra "exatamente uma por produto", que **nenhum `CHECK` expressa** — `CHECK` avalia uma linha e a regra fala de várias, exatamente como o limite de empréstimos do 03.13/D1(e). Escolher `posicao = 1` é preferir a regra que o banco consegue impor.

**Endereços — o padrão do preço, de novo.**

```sql
CREATE TABLE enderecos (
    id         INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    logradouro TEXT NOT NULL, numero TEXT NOT NULL,   -- numero e TEXT: "s/n"
    cidade     TEXT NOT NULL, cep TEXT NOT NULL,      -- CEP e TEXT: zeros
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT
) STRICT;
```

E em `pedidos`, **duas coisas ao mesmo tempo**: `endereco_id` referenciando a tabela, **e** os campos do endereço copiados. Parece redundância e é a decisão do A3.3: se o cliente mudar de endereço ou apagá-lo, o pedido entregue mês passado tem de continuar mostrando para onde foi. A FK serve à consulta do dia a dia; a cópia serve ao histórico. **Terceira aparição do mesmo padrão no módulo** — preço, endereço, dados fiscais.

**Histórico de status — a tabela que muda o desenho.**

```sql
CREATE TABLE historico_status (
    id          INTEGER PRIMARY KEY,
    pedido_id   INTEGER NOT NULL,
    status      TEXT NOT NULL CHECK (status IN ('pendente','concluido','cancelado')),
    em          TEXT NOT NULL,
    responsavel TEXT NOT NULL,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE
) STRICT;
CREATE INDEX idx_historico_pedido ON historico_status(pedido_id, em);
```

**A pergunta que este requisito levanta: `pedidos.status` ainda deve existir?** Ele passa a ser derivável — é o último registro do histórico. É o dilema do A3.5 outra vez: manter é cache, com risco de divergir; remover exige uma subconsulta em toda leitura de pedido.

A resposta usual é **manter os dois**, com a regra de que ninguém altera `pedidos.status` sem inserir no histórico, na mesma transação (03.15). E aceitar conscientemente que a coerência depende de disciplina, não do banco — a menos que se use um *trigger*.

**A divergência em que você provavelmente está certo.** Uma candidata forte: `email TEXT UNIQUE` **sem** `NOT NULL` em `codigo/cap16/schema.sql`. O 03.13 defendeu os dois juntos; o schema de referência abre exceção pelo cadastro de balcão. É defensável e é discutível — se todo cadastro passar pelo site, `NOT NULL` deveria estar lá, e a "exceção" é a Beatriz do 03.01 sendo acomodada em vez de corrigida.

**Outra:** `pedidos.data` como `TEXT` de data pura, sem hora. Dois pedidos do mesmo cliente no mesmo dia não têm ordem definida entre si — e num e-commerce real isso importa.

**O fecho — o que mudar no schema do 03.01.** As respostas que o módulo inteiro sustenta: `categoria` como tabela, não texto solto; `STRICT` em tudo; `CHECK` nos domínios fechados (`status`, `ativo`, quantidades e preços positivos); `UNIQUE(pedido_id, produto_id)`; ações de `ON DELETE` declaradas em vez de padrão; e índices nas chaves estrangeiras. Nenhuma delas foi inventada aqui — **todas resolvem um problema que o módulo fez você sentir antes de explicar**, e é essa a ordem que o D-014 escolheu de propósito.

---

## Erros mais comuns

1. **Pôr a chave no lado errado** da relação 1-N.
2. **Não reconhecer a N-N** e tentar resolver com lista numa célula.
3. **Grupo repetido em colunas** (`telefone1..3`) achando que respeita a 1FN.
4. **Copiar dado do pai** sem perguntar se é o mesmo fato.
5. **Guardar total derivável** sem mecanismo que o mantenha coerente.
6. **`BLOB` para foto** quando `TEXT` com o caminho serve melhor.
7. **Conferir migração só por contagem e total.** Não pega erro de atribuição.
8. **Achar que `CHECK` impõe regra entre linhas.** Ele avalia uma linha por vez.
9. **Modelar sem perguntar.** As perguntas do AP1 valem mais que o DDL.
