# Gabarito — Capítulo 03.10: CTEs (`WITH`)

Leia depois de tentar. Enunciados em [`../cap10.md`](../cap10.md).

> Todas as consultas deste gabarito foram executadas contra `dados/aurora.db`. Os números
> impressos aqui são saída real, não estimativa.

## A1 — Leia a CTE

| # | O que a CTE produz | O que a consulta final faz | Resultado |
|---|---|---|---|
| 1 | os produtos com `ativo = 1` | conta as linhas dessa lista | `11` |
| 2 | uma linha por categoria com a contagem | mantém só categorias com mais de 2 produtos | `acessorios 4`, `audio 4` (as outras duas têm 2 cada) |
| 3 | uma linha por pedido com a soma das quantidades | tira a média dessas somas | `1.9` |
| 4 | `a`: ids de clientes de campinas · `b`: o `cliente_id` de **cada** pedido | conta os pares — pedidos feitos por clientes de campinas | `7` |
| 5 | a sequência 1, 2, 4, 8… enquanto `x < 100` | lista a sequência | `1 2 4 8 16 32 64 128` |

**O detalhe do item 5.** A sequência termina em **128**, não em 64. A condição `x < 100` decide
se o passo *roda*, não se o resultado *entra*. Com `x = 64` a condição é verdadeira, então o
passo produz `128` — e `128` é adicionado antes de a condição ser testada de novo. Quem espera
"todos os valores menores que 100" conta errado por uma linha. É a mesma armadilha do `while`
em Python (01.13): a condição controla a iteração, não a saída.

**O detalhe do item 4.** A CTE `b` não agrupa nada — é uma linha por pedido. O `COUNT(*)` da
junção conta **pedidos**, não clientes. Se você respondeu "3 clientes de campinas", releu a
consulta certa mas contou a coisa errada. Ana, Fernanda, Beatriz e Rafael são de campinas;
Rafael não tem pedidos; os outros três somam 7 pedidos entre pedidos de todos os status.

## A2 — CTE ou não?

| # | Veredito | Por quê |
|---|---|---|
| 1 | **piora** | uma consulta de uma etapa não tem etapa para nomear; a CTE só adiciona duas linhas |
| 2 | **melhora muito** | três etapas conceituais viram três nomes; sem CTE, três níveis de aninhamento |
| 3 | **piora** | idem 1 |
| 4 | **melhora muito** | é o caso de reuso: sem CTE, o mesmo bloco escrito três vezes |
| 5 | **indiferente** | uma junção com filtro já se lê bem; use CTE se o filtro for longo |
| 6 | **melhora muito** | é o caso do 03.07: sem CTE, ou dobra a soma ou vira um remendo |

**O critério.** CTE não é enfeite. Ela paga por si mesma em três situações: (a) a consulta tem
**etapas** conceituais distintas; (b) a mesma etapa é usada **mais de uma vez**; (c) agregar
**duas tabelas filhas** do mesmo pai. Fora disso, ela adiciona linhas sem adicionar clareza —
e código que adiciona linhas sem adicionar clareza é custo.

## A3 — Ache o erro

**1. `WITH` repetido.** `WITH` aparece **uma** vez; as CTEs seguintes vêm por vírgula.

```
Erro de SQL: near "WITH": syntax error
```

Correção: `WITH a AS (SELECT 1 AS x), b AS (SELECT 2 AS y) SELECT * FROM a;`

**2. Comparação com a CTE, não com a coluna.** `media` é uma *tabela* de uma linha e uma
coluna. Comparar um número com uma tabela não define nada. Correção:

```sql
WITH media AS (SELECT AVG(preco_centavos) AS m FROM produtos)
SELECT nome FROM produtos WHERE preco_centavos > (SELECT m FROM media);
```

**3. Referência a uma CTE definida depois — e aqui o SQLite mente para você.**

Pelo padrão SQL, uma CTE só enxerga as CTEs declaradas **antes** dela (a exceção é a
recursiva, que enxerga a si mesma). `a AS (SELECT * FROM b)` com `b` declarada depois deveria
falhar. No PostgreSQL, falha. No SQLite:

