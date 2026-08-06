# Gabarito — Capítulo 05.03: Tipos avançados do Postgres

Leia depois de tentar. Enunciados em [`../cap03.md`](../cap03.md).

> Toda saída abaixo é execução real, PostgreSQL 16.2.

## A1 — Qual o tipo?

| # | Coluna | Tipo | Motivo |
|---|---|---|---|
| 1 | Preço | `integer` de centavos, ou `numeric(12,2)` | exatidão em soma |
| 2 | Quantidade | `integer` com `CHECK (> 0)` | contagem, não medida |
| 3 | Criação do pedido | `timestamptz` | é um instante que aconteceu |
| 4 | Abertura da loja | `time` | é local por definição, sem instante |
| 5 | ID gerado no celular | `uuid` | gerado fora do banco, offline |
| 6 | Etiquetas | `text[]` | lista curta, filtrada com `@>` |
| 7 | Atributos por categoria | `jsonb` | o formato varia por linha |
| 8 | CPF | `text` com `CHECK` de formato | não é número: tem zero à esquerda |
| 9 | Temperatura | `real` ou `double precision` | é medida, tem incerteza própria |
| 10 | Percentual de desconto | `numeric(5,2)` | entra em conta de dinheiro |
| 11 | Avaliação | `text` | sem limite artificial |
| 12 | Ativo | `boolean NOT NULL` | dois estados, e não três |

**O 4 é o que mais gente erra.** "Abre às 09:00" não é um instante — é uma regra local. Guardar como `timestamptz` obriga a inventar uma data e produz horários errados quando o servidor muda de fuso.

**O 8 é o clássico:** CPF com zero à esquerda vira outro número em coluna numérica, e ninguém soma CPF.

**E o 12 merece o `NOT NULL`.** Um `boolean` que aceita `NULL` tem três estados, e metade do código esquece o terceiro.

## A2 — Preveja o resultado

| # | Expressão | Resultado |
|---|---|---|
| 1 | `0.1+0.2 = 0.3` em `float8` | `false` |
| 2 | `'{"a":1,"a":2}'::jsonb` | `{"a": 2}` |
| 3 | `'{"a":1}'::json = '{"a":1}'::json` | **erro** |
| 4 | `(ARRAY['x','y','z'])[0]` | `NULL` |
| 5 | `->> 'tamanho'` (chave ausente) | `NULL` |
| 6 | `'2026-01-31' + interval '1 month'` | `2026-02-28 00:00:00` |
| 7 | `'2026-08-06'::date - '2026-06-02'::date` | `65` |
| 8 | `pg_column_size` de `json` e `jsonb` | `11` e `28` |

O 3, exato:

```
operator does not exist: json = json
```

**O 8 surpreende quase todo mundo**: para `{"a":1}`, o `jsonb` ocupa **28 bytes contra 11** do `json` — mais que o dobro. O cabeçalho por chave da estrutura decomposta pesa mais que os caracteres economizados. `jsonb` compensa pela consulta, e não pelo tamanho.

**E o par 4/5 é o mesmo defeito com duas caras:** índice fora do intervalo e chave ausente devolvem `NULL` em vez de erro. Os dois transformam engano em resultado vazio.

## A3 — Ache o erro

**1. Dinheiro em `double precision`.** Medido com 50 mil linhas de 19,99:

```
soma em float8:   999499.9999996105
valor exato:      999500.00
```

Quatrocentos microcentavos de erro em cinquenta mil linhas. Correção: `numeric(12,2)` ou centavos em `integer`.

**2. `timestamp` sem fuso com `DEFAULT now()`.** O `now()` devolve `timestamptz`, e a conversão para `timestamp` descarta o fuso silenciosamente, gravando o horário **do servidor**. Se o servidor mudar de fuso ou for replicado noutro, os registros deixam de ser comparáveis. Correção: `timestamptz NOT NULL DEFAULT now()`.

**3. UUID em coluna `text`.** 40 bytes onde caberiam 16, sem validação, com comparação caractere a caractere. Correção: `id uuid PRIMARY KEY DEFAULT gen_random_uuid()`.

**4. `->` onde precisava `->>`.** Compara `jsonb` com `text` — a consulta não casa nunca, e não dá erro. Correção: `attrs ->> 'cor' = 'preto'`, ou `attrs @> '{"cor":"preto"}'`.

**5. Índice GIN que ninguém usa.** Trezentas linhas cabem numa página; o índice nunca será escolhido, e ainda atrasa toda escrita. Correção: não criar. Índice se cria quando a consulta existe **e** é seletiva.

**6. `JSONB` engolindo a modelagem.** A coluna gerada é boa ideia e não conserta o problema de fundo: preço e status estão dentro do JSON, o que significa nenhum `CHECK`, nenhuma chave estrangeira, nenhum tipo. Correção: tirar do JSON tudo que tem regra, deixando lá o que varia por linha.

## A4 — Coluna ou JSONB?

