# Simulado CP2 — Módulo 03 (variante A)

**Tempo:** 60–90 min · **Composição:** 10 objetivas + 3 discursivas + 1 prático (~45 min)
**Aprovação:** ≥ 8/10 objetivas **e** prático ≥ 3 na rubrica. 6–7/10 ou prático = 2 → revisão dirigida + [variante B](modulo-03-b.md). ≤ 5/10 → refazer o módulo em ritmo de revisão.
**Regra de honestidade:** sem consultar durante as objetivas e discursivas; o prático é de consulta livre. Gabarito no fim — depois de terminar tudo.

## Objetivas

**Q1.** Uma tabela tem 8 clientes, 1 com `email` nulo. `SELECT COUNT(*), COUNT(email) FROM clientes` devolve:
a) 8, 8 · b) 8, 7 · c) 7, 7 · d) 7, 8

**Q2.** `WHERE cidade = NULL` não retorna as linhas com cidade nula porque:
a) A sintaxe está errada e daria erro · b) `NULL` comparado a qualquer coisa é **desconhecido**, e o `WHERE` só passa o verdadeiro · c) `NULL` é convertido para string vazia · d) Falta um `IS`

**Q3.** Juntar `pedidos` (20 linhas) com `itens_pedido` (31 linhas) por `pedido_id` produz um resultado com:
a) 20 linhas · b) 31 linhas · c) 51 linhas · d) 620 linhas

**Q4.** `NOT IN` com uma subconsulta que contém um `NULL` devolve:
a) Todas as linhas · b) As linhas corretas, ignorando o `NULL` · c) **Zero** linhas · d) Erro de sintaxe

**Q5.** `UPDATE produtos SET ativo = 1 WHERE categoria = 'audio'` em 4 produtos que **já estão** ativos devolve:
a) `Linhas afetadas: 0` · b) `Linhas afetadas: 4` · c) Erro · d) Aviso de operação redundante

**Q6.** No SQLite sem `STRICT`, `INSERT INTO t(a INTEGER) VALUES ('abacaxi')`:
a) Dá erro de tipo · b) Grava `0` · c) **Grava como texto**, sem erro · d) Grava `NULL`

**Q7.** Quantos `NULL` cabem numa coluna declarada `UNIQUE`?
a) Nenhum · b) Exatamente um · c) **Quantos forem** · d) Depende do `STRICT`

**Q8.** Um índice numa coluna com 5 valores distintos, numa tabela de 500 mil linhas:
a) Acelera ~700x · b) **Não traz ganho** e cobra escrita e disco · c) É recusado pelo banco · d) Só funciona com `STRICT`

**Q9.** Dentro de uma transação, um comando falha por violação de `CHECK`. A transação:
a) É desfeita automaticamente · b) **Continua aberta**, com as alterações anteriores aplicadas · c) É confirmada até o ponto do erro · d) Fecha a conexão

**Q10.** `itens_pedido.preco_unitario_centavos` repete o preço de `produtos` porque:
a) É um erro de normalização a corrigir · b) É cache para acelerar consultas · c) **São dois fatos diferentes**: preço de hoje e preço daquela venda · d) O SQLite exige a duplicação

## Discursivas

**D1.** Explique, em até 8 linhas, por que `LEFT JOIN` sozinho não responde "quais clientes nunca compraram" — e o que falta. Diga também por que `COUNT(*)` dá a resposta errada nesse cenário e o que usar no lugar.

**D2.** Enuncie o procedimento de cinco passos antes de um `UPDATE` em produção e explique **o que cada passo pega**. Depois responda: em que cenário esse procedimento passa mesmo com o comando destruindo dados?

**D3.** Descreva o *lost update* com um exemplo numérico. Diga qual letra de ACID ele viola e justifique a resposta. Apresente duas correções e diga quando cada uma é preferível.

## Prático (~45 min · consulta livre)

Sobre `dados/aurora.db`, entregue um arquivo `simulado.sql` com:

1. **(consulta)** Faturamento por cidade dos pedidos concluídos, com as cidades sem faturamento aparecendo com zero. Em centavos, sem inflar por multiplicação de linhas.
2. **(CTE)** Reescreva a consulta acima com no mínimo duas CTEs encadeadas e nomes que descrevem o que produzem.
3. **(escrita)** Um `UPDATE` que desative produtos nunca vendidos, com o `SELECT` de ensaio comentado acima, o número esperado, e `BEGIN`/`COMMIT`.
4. **(estrutura)** O `CREATE TABLE` de uma tabela `avaliacoes` (produto, nota de 1 a 5, comentário opcional, data), com `STRICT`, restrições e a ação de `ON DELETE` justificada em comentário.
5. **(índice)** Um `EXPLAIN QUERY PLAN` de uma consulta sua, com um comentário dizendo se é `SCAN` ou `SEARCH` e se um índice ajudaria — com a seletividade medida.
6. **(prova dos nove)** Uma consulta que confirme o total do item 1 por outro caminho.

