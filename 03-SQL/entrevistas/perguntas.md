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
