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

### P-03.05-01 `[conceitual · júnior]` — Qual a diferença entre `COUNT(*)` e `COUNT(coluna)`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `COUNT(*)` conta **linhas**; `COUNT(coluna)` conta **valores não nulos** daquela coluna;
2. Divergem quando a coluna tem nulos — e a diferença **é** a quantidade de nulos;
3. Daí a técnica de auditoria: `COUNT(*) - COUNT(coluna)`;
4. Terceira variante: `COUNT(DISTINCT coluna)`, que também ignora nulos.
</details>

### P-03.05-02 `[código · júnior]` — O que `SUM` devolve quando nenhuma linha passa pelo filtro?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. **`NULL`**, não zero — não havia nada para somar;
2. `COUNT` no mesmo caso devolve **0** — é o único ponto em que as funções divergem;
3. Correção prática: `COALESCE(SUM(...), 0)` em toda soma de relatório;
4. A ressalva madura: para `AVG`, `MIN` e `MAX`, substituir por zero costuma ser **errado** — média de nada não é média zero.
</details>

### P-03.05-03 `[conceitual · pleno]` — Como o `AVG` trata valores nulos?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Ignora — no numerador **e no denominador**; a média é dos valores preenchidos;
2. Se a regra de negócio disser que ausência é zero, seja explícito: `AVG(COALESCE(col, 0))`;
3. A escolha do denominador é decisão **de negócio**, não de sintaxe;
4. Boa prática: publicar toda média com o `COUNT` correspondente — média sem amostra esconde a decisão.
</details>

### P-03.05-04 `[pegadinha · pleno]` — Numa consulta com junção, a soma saiu certa e a contagem saiu inflada. Por quê?

<details><summary>Resposta esperada</summary>

Por que derruba: exige entender o que a junção faz com as **linhas**, não com os valores.

Pontos da saída forte:
1. A junção produz **uma linha por item**; um pedido com 3 itens aparece 3 vezes;
2. Para a **soma** isso é o desejado — cada item é somado uma vez, e o total sai correto;
3. Para a **contagem de pedidos** é errado: `COUNT(*)` conta linhas da junção → use `COUNT(DISTINCT p.id)`;
4. O padrão geral: cada agregação opera num **nível de granularidade**; misturar granularidades numa consulta só é a origem do "somar duas vezes". Quando duas são necessárias, separe em CTEs (03.10).
</details>

### P-03.06-01 `[conceitual · pleno]` — Qual a diferença entre `WHERE` e `HAVING`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `WHERE` filtra **linhas antes** do agrupamento e **não** pode usar agregações;
2. `HAVING` filtra **grupos depois** da agregação e **pode**;
3. A justificativa vem da ordem de execução: `FROM` → `WHERE` → `GROUP BY` → `HAVING`;
4. Quando a condição serve nos dois, prefira o `WHERE` — ele reduz o volume que chega ao agrupamento.
</details>

### P-03.06-02 `[código · pleno]` — Por que `SELECT categoria, nome, COUNT(*) FROM produtos GROUP BY categoria` dá erro?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `nome` não está no `GROUP BY` nem dentro de agregação — a regra de ouro;
2. O grupo tem vários nomes; não há como escolher um, e a pergunta não tem resposta;
3. **Alguns bancos aceitam** (SQLite, MySQL permissivo) devolvendo valor arbitrário — pior que o erro, porque o resultado parece correto;
4. Correção conforme a intenção: `MIN(nome)`, agrupar também por `nome`, ou subconsulta/função de janela se quiser a linha do máximo.
</details>

### P-03.06-03 `[conceitual · pleno]` — O que acontece com valores `NULL` num `GROUP BY`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Formam **um grupo próprio** — todos os nulos juntos, visíveis como uma linha do resultado;
2. Contrasta com o `WHERE`, onde o `NULL` é descartado; coincide com o `DISTINCT`;
3. Consequência prática: relatórios agrupados mostram uma linha vazia quando há nulos;
4. A decisão de exibir, excluir (`WHERE ... IS NOT NULL`) ou rotular (`COALESCE`) deve ser **explícita**.
</details>

### P-03.06-04 `[pegadinha · pleno]` — "Categorias com mais de 3 produtos, considerando apenas os ativos, ordenadas pelo faturamento." Escreva.

<details><summary>Resposta esperada</summary>

Por que derruba: é ordem de execução **aplicada**, e os três erros típicos são silenciosos ou confusos.