| # | Dado | Onde | Por quê |
|---|---|---|---|
| 1 | Preço | **coluna** | tem `CHECK`, entra em `sum` |
| 2 | Cor, só para alguns | **JSONB** | ausente na maioria das linhas |
| 3 | Status do pedido | **coluna** | quatro valores, `GROUP BY` constante |
| 4 | Resposta bruta da API | **`json`**, não `jsonb` | auditoria quer o texto original |
| 5 | Autonomia de bateria | **JSONB** | específico de uma categoria |
| 6 | CPF | **coluna** | identifica, tem formato, tem índice |

**O 4 é o único caso do manual em que `json` ganha de `jsonb`.** Auditoria de payload precisa do texto exatamente como chegou — com os espaços, com a ordem das chaves, com a duplicata. O `jsonb` normaliza tudo isso e a prova deixa de ser prova.

**O 2 admite discussão**, e a resposta boa reconhece isso: se "cor" existir em 80% dos produtos e aparecer em todo filtro de busca, ela merece coluna com `NULL` nos 20% restantes.

## AP1 — O catálogo com atributos

```sql
CREATE TABLE produtos (
    id              integer PRIMARY KEY,
    nome            text    NOT NULL,
    categoria       text    NOT NULL,
    preco_centavos  integer NOT NULL CHECK (preco_centavos >= 0),
    ativo           boolean NOT NULL DEFAULT true,
    atributos       jsonb   NOT NULL DEFAULT '{}'
        CHECK (jsonb_typeof(atributos) = 'object')
);
```

A consulta de chaves por categoria:

```sql
SELECT categoria, jsonb_object_keys(atributos) AS chave, count(*)
FROM produtos GROUP BY 1, 2 ORDER BY 1, 2;
```

**A pergunta que fecha, e são duas armadilhas.**

Com `atributos = '{}'`, o produto **desaparece do resultado**. `jsonb_object_keys` é uma função que devolve conjunto: zero chaves produzem zero linhas, e a linha inteira some — sem aviso. A correção é `LEFT JOIN LATERAL`:

```sql
SELECT p.categoria, k.chave, count(*)
FROM produtos p
LEFT JOIN LATERAL jsonb_object_keys(p.atributos) AS k(chave) ON true
GROUP BY 1, 2 ORDER BY 1, 2;
```

Com o `LEFT JOIN LATERAL`, o produto sem atributos aparece com `chave = NULL`, que é a informação que você queria.

**E a chave única de um produto só** aparece com contagem 1 — o que é o resultado correto, e é também o sinal que denuncia erro de digitação numa carga: uma chave `"bateria_hs"` com contagem 1 ao lado de `"bateria_h"` com contagem 8.

## AP2 — Meça o índice GIN

A referência, em 200 mil linhas:

```
consulta SELETIVA casa:   40 linhas
  sem índice:             33.5 ms
consulta AMPLA casa:      16667 linhas
  sem índice:             34.8 ms

criar o índice GIN:       752 ms
SELETIVA com índice:      4.8 ms   (ganho: 7x)
AMPLA com índice:         32.7 ms  (ganho: 1.1x)

tamanho da tabela:        20 MB
tamanho do índice GIN:    2560 kB
```

**Se os seus números forem diferentes, isso é esperado** — e o que precisa se repetir é o **formato**: ganho grande na seletiva, ganho quase nulo na ampla. Se a sua seletiva não ganhou nada, confira se rodou `ANALYZE` depois de criar o índice; sem estatísticas, o planejador pode não escolhê-lo.

**A segunda pergunta: `jsonb_path_ops`.** Ele indexa apenas caminhos completos, em vez de cada chave e cada valor separadamente. O resultado é um índice **bem menor** e consultas `@>` mais rápidas. O preço é perder os operadores `?`, `?|` e `?&` — buscar "quais linhas têm a chave X" deixa de usar o índice.

**A regra de escolha:** se a única consulta é `@>`, use `jsonb_path_ops`. Se você também pergunta por existência de chave, use o GIN padrão.

## AP3 — A tabela com dinheiro em `float`

A migração é uma linha:

```sql
ALTER TABLE vendas ALTER COLUMN total TYPE numeric(12,2);
```

Ela reescreve a tabela inteira e **segura uma trava exclusiva** enquanto o faz — em 50 mil linhas é instantâneo, em 50 milhões derruba a aplicação. O caminho sem parada é adicionar coluna nova, preencher em lotes, trocar as leituras, e só então descartar a antiga.

Os três números, medidos com 50 mil linhas de 19,99:

```
soma em float8:   999499.9999996105
soma convertida:  999500.00
valor exato:      999500.00
depois do ALTER:  999500.00
```

**A pergunta que separa: a soma mudou. Qual está certa?**

A de depois — e o motivo é preciso. **O dado nunca esteve corrompido:** cada 19,99 guardado em `float8` volta como exatamente 19,99 quando convertido para `numeric`, porque um `double` tem cerca de 15 dígitos significativos e a conversão usa a representação decimal mais curta que reproduz aquele bit a bit.

