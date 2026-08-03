# Exercícios — Capítulo 03.01: Por que bancos relacionais existem

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap01.md`](gabaritos/cap01.md).

## Aquecimento

### A1 — Vocabulário `[Aquecimento · ~10 min · relacione]`

**Tarefa.** Relacione cada termo à sua definição:

| # | Termo | | Definição |
|---|---|---|---|
| 1 | Tabela | a | A estrutura: quais tabelas, colunas, tipos e regras existem |
| 2 | Linha | b | Coluna que aponta para o identificador de outra tabela |
| 3 | Coluna | c | Uma coisa específica registrada |
| 4 | Chave primária | d | Coleção de coisas do mesmo tipo |
| 5 | Chave estrangeira | e | Ausência de valor |
| 6 | Schema | f | Um atributo, com tipo definido |
| 7 | `NULL` | g | Linguagem declarativa para dados relacionais |
| 8 | SQL | h | O identificador único de uma linha |

### A2 — Os quatro problemas `[Aquecimento · ~10 min · qual é qual?]`

**Tarefa.** Cada situação ilustra um dos quatro problemas do CSV (duplicação, integridade, concorrência, busca). Diga qual:

1. O relatório mostra `campinas: 12` e `Campinas: 3`.
2. Duas pessoas acrescentam uma venda ao mesmo tempo; uma some.
3. A Fernanda mudou de cidade e o arquivo tem o endereço antigo em 8 linhas.
4. Para saber a categoria de cada produto, é preciso abrir outro arquivo e casar na mão.
5. Alguém digitou um valor negativo numa venda e ninguém percebeu.
6. Responder "quanto vendemos em julho" exige ler as 40 mil linhas.

### A3 — Lendo o modelo `[Aquecimento · ~10 min · o diagrama]`

**Tarefa.** Consultando o diagrama da seção 6 do capítulo, responda:

1. Qual coluna liga `pedidos` a `clientes`?
2. Um cliente pode ter vários pedidos? E um pedido pode ter vários clientes?
3. Por que existe a tabela `itens_pedido` em vez de colunas `produto1`, `produto2`, `produto3` em `pedidos`?
4. Por que `itens_pedido` guarda `preco_unitario_centavos` se o preço já está em `produtos`?
5. Se um produto for renomeado, quantas linhas mudam?

### A4 — Primeiras consultas `[Aquecimento · ~10 min · preveja antes de rodar]`

**Tarefa.** Para cada consulta, **escreva sua previsão** e só então execute:

1. `SELECT nome FROM clientes;`
2. `SELECT nome, cidade FROM clientes LIMIT 2;`
3. `SELECT COUNT(*) FROM produtos;`
4. `SELECT * FROM pedidos LIMIT 3;`
5. `SELECT nome, email FROM clientes WHERE email IS NULL;`

## Aplicação

### AP1 — Montando o laboratório `[Aplicação · ~20 min · exploração]`

**Tarefa.** (1) Rode o criador do banco e registre a saída; (2) para **cada** uma das quatro tabelas, execute `SELECT * FROM tabela LIMIT 5` e registre as colunas que existem; (3) conte as linhas de cada tabela com `COUNT(*)`; (4) encontre a linha da Beatriz e explique o que aparece na coluna de e-mail; (5) rode `SELECT * FROM clientes` **duas vezes** e verifique se a ordem foi a mesma — e explique por que não se pode contar com isso.

### AP2 — CSV × banco `[Aplicação · ~20 min · contando alterações]`

**Tarefa.** Para cada cenário, conte quantas alterações seriam necessárias no `vendas.csv` do módulo 01 e quantas no banco, e explique a diferença:

1. A Fernanda muda de e-mail.
2. O produto "Mouse Sem Fio" é renomeado para "Mouse Sem Fio Pro".
3. A cidade "sorocaba" passa a ser grafada "Sorocaba" em todo o sistema.
4. Um pedido inteiro é cancelado.

Registre o raciocínio, não só os números.

### AP3 — Traduzindo perguntas `[Aplicação · ~20 min · quais tabelas?]`

**Tarefa.** Para cada pergunta de negócio, diga **quais tabelas** seriam necessárias e **como** elas se ligariam (não é preciso escrever SQL ainda):

1. Quantos clientes temos por cidade?
2. Qual o produto mais vendido em quantidade?
3. Quanto a Fernanda gastou no total?
4. Quais produtos nunca foram vendidos?
5. Qual o valor médio de um pedido?
6. Quais clientes compraram na categoria "audio"?

## Desafio

### D1 — O caso da planilha `[Desafio · ~40 min · diagnóstico de modelo]`

**Tarefa.** Uma escola controla matrículas numa planilha com as colunas `aluno, email_aluno, curso, professor, email_professor, nota, data_matricula` — uma linha por matrícula.

- **(a)** Liste **cinco** problemas concretos desse modelo, cada um com um exemplo do que daria errado;
- **(b)** proponha a divisão em tabelas, dizendo o que cada uma guarda e como se ligam;
- **(c)** desenhe o diagrama no estilo do capítulo;
- **(d)** para cada um dos cinco problemas, explique como a sua proposta o resolve;
- **(e)** identifique **um** problema que a sua proposta **não** resolve — e o que resolveria.

**Fecho:** 5 linhas sobre por que "juntar tudo numa tabela só" é tentador e por que falha.

<details><summary>💡 Dica 1 (conceito)</summary>
Pergunte-se, para cada coluna: "este dado se repete em várias linhas?" Se sim, ele provavelmente descreve outra coisa, e essa coisa merece a própria tabela.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Comece pelos substantivos do enunciado: aluno, curso, professor, matrícula. Cada substantivo costuma virar uma tabela — e a matrícula é a que **liga** as outras.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Tabela de problemas (problema · exemplo concreto · como a proposta resolve) → diagrama → o problema não resolvido → reflexão.
</details>
