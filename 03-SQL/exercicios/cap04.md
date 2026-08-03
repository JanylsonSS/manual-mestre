# Exercícios — Capítulo 03.04: Ordenação, `LIMIT` e `DISTINCT`

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap04.md`](gabaritos/cap04.md).

## Aquecimento

### A1 — Preveja a ordem `[Aquecimento · ~10 min · qual linha vem primeiro?]`

**Tarefa.** Diga qual linha aparece **primeiro** no resultado:

1. `SELECT nome FROM produtos ORDER BY preco_centavos;`
2. `SELECT nome FROM produtos ORDER BY preco_centavos DESC;`
3. `SELECT nome, cidade FROM clientes ORDER BY cidade;`
4. `SELECT nome, cidade FROM clientes ORDER BY cidade DESC;`
5. `SELECT nome FROM produtos ORDER BY categoria, preco_centavos DESC;`
6. `SELECT nome FROM produtos;` *(sem `ORDER BY`)*

### A2 — Escreva a consulta `[Aquecimento · ~10 min · ranking e listagem]`

**Tarefa.** Escreva a consulta para cada pergunta:

1. Os 3 produtos mais caros.
2. Os 3 produtos mais baratos que estejam ativos.
3. As cidades onde há clientes (sem repetição).
4. Os 5 pedidos mais recentes.
5. As categorias de produto, em ordem alfabética, sem repetição.
6. Produtos ordenados por categoria e, dentro dela, por nome.
7. Página 2 de uma listagem de clientes de 3 em 3, ordenada por nome.
8. O produto mais caro de cada... — **pegadinha**: por que esta pergunta não cabe neste capítulo?

### A3 — `DISTINCT` resolve? `[Aquecimento · ~10 min · sim ou não]`

**Tarefa.** Para cada intenção, diga se `DISTINCT` resolve — e, se não, o que faltaria:

1. Listar as cidades onde há clientes.
2. Listar as cidades e quantos clientes há em cada.
3. Listar os pares (cidade, categoria) em que houve venda.
4. Listar cada cidade com o nome de um cliente dela.
5. Contar quantas cidades distintas existem.
6. Listar os status de pedido existentes.

### A4 — Ache o bug `[Aquecimento · ~10 min · o que vai dar errado?]`

**Tarefa.** Cada consulta tem um problema. Identifique e corrija:

1. `SELECT nome FROM produtos LIMIT 5;`
2. `SELECT nome, categoria FROM produtos ORDER BY categoria LIMIT 4 OFFSET 4;`
3. `SELECT preco_centavos / 100.0 AS reais FROM produtos WHERE reais > 300;`
4. `SELECT nome, preco_centavos / 100.0 FROM produtos ORDER BY 2 DESC;`
5. `SELECT DISTINCT cidade, id FROM clientes;` *(a intenção era listar as cidades)*
6. `SELECT nome FROM clientes ORDER BY cidade;` *(o relatório reclama que "o primeiro está vazio")*

## Aplicação

### AP1 — Rankings `[Aplicação · ~20 min · com desempate explícito]`

**Tarefa.** Construa cinco rankings, **todos** com critério de desempate explícito: (1) produtos mais caros; (2) produtos mais baratos por categoria; (3) clientes mais antigos; (4) pedidos mais recentes; (5) produtos ativos ordenados por categoria e preço. Para cada um, explique em uma linha **qual empate** o seu desempate resolve.

### AP2 — Reproduzindo o bug `[Aplicação · ~25 min · paginação]`

**Tarefa.** (1) Escreva uma paginação de produtos de 4 em 4 ordenada **apenas** por `categoria`; (2) liste as três páginas e junte os resultados; (3) verifique se algum produto se repetiu ou faltou — e explique por que, no laboratório atual, provavelmente **não** aconteceu; (4) explique em que condições aconteceria; (5) corrija com ordenação total e prove que as três páginas cobrem exatamente os 12 produtos, sem repetição.

### AP3 — Legibilidade `[Aplicação · ~20 min · reescrevendo]`

**Tarefa.** Reescreva as três consultas abaixo em versão publicável (apelidos, formatação, ordenação explícita) e explique **cada** mudança:

```sql
select * from produtos where preco_centavos>30000 order by 4 desc limit 5;
SELECT nome,preco_centavos/100.0 FROM produtos WHERE ativo=1;
select distinct categoria,ativo from produtos;
```

## Desafio

### D1 — O painel de produtos `[Desafio · ~45 min · pronto para virar tela]`

**Tarefa.** Construa a consulta que alimentaria uma listagem paginada de produtos:

- **(a)** colunas `id`, nome, categoria e preço **em reais**, todas com apelidos legíveis;
- **(b)** apenas produtos ativos;
- **(c)** ordenada por categoria e, dentro dela, do mais caro para o mais barato;
- **(d)** paginação de 4 em 4, com ordenação **total** — demonstre as três páginas e prove que nenhum produto se repete e nenhum falta;
- **(e)** escreva a versão **frágil** da mesma consulta (sem o desempate) e explique em qual página a fragilidade se manifestaria;
- **(f)** proponha a consulta de **paginação por cursor** equivalente à página 2, e explique a diferença de custo.

**Fecho:** 5 linhas sobre por que este bug sobrevive tanto tempo em produção.

<details><summary>💡 Dica 1 (conceito)</summary>
Para provar o item (d), junte os `id` das três páginas, ordene, e compare com a lista completa de produtos ativos.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Paginação por cursor: em vez de `OFFSET 4`, use `WHERE id > <ultimo_id_da_pagina_anterior>` quando a ordem for por `id` — ou a comparação de tupla quando a ordem for composta.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Consulta base com AS → filtro de ativos → `ORDER BY categoria, preco_centavos DESC, id` → três páginas → prova da cobertura → versão frágil → versão por cursor → reflexão.
</details>
