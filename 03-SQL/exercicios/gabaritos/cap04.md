# Gabaritos — Capítulo 03.04

Abra somente após tentativa honesta.

## A1 — Preveja a ordem

1. **Cabo HDMI 2m** (3490) — o mais barato.
2. **Monitor 24 polegadas** (89900) — o mais caro.
3. **Helena Prado** — `cidade` é `NULL`, e no SQLite/PostgreSQL o nulo vem **primeiro** no `ASC`.
4. **Carlos Menezes** ou **Juliana Castro** — ambos de "sorocaba"; **o desempate é arbitrário**, e essa é a resposta correta.
5. **Hub USB-C 6 portas** — categoria "acessorios" vem primeiro no alfabeto, e ele é o mais caro dela (12990).
6. **Indefinido** — sem `ORDER BY` não há primeira linha. Qualquer resposta específica está errada, mesmo que coincida com o que aparece na tela.

**Critério:** 6/6. Os itens 4 e 6 são o alvo do exercício: a resposta certa é reconhecer a **ausência de garantia**, não adivinhar o que o banco devolveu hoje.

## A2 — Escreva a consulta

```sql
-- 1
SELECT nome, preco_centavos FROM produtos ORDER BY preco_centavos DESC, id LIMIT 3;

-- 2
SELECT nome, preco_centavos FROM produtos WHERE ativo = 1
ORDER BY preco_centavos ASC, id LIMIT 3;

-- 3
SELECT DISTINCT cidade FROM clientes ORDER BY cidade;      -- 4 linhas (o NULL conta)

-- 4
SELECT id, data FROM pedidos ORDER BY data DESC, id DESC LIMIT 5;

-- 5
SELECT DISTINCT categoria FROM produtos ORDER BY categoria; -- 4 categorias

-- 6
SELECT nome, categoria FROM produtos ORDER BY categoria, nome;

-- 7
SELECT nome FROM clientes ORDER BY nome, id LIMIT 3 OFFSET 3;
```

**Item 8 — a pegadinha:** *"o produto mais caro de cada categoria"* pede **um resultado por grupo**, e isso não se obtém com `ORDER BY` + `LIMIT` — o `LIMIT` corta o resultado inteiro, não cada grupo. A ferramenta é `GROUP BY` (03.06), e a versão completa exige subconsulta ou função de janela. Reconhecer que a pergunta **não cabe** neste capítulo é a resposta.

**Critério:** 7 consultas + o reconhecimento do item 8. O desempate por `id` em todas as que usam `LIMIT` é o que se avalia.

## A3 — `DISTINCT` resolve?

| # | Resolve? | O que falta |
|---|---|---|
| 1 | **Sim** | `SELECT DISTINCT cidade FROM clientes` |
| 2 | **Não** | precisa contar por grupo → `GROUP BY` (03.06) |
| 3 | **Sim** | é justamente o caso legítimo de `DISTINCT` com duas colunas |
| 4 | **Não** | "um cliente de exemplo" é uma escolha dentro do grupo → `GROUP BY` + agregação |
| 5 | **Sim, com agregação** | `SELECT COUNT(DISTINCT cidade) FROM clientes` |
| 6 | **Sim** | `SELECT DISTINCT status FROM pedidos` |

**Ponto de atenção no item 5:** `COUNT(DISTINCT cidade)` devolve **3**, e não 4 — porque `COUNT` de uma coluna **ignora os `NULL`**, enquanto `SELECT DISTINCT cidade` os lista. As duas consultas discordam sobre a Helena, e as duas estão certas: são perguntas diferentes. Esse é exatamente o assunto do 03.05.

**Critério:** 6/6, com a divergência do item 5 percebida.

## A4 — Ache o bug