Pontos da saída forte:
1. `WHERE ativo = 1` (linha) → `GROUP BY categoria` → `HAVING COUNT(*) > 3` (grupo) → `ORDER BY`;
2. Erro típico 1: `ativo = 1` no `HAVING` — funciona em alguns bancos, é mais lento e engana o leitor;
3. Erro típico 2: `COUNT(*) > 3` no `WHERE` — erro de verdade, a agregação ainda não existe;
4. **O movimento que impressiona**: perguntar antes se "mais de 3 produtos" conta só os ativos ou todos — a mesma frase em português comporta duas consultas diferentes.
</details>

### P-03.07-01 `[conceitual · júnior]` — O que é um `INNER JOIN`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Combina linhas de duas tabelas mantendo os pares em que a condição do `ON` é verdadeira;
2. Cada par aprovado vira **uma linha** com as colunas das duas;
3. O `ON` quase sempre compara uma chave estrangeira com a chave primária correspondente;
4. **Linhas sem correspondência desaparecem dos dois lados** — é o que distingue o `INNER`, e o gancho para o `LEFT JOIN`.
</details>

### P-03.07-02 `[código · pleno]` — O que é um produto cartesiano e como ele acontece sem querer?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Todos os pares possíveis — N × M linhas;
2. Acontece por `ON` esquecido ao acrescentar uma tabela, ou condição sempre verdadeira;
3. Sintoma: consulta que não termina, contagem absurda;
4. Diagnóstico: nº de `JOIN` = nº de `ON`, **e** cada `ON` compara colunas das duas tabelas. A sintaxe com vírgula esconde o problema; `JOIN ... ON` o transforma em erro de sintaxe.
</details>

### P-03.07-03 `[conceitual · pleno]` — Juntando `pedidos` com `itens_pedido`, quantas linhas o resultado tem?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Uma por **item**, não por pedido — a granularidade é da tabela mais fina;
2. Um pedido com 3 itens aparece 3 vezes;
3. Consequência: `COUNT(*)` conta itens; para pedidos, `COUNT(DISTINCT p.id)`;
4. Prever o número de linhas antes de rodar é a defesa contra somas infladas.
</details>

### P-03.07-04 `[pegadinha · sênior]` — Uma consulta junta `pedidos`, `itens_pedido` e `pagamentos` para mostrar o total dos itens e o total pago. Os dois saíram maiores. Por quê?

<details><summary>Resposta esperada</summary>

Por que derruba: é a evolução da multiplicação de linhas, e só aparece quando há dois filhos dos dois lados.

Pontos da saída forte:
1. Um pedido com 3 itens e 2 pagamentos produz **6 linhas** — cada item pareado com cada pagamento;
2. A soma dos itens conta cada item **2 vezes**; a dos pagamentos, cada um **3 vezes** — **fatores diferentes**;
3. Com **um** pagamento por pedido o resultado fica correto — o bug dorme até o primeiro parcelamento;
4. Solução: agregar cada filho **separadamente**, com CTEs (03.10) ou subconsultas (03.09). Regra geral: duas tabelas filhas do mesmo pai não convivem numa junção quando há agregação.
</details>

### P-03.08-01 `[conceitual · júnior]` — Qual a diferença entre `INNER JOIN` e `LEFT JOIN`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `INNER` mantém só os pares que satisfazem o `ON`; `LEFT` mantém **todas** as linhas da esquerda;
2. Onde não há par, as colunas da direita vêm com `NULL` — fabricado pela junção, não presente nos dados;
3. Consequência prática: com `INNER`, registros somem **sem aviso** e o relatório fica incompleto em silêncio;
4. Detalhe de quem já usou: em `LEFT JOIN`, `COUNT(coluna_da_direita)` em vez de `COUNT(*)`.
</details>

### P-03.08-02 `[código · pleno]` — Como você encontra clientes que nunca compraram?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Anti-join: `LEFT JOIN pedidos p ON ... WHERE p.id IS NULL`;
2. O `IS NULL` deve testar uma coluna que **nunca é nula** na tabela original — a chave primária;
3. Se testar coluna que aceita nulos, mistura "não havia par" com "havia par com valor nulo";
4. Alternativas: `NOT EXISTS` (segura) e `NOT IN` (arriscada — nulos na lista devolvem zero linhas, 03.03).
</details>

### P-03.08-03 `[conceitual · pleno]` — Por que `RIGHT JOIN` é raro na prática?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Todo `RIGHT` se reescreve como `LEFT` invertendo as tabelas;
2. A convenção de pôr a tabela principal à esquerda torna a consulta muito mais legível, sobretudo com 3+ tabelas;
3. Alguns bancos nem suportam — o SQLite só a partir da versão 3.39 (2022);
4. `FULL OUTER` também é raro; o caso real é **conciliação** entre duas fontes, e emula-se com dois `LEFT` + `UNION`.
</details>

### P-03.08-04 `[pegadinha · pleno]` — O relatório deveria listar todos os clientes com pedidos concluídos, mas alguns sumiram. O `LEFT JOIN` está lá. Por quê?

