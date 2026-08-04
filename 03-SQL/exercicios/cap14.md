# Exercícios — Capítulo 03.14: Índices

> **Antes de tudo:** `python codigo/cap14/preparar_indices.py`, depois
> `python codigo/cap14/medir.py`. Todos os exercícios usam `dados/indices.db`.
> Para as consultas soltas: `AURORA_BANCO=dados/indices.db python codigo/sql.py "..."`.

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap14.md`](gabaritos/cap14.md).

## Aquecimento

### A1 — `SCAN` ou `SEARCH`? `[Aquecimento · ~10 min · preveja o plano]`

**Tarefa.** Com **apenas** estes dois índices criados:

```sql
CREATE INDEX idx_cliente ON eventos(cliente_id);
CREATE INDEX idx_dt      ON eventos(data, tipo);
```

Preveja o plano de cada consulta **antes** de rodar `EXPLAIN QUERY PLAN`:

1. `SELECT * FROM eventos WHERE cliente_id = 27384;`
2. `SELECT * FROM eventos WHERE valor = 45000;`
3. `SELECT * FROM eventos WHERE data = '2026-03-15';`
4. `SELECT * FROM eventos WHERE tipo = 'login';`
5. `SELECT * FROM eventos WHERE data = '2026-03-15' AND tipo = 'login';`
6. `SELECT * FROM eventos WHERE id = 999;`
7. `SELECT COUNT(*) FROM eventos;`
8. `SELECT * FROM eventos WHERE cliente_id IN (1,2,3);`

**Dois resultados vão surpreender.** Identifique quais e explique.

### A2 — Vale a pena? `[Aquecimento · ~10 min · meça a cardinalidade primeiro]`

**Tarefa.** Para cada coluna, calcule `COUNT(DISTINCT coluna)`, estime que fração da tabela um filtro de igualdade devolve, e decida: **indexar ou não?**

1. `id` · 2. `cliente_id` · 3. `valor` · 4. `data` · 5. `tipo`
6. Uma coluna hipotética `ativo` com valores 0 e 1.

Para cada "sim", diga **qual consulta** justifica o índice. Um índice sem consulta que o use é só custo.

### A3 — Por que não usou? `[Aquecimento · ~10 min · o índice existe e é ignorado]`

**Tarefa.** Com `idx_cliente` e `idx_dt` criados, cada consulta abaixo faz `SCAN`. Diga **por quê** e reescreva a que der para reescrever:

1. `WHERE cliente_id + 0 = 27384`
2. `WHERE data LIKE '2026-03%'`
3. `WHERE data LIKE '%03-15'`
4. `WHERE tipo = 'login'`
5. `WHERE UPPER(tipo) = 'LOGIN'`
6. `WHERE valor > 1000`

### A4 — A ordem importa `[Aquecimento · ~10 min · índice composto]`

**Tarefa.** Com **só** o índice `(data, tipo)`, diga quais destes usam o índice — e confirme:

1. `WHERE data = '2026-03-15'`
2. `WHERE tipo = 'login'`
3. `WHERE data = '2026-03-15' AND tipo = 'login'`
4. `ORDER BY data LIMIT 5`
5. `ORDER BY tipo LIMIT 5`

Depois responda: se as consultas mais frequentes do sistema filtrassem **só** por `tipo` e por `tipo + data`, qual seria a ordem correta das colunas no índice?

## Aplicação

### AP1 — O benchmark `[Aplicação · ~25 min · com método]`

**Tarefa.** Meça três consultas antes e depois de criar o índice apropriado, seguindo o método do `medir.py`: conexão nova a cada medição, 7 repetições, **mediana**.

1. `WHERE valor BETWEEN 45000 AND 45100`
2. `WHERE data = '2026-03-15'`
3. `WHERE cliente_id = 27384 AND tipo = 'compra'`

Para cada uma: plano antes, tempo antes, índice criado, plano depois, tempo depois, ganho.

**A parte que ensina:** rode cada medição **duas vezes** e compare. A variação entre as duas rodadas é o seu ruído de medição — qualquer "ganho" menor que ele não é ganho.

### AP2 — Reescrevendo o filtro `[Aplicação · ~20 min · sem criar índice novo]`

**Tarefa.** Faça estas quatro consultas passarem de `SCAN` a `SEARCH` **sem criar nenhum índice** — só reescrevendo o `WHERE`. Os índices disponíveis são `idx_cliente` e `idx_dt`.

1. Todos os eventos de março de 2026.
2. Eventos do cliente cujo id, somado a zero, é 27384.
3. Eventos de 2026 (o ano inteiro).
4. Eventos entre 1º e 15 de março.

Para cada uma: consulta original com função ou `LIKE`, consulta reescrita, plano antes, plano depois, **tempo antes e depois**.

**A pergunta que decide o exercício.** Meça os tempos, não só os planos. **Em pelo menos uma das quatro, o `SEARCH` é mais lento que o `SCAN` que ele substituiu.** Descubra qual, calcule a seletividade daquele filtro, e responda: fazer `SCAN` virar `SEARCH` é sempre uma melhoria?

### AP3 — A conta completa `[Aplicação · ~25 min · ganho contra custo]`

**Tarefa.** Escolha uma coluna que **merece** índice e monte a conta que você apresentaria a um time:

1. o ganho de leitura, em ms e em fator;
2. o custo em disco: tamanho do arquivo antes e depois;
3. o custo de escrita: 20 000 `INSERT` com e sem o índice;
4. a estimativa de uso: quantas leituras contra quantas escritas por dia, no seu cenário;
5. **a conclusão com número**: em que razão leitura/escrita o índice deixa de compensar?

## Desafio

### D1 — O parecer `[Desafio · ~50 min · um relatório que decide]`

**Cenário.** Quatro consultas de um sistema em produção estão lentas. Você entrega um parecer; outra pessoa executa.

```sql
-- Q1: painel do cliente
SELECT * FROM eventos WHERE cliente_id = ? ORDER BY data DESC LIMIT 20;

