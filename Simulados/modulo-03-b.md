# Simulado CP2 — Módulo 03 (variante B)

**Quando usar:** depois de revisão dirigida, se a [variante A](modulo-03.md) ficou entre 6 e 7 objetivas, ou se o prático saiu 2. Mesmos objetivos, itens diferentes — decorar a variante A não ajuda aqui.

**Tempo:** 60–90 min · **Aprovação:** ≥ 8/10 objetivas **e** prático ≥ 3.

## Objetivas

**Q1.** `SELECT AVG(preco) FROM produtos` numa tabela com 10 produtos, 2 com preço nulo, calcula a média sobre:
a) 10 valores, tratando nulos como 0 · b) **8 valores** · c) 10 valores, tratando nulos como a média · d) Devolve `NULL`

**Q2.** A diferença entre `WHERE` e `HAVING` é que:
a) `HAVING` é mais rápido · b) `WHERE` filtra **linhas antes** do agrupamento; `HAVING` filtra **grupos depois** · c) `WHERE` só funciona com índice · d) São sinônimos

**Q3.** Você tem um `LEFT JOIN` de `clientes` com `pedidos`. Para contar pedidos por cliente, o correto é:
a) `COUNT(*)` · b) **`COUNT(pedidos.id)`** · c) `COUNT(clientes.id)` · d) `SUM(1)`

**Q4.** Numa CTE, `WITH a AS (...) WITH b AS (...)` produz:
a) Duas CTEs válidas · b) **Erro de sintaxe** · c) Só a segunda é considerada · d) Aviso, mas funciona

**Q5.** `DELETE FROM clientes WHERE id = 1`, com pedidos apontando para esse cliente e `PRAGMA foreign_keys = ON`:
a) Apaga o cliente e os pedidos · b) Apaga o cliente e deixa órfãos · c) **É recusado** · d) Apaga só se não houver pedidos concluídos

**Q6.** `CAST(19.99 * 100 AS INTEGER)` devolve:
a) 1999 · b) **1998** · c) 2000 · d) 19.99

**Q7.** Uma coluna `TEXT NOT NULL` aceita o valor `'   '` (três espaços)?
a) Não, `NOT NULL` impede · b) **Sim** — `''` e espaços não são `NULL` · c) Depende do `STRICT` · d) Só com `DEFAULT`

**Q8.** `WHERE UPPER(nome) = 'ANA'` numa coluna com índice em `nome` produz:
a) `SEARCH`, usando o índice · b) **`SCAN`** · c) Erro · d) `SEARCH`, mas mais lento

**Q9.** `BEGIN` comum, numa operação em que você lê o saldo para decidir se saca:
a) É suficiente, porque reserva a escrita · b) **Não é suficiente** — só reserva no primeiro `UPDATE` · c) É equivalente a `BEGIN IMMEDIATE` · d) Impede outras leituras

**Q10.** Você migrou dados para um schema novo. Contagens e faturamento total batem. Isso prova:
a) Que a migração está correta · b) **Nada sobre atribuição** — trocar `cliente_id` entre pedidos passa nos dois testes · c) Que não houve perda de linhas, e nada mais é verificável · d) Que os tipos foram preservados

## Discursivas

**D1.** Explique por que juntar um pedido com **duas** tabelas filhas (itens e pagamentos) e somar produz totais inflados. Descreva a solução com CTEs e diga por que `COUNT(DISTINCT ...)` **não** resolve o caso da soma.

**D2.** Um schema declara `email TEXT UNIQUE` e a base acumulou linhas sem e-mail. Explique o que a restrição garante e o que não garante. Depois descreva o que você faria para aplicar `NOT NULL` numa tabela em produção que já viola a regra.

**D3.** Explique a seletividade como critério de indexação. Use dois exemplos numéricos opostos e explique o **mecanismo** — por que um índice pode ser inútil, e por que pode até piorar.

## Prático (~45 min · consulta livre)

Sobre `dados/aurora.db`, entregue `simulado-b.sql` com:

1. **(consulta)** Os 3 clientes com maior ticket médio entre pedidos concluídos, mostrando também quantos pedidos cada um fez.
2. **(ausência)** Uma consulta que liste categorias sem nenhuma venda — provando que a lista não está vazia por engano.
3. **(escrita)** Um roteiro que cancele pedidos pendentes anteriores a uma data, com investigação, ensaio, `BEGIN`, critério explícito de `ROLLBACK` e verificação final.
4. **(estrutura)** O `CREATE TABLE` de `enderecos` (cliente, logradouro, número, cidade, CEP), com os tipos justificados em comentário — inclusive por que número e CEP são `TEXT`.
5. **(concorrência)** Descreva em comentário, em até 6 linhas, o que aconteceria se duas conexões executassem seu roteiro do item 3 ao mesmo tempo.
6. **(prova dos nove)** Confirme o item 1 por outro caminho, em centavos.

### Rubrica (0–4)