<details><summary>Resposta esperada</summary>

Por que derruba: a consulta **parece correta** — o `LEFT JOIN` está escrito e a intenção é evidente.

Pontos da saída forte, em três tempos:
1. **A ordem** — o `ON` monta os pares e preserva as linhas sem par; o `WHERE` age **depois**, sobre o resultado montado;
2. **O efeito** — na linha preservada, `p.status` é `NULL`, e `NULL = 'concluido'` é **desconhecido**; o `WHERE` a descarta, e o `LEFT` virou `INNER`;
3. **A correção** — mover a condição para o `ON` com `AND`;
4. **A generalização** — num `LEFT JOIN`, toda condição sobre a direita pertence ao `ON`; a exceção é o `IS NULL` do anti-join, que precisa do `WHERE` porque testa o `NULL` fabricado. Bônus: o otimizador chega a converter a consulta em `INNER` internamente — o banco não erra, obedece.
</details>

### P-03.09-01 `[conceitual · pleno]` — Qual a diferença entre subconsulta correlacionada e não correlacionada?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. A não correlacionada **não menciona** a consulta externa e roda **uma vez**;
2. A correlacionada menciona um apelido de fora e é avaliada **por linha externa**;
3. Um exemplo de cada uma vale mais que a definição;
4. A ressalva madura: otimizadores reescrevem `EXISTS` correlacionado como semi-junção — o caso realmente caro é a correlacionada **com agregação no `SELECT`**.
</details>

### P-03.09-02 `[código · pleno]` — Por que preferir `NOT EXISTS` a `NOT IN`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `NOT IN` com um `NULL` na lista devolve **zero linhas**, sempre;
2. O mecanismo: `x NOT IN (a, NULL)` vira uma conjunção que inclui `x <> NULL`, **desconhecido**;
3. `NOT EXISTS` não compara valores, apenas verifica existência — é imune;
4. O bug é **silencioso**: nenhum erro, resultado plausível, e aparece meses depois quando o primeiro nulo entra.
</details>

### P-03.09-03 `[decisão · pleno]` — Quando usar `JOIN` e quando usar subconsulta?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `JOIN` quando precisa de **colunas** da outra tabela;
2. `EXISTS` quando precisa apenas **verificar** — e sem multiplicar linhas (dispensa `DISTINCT`);
3. Subconsulta no `FROM` para agregação em **dois níveis** (ticket médio);
4. Subconsulta no `SELECT` quando há **duas** tabelas filhas a agregar — a junção as multiplicaria (03.07).
</details>

### P-03.09-04 `[pegadinha · sênior]` — Esta consulta funcionou por dois anos e hoje devolve zero linhas. Nada no código mudou.

<details><summary>Resposta esperada</summary>

```sql
SELECT * FROM produtos WHERE id NOT IN (SELECT produto_id FROM itens_pedido);
```

Por que derruba: a informação decisiva **não está na consulta**, está nos dados.

Pontos da saída forte:
1. **A hipótese** — apareceu um `NULL` em `produto_id`;
2. **O mecanismo** — `NOT IN` vira conjunção de desigualdades; `id <> NULL` é desconhecido, e nenhuma linha passa;
3. **O diagnóstico** — `SELECT COUNT(*) FROM itens_pedido WHERE produto_id IS NULL`;
4. **As correções, em ordem** — reescrever com `NOT EXISTS`; filtrar `IS NOT NULL` na subconsulta; declarar a coluna `NOT NULL` (03.13). E o movimento final: a consulta **sempre esteve errada**, apenas não tinha como se manifestar.
</details>

### P37 — "Qual a diferença entre uma CTE e uma subconsulta no `FROM`?" `[conceitual]`

**O que testam:** se você entende que a diferença é de **legibilidade e reuso**, não de semântica.

**Resposta forte, em três movimentos:**
1. **Resultado:** idêntico. A mesma consulta escrita das duas formas devolve o mesmo valor, ao último dígito.
2. **Leitura:** a subconsulta se lê **de dentro pra fora**; a CTE, **de cima pra baixo**, como um roteiro de etapas nomeadas.
3. **Reuso:** a CTE pode ser referenciada **mais de uma vez** no mesmo comando; a tabela derivada teria que ser reescrita — e reescrita significa duas cópias que precisam mudar juntas.

**O que não dizer:** "CTE é mais rápida". Não é uma propriedade da CTE. Em alguns bancos e versões ela chegou a ser uma barreira de otimização (o PostgreSQL materializava CTEs até a versão 12). Desempenho se mede (03.14), não se supõe.

### P38 — "Quando você **não** usaria uma CTE?" `[julgamento]`

**O que testam:** se você aplica a ferramenta por critério ou por hábito.

