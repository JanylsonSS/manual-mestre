# Gabaritos — Capítulo 03.03

Abra somente após tentativa honesta.

## A1 — Preveja a saída

| # | Consulta | Linhas | Observação |
|---|---|---|---|
| 1 | `FROM clientes` | **8** | todas |
| 2 | `cidade = 'santos'` | **2** | Ana e Diego |
| 3 | `cidade IS NULL` | **1** | Helena |
| 4 | `cidade <> 'santos'` | **5** | 8 − 2 − **1 da Helena**; a soma 2+5 dá 7, não 8 |
| 5 | `BETWEEN 8990 AND 15990` | **3** | inclusivo nas duas pontas: Mouse (8990) e Caixa (15990) entram |
| 6 | `categoria IN ('audio')` | **4** | equivale a `= 'audio'` |
| 7 | `status <> 'concluido'` | **3** | 2 pendentes + 1 cancelado (nenhum `status` é nulo aqui) |
| 8 | `email = NULL` | **0** | sempre zero, sem erro |

**Critério:** 8/8, com as previsões escritas **antes**. O item 4 é o alvo: quem previu 6 caiu na armadilha. O item 5 pega quem confundiu `BETWEEN` com o `range` do Python — as duas pontas entram.

## A2 — Traduza a pergunta

```sql
-- 1 (3 linhas)
SELECT nome FROM clientes WHERE data_cadastro >= '2026-01-01';

-- 2 (2 linhas)
SELECT nome FROM produtos WHERE categoria = 'audio' AND preco_centavos > 40000;

-- 3 — a negação com tratamento explícito do desconhecido
SELECT * FROM pedidos WHERE status <> 'cancelado' OR status IS NULL;

-- 4 (1 linha)
SELECT nome FROM clientes WHERE nome LIKE 'A%';

-- 5 (1 linha)
SELECT nome FROM produtos WHERE nome LIKE '%USB%';

-- 6 (1 linha)
SELECT nome FROM clientes WHERE email IS NULL;

-- 7 (2 linhas)
SELECT nome FROM produtos WHERE ativo = 0 OR preco_centavos < 5000;

-- 8 (6 linhas)
SELECT id FROM pedidos WHERE data >= '2026-01-01' AND cliente_id IN (1, 2, 4);
```

**Ponto de atenção no item 2:** R$ 400,00 = `40000` centavos. Escrever `preco_centavos > 400` traria quase tudo e não daria erro — a unidade é responsabilidade de quem escreve, e o nome da coluna (`preco_centavos`) existe justamente para lembrar.

**Item 3:** o enunciado pede explicitamente "incluindo os de status desconhecido". No laboratório atual não há `status` nulo, então as duas versões devolvem 3 — e é por isso que a versão sem `OR IS NULL` passaria no teste e falharia em produção.

**Critério:** 8/8, com o item 3 tratando o `NULL` mesmo sem haver nulos hoje.

## A3 — Lógica de três valores

| # | Expressão | Resultado | Passa no `WHERE`? |
|---|---|---|---|
| 1 | `10 = 10` | verdadeiro | **sim** |
| 2 | `10 <> 10` | falso | não |
| 3 | `NULL = 10` | **desconhecido** | não |
| 4 | `NULL <> 10` | **desconhecido** | não |
| 5 | `NULL = NULL` | **desconhecido** | não |
| 6 | `NULL IS NULL` | verdadeiro | **sim** |
| 7 | `NULL IS NOT NULL` | falso | não |
| 8 | `5 > 3 AND NULL = 1` | **desconhecido** | não |

**Critério:** 8/8. O item 8 mostra a propagação: verdadeiro `AND` desconhecido é **desconhecido**, não verdadeiro. (Curiosidade que vale saber: verdadeiro **`OR`** desconhecido é **verdadeiro** — se um lado já garante a passagem, o desconhecido do outro não importa.)

## A4 — Ache o erro

1. `= NULL` nunca é verdadeiro → **`WHERE email IS NULL`**.
2. Aspas duplas delimitam identificadores → **`'campinas'`** com aspas simples. (O SQLite aceita e o PostgreSQL recusa — o hábito errado só aparece na migração.)
3. `AND` tem precedência → parênteses: **`WHERE (cidade = 'campinas' OR cidade = 'santos') AND data_cadastro >= '2026-01-01'`**.
4. A conta na coluna impede o uso de índice → **`WHERE preco_centavos > 30000`**.
5. `LIKE 'Mouse'` sem curinga é igualdade → **`LIKE 'Mouse%'`** (começa com) ou **`'%Mouse%'`** (contém).
6. A negação exclui os `NULL` → **`WHERE status <> 'cancelado' OR status IS NULL`**.

