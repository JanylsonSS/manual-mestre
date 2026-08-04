# Resumo — Módulo 03: SQL

Uma página. Usado nas revisões D+30/D+90 dos capítulos deste módulo.

## Consulta (03.01–03.05)

O modelo **relacional** existe para resolver o que planilha e arquivo não resolvem: dado repetido que desatualiza, ausência de tipo, nenhuma garantia de integridade e nenhuma concorrência. **Tabela** é a coisa, **linha** é a ocorrência, **coluna** é o fato. **Chave primária** identifica; **chave estrangeira** aponta para a chave primária de outra tabela e o banco recusa referência quebrada.

`SELECT colunas FROM tabela WHERE condição`. O `WHERE` decide **quais linhas**; o `SELECT`, **quais colunas**. Operadores: `=`, `<>`, `>`, `BETWEEN`, `IN`, `LIKE` (`%` = qualquer coisa, `_` = um caractere).

**`NULL` é o fio condutor do módulo inteiro.** Ele não é zero nem vazio: é **desconhecido**, e a lógica é de **três valores**. `NULL = NULL` não é verdadeiro — é desconhecido. Daí `IS NULL` / `IS NOT NULL`, nunca `= NULL`. Essa mesma mecânica reaparece em cinco capítulos: no `WHERE` (03.03), na agregação (03.05), no `LEFT JOIN` (03.08), no `NOT IN` (03.09) e nas restrições (03.13).

`ORDER BY col DESC`, `LIMIT n`, `DISTINCT`. Aliases com `AS` — e o `AS` é para quem lê, não para o banco. Datas em texto **ISO `YYYY-MM-DD`**: a ordem alfabética coincide com a cronológica.

Agregação: `COUNT(*)` conta **linhas**; `COUNT(coluna)` conta **valores não nulos** — a diferença entre os dois **mede** os nulos. `SUM`, `AVG`, `MIN`, `MAX` **ignoram `NULL`**, o que muda a média sem avisar. Dinheiro sempre em **centavos inteiros**, e toda prova dos nove se faz em centavos.

## Agrupamento e junções (03.06–03.08)

`GROUP BY` divide em grupos e devolve **uma linha por grupo**; `WHERE` filtra **linhas antes**, `HAVING` filtra **grupos depois**. `GROUP BY` **agrupa os nulos numa linha só** — comportamento oposto ao do `UNIQUE`.

`JOIN` combina linhas de tabelas relacionadas pela condição do `ON`. A habilidade central é **prever o número de linhas**: juntar pai com filho **multiplica** o pai pelo número de filhos, e somar depois disso infla o total. `INNER` mantém só quem casa dos dois lados.

`LEFT JOIN` preserva a tabela da esquerda e preenche o resto com `NULL` — é o que responde perguntas **pela ausência**: quem nunca comprou, o que nunca vendeu (`WHERE chave IS NULL`, o *anti-join*). Num `LEFT JOIN`, `COUNT(*)` conta 1 para a linha preservada e `COUNT(p.id)` conta 0 — a resposta certa. Com **dois** `JOIN`, é preciso `COUNT(DISTINCT p.id)`.

## Composição (03.09–03.11)

**Subconsultas** em três posições: `WHERE`, `FROM` e `SELECT`. Não correlacionada roda **uma vez**; correlacionada menciona a consulta externa e roda **por linha**. `NOT IN` com um `NULL` na lista devolve **zero linhas** — use `NOT EXISTS`, que é imune.

**CTEs (`WITH`)** transformam aninhamento em etapas nomeadas, lidas de cima para baixo. `WITH` aparece **uma** vez; as demais vêm por vírgula. O resultado é idêntico ao da subconsulta — muda a leitura e o **reuso**. E resolve na raiz o problema das duas tabelas filhas: cada uma agregada na sua CTE, reduzida a uma linha por pai **antes** de qualquer junção.