### Rubrica (0–4)

| Nota | Critério |
|---|---|
| 4 | Tudo correto; conferências presentes; decisões justificadas em comentário; nenhuma soma inflada; a seletividade do item 5 é medida, não estimada |
| 3 | Correto, com uma justificativa fraca ou a prova dos nove ausente |
| 2 | Consultas funcionam mas há soma inflada, `COUNT(*)` indevido num `LEFT JOIN`, ou `UPDATE` sem ensaio |
| 1 | Consultas com erro de sintaxe ou que não respondem ao pedido |

---

## Gabarito

**Q1 — b.** `COUNT(*)` conta linhas (8); `COUNT(email)` conta valores não nulos (7). A diferença **mede** os nulos. (03.05)

**Q2 — b.** Lógica de três valores: `= NULL` é desconhecido, e o `WHERE` só deixa passar o verdadeiro. A sintaxe é válida — o comando roda e devolve zero linhas, que é o pior dos mundos. (03.03)

**Q3 — b.** Um `INNER JOIN` pai-filho produz **uma linha por filho**: 31. O pai se repete tantas vezes quantos filhos tiver, e é por isso que somar uma coluna de `pedidos` depois da junção infla. (03.07)

**Q4 — c.** `NOT IN` vira uma conjunção de desigualdades; `x <> NULL` é desconhecido, e o `AND` nunca é verdadeiro. Use `NOT EXISTS`. (03.09)

**Q5 — b.** O contador informa as linhas que o `WHERE` **encontrou**, não as que mudaram de valor. Serve para conferir o alcance do filtro. (03.11)

**Q6 — c.** Afinidade de tipos: converte quando dá, guarda como veio quando não dá. `typeof()` revelaria `text` numa coluna `INTEGER`. Com `STRICT`, seria recusado. (03.12)

**Q7 — c.** `UNIQUE` recusa valores **iguais**, e dois `NULL` nunca são iguais. Campo único e obrigatório exige `NOT NULL UNIQUE`. (03.13)

**Q8 — b.** 5 valores distintos = ~100 mil linhas por valor = 20% da tabela. Medido: ganho zero. O índice guarda ponteiros, e cem mil idas ao disco custam mais que ler tudo em sequência. (03.14)

**Q9 — b.** O erro **não** desfaz a transação. Um `COMMIT` a seguir grava a metade da operação. `ROLLBACK` explícito é obrigação de quem escreve. (03.15)

**Q10 — c.** Desnormalização deliberada: `produtos.preco_centavos` é *quanto custa hoje*; `preco_unitario_centavos` é *quanto custou naquela venda*. Normalização elimina fato repetido, não valores parecidos. (03.16)

**D1.** O `LEFT JOIN` preserva todos os clientes, inclusive os sem pedido — mas os traz **junto** com os que compraram. Falta `WHERE pedidos.id IS NULL`, que isola as linhas em que não houve correspondência: é o *anti-join*. Sobre a contagem: a linha preservada **existe**, então `COUNT(*)` conta 1 para quem nunca comprou; `p.id` nessa linha é `NULL`, então `COUNT(p.id)` conta 0 — a resposta certa. Com dois `JOIN`, é preciso `COUNT(DISTINCT p.id)`, porque a multiplicação de linhas infla também a contagem. (03.08)

**D2.** Rascunho (nunca ensaie em produção) → `SELECT` de ensaio com o `WHERE` exato, anotando as linhas (pega `WHERE` largo demais **e** `WHERE` que não acha nada) → `BEGIN` (torna reversível) → o comando com o `WHERE` **copiado**, não redigitado (pega erro de digitação) → conferir linhas afetadas contra o ensaio (pega divergência de alcance). **O cenário em que o procedimento passa e os dados somem:** `ON DELETE CASCADE`. Apagar um cliente exibe `Linhas afetadas: 1` e o ensaio também devolve 1 — os dois batem —, enquanto dez linhas de histórico são removidas em cascata. O contador conta o comando, não o efeito; com `CASCADE`, o ensaio precisa contar os **descendentes**. (03.11, 03.13)

**D3.** A lê o saldo (1000), B lê o saldo (1000), A grava 900, B grava 800. Esperado 700; resultado 800 — o saque de A evaporou, sem erro nenhum. **Não viola letra nenhuma de ACID**: cada transação foi atômica, consistente, isolada e durável, e as duas leituras retornaram valores confirmados. O defeito está no padrão ler-modificar-escrever da aplicação, e a prova é que acontece no SQLite, que implementa `SERIALIZABLE`. Correções: **(1)** expressar a mudança como operação — `SET saldo = saldo - 100` —, preferível sempre que couber, porque dispensa transação e não bloqueia ninguém; **(2)** `BEGIN IMMEDIATE`, quando a decisão é complexa demais para caber num `WHERE` — o custo é que os outros esperam. Há ainda o bloqueio otimista, indicado quando esperar é caro e o conflito é raro. (03.15)