**Critério:** 6/6 com a correção escrita. Os itens 1, 3 e 6 são as três causas que a seção 14 do capítulo aponta como os achados mais frequentes em revisão de código SQL.

## AP1 — O caçador de `NULL`

**Resultado da auditoria no laboratório:**

| Tabela | Coluna | `NULL` |
|---|---|---|
| `clientes` | `email` | **1** (Beatriz) |
| `clientes` | `cidade` | **1** (Helena) |
| todas as demais colunas | — | 0 |

**Consultas que perderiam linhas (item 3):**

```sql
-- Perde a Beatriz:
SELECT nome FROM clientes WHERE email <> 'fernanda@aurora.com';
-- Corrigida:
SELECT nome FROM clientes WHERE email <> 'fernanda@aurora.com' OR email IS NULL;

-- Perde a Helena:
SELECT nome FROM clientes WHERE cidade <> 'campinas';
-- Corrigida:
SELECT nome FROM clientes WHERE cidade <> 'campinas' OR cidade IS NULL;
```

**Item 4 — por que auditar primeiro:** porque a existência de `NULL` numa coluna muda o comportamento de **toda** consulta que a negue, e essa informação não aparece em lugar nenhum além dos dados. O schema diz o que **pode** ser nulo (`NOT NULL` ou não); só a auditoria diz o que **é**. Uma coluna que aceita `NULL` mas nunca teve nenhum é uma bomba-relógio: as consultas funcionam até o primeiro nulo entrar.

**Critério:** a tabela completa (todas as colunas verificadas, não só as suspeitas) e o par erro/correção para as duas colunas com nulo.

## AP2 — Precedência

```sql
-- (1) Sem parênteses -> 3 linhas (duas de 2025!)
WHERE cidade = 'campinas' OR cidade = 'santos' AND data_cadastro >= '2026-01-01'

-- (2) Com parênteses -> 1 linha
WHERE (cidade = 'campinas' OR cidade = 'santos') AND data_cadastro >= '2026-01-01'

-- (3) Com IN -> 1 linha
WHERE cidade IN ('campinas', 'santos') AND data_cadastro >= '2026-01-01'
```

**Item 4 — leitura literal:** (1) lê-se *"de Campinas, **ou** (de Santos e de 2026)"* — o filtro de data não se aplica a Campinas. (2) e (3) leem-se *"(de Campinas ou Santos) **e** de 2026"*.

**Item 5 — qual deixar no código:** a **(3)**. Ela é a única em que a precedência **não importa**, porque não há mistura de `AND` e `OR` — o `IN` absorveu o `OR`. Uma consulta que não depende de o leitor lembrar de uma regra é melhor que uma consulta correta que depende. A (2) é aceitável; a (1) é um bug esperando ser descoberto.

**Critério:** as três executadas, a leitura literal de cada uma, e a escolha da (3) justificada por **eliminar a ambiguidade**, não por ser mais curta.

## AP3 — Busca textual

```sql
-- 1. prefixo (4 linhas: Mouse Sem Fio, Monitor, Microfone, Mousepad)
SELECT nome FROM produtos WHERE nome LIKE 'M%';

-- 2. termina com dígito (4 linhas)
SELECT nome FROM produtos
WHERE nome LIKE '%0' OR nome LIKE '%1' OR nome LIKE '%2'
   OR nome LIKE '%7' OR nome LIKE '%9';

-- 3. contém (1 linha)
SELECT nome FROM produtos WHERE nome LIKE '%USB%';

-- 4. segundo caractere é 'o' (4 linhas)
SELECT nome FROM produtos WHERE nome LIKE '_o%';

-- 6. portável (funciona também em PostgreSQL)
SELECT nome FROM produtos WHERE LOWER(nome) LIKE '%usb%';
```

**Item 2 — o incômodo é o ensinamento:** `LIKE` não tem classe de caracteres ("qualquer dígito"). Listar as possibilidades com `OR` funciona e é feio; a solução real são **expressões regulares**, que existem em PostgreSQL (`~ '[0-9]$'`) e não no SQLite padrão. Reconhecer o limite da ferramenta é parte da resposta.

