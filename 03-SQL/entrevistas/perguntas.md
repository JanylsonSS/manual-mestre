# Perguntas de entrevista — Módulo 03

Acumulativo: cada capítulo acrescenta seus itens (IDs `P-MM.CC-nn`). Formato do §30 da spec.

### P-03.01-01 `[conceitual · júnior]` — Por que usar um banco relacional em vez de arquivos?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. **Duplicação** — um fato em vários lugares diverge com o tempo;
2. **Integridade** — o banco impõe regras (tipos, chaves, constraints) que o arquivo não impõe;
3. **Concorrência** — escrita simultânea controlada por transações, em vez de "quem salva por último vence";
4. **Busca** — índices e junções respondem sem ler tudo, e cruzam fontes diferentes.

Bônus de maturidade: reconhecer quando o arquivo continua sendo a escolha certa (dados pequenos, imutáveis, leitura única).
</details>

### P-03.01-02 `[conceitual · júnior]` — O que é SQL e o que ele tem de diferente de Python?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. SQL é **declarativo**: descreve o resultado, não o algoritmo;
2. O otimizador do banco escolhe o plano de execução — duas consultas diferentes podem virar o mesmo plano;
3. Python é imperativo: o laço e o acumulador são escritos por você;
4. Consequência prática: depurar SQL é ler o **plano de execução** (`EXPLAIN`), não percorrer passo a passo.
</details>

### P-03.01-03 `[conceitual · júnior]` — O que é chave primária e chave estrangeira?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Primária identifica a linha unicamente dentro da tabela;
2. Estrangeira guarda a chave primária de outra tabela, criando a ligação;
3. A estrangeira habilita **integridade referencial**: o banco recusa apontar para o que não existe;
4. Por isso a ligação é uma **garantia**, não uma convenção de nomenclatura.
</details>

### P-03.01-04 `[decisão · pleno]` — Se o modelo relacional é tão bom, por que existem bancos NoSQL?

<details><summary>Resposta esperada</summary>

Por que derruba: quem trata o modelo como dogma erra dos dois lados ("NoSQL é moda" ou "relacional é ultrapassado").

Pontos da saída forte, pelos três eixos:
1. **Estrutura** — schema definido é vantagem com dados de forma estável, obstáculo com dados heterogêneos;
2. **Escala** — distribuir junções e transações é caro; alguns sistemas trocam garantias por desempenho, deliberadamente;
3. **Garantias** — ACID versus consistência eventual: aceitável num contador de visualizações, inaceitável num saldo;
4. **O fecho** — a decisão vem do problema; o padrão continua sendo relacional, e bancos relacionais modernos absorveram parte do NoSQL (colunas JSON).
</details>

### P-03.02-01 `[conceitual · júnior]` — O que é chave primária e por que não usar o e-mail?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Identificador **único, não nulo e estável** de cada linha;
2. O e-mail falha nas três: muda, pode ser desconhecido, é regra de negócio;
3. A prática é a chave **artificial** — sem significado, e por isso permanente;
4. O e-mail continua na tabela como atributo, com `UNIQUE` se a regra exigir.
</details>

### P-03.02-02 `[conceitual · júnior]` — O que é integridade referencial?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Toda chave estrangeira aponta para uma linha que existe;
2. O banco impõe recusando **duas** operações: referência inexistente e exclusão com dependentes;
3. O comportamento de exclusão é configurável (`RESTRICT`, `CASCADE`, `SET NULL`), e o padrão é recusar;
4. No SQLite exige `PRAGMA foreign_keys = ON` — desligado por padrão.
</details>

### P-03.02-03 `[código · pleno]` — Como implementar um-para-muitos? E muitos-para-muitos?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Um-para-muitos: a FK fica do lado **"muitos"** (`pedidos.cliente_id`);
2. Muitos-para-muitos: **tabela intermediária** com duas FKs (`itens_pedido`);
3. Por que o cliente não guarda lista: coluna não comporta lista de tamanho variável, e a integridade se perderia;
4. Bônus: a tabela intermediária frequentemente ganha atributos próprios (quantidade, preço no momento) e vira entidade de negócio.
</details>

### P-03.02-04 `[decisão · pleno]` — Precisa apagar um cliente por pedido de exclusão de dados, mas ele tem cinco pedidos. O que faz?

<details><summary>Resposta esperada</summary>

Por que derruba: quem responde só "`ON DELETE CASCADE`" não pensou na consequência contábil.

Pontos da saída forte — os três caminhos e seus custos:
1. **Cascatear** apaga o histórico de vendas; o faturamento muda retroativamente e a contabilidade não fecha;
2. **Recusar** preserva tudo, e não atende ao pedido;
3. **Anonimizar** é o caminho usado: manter a linha e o `id`, substituir dados pessoais por marcadores, registrar a data;
4. O fecho maduro: é decisão de negócio com apoio jurídico (a LGPD prevê retenção para obrigação legal), não escolha de quem escreve o SQL.
</details>