**Resposta forte:** em consultas de **uma etapa só** — não há etapa para nomear, e a CTE só acrescenta duas linhas de ruído. O sinal de que ela **vale** a pena é o oposto: etapas conceituais distintas, a mesma etapa usada duas vezes, ou duas tabelas filhas do mesmo pai.

**O teste do nome, que impressiona:** "se o único nome honesto para o bloco é `temp` ou `dados`, o bloco não é uma etapa. E se preciso de 'e' no nome — `clientes_e_pedidos_e_totais` — ele faz coisas demais e deveria ser duas CTEs." É o mesmo critério de quando extrair uma função.

### P39 — "Você tem pedidos com itens e com pagamentos. Como calcula os dois totais na mesma consulta?" `[caso prático — o clássico]`

**Por que é clássico:** é a armadilha do 03.07 numa roupa nova, e derruba muita gente sênior.

**A resposta errada** — juntar as duas filhas direto ao pai e somar: cada item se combina com cada pagamento, e **as duas somas inflam**.

**A resposta forte:** uma CTE por filha, cada uma agregando ao nível de `pedido_id`; depois `LEFT JOIN` das duas ao pedido, com `COALESCE` para quem não tem pagamento.

**O movimento que fecha:** citar a verificação. "Eu confiro somando as duas fontes separadamente e comparando com o resultado da junção — em centavos, nunca em reais. Se baterem, nenhuma linha multiplicou."

### P40 — "O relatório está somando o dobro desde ontem. Como você investiga?" `[depuração — pergunta aberta]`

**O que testam:** método, não memória.

**A sequência que impressiona:**
1. **Confirmar o dobro exato.** Se for exatamente 2×, é multiplicação de linhas; se for um fator irregular, é outra coisa (dado duplicado na origem, filtro perdido).
2. **Contar antes de somar.** `SELECT COUNT(*)` na junção contra `COUNT(*)` na tabela base: se a junção tem mais linhas, achou o ponto.
3. **Perguntar o que mudou ontem.** Uma tabela filha nova na junção? Uma linha duplicada numa tabela que era 1:1 e virou 1:N sem ninguém avisar?
4. **Corrigir na raiz** — agregar cada filha na sua CTE — em vez de dividir por dois.
5. **Deixar a checagem no lugar:** uma consulta de conferência que compara o total pela junção com o total pela fonte, rodada junto com o relatório.

**O que derruba:** propor `DISTINCT` como primeira medida. `DISTINCT` esconde a multiplicação em contagens e **não corrige somas** — e ainda apaga duplicatas legítimas.

### P41 — "Você precisa corrigir o e-mail de um cliente em produção. Descreva o que você faz." `[procedimento]`

**O que testam:** não é a sintaxe do `UPDATE` — é se você tem procedimento ou improvisa.

**A resposta forte é uma sequência, não um comando:**
1. `SELECT id, nome, email FROM clientes WHERE id = ...` — **anotar o valor antigo** (é o que torna a operação reversível);
2. confirmar que devolve **uma** linha;
3. `BEGIN`;
4. `UPDATE ... WHERE id = ...` pela **chave primária**, nunca por nome ou e-mail;
5. conferir `Linhas afetadas: 1`;
6. `SELECT` de verificação **dentro** da transação;
7. `COMMIT`.

**O detalhe que separa:** filtrar pela chave primária, e não por `WHERE email = 'antigo@...'`. Duas pessoas podem ter o mesmo e-mail cadastrado por engano — e é justamente quando há um engano no cadastro que você está mexendo ali.

### P42 — "Qual a diferença entre `DELETE` e `TRUNCATE`?" `[conceitual]`

**Resposta forte:** `DELETE` aceita `WHERE`, remove linha a linha, dispara verificação de chave estrangeira e é transacional — dá para desfazer. `TRUNCATE` esvazia a tabela inteira de uma vez, é muito mais rápido em tabelas grandes, e em vários bancos **não é revertível por `ROLLBACK`** (no PostgreSQL é; no MySQL com InnoDB, não). O SQLite não tem `TRUNCATE`.

**O que impressiona:** dizer que a diferença de reversibilidade **varia por banco** e que você verificaria antes de usar em produção. Quem afirma categoricamente "TRUNCATE não pode ser desfeito" está certo com frequência e errado o suficiente.

### P43 — "O que é *soft delete* e quando você usaria?" `[julgamento]`

**Resposta forte:** marcar a linha como inativa (`ativo = 0`, `deleted_at = <data>`) em vez de removê-la. Use quando o dado aparece em histórico, relatório fechado ou obrigação legal — o que é quase sempre em dados de negócio.

