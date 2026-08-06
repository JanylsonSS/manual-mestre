# Exercícios — Capítulo 05.03: Tipos avançados do Postgres

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap03.md`](gabaritos/cap03.md).

> Suba o laboratório antes: `python codigo/laboratorio.py`.

## Aquecimento

### A1 — Qual o tipo? `[Aquecimento · ~12 min]`

Escolha o tipo de cada coluna e escreva o motivo em uma linha:

1. Preço de um produto.
2. Quantidade de itens num pedido.
3. Momento em que o pedido foi criado.
4. Horário de abertura de uma loja física.
5. Identificador gerado pelo aplicativo do celular, ainda sem internet.
6. Etiquetas de um produto (`anc`, `usb-c`).
7. Atributos que mudam conforme a categoria do produto.
8. CPF.
9. Temperatura medida por um sensor.
10. Percentual de desconto aplicado.
11. Texto livre de uma avaliação.
12. Se o produto está ativo.

### A2 — Preveja o resultado `[Aquecimento · ~12 min]`

```sql
-- 1
SELECT 0.1::float8 + 0.2::float8 = 0.3::float8;
-- 2
SELECT '{"a":1,"a":2}'::jsonb;
-- 3
SELECT '{"a":1}'::json = '{"a":1}'::json;
-- 4
SELECT (ARRAY['x','y','z'])[0];
-- 5
SELECT '{"cor":"preto"}'::jsonb ->> 'tamanho';
-- 6
SELECT '2026-01-31'::date + interval '1 month';
-- 7
SELECT '2026-08-06'::date - '2026-06-02'::date;
-- 8
SELECT pg_column_size('{"a":1}'::json), pg_column_size('{"a":1}'::jsonb);
```

### A3 — Ache o erro `[Aquecimento · ~12 min]`

```sql
-- 1
CREATE TABLE vendas (total double precision NOT NULL);

-- 2
CREATE TABLE pedidos (criado_em timestamp NOT NULL DEFAULT now());

-- 3
CREATE TABLE usuarios (id text PRIMARY KEY DEFAULT gen_random_uuid()::text);

-- 4
SELECT * FROM catalogo WHERE attrs -> 'cor' = 'preto';

-- 5
CREATE TABLE produtos (atributos jsonb);
CREATE INDEX ON produtos USING gin (atributos);
-- (a tabela tem 300 linhas e nenhuma consulta filtra por atributos)

-- 6
CREATE TABLE eventos (
    dados jsonb NOT NULL,
    valor_total numeric GENERATED ALWAYS AS
        ((dados ->> 'valor')::numeric) STORED
);
-- (e o time decidiu guardar TUDO, inclusive preço e status, dentro de `dados`)
```

### A4 — Coluna ou JSONB? `[Aquecimento · ~10 min]`

1. Preço do produto.
2. Cor, que só existe para vestuário e periféricos.
3. Status do pedido, que tem quatro valores e aparece em todo relatório.
4. Resposta bruta de uma API de frete, guardada para auditoria.
5. Autonomia de bateria, que só produtos de áudio têm.
6. CPF do cliente.

---

## Aplicação

### AP1 — O catálogo com atributos `[Aplicação · ~30 min]`

Modele `produtos` com parte estruturada e parte livre, e carregue os doze produtos da Aurora com atributos que façam sentido por categoria.

**Requisitos:** `preco_centavos`, `categoria` e `ativo` fora do JSON; um `CHECK` garantindo que `atributos` é um objeto; e uma consulta que liste, por categoria, quais chaves aparecem.

**A pergunta que fecha:** o que acontece com a sua consulta de chaves quando um produto tem `atributos = '{}'`? E quando tem uma chave que só ele tem?

### AP2 — Meça o índice GIN `[Aplicação · ~30 min]`

Reproduza a medição da §6.4 na **sua** máquina, com 200 mil linhas.

**Requisitos:** uma consulta seletiva e uma ampla; tempos antes e depois do índice; `EXPLAIN` das quatro execuções; e o tamanho da tabela e do índice.

**As duas perguntas:** os seus ganhos foram parecidos com 7× e 1,1×? E o que muda se você trocar `gin (corpo)` por `gin (corpo jsonb_path_ops)`?

### AP3 — A tabela com dinheiro em `float` `[Aplicação · ~25 min]`

Você herdou `CREATE TABLE vendas (id integer, total double precision)` com 50 mil linhas.

Migre para `numeric(12,2)` **sem perder dado e sem derrubar a aplicação**, e prove que a soma antes e depois da migração é a mesma — ou explique por que ela não é.

**A pergunta que separa:** se a soma mudou, qual das duas está certa?

---

## Desafio

### D1 — O relatório de duas dimensões `[Desafio · ~50 min]`

Um relatório que cruza mês do pedido com um atributo que está dentro do `JSONB` do produto.

**Requisitos:**

- Agrupar por `date_trunc('month', data)` e por `atributos ->> 'cor'`.
- Somar receita em centavos.
- Considerar apenas pedidos `pago`.
- Tratar de propósito os produtos que não têm a chave `cor`.

**As três perguntas que valem a nota:**

1. Você ignorou, agrupou como "sem cor", ou falhou? Justifique.
2. O resultado muda se você usar `LEFT JOIN` em vez de `JOIN`? Mostre os dois.
3. Um índice ajudaria esta consulta? Meça antes de responder.

---

## Mini projeto

### MP — Busca por atributo `[Mini projeto · ~40 min]`

Uma função de busca no catálogo que aceita filtros mistos: categoria, faixa de preço e atributos arbitrários.

**Requisitos:**

- Assinatura que aceite um dicionário de atributos.
- Usar `@>` para os atributos e comparação normal para preço e categoria.
- Um índice GIN, com medição que justifique tê-lo.
- Recusar filtros de atributo que sejam array em vez de objeto.

**E a pergunta que fecha:** um usuário busca `{"bateria_h": 30}`. Um produto tem `{"bateria_h": "30"}`, com aspas. Ele aparece? Por quê — e o que você faz a respeito?