**Item 5 — a diferença:** `'%mecanico%'` encontra "Teclado Mecanico K2"; `'%mecânico%'` devolve **zero linhas**. A insensibilidade a maiúsculas do SQLite vale só para ASCII — `â` e `a` são caracteres distintos, e nenhuma regra os aproxima. Em sistemas brasileiros, isso é motivo frequente de "a busca não acha", e a solução profissional é guardar uma coluna canonizada (sem acento, minúscula) para busca, mantendo a original para exibição — o mesmo padrão do 01.15.

**Critério:** as seis executadas; o item 5 com a explicação de que acento não é caixa; o item 6 com `LOWER`.

## D1 — O relatório que não fecha

**(a) Reprodução:**

```sql
SELECT COUNT(*) FROM clientes WHERE cidade = 'campinas';    -- 3
SELECT COUNT(*) FROM clientes WHERE cidade <> 'campinas';   -- 4
SELECT COUNT(*) FROM clientes;                              -- 8
```

3 + 4 = 7. Falta uma.

**(b) Por quê:** a Helena tem `cidade = NULL`. `NULL = 'campinas'` é **desconhecido** (não passa) e `NULL <> 'campinas'` também é **desconhecido** (não passa). O `WHERE` só deixa passar o verdadeiro, então ela é descartada nas duas consultas. Não é um caso especial nem um defeito: é a consequência direta da regra única, aplicada a um valor que o banco não conhece.

**(c) Duas correções:**

```sql
-- Correção 1: tratar o desconhecido explicitamente
SELECT COUNT(*) FROM clientes WHERE cidade <> 'campinas' OR cidade IS NULL;   -- 5

-- Correção 2: substituir o desconhecido por um valor antes de comparar
SELECT COUNT(*) FROM clientes WHERE COALESCE(cidade, '') <> 'campinas';       -- 5
```

**Comparação:** a primeira é mais explícita e mais rápida (pode usar índice); a segunda é mais curta e some com o `NULL` de todas as comparações da consulta, o que é conveniente e perigoso — ela **decide silenciosamente** que desconhecido equivale a string vazia. Prefira a primeira; use a segunda quando a substituição for uma regra de negócio de verdade (por exemplo, `COALESCE(cidade, 'não informada')` num relatório).

**(d) Correção estrutural:**

```sql
ALTER TABLE clientes ADD COLUMN cidade TEXT NOT NULL DEFAULT 'nao informada';
```

Declarar `NOT NULL` com um `DEFAULT` significativo elimina a classe inteira de problema: não existindo `NULL` na coluna, nenhuma negação perde linhas, e "cidade desconhecida" passa a ser um valor que aparece nos relatórios em vez de sumir deles. É a razão pela qual equipes maduras declaram `NOT NULL` sempre que possível (03.13). A ressalva honesta: nem toda ausência deve virar valor — `data_de_falecimento` **precisa** ser nula para os vivos, e substituí-la por uma data-marcador seria pior.

**(e) Auditoria:**

```sql
SELECT 'clientes.email'  AS coluna, COUNT(*) - COUNT(email)  AS nulos FROM clientes
UNION ALL
SELECT 'clientes.cidade', COUNT(*) - COUNT(cidade) FROM clientes
UNION ALL
SELECT 'pedidos.status',  COUNT(*) - COUNT(status) FROM pedidos;
```

**Interpretação:** duas colunas com um `NULL` cada, ambas em `clientes`. Isso significa que **toda** consulta que negue `email` ou `cidade` está sujeita ao bug — e que as outras tabelas estão livres dele. É um mapa de risco de três linhas.

**Reflexão esperada:** um erro de sintaxe é o melhor tipo de erro — ele aparece imediatamente, no lugar exato, e impede que o programa siga adiante. Este bug é o oposto em todas as dimensões: **não avisa** (a consulta roda), **não aparece perto da causa** (o número errado vira um relatório, uma decisão, um número em reunião), e **não é reproduzível por testes ingênuos** (dados de teste raramente têm `NULL`). O custo cresce com o tempo entre a introdução e a descoberta — e como não há sintoma, esse tempo pode ser de meses. É por isso que a defesa não pode ser atenção: tem que ser estrutural (`NOT NULL` onde possível) e procedimental (auditar nulos ao chegar num banco, e tratar `NULL` explicitamente em toda negação).

**Critério de "está bom":** a divergência reproduzida com números reais; a explicação (b) usando "desconhecido" e não "vazio"; as duas correções com a comparação honesta entre elas; a correção estrutural com a **ressalva** de que nem toda ausência deve virar valor.