**O contraponto que mostra maturidade:** *soft delete* tem custo. Toda consulta passa a precisar de `WHERE ativo = 1`, e **a que esquecer vai mostrar dados que não deveriam aparecer**. Índices crescem com linhas que ninguém consulta. E ele **não** satisfaz um pedido de exclusão sob a LGPD — para isso a resposta é anonimizar, preservando a linha e destruindo o dado pessoal.

### P44 — "Rodei um `UPDATE` sem `WHERE` em produção. O que você faz agora?" `[comportamental sob pressão]`

**O que testam:** frieza e honestidade, não conhecimento.

**A sequência que impressiona:**
1. **Parar de escrever.** Nenhum comando novo — sobretudo nenhum `UPDATE` "de correção" improvisado, que costuma piorar.
2. **Verificar se há transação aberta.** Se houver, `ROLLBACK` e acabou.
3. **Se já foi confirmado: avisar imediatamente.** Antes de tentar consertar, não depois.
4. **Avaliar a recuperação** — backup, log de transações, ou *point-in-time recovery* — e quanto tempo cada opção leva.
5. **Depois de resolvido, o post-mortem sem culpado:** por que era possível rodar aquilo direto em produção?

**O que derruba:** dizer que tentaria consertar sozinho antes de avisar. E dizer que isso nunca aconteceria com você.

### P45 — "Que tipo você usa para guardar dinheiro?" `[conceitual — a mais frequente do módulo]`

**Resposta forte:** inteiro na menor unidade (centavos), ou `DECIMAL`/`NUMERIC` nos bancos em que ele é decimal exato — PostgreSQL, por exemplo. **Nunca `FLOAT`/`REAL`/`DOUBLE`.**

**A justificativa que fecha a pergunta:** `0.1 + 0.2` devolve `0.30000000000000004`, e `0.1 + 0.2 = 0.3` é **falso**. Não é bug de banco: é o IEEE 754, e vale igual em Python, Java e JavaScript. Somado sobre milhares de linhas, o erro acumula de forma imprevisível.

**A ressalva que impressiona:** no SQLite, `NUMERIC(10,2)` **não** é decimal exato — a precisão declarada é ignorada e o valor vira `REAL`. Quem migra de PostgreSQL confiando no mesmo nome tem uma surpresa cara.

### P46 — "O que é afinidade de tipos?" `[conceitual — específica de SQLite]`

**Resposta forte:** no SQLite o tipo pertence ao **valor**, não à coluna. A declaração é uma preferência: o banco converte quando dá e guarda como veio quando não dá.

**Os exemplos que provam domínio:** `'abacaxi'` entra numa coluna `INTEGER` e fica como texto; `'42'` na mesma coluna vira o número 42; **`'3.7'` vira `real`, não `integer`**, porque a conversão para inteiro só ocorre sem perda. Três comportamentos na mesma coluna.

**O fechamento:** desde a 3.37 existe `STRICT`, que recusa o inconversível e também tipos inventados — porque sim, `CREATE TABLE t (x BANANA)` é aceito numa tabela comum.

### P47 — "Como você muda o tipo de uma coluna com 10 milhões de linhas em produção?" `[caso prático]`

**O que testam:** se você sabe que não existe um comando para isso, e como pensa sobre operações longas.

**A resposta forte:** não há `ALTER COLUMN` no SQLite, e mesmo onde existe (PostgreSQL) um `ALTER` dessa magnitude reescreve a tabela e a bloqueia. O caminho é: tabela nova com o tipo certo → cópia **em lotes** → sincronização das linhas que mudaram durante a cópia → troca de nome numa transação curta → manter a antiga por alguns dias antes de remover.

**O detalhe que separa:** ao converter valores, `CAST` **trunca**. `CAST(19.99 * 100 AS INTEGER)` dá **1998**, não 1999, porque `19.99 * 100` é `1998.9999999999998`. Uma migração de dinheiro sem `ROUND` perde um centavo por linha, sem erro, em toda a base.

### P48 — "Qual a diferença entre `CHAR`, `VARCHAR` e `TEXT`?" `[conceitual — pega quem decorou]`

**Resposta forte, em duas partes.** Em bancos com tipos estritos: `CHAR(n)` é fixo e preenche com espaços à direita; `VARCHAR(n)` é variável com limite imposto; `TEXT` é variável sem limite. **No SQLite os três são a mesma coisa** — todos têm afinidade `TEXT`, e `VARCHAR(3)` guarda 26 caracteres sem reclamar.

**O que impressiona:** dizer que a resposta depende do banco, e que confiar num `VARCHAR(n)` como validação é um erro em qualquer um deles — o limite de tamanho é regra de negócio e pertence a um `CHECK` ou à aplicação, onde pode devolver uma mensagem útil ao usuário.

### P49 — "Qual a diferença entre `PRIMARY KEY` e `UNIQUE`?" `[conceitual]`