**O erro estava na soma, não no armazenamento.** Cada adição em ponto flutuante arredonda, e cinquenta mil arredondamentos acumulam os 0,0000004 de diferença.

É por isso que `sum(total::numeric)` já dava o valor exato **antes** da migração: convertendo cada parcela primeiro, a soma acontece em decimal. **E é por isso que a migração não perde dado** — o que ela conserta é o futuro, não o passado.

**A ressalva honesta:** isso vale porque 19,99 tem quatro dígitos significativos. Valores com mais de 15 dígitos, ou que já sejam resultado de contas acumuladas em `float`, podem ter perdido informação de verdade — e aí a conversão preserva o erro em vez de removê-lo.

## D1 — O relatório de duas dimensões

```sql
SELECT date_trunc('month', pe.data)::date AS mes,
       coalesce(pr.atributos ->> 'cor', '(sem cor)') AS cor,
       sum(ip.quantidade * ip.preco_unitario_centavos) AS receita_centavos
FROM pedidos pe
JOIN itens_pedido ip ON ip.pedido_id = pe.id
JOIN produtos pr     ON pr.id = ip.produto_id
WHERE pe.status = 'pago'
GROUP BY 1, 2
ORDER BY 1, 2;
```

**1. Ignorar, agrupar ou falhar?**

**Agrupar como `(sem cor)`**, e o motivo é de negócio: um relatório de receita cujo total não bate com a receita real é pior do que um relatório com uma linha esquisita. Ignorar produz um total menor que o verdadeiro, e ninguém percebe até alguém somar à mão.

**Falhar** é defensável num contexto: se o contrato diz que todo produto tem cor, um relatório que falha denuncia a carga quebrada. Mas aí a validação pertence à carga, e não ao relatório.

**2. `LEFT JOIN` muda o resultado?**

Aqui, **não** — porque `itens_pedido.produto_id` tem chave estrangeira `NOT NULL`, então todo item tem produto. Isso é o que a restrição do 05.01 compra: uma classe inteira de `LEFT JOIN` defensivo deixa de ser necessária.

**Muda no caso oposto:** um `LEFT JOIN` de `pedidos` para `itens_pedido` traria pedidos sem item, com `receita = NULL`. Se existem pedidos sem item no seu banco, os dois relatórios discordam — e a diferença é exatamente o que precisa ser investigado.

**3. Índice ajudaria?**

Nesta consulta, contra 20 pedidos, **não** — e a resposta correta é "medi, e não". A consulta lê a tabela inteira porque a tabela inteira é o relatório: não há filtro seletivo, só `status = 'pago'`, que pega a maioria das linhas. É o mesmo fenômeno da §6.4: filtro amplo, índice inútil.

O que ajudaria em volume real é um índice em `pedidos (status, data)`, e ainda assim só se `pago` fosse a minoria.

## MP — Busca por atributo

O núcleo:

```python
def buscar(cursor, categoria=None, preco_max=None, atributos=None):
    condicoes, valores = ["ativo = true"], []
    if categoria:
        condicoes.append("categoria = %s")
        valores.append(categoria)
    if preco_max is not None:
        condicoes.append("preco_centavos <= %s")
        valores.append(preco_max)
    if atributos:
        if not isinstance(atributos, dict):
            raise TypeError("atributos precisa ser um objeto, não %s"
                            % type(atributos).__name__)
        condicoes.append("atributos @> %s")
        valores.append(Jsonb(atributos))
    cursor.execute("SELECT id, nome, preco_centavos FROM produtos WHERE "
                   + " AND ".join(condicoes), valores)
    return cursor.fetchall()
```

**A recusa de array não é preciosismo.** `'[1,2]'::jsonb @> ...` é válido e devolve resultados sem sentido; a exceção transforma um erro de chamada em falha imediata.

**A pergunta que fecha: `{"bateria_h": 30}` acha `{"bateria_h": "30"}`?**

**Não.** Medido:

```
'{"b": 30}'   @> '{"b": 30}'  ->  True
'{"b": "30"}' @> '{"b": 30}'  ->  False
jsonb_typeof do primeiro  ->  'number'
jsonb_typeof do segundo   ->  'string'
```

O `JSONB` guarda o tipo de cada valor, e `30` e `"30"` são valores diferentes. **A busca falha em silêncio**, que é o pior modo de falhar.

**O que fazer, em três níveis.** O primeiro é normalizar na escrita: uma função de carga que converte para número o que é número, antes de gravar. O segundo é um `CHECK` que recuse tipos errados nas chaves conhecidas:

```sql
CHECK (NOT (atributos ? 'bateria_h')
       OR jsonb_typeof(atributos -> 'bateria_h') = 'number')
```

O terceiro — e é o que a §12 do capítulo recomenda — é reconhecer que uma chave com tipo conhecido, presente em muitas linhas e usada em filtro **não é atributo variável**: é coluna.