```
      12

(1 linha)
```

Ele **aceitou** — porque não existe tabela chamada `b`, e o SQLite resolve o nome procurando
também nas CTEs seguintes. Note que ele não está sendo esperto: se o nome não existir em lugar
nenhum, o erro aparece (`no such table: inexistente`). O risco é maior justamente por
funcionar: você escreve assim aqui, o hábito pega, e a consulta quebra no banco do trabalho.
É a mesma lição do 03.03 sobre aspas duplas — **a permissividade do dialeto não é permissão.**
Declare na ordem em que se lê.

**4. Coluna sem apelido.** A CTE expõe a coluna com o nome literal `SUM(quantidade)`; não
existe `soma`.

```
Erro de SQL: no such column: soma
```

Correção: `SUM(quantidade) AS soma` dentro da CTE. Regra prática: **toda coluna calculada
dentro de uma CTE recebe apelido**, sempre — quem vai usá-la é o `SELECT` de fora.

**5. Recursiva sem parada.** Sem o `WHERE`, o passo nunca deixa de produzir linhas. Correção:
`WHERE n < 100`. Rode isto só sabendo como interromper (`Ctrl+C`).

**6. Ponto e vírgula no meio.** O `;` encerra o comando; o `SELECT` seguinte é um comando novo,
e `cte` não existe mais. A CTE vive **dentro** de um comando — só isso. Correção: remover o `;`.

## A4 — Nomeie a etapa

| # | Nome sugerido | Merece ser CTE? |
|---|---|---|
| 1 | `totais_por_pedido` | **sim** — é a etapa mais reutilizada do módulo |
| 2 | `produtos_ativos` | **talvez** — só se o filtro reaparecer ou for longo |
| 3 | `pedidos_concluidos_por_cliente` | **sim** — etapa de agregação com filtro |
| 4 | `preco_medio` | **sim, se reusado** — clássico caso (d) do A2 |
| 5 | — | **não** — `id > 0` não filtra nada; a etapa não existe |
| 6 | `preco_maximo_por_categoria` | **sim** — agregação nomeável |