**Resposta forte:** as duas garantem unicidade. `PRIMARY KEY` é uma só por tabela e implica `NOT NULL` na maioria dos bancos; `UNIQUE` pode haver várias e **aceita `NULL`**.

**O detalhe que separa:** `UNIQUE` aceita **vários** nulos, não apenas um — porque `NULL = NULL` é desconhecido, então dois nulos nunca são detectados como duplicados. Consequência prática: um campo que precisa ser único **e** obrigatório exige `NOT NULL UNIQUE`, os dois. Só `UNIQUE` deixa a tabela encher de linhas sem valor, e a unicidade que você acha que tem não existe para elas.

**Bônus específico de SQLite:** uma `PRIMARY KEY` de texto aceita `NULL` — furo antigo mantido por compatibilidade, que `STRICT` ou um `NOT NULL` explícito fecham.

### P50 — "Onde você põe as regras de negócio: no banco ou na aplicação?" `[julgamento — não há resposta única]`

**O que testam:** se você tem critério ou doutrina.

**A resposta forte divide por criticidade,** com uma pergunta: *se essa regra for violada, dá para consertar depois?* Unicidade de identificadores, integridade referencial e faixas que quebram relatórios vão para o **banco** — violá-las corrompe dados de forma cara de desfazer. Limites por plano, promoções e permissões ficam na **aplicação** — mudam com frequência e um caso a mais não corrompe nada.

**O argumento decisivo:** existe sempre mais de um caminho de escrita. O formulário valida; o script de importação, a API de parceiros e o analista com acesso direto não passam por ele. A restrição no banco é a única que vale para todos os caminhos, inclusive os que ainda não existem.

**A ressalva que mostra maturidade:** bancos NoSQL frequentemente abrem mão dessas garantias em troca de escala e flexibilidade de schema — o que transfere a validação inteira para a aplicação. Não é errado; é uma troca, e saber o que se troca é o que distingue arquitetura de moda.

### P51 — "Uma coluna `UNIQUE` está aceitando duplicatas. Como você investiga?" `[depuração]`

**A sequência que impressiona:**
1. **São `NULL`s?** É a causa mais frequente, e a mais invisível: `SELECT COUNT(*) - COUNT(coluna)` mostra quantos nulos há.
2. **A restrição existe mesmo?** `SELECT sql FROM sqlite_master WHERE name = 't'` — muita "regra" mora só na cabeça do time.
3. **É diferença de caixa ou espaço?** `'Ana@x.com'` e `'ana@x.com'` são valores distintos para o banco. `COLLATE NOCASE` ou normalização na escrita resolvem; espaços em branco no fim são o mesmo problema com outra roupa.
4. **A unicidade é sobre uma coluna ou sobre um par?** "Uma inscrição por pessoa por curso" não é `UNIQUE(email)` — é `UNIQUE(email, curso)`. Quem procura o erro coluna a coluna nunca acha.

### P52 — "O que acontece ao apagar um cliente que tem pedidos?" `[caso prático]`

**Resposta forte:** depende da ação declarada na chave estrangeira. `RESTRICT`/`NO ACTION` recusa o `DELETE`; `CASCADE` apaga os pedidos junto; `SET NULL` deixa os pedidos órfãos com `cliente_id` nulo.

**A escolha e o porquê:** para pedidos, `RESTRICT`. Histórico financeiro não deve sumir com um cadastro — e recusar é reversível, enquanto apagar não é.

**O detalhe que quase ninguém traz:** `CASCADE` torna o alcance do comando **invisível**. O banco reporta `Linhas afetadas: 1` mesmo tendo removido dez, porque conta as linhas do comando e não as do efeito. Qualquer conferência baseada nesse número passa enquanto o histórico desaparece. Antes de um `DELETE` numa cadeia com `CASCADE`, o ensaio tem que contar os **descendentes**.

### P53 — "O que é um índice e por que ele acelera?" `[conceitual]`

**Resposta forte:** uma cópia ordenada da coluna, organizada como **B-tree**, guardando um ponteiro para a linha original. Buscar nela é descer poucos níveis em vez de percorrer tudo — ~20 comparações em um milhão de linhas contra um milhão. Multiplicar a tabela por mil acrescenta **dez** comparações.

**O que separa uma boa resposta:** mencionar o custo sem ser perguntado. O índice ocupa disco (medido: +34% no arquivo com um só) e torna **toda** escrita mais lenta, porque a cópia ordenada precisa ser atualizada a cada `INSERT`, `UPDATE` e `DELETE`.

### P54 — "Quando você **não** criaria um índice?" `[julgamento — a pergunta que separa]`

**O que testam:** se você entende o custo ou só o benefício.