1. `LIMIT` sem `ORDER BY` → acrescente `ORDER BY nome` (ou o critério que a pergunta pedir).
2. Ordenação **não total** — `categoria` empata → `ORDER BY categoria, id`.
3. Apelido no `WHERE` — funciona no SQLite, falha no padrão → `WHERE preco_centavos > 30000` (que também permite índice).
4. `ORDER BY 2` por posição — quebra se alguém acrescentar coluna → dê nome com `AS` e ordene pelo apelido.
5. Incluir `id` (único) faz cada linha ser distinta → `SELECT DISTINCT cidade FROM clientes`.
6. Não é bug de SQL, é de expectativa: ordenando por `cidade`, a Helena (`NULL`) vem primeiro → `ORDER BY (cidade IS NULL), cidade` para mandar os nulos para o fim.

**Critério:** 6/6. O item 6 é o que exige interpretar a queixa em vez de corrigir sintaxe.

## AP1 — Rankings

**Referência e o empate que cada desempate resolve:**

| # | Consulta | Empate resolvido |
|---|---|---|
| 1 | `ORDER BY preco_centavos DESC, id` | dois produtos com o mesmo preço |
| 2 | `ORDER BY categoria, preco_centavos ASC, id` | mesmo preço dentro da categoria |
| 3 | `ORDER BY data_cadastro ASC, id` | dois cadastros no mesmo dia |
| 4 | `ORDER BY data DESC, id DESC` | vários pedidos na mesma data |
| 5 | `WHERE ativo = 1 ORDER BY categoria, preco_centavos DESC, id` | mesmo preço na mesma categoria |

**Observação:** no laboratório atual, nenhum desses empates chega a ocorrer — e é justamente por isso que o exercício pede a justificativa. O desempate não é para o dado de hoje; é para o dia em que dois produtos tiverem o mesmo preço, o que é questão de tempo.

**Critério:** os cinco com desempate **e** a justificativa nomeando o empate concreto.

## AP2 — Reproduzindo o bug

**Item 3 — por que provavelmente não aconteceu:** o SQLite devolve as linhas na ordem física quando não há critério de desempate, e essa ordem é estável enquanto ninguém insere, altera ou remove nada. O laboratório é estático, então as três páginas saem consistentes — **e isso é exatamente o problema**: o teste passa.

**Item 4 — em que condições aconteceria:**

- alguém **insere** um produto entre a consulta da página 1 e a da página 2 (tudo desloca uma posição);
- alguém **atualiza** um produto e o banco o regrava noutra posição física;
- um **índice** novo muda o caminho escolhido pelo otimizador;
- o banco executa a consulta **em paralelo** (PostgreSQL, tabelas grandes), e a ordem entre empatados varia entre execuções.

**Item 5 — prova de cobertura:**

```sql
-- as três páginas, com ordenação total
SELECT id, nome FROM produtos ORDER BY categoria, id LIMIT 4 OFFSET 0;
SELECT id, nome FROM produtos ORDER BY categoria, id LIMIT 4 OFFSET 4;
SELECT id, nome FROM produtos ORDER BY categoria, id LIMIT 4 OFFSET 8;
-- juntando os 12 id e ordenando, deve dar 1..12 sem repetição
```

**Critério:** as três páginas executadas, a explicação de por que o bug **não** apareceu (item 3) e as condições em que apareceria (item 4). Quem respondeu "não aconteceu, logo a consulta está certa" perdeu o exercício.

## AP3 — Legibilidade

```sql
-- 1. antes: select * from produtos where preco_centavos>30000 order by 4 desc limit 5;
SELECT nome                        AS produto,
       categoria,
       preco_centavos / 100.0      AS preco_reais
FROM produtos
WHERE preco_centavos > 30000
ORDER BY preco_reais DESC, id
LIMIT 5;
```

Mudanças: `SELECT *` → colunas nomeadas (evita quebra quando a tabela mudar) · `ORDER BY 4` → apelido (a posição 4 muda se alguém acrescentar coluna) · desempate por `id` (o `LIMIT` exige ordenação total) · espaçamento e maiúsculas nas palavras-chave.

```sql
-- 2. antes: SELECT nome,preco_centavos/100.0 FROM produtos WHERE ativo=1;
SELECT nome                   AS produto,
       preco_centavos / 100.0 AS preco_reais
FROM produtos
WHERE ativo = 1
ORDER BY produto;
```

