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