### P-03.03-01 `[conceitual · júnior]` — Qual a diferença entre `WHERE x = NULL` e `WHERE x IS NULL`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `= NULL` é sempre **desconhecido**, nunca verdadeiro — devolve zero linhas mesmo havendo nulos;
2. `IS NULL` é o operador dedicado à ausência de valor;
3. SQL usa lógica de **três valores**: verdadeiro, falso, desconhecido;
4. O `WHERE` só deixa passar o **verdadeiro** — falso e desconhecido têm o mesmo destino.
</details>

### P-03.03-02 `[pegadinha · pleno]` — Você filtra `WHERE status <> 'cancelado'` e as contagens não fecham. Por quê?

<details><summary>Resposta esperada</summary>

Por que derruba: o bug é **silencioso** — a consulta roda e devolve um resultado plausível.

Pontos da saída forte:
1. Linhas com `status` nulo não passam: `NULL <> 'cancelado'` é desconhecido;
2. Correção na consulta: `WHERE status <> 'cancelado' OR status IS NULL`;
3. O caso mais grave é `NOT IN` com nulos na lista — devolve **zero linhas**, sempre;
4. A defesa estrutural: declarar `NOT NULL` sempre que possível, eliminando a classe de problema.
</details>

### P-03.03-03 `[código · júnior]` — Por que evitar `SELECT *` em código de produção?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Traz colunas não usadas — custo de leitura, memória e rede;
2. **Quebra em silêncio** quando a tabela muda (coluna acrescentada ou reordenada);
3. Impede índices que cobririam a consulta inteira;
4. Em exploração manual é apropriado — a crítica é sobre código que fica.
</details>

### P-03.03-04 `[pegadinha · pleno]` — `WHERE cidade = 'campinas' OR cidade = 'santos' AND ativo = 1` — o que está errado?

<details><summary>Resposta esperada</summary>

Por que derruba: a consulta é **sintaticamente válida** e roda — é esse o problema.

Pontos da saída forte:
1. `AND` tem precedência: lê-se `cidade = 'campinas' OR (cidade = 'santos' AND ativo = 1)`;
2. Resultado: **todos** os de Campinas (inclusive inativos) e só os ativos de Santos;
3. O segundo movimento — **não dá para saber a intenção olhando o código**; o problema real é a ambiguidade, e a correção é usar parênteses sempre;
4. Bônus integrador: se `ativo` aceitar `NULL`, há um terceiro problema — as linhas com `ativo` nulo somem do segundo ramo.
</details>

### P-03.04-01 `[conceitual · júnior]` — O que acontece se você usar `LIMIT` sem `ORDER BY`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. O resultado é **indeterminado** — `LIMIT` corta um conjunto sem ordem definida;
2. O banco pode devolver linhas diferentes a cada execução;
3. Funciona por acaso em bancos pequenos e estáticos (ordem física estável);
4. O sintoma aparece como **bug de paginação**: item repetido numa página e ausente de outra.
</details>

### P-03.04-02 `[código · júnior]` — `SELECT DISTINCT a, b` — o `DISTINCT` se aplica a quê?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. À **linha inteira** do resultado — ao par (a, b), não à primeira coluna;
2. Não existe "distinct de uma coluna só" no `SELECT`; para isso, peça só aquela coluna;
3. Para um representante por grupo (com agregação), a ferramenta é `GROUP BY`;
4. Bônus: `DISTINCT` trata múltiplos `NULL` como **um** valor, ao contrário do `WHERE`.
</details>

### P-03.04-03 `[conceitual · pleno]` — Por que o apelido do `SELECT` funciona no `ORDER BY` e não no `WHERE`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Ordem de execução: `FROM` → `WHERE` → `SELECT` → `DISTINCT` → `ORDER BY` → `LIMIT`;
2. Quando o `WHERE` roda, o apelido ainda não foi criado; o `ORDER BY` roda depois e o enxerga;
3. Alguns bancos (SQLite, MySQL) aceitam o apelido no `WHERE` como **extensão não padrão**;
4. A forma correta repete a expressão no `WHERE` — que, de quebra, permite usar índice.
</details>

### P-03.04-04 `[pegadinha · pleno]` — Uma tela pagina de 20 em 20 e às vezes um item aparece em duas páginas, e outro nunca aparece. O código não mudou. O que houve?

<details><summary>Resposta esperada</summary>

Por que derruba: o sintoma parece impossível e a causa é de uma linha.

Pontos da saída forte, em três movimentos:
1. **Diagnóstico** — a ordenação não é **total**; a ordem entre empatados é arbitrária e pode diferir entre as consultas de cada página;
2. **Correção imediata** — incluir a chave primária como último critério: `ORDER BY criado_em DESC, id DESC`;
3. **O que separa** — mesmo com ordenação total, uma **inserção** entre as duas consultas desloca tudo e o sintoma volta; a solução definitiva é **paginação por cursor**;
4. Por que sobrevive: exige movimento de dados, e ambientes de teste são estáticos.
</details>