-- Q2: relatório mensal por tipo
SELECT tipo, COUNT(*) FROM eventos
WHERE data >= '2026-03-01' AND data < '2026-04-01' GROUP BY tipo;

-- Q3: busca de eventos de login
SELECT * FROM eventos WHERE tipo = 'login';

-- Q4: auditoria de valores altos
SELECT * FROM eventos WHERE valor > 89000;
```

Para **cada** consulta, entregue: plano atual; seletividade medida do filtro; recomendação (qual índice, ou nenhum); ganho medido; custo em disco e escrita; e a decisão final justificada.

- **(a)** **Pelo menos uma das quatro não deve receber índice.** Diga qual e prove com número.
- **(b)** Uma delas se beneficia de índice **composto** — identifique e justifique a ordem das colunas.
- **(c)** Uma delas pode ser resolvida **sem** índice, mudando a consulta. Qual?
- **(d)** Some o custo total: quantos MB e quanto de escrita as suas recomendações custam juntas?
- **(e)** A pergunta que você faria ao time antes de aplicar em produção.

**Fecho:** 5 linhas sobre por que "criar um índice" é uma resposta e não um diagnóstico.

<details><summary>💡 Dica 1 (conceito)</summary>
Q4 depende de quantas linhas passam de 89 000 — meça com `COUNT(*)` antes de decidir. Q3 você já mediu no capítulo.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para (b): Q1 filtra por `cliente_id` **e** ordena por `data`. Um índice em `(cliente_id, data)` pode servir às duas coisas de uma vez — o filtro pela primeira coluna, a ordenação pela segunda, sem etapa de ordenação.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Uma seção por consulta com os seis itens → tabela-resumo das quatro decisões → soma dos custos → a pergunta ao time → fecho.
</details>