| Nota | Critério |
|---|---|
| 4 | Tudo correto; conferências presentes; tipos justificados; o item 5 identifica corretamente o risco e a mitigação |
| 3 | Correto, com uma justificativa fraca ou a prova dos nove ausente |
| 2 | Funciona, mas com soma inflada, ensaio ausente ou tipos mal escolhidos |
| 1 | Erro de sintaxe ou não responde ao pedido |

---

## Gabarito

**Q1 — b.** Agregações **ignoram** `NULL`. `AVG` divide pela contagem de valores presentes (8), não pelo total de linhas. É a diferença que mais engana em relatório. (03.05)

**Q2 — b.** `WHERE` age antes do agrupamento e não pode usar agregados; `HAVING` age sobre os grupos formados e pode. (03.06)

**Q3 — b.** A linha preservada existe, então `COUNT(*)` conta 1 mesmo para quem não tem pedido; `pedidos.id` é `NULL` ali, e `COUNT` de coluna ignora nulos. (03.08)

**Q4 — b.** `near "WITH": syntax error`. `WITH` aparece uma vez; as CTEs seguintes vêm por vírgula. (03.10)

**Q5 — c.** `FOREIGN KEY constraint failed`. A chave estrangeira impede o órfão — e só age com o pragma ligado, que vem **desligado** por padrão no SQLite. (03.11, 03.13)

**Q6 — b.** `19.99 * 100` é `1998.9999999999998` em ponto flutuante, e `CAST` **trunca**. Uma migração de dinheiro sem `ROUND` perde um centavo por linha, sem erro. (03.12)

**Q7 — b.** String vazia e espaços são `text` de comprimento 0, não `NULL`. Só um `CHECK (LENGTH(TRIM(nome)) > 0)` recusa. (03.12, 03.16)

**Q8 — b.** O índice guarda `nome`, não `UPPER(nome)` — são valores diferentes, e a ordenação de um não ajuda a buscar o outro. Vale para qualquer função sobre a coluna. (03.14)

**Q9 — b.** `BEGIN` abre em modo de leitura e só reserva a escrita no primeiro comando de alteração — tarde demais para impedir que outra conexão leia o mesmo valor. `BEGIN IMMEDIATE` reserva antes de ler. (03.15)

**Q10 — b.** Trocar o `cliente_id` entre dois pedidos preserva contagens e faturamento total, e embaralha a atribuição. É preciso ao menos um agregado **por grupo** — faturamento por cliente. (03.16)

**D1.** Com duas filhas, a junção produz o **produto cartesiano** entre elas para cada pai: um pedido com 3 itens e 2 pagamentos vira 6 linhas. Cada item é contado 2 vezes e cada pagamento 3 vezes, então as duas somas inflam. A solução é uma **CTE por filha**, cada uma agregando ao nível do pedido — reduzindo a **uma linha por pedido** — e só então juntando ao pai; com uma linha de cada lado, não há o que multiplicar. **`COUNT(DISTINCT ...)` não resolve a soma** porque ele elimina repetições de *identificadores*, e a soma opera sobre *valores*: dois pagamentos de R$ 50,00 são legitimamente iguais, e `DISTINCT` os fundiria num só. Ele corrige contagens e corrompe somas. (03.07, 03.10)

**D2.** `UNIQUE` garante que dois valores **presentes** não se repitam. Não garante presença: `NULL` nunca é igual a `NULL`, então vários nulos convivem, e a unicidade que se imagina ter não existe para eles. Para aplicar `NOT NULL` numa tabela que já viola: **(1)** auditar — `SELECT COUNT(*) FROM t WHERE col IS NULL` —, e note que a auditoria de duplicados é uma pergunta **separada**, com `WHERE col IS NOT NULL` na subconsulta, senão o `GROUP BY` junta os nulos e acusa duplicata inexistente; **(2)** listar as linhas problemáticas; **(3)** decidir com quem conhece o negócio — preencher inventa dado, excluir destrói histórico, adiar é geralmente o certo; **(4)** aplicar a parte que não viola nada agora (o `UNIQUE`) e adiar o `NOT NULL` até o dado ser obtido; **(5)** como não há `ADD CONSTRAINT` no SQLite, a migração de quatro passos, em transação. (03.12, 03.13)

**D3.** Seletividade é a fração da tabela que o filtro devolve, e é o único critério que decide. **Exemplo A:** `cliente_id` com ~50 mil valores distintos em 500 mil linhas devolve ~13 linhas — 763x mais rápido com índice. **Exemplo B:** `tipo` com 5 valores devolve ~100 mil linhas, 20% da tabela — ganho zero, medido. O **mecanismo** explica os dois: o índice guarda **ponteiros**, não as linhas; encontrar as chaves é rápido nos dois casos, mas devolver os dados exige ir buscar cada linha na tabela. Treze idas são instantâneas; cem mil idas, cada uma para um lugar diferente do disco, custam mais que ler a tabela em sequência. E pode **piorar**: medido num filtro de 12,5%, o índice foi usado e a consulta ficou 51% mais lenta que a varredura. A referência prática é 5% a 10%, e acima disso a medição decide. (03.14)