**A resposta forte, com o caso medido:** coluna pouco seletiva. Na mesma tabela de 500 mil linhas, um índice em `cliente_id` (13 linhas devolvidas) deu **1518x**; um índice em `tipo` (100 mil linhas devolvidas) deu **ganho zero** — foi usado pelo otimizador e não mudou nada, cobrando disco e escrita para sempre.

**A regra:** o índice compensa quando o filtro devolve menos de ~5% a 10% da tabela. Também não indexar: tabela pequena, tabela de escrita intensa, consulta que roda uma vez por mês, e coluna que nenhuma consulta filtra — cardinalidade boa responde "poderia ajudar", não "é necessário".

**O caso que impressiona:** em 12,5% da tabela, medido, o índice tornou a consulta **51% mais lenta**. Não é neutro — é prejuízo.

### P55 — "A consulta está lenta. Qual o primeiro passo?" `[procedimento]`

**A resposta errada é "criar um índice".** A certa é `EXPLAIN QUERY PLAN`.

**A sequência:** ler o plano (é `SCAN`?) → medir a seletividade do filtro (`COUNT(*)` do `WHERE` contra o total) → só então decidir → **medir de novo depois** → se não melhorou, `DROP INDEX`.

**O passo que quase ninguém cita é o último.** Índice criado que não ajudou costuma ficar para sempre, porque ninguém volta para conferir. Desfazer é parte do procedimento, não uma exceção.

**Um detalhe de método que mostra experiência:** o plano fica em cache na conexão. Medir, criar o índice e medir de novo na mesma conexão pode reaproveitar o plano antigo e produzir um número errado — e um número errado convence mais que nenhum número.

### P56 — "Por que `WHERE UPPER(nome) = 'ANA'` não usa o índice?" `[conceitual — pega o mecanismo]`

**Resposta forte:** o índice guarda `nome`, não `UPPER(nome)`. São valores diferentes, e a ordenação de um não ajuda a buscar o outro. Vale para qualquer função sobre a coluna no `WHERE`: `SUBSTR(cpf,1,3)`, `strftime('%Y', data)`, até `cliente_id + 0` — medido, 36,61 ms contra 0,04 ms da versão sem a soma.

**As saídas:** índice sobre expressão (onde o banco suportar), coluna normalizada gravada já em minúsculas, ou `COLLATE NOCASE`. Para datas, reescrever como faixa: `data >= '2026-03-01' AND data < '2026-04-01'` em vez de extrair o mês.

**A ressalva que poucos trazem:** reescrever o filtro para usar índice **não pode mudar a resposta**. `UPPER(nome) = 'ANA'` e `nome = 'Ana'` são perguntas diferentes se houver `'ANA'` ou `'ana'` na base — e verificar isso faz parte da otimização.

### P57 — "Explique ACID." `[conceitual — a mais previsível do módulo]`

**A resposta boa:** **A**tomicidade (tudo ou nada), **C**onsistência (as restrições valem ao fim), **I**solamento (ninguém vê estado intermediário), **D**urabilidade (confirmado sobrevive à queda de energia) — cada uma com um exemplo.

**A resposta que separa** termina dizendo o que ACID **não** garante. Ele descreve o comportamento de cada transação; não escolhe o padrão de acesso da aplicação. Medido no SQLite, que implementa o nível **mais rígido** de isolamento (`SERIALIZABLE`): dois saques concorrentes de uma conta de R$ 1.000,00, esperado R$ 700,00, resultado R$ 800,00 — **sem erro nenhum**. As quatro letras cumpridas, o dinheiro perdido.

### P58 — "O que é *lost update* e como evitar?" `[caso prático]`

**O mecanismo:** A lê 1000, B lê 1000, A grava 900, B grava 800. As duas leituras eram válidas; a segunda escrita sobrescreveu a primeira. É o padrão **ler-modificar-escrever**, e ele não produz erro.

**As três correções, em ordem de preferência:**
1. **Operação em vez de valor** — `SET saldo = saldo - 100`. Dispensa transação, não bloqueia ninguém. Primeira escolha sempre que a mudança couber como expressão.
2. **`BEGIN IMMEDIATE`** — quando a decisão é complexa demais para caber num `WHERE`. Bloqueio pessimista: assume o conflito e previne.
3. **Bloqueio otimista** — gravar com `WHERE valor = <o que foi lido>` e conferir `rowcount`; zero significa "alguém mudou no meio, releia". Assume que o conflito é raro e apenas detecta. Se conflitos forem frequentes, todo mundo refaz o tempo todo e fica pior que esperar.

**O detalhe que impressiona:** a escolha entre 2 e 3 é uma aposta na **frequência do conflito** — os nomes "pessimista" e "otimista" dizem exatamente isso.