**O teste do nome.** Se você não consegue nomear o bloco sem usar "e" ("clientes_e_pedidos_e_
totais"), o bloco está fazendo coisas demais — quebre em duas CTEs. Se o único nome honesto é
`temp`, `dados` ou `sub`, o bloco não é uma etapa e não merece CTE. **O nome é o teste da
abstração**, exatamente como em funções (01.16).

## AP1 — Refatorando

**(1) Ticket médio.** Comandos `[1]` e `[2]` de `codigo/cap10/etapas.sql`. Ambos devolvem
`489.31764705882347` com 17 pedidos. Idênticos ao último dígito — a CTE não muda o plano de
execução aqui, muda a ordem de leitura.

**(2) Produto mais caro por categoria.**

```sql
WITH maximos AS (
    SELECT categoria, MAX(preco_centavos) AS teto
    FROM produtos GROUP BY categoria
)
SELECT p.categoria, p.nome, p.preco_centavos / 100.0 AS preco
FROM produtos p
JOIN maximos m ON m.categoria = p.categoria AND m.teto = p.preco_centavos
ORDER BY preco DESC;
```

Melhorou? **Sim, e por um motivo específico:** a versão do 03.09 usava uma subconsulta
correlacionada no `WHERE`, reavaliada por linha. Aqui a etapa "qual é o teto de cada
categoria" fica explícita e é calculada uma vez. O ganho é de leitura; o de desempenho, se
houver, é do otimizador — não conte com ele sem medir (03.14).

**(3) Clientes acima da média.** Comando `[3]` do arquivo. Três CTEs encadeadas contra três
níveis de aninhamento. Melhorou sem discussão.

**A resposta honesta às três.** Em (1) a CTE empatou em resultado e ganhou em leitura; em (2)
ganhou pouco; em (3) ganhou muito. O padrão: **quanto mais etapas, maior o ganho.** Uma etapa
só, não refatore.

## AP2 — O reuso

Consulta (1) é o comando `[4]` do arquivo:

```
Carlos Menezes   2528.4  30.4
Fernanda Lima    1812.2  21.8
Ana Souza         988.6  11.9
Helena Prado      982.6  11.8
Beatriz Nogueira  899.0  10.8
Juliana Castro    738.7   8.9
Diego Alves       368.9   4.4
```

Os percentuais somam 100,1 por arredondamento — some-os e confira; é uma checagem barata que
pega erro de denominador.

**A contagem de duplicação.** A CTE `gasto` tem 5 linhas. Sem CTE, ela aparece duas vezes: no
`FROM` e dentro do `(SELECT SUM(total) FROM ...)`. São 5 linhas duplicadas — e, pior, **5
linhas que precisam mudar juntas**. Se amanhã o filtro virar `status IN ('concluido','pago')`
e você alterar só uma cópia, a consulta não dá erro: dá um percentual errado, silenciosamente.
Esse é o custo real da duplicação — não o teclado, o desalinhamento.

## AP3 — As duas filhas

O comando `[5]` mostra o padrão com uma filha. Com duas, ele se repete sem mudar de forma:

```sql
WITH itens AS (
    SELECT pedido_id, SUM(quantidade * preco_unitario_centavos) AS total_itens
    FROM itens_pedido GROUP BY pedido_id
),
pagos AS (
    SELECT pedido_id, SUM(valor_centavos) AS total_pago
    FROM pagamentos GROUP BY pedido_id
)
SELECT p.id,
       COALESCE(i.total_itens, 0) / 100.0 AS itens,
       COALESCE(g.total_pago,  0) / 100.0 AS pago
FROM pedidos p
LEFT JOIN itens i ON i.pedido_id = p.id
LEFT JOIN pagos g ON g.pedido_id = p.id
ORDER BY p.id;
```

**Por que resolve na raiz (as três linhas pedidas).** A soma dobrava porque a junção
multiplicava as linhas de uma filha pelas da outra **antes** de o `SUM` rodar. Cada CTE reduz
sua filha a **uma linha por pedido** antes de qualquer junção. Com uma linha de cada lado, a
junção não tem o que multiplicar. Não é um remendo sobre o sintoma — o sintoma deixa de
existir.

Compare com as duas saídas anteriores: no 03.07 o remendo foi `COUNT(DISTINCT ...)`, que
corrige contagens mas **não** corrige somas; no 03.09 o remendo foi a subconsulta correlacionada,
que corrige mas é reavaliada por linha e não tem nome. A CTE corrige, tem nome e roda uma vez.

## D1 — O painel executivo

```sql
WITH totais_por_pedido AS (
    SELECT p.id AS pedido_id, p.cliente_id,
           SUM(i.quantidade * i.preco_unitario_centavos) AS total_centavos
    FROM pedidos p
    JOIN itens_pedido i ON i.pedido_id = p.id
    WHERE p.status = 'concluido'
    GROUP BY p.id, p.cliente_id
),
resumo_por_cliente AS (
    SELECT cliente_id,
           COUNT(*)            AS pedidos,
           SUM(total_centavos) AS gasto,
           AVG(total_centavos) AS ticket
    FROM totais_por_pedido
    GROUP BY cliente_id
),
totais_gerais AS (
    SELECT SUM(gasto) AS faturamento, AVG(gasto) AS media_gasto
    FROM resumo_por_cliente
)
SELECT c.nome, c.cidade,
       COALESCE(r.pedidos, 0)         AS pedidos,
       COALESCE(r.gasto,   0) / 100.0 AS gasto,
       COALESCE(r.ticket,  0) / 100.0 AS ticket_medio,
       ROUND(COALESCE(r.gasto, 0) * 100.0
             / (SELECT faturamento FROM totais_gerais), 1) AS pct,
       ROUND((COALESCE(r.gasto, 0)
              - (SELECT media_gasto FROM totais_gerais)) / 100.0, 2) AS vs_media
FROM clientes c
LEFT JOIN resumo_por_cliente r ON r.cliente_id = c.id
ORDER BY gasto DESC;
```

Saída real:

```
nome             | cidade   | pedidos | gasto  | ticket_medio | pct  | vs_media
-----------------+----------+---------+--------+--------------+------+---------
Carlos Menezes   | sorocaba |       3 | 2528.4 |        842.8 | 30.4 |  1340.06
Fernanda Lima    | campinas |       5 | 1812.2 |       362.44 | 21.8 |   623.86
Ana Souza        | santos   |       3 |  988.6 |   329.5333... | 11.9 |  -199.74
Helena Prado     | NULL     |       2 |  982.6 |        491.3 | 11.8 |  -205.74
Beatriz Nogueira | campinas |       1 |  899.0 |        899.0 | 10.8 |  -289.34
Juliana Castro   | sorocaba |       2 |  738.7 |       369.35 |  8.9 |  -449.64
Diego Alves      | santos   |       1 |  368.9 |        368.9 |  4.4 |  -819.44
Rafael Torres    | campinas |       0 |    0.0 |          0.0 |  0.0 | -1188.34

(8 linhas)
```

**As três verificações que provam os critérios (b) e (c).**

- **(b)** São **8 linhas** para 8 clientes. Rafael Torres aparece com zeros — se a sua saída
  tem 7 linhas, o `LEFT JOIN` virou `JOIN` em algum ponto. `Helena Prado` com `cidade` NULL é
  o outro caso do 03.03 sobrevivendo até aqui: NULL na *cidade* não elimina ninguém, porque
  ninguém filtrou por cidade.
- **(c)** A prova dos nove: a soma da coluna `gasto` tem de bater com o faturamento calculado
  direto da tabela de itens, **sem passar pelas CTEs**. Faça a conferência **em centavos** —
  nunca em reais, pela razão do gabarito do 03.05:

  ```sql
  SELECT SUM(i.quantidade * i.preco_unitario_centavos)
  FROM itens_pedido i JOIN pedidos p ON p.id = i.pedido_id
  WHERE p.status = 'concluido';          -- 831840
  ```

  E a mesma soma vinda do painel (`SELECT SUM(gasto) FROM resumo_por_cliente`) → **831840**.
  Iguais ao centavo: nenhuma linha foi multiplicada. Se você somar a coluna em reais na mão
  (2528,4 + 1812,2 + 988,6 + 982,6 + 899,0 + 738,7 + 368,9 = 8318,40) o total também fecha aqui
  — mas essa coincidência não é garantia: bastam centavos truncados na exibição para a conta em
  reais divergir enquanto a de centavos fecha. Confira sempre no inteiro.
- **(d)** A versão aninhada precisa repetir o bloco `totais_por_pedido` **duas vezes** (uma no
  `FROM`, outra dentro da subconsulta da média) e chega a três níveis de indentação. Ela cabe
  na tela; o problema não é caber.

**O fecho.** A consulta com CTE tem mais linhas que a aninhada e é mais rápida de entender —
essas duas coisas não se contradizem. Legibilidade em SQL é critério de engenharia porque
consultas não são escritas uma vez: elas são lidas no plantão, alteradas por quem não as
escreveu, e auditadas quando o número no relatório parece errado. Uma consulta que só o autor
entende é uma consulta que ninguém pode corrigir sob pressão. O nome da CTE é a documentação
que não pode ficar desatualizada, porque o banco a executa.

---

## Erros mais comuns

1. **Repetir `WITH`.** Uma vez só; o resto por vírgula.
2. **Esquecer o apelido** de coluna calculada dentro da CTE.
3. **Comparar com a CTE** em vez de com `(SELECT coluna FROM cte)`.
4. **Achar que CTE é sempre melhor.** Em consulta de uma etapa, ela atrapalha.
5. **Nomear `temp`, `t1`, `dados`.** Se o nome não descreve, a CTE não valeu a pena.
6. **Recursiva sem condição de parada.**
7. **Perder o `LEFT`** em painéis: some quem nunca comprou, e some sem avisar.
8. **Confiar na ordem livre do SQLite** para referência entre CTEs (A3.3).