Mudanças: `AS` na expressão (sem ele, a coluna do resultado se chama `preco_centavos/100.0`) · `ORDER BY` explícito (uma listagem sem ordem é uma listagem que muda sozinha).

```sql
-- 3. antes: select distinct categoria,ativo from produtos;
SELECT DISTINCT categoria FROM produtos ORDER BY categoria;
```

Mudança: a coluna `ativo` fazia cada par (categoria, ativo) ser distinto, produzindo mais linhas que categorias. Se a intenção fosse "categorias que têm algum produto ativo", a consulta correta é `SELECT DISTINCT categoria FROM produtos WHERE ativo = 1`.

**Critério:** cada mudança justificada por um **problema concreto**, não por gosto.

## D1 — O painel de produtos

**Consulta base (itens a, b, c):**

```sql
SELECT id                     AS produto_id,
       nome                   AS produto,
       categoria,
       preco_centavos / 100.0 AS preco_reais
FROM produtos
WHERE ativo = 1
ORDER BY categoria ASC, preco_centavos DESC, id
LIMIT 4 OFFSET 0;          -- página 1 (troque o OFFSET para 4 e 8)
```

**Página 1 (referência):**

```text
produto_id | produto               | categoria  | preco_reais
-----------+-----------------------+------------+------------
         7 | Hub USB-C 6 portas    | acessorios |       129.9
         8 | Suporte para Notebook | acessorios |        79.9
        10 | Cabo HDMI 2m          | acessorios |        34.9
         1 | Fone Bluetooth XZ-9   | audio      |       469.9
```

Note que o Mousepad Grande (`ativo = 0`) **não** aparece — são 11 produtos ativos, distribuídos em três páginas (4 + 4 + 3).

**(e) A versão frágil:** remover o `, id` final. A fragilidade se manifestaria na fronteira entre páginas — e no laboratório atual não haveria empate de `(categoria, preco_centavos)`, então **nada quebraria hoje**. Apontar isso é parte da resposta: a consulta frágil está correta para os dados atuais e errada para os dados futuros.

**(f) Paginação por cursor:**

```sql
-- Página 2 sem OFFSET: "os 4 seguintes ao último item da página 1"
-- (último item da página 1: categoria='audio', preco=46990, id=1)
SELECT id, nome, categoria, preco_centavos / 100.0 AS preco_reais
FROM produtos
WHERE ativo = 1
  AND (categoria, -preco_centavos, id) > ('audio', -46990, 1)
ORDER BY categoria, preco_centavos DESC, id
LIMIT 4;
```

**Diferença de custo:** o `OFFSET 8` obriga o banco a produzir e **descartar** 8 linhas antes de entregar as 4 pedidas — custo proporcional à página, e a página 1.000 descarta 3.996 linhas. O cursor usa a comparação para **saltar direto** ao ponto, aproveitando o índice: custo constante, independente da página. Há um preço: o cursor não permite "ir para a página 47", só "próxima" e "anterior" — e é por isso que listas infiníveis de aplicativo usam cursor, enquanto tabelas administrativas com numeração de páginas continuam usando `OFFSET`.

**Reflexão esperada:** este bug sobrevive porque **todas as condições que o revelam estão ausentes do ambiente onde ele seria encontrado**. Em desenvolvimento, os dados são poucos e estáticos: a ordem física não muda, e as páginas saem consistentes. Nos testes automatizados, o mesmo. Em produção, onde os dados se movem, o sintoma é intermitente, não gera erro, não aparece em log, e a queixa do usuário ("sumiu um item da lista") costuma ser atribuída a engano dele. Some-se que a correção é uma palavra — `, id` — e não parece merecer investigação. É o retrato de uma classe inteira de defeitos: **os que só existem sob condições que ninguém reproduz de propósito**. A defesa não é testar mais; é conhecer a regra e aplicá-la sempre, mesmo sem sintoma.

**Critério de "está bom":** as três páginas com prova de cobertura (11 produtos ativos, sem repetição); o reconhecimento honesto de que a versão frágil **não quebra hoje**; a consulta por cursor funcionando; a reflexão explicando a sobrevivência do bug pela ausência de condições, não por descuido.