**Escrita** (`INSERT`, `UPDATE`, `DELETE`): a sintaxe é curta, o perigo mora no `WHERE`. O procedimento de **cinco passos**: rascunho → `SELECT` de ensaio (anote as linhas) → `BEGIN` → comando com o `WHERE` **copiado** → conferir linhas afetadas contra o ensaio. `UPDATE` sem `WHERE` não é erro de sintaxe: é comando válido que atinge a tabela inteira. E quando o pedido diz "apagar", quase sempre quer dizer "desativar".

## Estrutura (03.12–03.14)

**DDL.** O SQLite tem cinco tipos reais (`INTEGER`, `REAL`, `TEXT`, `BLOB`, `NULL`) e o tipo declarado é uma **afinidade**, não uma lei: `'abacaxi'` entra numa coluna `INTEGER` sem erro, `'42'` vira número, `'3.7'` vira `real`. `STRICT` (3.37+) devolve o rigor — garante **tipo**, não **faixa**. As três decisões de toda base: dinheiro em centavos (`0.1 + 0.2 = 0.3` é **falso**), data em `TEXT` ISO, booleano em `INTEGER` 0/1. Não há `ALTER COLUMN`: mudar tipo são quatro passos (criar, copiar, apagar, renomear), em transação — e `CAST` **trunca**, então `CAST(19.99*100 AS INTEGER)` dá 1998.

**Constraints.** `NOT NULL`, `UNIQUE`, `PRIMARY KEY`, `CHECK`, `FOREIGN KEY`. Uma restrição recusa o **comprovadamente falso** — e `NULL` é desconhecido. Daí os dois buracos: `UNIQUE` aceita **vários** nulos e `NULL` atravessa qualquer `CHECK`. Campo único e obrigatório precisa de `NOT NULL UNIQUE`, os dois. `ON DELETE`: `CASCADE` apaga junto (e o alcance é invisível — `Linhas afetadas: 1` pode remover 10), `SET NULL` deixa órfão, `RESTRICT` recusa. Na dúvida, `RESTRICT`: recusar é reversível.

**Índices.** Cópia ordenada em B-tree: ~20 comparações em vez de um milhão. `EXPLAIN QUERY PLAN` mostra `SCAN` (varre) ou `SEARCH` (usa índice) — e é o **primeiro** comando diante de consulta lenta. O que decide é a **seletividade**: 13 linhas de 500 mil deram 763x; 100 mil de 500 mil deram ganho zero; e a 12,5% o índice deixou a consulta **51% mais lenta**. Índice custa disco e escrita (três índices: +66%), para sempre. Qualquer função sobre a coluna no `WHERE` o desliga.

## Garantias e projeto (03.15–03.16)

**ACID**: **A**tômico (tudo ou nada), **C**onsistente (restrições valem no fim), **I**solado (ninguém vê o meio), **D**urável (confirmado resiste à queda de energia). E a lição do capítulo: **as quatro podem estar íntegras enquanto o resultado está errado**. O *lost update* — dois leem, dois gravam, um sobrescreve o outro — perde dinheiro **sem mensagem nenhuma**, mesmo no SQLite, que é `SERIALIZABLE`. Correções: operação em vez de valor (`SET x = x - 100`), `BEGIN IMMEDIATE` quando a leitura decide a escrita, ou bloqueio otimista com `rowcount`. Um erro **não** desfaz a transação: ela fica aberta, e um `COMMIT` grava a metade. SQLite: **um escritor por vez** no banco inteiro.

**Modelagem.** Que coisas existem (tabelas), que fatos as descrevem (colunas), como se relacionam (chaves). Em 1-N a chave vai no lado **muitos**; N-N sempre vira **tabela do meio**, que ganha os fatos do encontro. Normalize até a **3FN** — *cada fato mora em um só lugar* — e desnormalize quando o dado repetido for **outro fato**: `preco_unitario_centavos` é *quanto custou naquela venda*, não *quanto custa hoje*. Um schema só está pronto depois de você tentar quebrá-lo, e toda migração termina em conferência de contagens **e** de um agregado **por grupo** — conferir só o total passa com os dados embaralhados.