### P59 — "Está aparecendo `database is locked`. O que investigar?" `[depuração]`

**A sequência:** transação longa aberta em algum lugar (a causa mais comum) → `COMMIT` esquecido num caminho de erro → `timeout` curto demais no driver → modo de journal.

**O que mostra experiência:** dizer que no SQLite há **um escritor por vez no banco inteiro** — não por linha, não por tabela. Não é um defeito a contornar; é o modelo. E que ajustar o `timeout` **transforma o erro numa espera**, o que resolve boa parte dos casos sem mudar código.

**A pergunta de volta que impressiona:** "há chamada de rede ou leitura de arquivo dentro de alguma transação?" É a causa mais frequente de transação longa, e a de correção mais direta.

### P60 — "Por que não usar SQLite em produção?" `[premissa capciosa — cuidado]`

**Não aceite a premissa.** SQLite é o banco mais instalado do mundo: está em todo celular, todo navegador, todo sistema embarcado. Para aplicativo local, site de leitura intensa ou análise sobre arquivo, é frequentemente a escolha **certa** — sem servidor, sem configuração, um arquivo.

**O limite real, dito com precisão:** um escritor por vez no banco inteiro. Isso torna inadequado o cenário de muitas escritas simultâneas — um sistema transacional com centenas de usuários gravando ao mesmo tempo. É onde PostgreSQL e MySQL entram, bloqueando por linha em vez do banco todo.

**A ressalva que fecha:** bloqueio por linha resolve a concorrência e cria o *deadlock* — duas transações esperando uma pela outra. Nenhuma das duas arquiteturas é gratuita; conhecer o que cada uma cobra é o que permite escolher em vez de repetir.

### P61 — "Modele um sistema de reservas de hotel." `[caso prático — o formato clássico de entrevista sênior]`

**O erro é começar a desenhar.** Comece perguntando: um quarto tem tipo, e a reserva é de um quarto específico ou de um tipo? Cancelamento apaga a reserva ou muda o status? O preço da diária varia por período? Um hóspede pode reservar para outra pessoa?

**Depois:** entidades (`hoteis`, `quartos`, `hospedes`, `reservas`), relações (um hotel tem N quartos; uma reserva é de um quarto e um hóspede), e as decisões justificadas — sobretudo a do **preço da diária copiado para dentro da reserva**, pelo motivo do `preco_unitario_centavos`.

**O que se avalia não é a resposta certa, é o processo:** as perguntas antes, as relações identificadas, o que você justifica e o que reconhece como discutível.

### P62 — "O que é normalização, e até onde normalizar?" `[conceitual]`

**As três formas com um exemplo cada:** 1FN — nada de lista numa célula; 2FN — toda coluna depende da chave inteira; 3FN — nenhuma coluna depende de outra coluna comum. A regra prática que resume: **cada fato mora em um só lugar**.

**A resposta madura:** até a 3FN por padrão, desnormalizando **com motivo escrito**. E o exemplo que prova domínio: `itens_pedido.preco_unitario_centavos` repete o preço de `produtos` de propósito, porque não é o mesmo fato — um é *quanto custa hoje*, o outro é *quanto custou naquela venda*.

**O que impressiona:** dizer que normalização elimina **fato repetido**, não valores parecidos. É a distinção que separa desnormalização deliberada de erro.

### P63 — "Como você migra um schema em produção sem perder dados?" `[procedimento]`

**A sequência:** migração **versionada** (arquivo numerado, com o comando que aplica e o que reverte) → transacional, apagando o resultado se falhar no meio → **conferência antes de declarar sucesso** → plano de reversão → a estrutura nova convivendo com a antiga durante a transição.

**O detalhe que separa — o que conferir.** Contagem de cada tabela **não é suficiente**: trocar o `cliente_id` entre dois pedidos preserva contagens e faturamento total, e embaralha o relatório de melhores clientes sem que nada acuse. É preciso ao menos um agregado **por grupo**. E a conferência de valores se faz em **centavos**, porque em ponto flutuante duas somas corretas podem diferir.

### P64 — "Qual a diferença entre OLTP e OLAP?" `[conceitual — arquitetura]`

**OLTP registra:** muitas escritas pequenas, schema normalizado, integridade acima de tudo, transações curtas. É o schema que você acabou de projetar.

**OLAP analisa:** poucas escritas em lote, tabelas largas, dados repetidos de propósito, junções evitadas, integridade relaxada porque os dados chegam já validados.

**O que fecha a resposta:** as duas formas invertem quase todas as decisões, e nenhuma está errada — elas resolvem problemas diferentes. Confundi-las é a causa mais comum de um data warehouse lento ou de um sistema transacional inconsistente. **A tradução de uma para a outra é o trabalho de engenharia de dados.**
