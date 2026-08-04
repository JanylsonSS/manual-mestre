# Exercícios — Capítulo 03.16: Modelagem e mini projeto

> **Antes de tudo:** `python codigo/cap16/criar_aurora_v2.py`. Os exercícios usam
> `dados/aurora_v2.db` e, para os schemas novos, `dados/ddl.db` do 03.12.

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap16.md`](gabaritos/cap16.md).

## Aquecimento

### A1 — 1-N ou N-N? `[Aquecimento · ~10 min · e onde vai a chave?]`

**Tarefa.** Para cada relação, diga o tipo e **onde** fica a chave estrangeira (ou se é preciso uma tabela do meio):

1. Cliente ↔ pedidos
2. Pedido ↔ produtos
3. Produto ↔ categoria
4. Aluno ↔ turmas
5. Pessoa ↔ CPF
6. Post ↔ comentários
7. Ator ↔ filmes
8. Funcionário ↔ chefe

### A2 — Que forma normal violou? `[Aquecimento · ~10 min · 1FN, 2FN ou 3FN?]`

**Tarefa.** Cada tabela tem um defeito. Diga qual forma normal violou e como corrigir:

1. `pedidos(id, cliente_id, produtos_comprados)` — a última guarda `"mouse, teclado"`
2. `itens(pedido_id, produto_id, quantidade, nome_produto)` — chave é `(pedido_id, produto_id)`
3. `pedidos(id, cliente_id, cidade_do_cliente, data)`
4. `funcionarios(id, nome, depto_id, nome_depto, telefone_depto)`
5. `contatos(id, nome, telefone1, telefone2, telefone3)`
6. `vendas(id, produto_id, preco_atual_do_produto, quantidade)`

### A3 — Erro ou decisão? `[Aquecimento · ~10 min · repetição deliberada]`

**Tarefa.** Em cada caso um dado aparece duas vezes. Diga se é **erro** ou **decisão** — e justifique:

1. `itens_pedido.preco_unitario_centavos` e `produtos.preco_centavos`
2. `pedidos.cidade_do_cliente` e `clientes.cidade`
3. O endereço de entrega copiado para dentro do pedido
4. `produtos.nome` repetido em `itens_pedido.nome_produto`
5. O total do pedido guardado em `pedidos.total_centavos`
6. O nome do cliente copiado para a nota fiscal emitida

### A4 — Substantivos `[Aquecimento · ~10 min · da frase ao diagrama]`

**Tarefa.** Para cada frase, liste as entidades, as relações e o tipo de cada relação:

1. "Uma clínica tem médicos que atendem pacientes em consultas agendadas."
2. "Um curso tem módulos, cada módulo tem aulas, e alunos se matriculam em cursos."
3. "Um restaurante tem pratos, cada prato leva vários ingredientes, e cada ingrediente é usado em vários pratos."
4. "Uma transportadora tem veículos e motoristas; cada entrega usa um veículo e um motorista."

## Aplicação

### AP1 — O schema da locadora `[Aplicação · ~30 min · do domínio ao DDL]`

**Domínio.** *"Uma locadora de equipamentos aluga itens para clientes. Cada aluguel tem data de retirada, data prevista de devolução e data real de devolução. Um item pertence a uma categoria e tem um valor de diária. Clientes podem ter aluguéis em aberto."*

**Tarefa.** Entregue, nesta ordem:

1. as perguntas que você faria ao cliente **antes** de desenhar (mínimo três);
2. o diagrama ER;
3. o DDL com `STRICT`, `NOT NULL`, `CHECK`, ações de `ON DELETE` e índices;
4. uma linha de justificativa por coluna não-óbvia;
5. **três** comandos que o schema deve recusar, executados, com a mensagem.

**A decisão que vale a nota:** o valor da diária muda com o tempo. Onde ele fica, e por quê?

### AP2 — Consertando `[Aplicação · ~25 min · normalizar e migrar]`

**Tarefa.** Este schema é real na sua feiura:

```sql
CREATE TABLE vendas (
    id INTEGER PRIMARY KEY,
    cliente_nome TEXT,
    cliente_email TEXT,
    cliente_cidade TEXT,
    produtos TEXT,              -- "mouse:2, teclado:1"
    total REAL,
    data TEXT                   -- "04/08/2026"
);
```

1. Liste **todos** os problemas — de forma normal, de tipo e de restrição.
2. Projete o schema normalizado.
3. Crie o schema ruim, insira 6 vendas, e escreva a migração para o novo.
4. Confira que nada se perdeu.
5. **A pergunta difícil:** dois registros têm `cliente_nome = 'Ana Souza'` com e-mails diferentes. São a mesma pessoa? O que você faz?

### AP3 — A conferência `[Aplicação · ~20 min · provar que preservou]`

**Tarefa.** Sobre `aurora.db` e `aurora_v2.db`, escreva as consultas de conferência que provam a equivalência:

1. contagem de cada tabela;
2. faturamento total dos pedidos concluídos, em centavos;
3. faturamento por cliente — as duas listas idênticas;
4. o conjunto de produtos que nunca venderam;
5. **uma conferência que a contagem não pegaria**: invente um erro de migração que passa pelos itens 1 e 2, e escreva a consulta que o detecta.

## Desafio

### D1 — O projeto do módulo `[Desafio · ~60 min · o schema da Aurora, seu]`

**Tarefa.** Projete e implemente do zero o schema da Aurora com **três** requisitos novos:

- um produto pode ter **várias fotos** (ordem importa: uma é a principal);
- um cliente pode ter **vários endereços**, e cada pedido é entregue em um deles;
- cada pedido tem um **histórico de mudanças de status**, com data e responsável.

**Entregue:** o diagrama ER · o DDL completo · `decisoes.md` com uma linha por coluna não-óbvia · `ataques.sql` com quinze comandos que devem ser recusados, todos recusados · a carga dos dados existentes com conferência.

**A parte que fecha o módulo:** compare o seu schema com `codigo/cap16/schema.sql`, decisão por decisão. Para cada divergência, argumente quem está certo — e **encontre pelo menos uma em que você está**.

**Fecho:** 5 linhas sobre o que você mudaria no schema do 03.01 sabendo o que sabe agora.

<details><summary>💡 Dica 1 (conceito)</summary>
O endereço de entrega tem a mesma natureza do `preco_unitario_centavos`: se o cliente mudar de endereço, o pedido antigo precisa continuar mostrando para onde foi entregue. Isso muda o desenho.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
"Ordem importa" nas fotos pede uma coluna de posição — e uma `UNIQUE(produto_id, posicao)` para que duas fotos não disputem o mesmo lugar. Para "a principal", decida entre `posicao = 1` e uma coluna booleana, e justifique (a segunda precisa de uma regra que o `CHECK` não expressa).
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`categorias` → `clientes` → `enderecos` → `produtos` → `fotos_produto` → `pedidos` (com `endereco_id` e os dados do endereço copiados) → `itens_pedido` → `historico_status`. Crie nessa ordem: pai antes de filho.
</details>
