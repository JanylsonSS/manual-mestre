# Gabarito — Capítulo 03.14: Índices

Leia depois de tentar. Enunciados em [`../cap14.md`](../cap14.md).

> Todos os planos e tempos abaixo são saída real, medidos com mediana de 7 repetições e
> conexão nova a cada medição (§6.8). Seus tempos absolutos vão diferir — o hardware é outro.
> **As proporções são o que importa**, e elas se sustentam.

## A1 — `SCAN` ou `SEARCH`?

| # | Consulta | Plano real |
|---|---|---|
| 1 | `cliente_id = 27384` | `SEARCH ... USING INDEX idx_cliente` |
| 2 | `valor = 45000` | `SCAN eventos` — não há índice em `valor` |
| 3 | `data = '2026-03-15'` | `SEARCH ... USING INDEX idx_dt (data=?)` |
| 4 | `tipo = 'login'` | **`SCAN eventos`** |
| 5 | `data = ... AND tipo = ...` | `SEARCH ... USING INDEX idx_dt (data=? AND tipo=?)` |
| 6 | `id = 999` | `SEARCH ... USING INTEGER PRIMARY KEY (rowid=?)` |
| 7 | `SELECT COUNT(*)` | `SCAN ... USING COVERING INDEX idx_cliente` |
| 8 | `cliente_id IN (1,2,3)` | `SEARCH ... USING INDEX idx_cliente (cliente_id=?)` |

**As duas surpresas:**

**O item 6 — `id = 999` usa índice sem que ninguém tenha criado um.** `id` é
`INTEGER PRIMARY KEY`, e no SQLite essa combinação exata faz a coluna virar apelido do `rowid`
interno (03.12), que **é** a chave da B-tree da própria tabela. A tabela já está ordenada por
ele. Criar `CREATE INDEX idx_id ON eventos(id)` seria puro desperdício — uma cópia ordenada de
algo já ordenado, cobrando escrita.

**O item 7 — `COUNT(*)` faz `SCAN`, mas de um índice.** O plano diz
`SCAN eventos USING COVERING INDEX idx_cliente`. Para contar linhas, o banco precisa percorrer
alguma coisa; percorrer o índice é mais barato que percorrer a tabela, porque o índice tem uma
coluna e a tabela tem cinco — menos bytes, menos páginas de disco. É o **índice de cobertura**
(§7): quando tudo o que a consulta precisa já está no índice, a tabela não é tocada.

**Sobre o item 4:** o índice `(data, tipo)` **não** serve para filtrar só por `tipo`. É a regra
do prefixo, medida no A4.

**Sobre o item 8:** `IN` com poucos valores vira uma busca por valor. Com uma lista muito longa,
o otimizador pode preferir varrer — outra decisão dele, não sua.

## A2 — Vale a pena?

| Coluna | Distintos | Fração por valor | Indexar? |
|---|---|---|---|
| `id` | 500 000 | 0,0002% | **não** — já é o `rowid` (A1.6) |
| `cliente_id` | 49 997 | ~0,002% | **sim** — 763x medido |
| `valor` | 89 582 | ~0,001% | **sim, se houver consulta** |
| `data` | 224 | ~0,45% | **sim** — ainda bem abaixo de 5% |
| `tipo` | 5 | **20%** | **não** — ganho zero medido |
| `ativo` (0/1) | 2 | **50%** | **não** — nunca |

**O corte fica entre `data` e `tipo`**, e o número que o define é a fração da tabela devolvida:
0,45% compensa, 20% não. A referência prática de 5% a 10% cai confortavelmente no meio.

**O item 3 é o que separa o cuidadoso do apressado.** `valor` tem cardinalidade excelente — mas
isso responde "o índice **funcionaria**?", não "o índice **é necessário**?". Se nenhuma consulta
do sistema filtra por `valor`, o índice paga escrita e disco todo dia para nunca ser usado. **A
cardinalidade decide se um índice pode ajudar; a existência de uma consulta decide se ele deve
existir.** São duas perguntas, e pular a segunda é como bases antigas acumulam quarenta índices.

**O item 6 merece um comentário, porque é o caso em que se erra com convicção.** Colunas
booleanas parecem excelentes candidatas — são muito filtradas. Mas `ativo = 1` devolve tipicamente
a maioria da tabela, e o índice é inútil. A exceção existe e é elegante: se a distribuição for
muito desigual (99,9% ativos, 0,1% inativos), `WHERE ativo = 0` é seletivo. Em bancos com
**índice parcial** — `CREATE INDEX ... WHERE ativo = 0`, que o SQLite suporta — indexa-se só a
fatia rara, com índice minúsculo. É a resposta que impressiona.

## A3 — Por que não usou?

| # | Motivo | Reescrita |
|---|---|---|
| 1 | `cliente_id + 0` é expressão, não a coluna | `WHERE cliente_id = 27384` |
| 2 | `LIKE` com padrão não usa índice comum aqui | `data >= '2026-03-01' AND data < '2026-04-01'` |
| 3 | coringa **no começo**: busca por sufixo | **irreescrevível** — ver abaixo |
| 4 | `tipo` não é prefixo de `(data, tipo)` | criar `(tipo, ...)`, se justificar |
| 5 | `UPPER(tipo)` é expressão | `WHERE tipo = 'login'` (o dado já é minúsculo) |
| 6 | `valor` não tem índice | criar, se houver consulta que justifique |

**A regra única por trás de 1, 3 e 5:** o índice guarda **o valor da coluna**. `cliente_id + 0`,
`UPPER(tipo)` e "o que termina em `03-15`" são coisas diferentes do que está indexado, e nenhuma
ordenação por `cliente_id` ou por `tipo` ajuda a encontrá-las.

**O item 3 é o único sem saída por reescrita.** Uma lista ordenada alfabeticamente serve para
achar o que **começa** com algo; para o que **termina** com algo, ela não vale nada — pense em
procurar todas as palavras terminadas em "ção" no dicionário. As soluções reais são: índice de
texto completo (FTS), ou uma coluna auxiliar guardando o texto invertido — e indexá-la.

**O item 5 tem uma sutileza que vale a entrevista.** `UPPER(tipo) = 'LOGIN'` funciona aqui
porque os dados já são minúsculos, mas essa reescrita **muda a semântica**: se houvesse
`'Login'` na base, a original o encontraria e a reescrita não. A correção que preserva o
comportamento é `COLLATE NOCASE` na coluna (03.13) ou normalizar na escrita. **Reescrever para
usar índice não pode alterar a resposta** — e verificar isso é parte do trabalho.

## A4 — A ordem importa

Com **só** o índice `(data, tipo)`:

| # | Consulta | Plano |
|---|---|---|
| 1 | `WHERE data = '2026-03-15'` | `SEARCH ... idx_dt (data=?)` |
| 2 | `WHERE tipo = 'login'` | **`SCAN eventos`** |
| 3 | `WHERE data = ... AND tipo = ...` | `SEARCH ... idx_dt (data=? AND tipo=?)` |
| 4 | `ORDER BY data LIMIT 5` | `SCAN ... USING INDEX idx_dt` |
| 5 | `ORDER BY tipo LIMIT 5` | **`SCAN eventos`** |

**A regra do prefixo, confirmada nos itens 2 e 5.** O índice está ordenado por `data` e, dentro
de cada data, por `tipo`. Ele serve para `data` sozinha, para `data + tipo`, e para ordenar por
`data`. **Não serve para nada que comece por `tipo`.**

O item 4 é instrutivo: o plano diz `SCAN`, mas `SCAN ... USING INDEX` — o banco percorre o
índice inteiro, na ordem, e por isso já entrega ordenado, pulando a etapa de ordenação. `SCAN`
não significa "ruim"; significa "percorrendo tudo". Percorrer tudo **na ordem certa** ainda é
melhor que percorrer tudo e depois ordenar.

**A resposta da pergunta final:** se as consultas filtram por `tipo` e por `tipo + data`, o
índice tem que ser `(tipo, data)`. **A coluna que aparece sozinha nos filtros vem primeiro** —
sempre. Um índice `(a, b)` atende `a` e `a+b`; nunca `b`.

## AP1 — O benchmark

| Consulta | Antes | Índice | Depois | Ganho | Linhas devolvidas |
|---|---|---|---|---|---|
| `valor BETWEEN 45000 AND 45100` | 49,91 ms | `(valor)` | 1,810 ms | **28x** | ~560 |
| `data = '2026-03-15'` | 67,53 ms | `(data)` | 7,012 ms | **10x** | ~2 200 |
| `cliente_id = 27384 AND tipo = 'compra'` | 35,97 ms | `(cliente_id)` | 0,024 ms | **1518x** | 13 |

Todos os planos passaram de `SCAN eventos` a `SEARCH eventos USING INDEX`.

**Os três ganhos são reais e diferem por duas ordens de grandeza — e a última coluna explica
tudo.** 13 linhas dão 1518x; 560 linhas dão 28x; 2 200 linhas dão 10x. O ganho é inversamente
proporcional ao número de linhas devolvidas, exatamente como a §6.5 previu. Se você extrapolar
essa curva para as 62 mil linhas de março, chega ao resultado do AP2 antes de medi-lo: o ganho
cruza o zero e vira prejuízo.

**Sobre a terceira:** o índice é só em `cliente_id`, mas o filtro tem duas condições. O banco usa
o índice para as 13 linhas do cliente e testa `tipo = 'compra'` em cada uma. Filtrar 13 linhas na
mão é gratuito — **não vale criar índice composto quando a primeira coluna já reduz a quase
nada.**

**A parte que ensina — o ruído.** Rodando duas vezes, as medições variam tipicamente na segunda
casa decimal para as rápidas e alguns milissegundos para as lentas. Isso significa que uma
"melhora" de 46 ms para 44 ms **não é melhora**: está dentro do ruído. Os ganhos desta tabela
são de 20x a 700x, ordens de grandeza acima da variação — é o que os torna confiáveis. **Um
número sem noção do seu ruído não é uma medição, é uma impressão com casas decimais.**

## AP2 — Reescrevendo o filtro

| Consulta | Plano antes | Antes | Plano depois | Depois |
|---|---|---|---|---|
| março (`LIKE '2026-03%'` → faixa) | `SCAN` | 175,80 ms | `SEARCH` | **266,27 ms** |
| cliente (`+ 0` → coluna limpa) | `SCAN` | 36,61 ms | `SEARCH` | **0,04 ms** (982x) |
| 1 a 15 de março (`LIKE` → faixa) | `SCAN` | 200,54 ms | `SEARCH` | 147,66 ms |
| 2026 inteiro | `SCAN` | — | `SEARCH` | pior ainda — é a tabela toda |

**A resposta da pergunta que decide o exercício: não, fazer `SCAN` virar `SEARCH` não é sempre
uma melhoria.** A consulta de março ficou **51% mais lenta** depois de passar a usar o índice.

O motivo é a seletividade, medida: março tem **62 493 linhas — 12,5% da tabela**. Acima da
faixa de 5% a 10%, e o mecanismo da §6.5 se inverte: 62 mil idas ao disco, cada uma para um
lugar diferente, custam mais que ler as 500 mil em sequência. O banco **escolheu** usar o
índice e escolheu mal — é o otimizador errando com base em estimativas (caixa-preta 1).

Compare com a segunda linha: 13 linhas devolvidas, 982x mais rápido. **Mesma reescrita, mesma
tabela, mesmo tipo de índice, resultados em direções opostas.**

E a terceira mostra o meio-termo: 1 a 15 de março devolve metade de março, e o ganho é modesto
(200 → 148 ms). É a região de transição, onde a resposta é "depende" e só a medição decide.

**A lição que este exercício existe para ensinar:** `SCAN` não é um defeito e `SEARCH` não é um
troféu. São dois caminhos com custos diferentes, e qual deles é melhor depende de **quantas
linhas saem no fim**. Otimizar olhando só o plano é otimizar a métrica errada — e é por isso
que o passo `H → I` do fluxograma da §8 (medir de novo) não é opcional.

## AP3 — A conta completa

Tomando `cliente_id`, a coluna que merece:

| Item | Medido |
|---|---|
| Leitura sem índice | 35,2 ms |
| Leitura com índice | 0,046 ms |
| **Ganho** | **763x — 35,1 ms por consulta** |
| Disco antes | 16,6 MB |
| Disco depois | 22,3 MB (**+34%**) |
| 20 000 `INSERT` sem índices extras | 171,0 ms |
| 20 000 `INSERT` com 1 índice | 217,8 ms (**+27%**) |
| Custo por escrita | ~0,0023 ms |

**A conclusão com número.** Cada leitura economiza 35,1 ms; cada escrita custa 0,0023 ms. O
índice deixa de compensar quando:

```
escritas × 0,0023 ms  >  leituras × 35,1 ms
escritas  >  leituras × 15 000
```

**Quinze mil escritas para cada leitura** — uma razão que praticamente nenhum sistema real
atinge. Para `cliente_id`, a decisão não é apertada: é folgada por quatro ordens de grandeza.

**E é justamente por isso que a conta importa.** Ela não serviu para descobrir se indexar; serviu
para descobrir **o quanto** a decisão é segura. Uma decisão folgada pode ser tomada rápido e
esquecida. Uma decisão apertada — digamos, 3 para 1 — precisa ser revisitada quando o padrão de
uso mudar, e alguém tem que saber disso. **O valor da conta não é o resultado; é a margem.**

## D1 — O parecer

**Seletividade medida das quatro:**

```
Q1  cliente_id = ?          13 linhas   =  0,00%
Q2  março                62 493 linhas   = 12,50%
Q3  tipo = 'login'      100 271 linhas   = 20,05%
Q4  valor > 89000         5 592 linhas   =  1,12%
```

| | Recomendação | Justificativa |
|---|---|---|
| **Q1** | `CREATE INDEX ON eventos(cliente_id)` | 0,00% da tabela; 763x medido |
| **Q2** | **não criar** — reescrever | 12,5%: acima do limiar; ver (c) |
| **Q3** | **não criar** | 20,05%: ganho zero medido no capítulo |
| **Q4** | `CREATE INDEX ON eventos(valor)` — **se rodar com frequência** | 1,12%; medido 43,04 → 19,66 ms (**2,2x**) |

**(a) Duas não devem receber índice, e por motivos diferentes.** Q3 é o caso do livro: 20% da
tabela, o índice é usado e não muda nada. Q2 é pior que isso — **medido, o índice torna a
consulta 51% mais lenta** (175,80 → 266,27 ms), porque 12,5% já são suficientes para as idas aleatórias ao
disco superarem a leitura sequencial. Q2 é o argumento mais forte do parecer: não é que o índice
seja desnecessário, é que ele **prejudica**.

**(b) O índice composto é o da Q1** — `(cliente_id, data)`. A consulta filtra por `cliente_id` e
ordena por `data DESC`; com as duas colunas na ordem certa, o índice serve ao filtro **e** à
ordenação, dispensando a etapa de ordenar.

**A honestidade que o parecer exige:** medido, `(cliente_id, data)` deu 0,047 ms contra 0,048 ms
do índice simples — **empate**. O motivo é que o filtro devolve 13 linhas, e ordenar 13 linhas é
gratuito. O índice composto seria decisivo se cada cliente tivesse dezenas de milhares de
eventos. **A justificativa teórica está certa e o ganho prático é nulo neste volume** — e
escrever isso no parecer, em vez do ganho que se esperava encontrar, é o que faz dele um parecer
e não uma peça de convencimento.

**(c) Q2 se resolve sem índice**, mudando a consulta. Ela agrupa por `tipo` e conta — não precisa
das cinco colunas de 62 mil linhas. Um índice em `(data, tipo)` a atenderia por **cobertura**
(§7): tudo o que a consulta lê está no índice, e a tabela não é tocada. Medido:

```
sem indice    SCAN eventos                                       89,3 ms
(data, tipo)  SEARCH eventos USING COVERING INDEX idx_dt         32,4 ms
```

**2,8x — e note a palavra `COVERING` no plano.** É a mesma faixa de 12,5% que tornou o índice
prejudicial no AP2; a diferença é que aqui a tabela nunca é tocada, então não há 62 mil idas
aleatórias ao disco. É a distinção entre "o índice ajuda a **achar** as linhas" e "o índice
**é** a resposta" — e ela inverte a recomendação para a mesma seletividade.

**(d) O custo somado.** Dois índices simples, ~5,7 MB cada, **~11,4 MB** sobre 16,6 MB — o
arquivo cresce ~69%. Escrita: ~27% mais lenta por índice, acumulando para cerca de **+50%** com
os dois. Não é um detalhe a mencionar de passagem: numa tabela de eventos, que é
escrita-intensiva por natureza, metade a mais de tempo de gravação é uma decisão de arquitetura.

**(e) A pergunta ao time:** *qual é a razão entre leituras e escritas nesta tabela, e ela está
crescendo?* Uma tabela de eventos tende a receber muito mais escrita que leitura, e essa é
exatamente a situação em que a conta do AP3 pode virar. Uma pergunta subsidiária: a Q4 (auditoria
de valores altos) roda com que frequência? Se é uma vez por mês, um índice permanente para
economizar 40 ms mensais é uma dívida sem retorno — e o correto é deixá-la varrer.

**O fecho.** "Criar um índice" é uma resposta; o pedido era um diagnóstico. Das quatro consultas
lentas, duas não deveriam receber índice, uma delas ficaria **pior** com ele, e uma se resolve
mudando o que se pede em vez de como se busca. Nada disso aparece para quem trata lentidão como
sintoma de índice faltando — e o custo do erro não é a consulta que continua lenta, é o índice
permanente que ficou cobrando escrita para sempre, sem que ninguém volte para conferir se
ajudou. **Diagnóstico é o que produz a decisão de não fazer**, e essa é a decisão que nenhum
palpite produz.

---

## Erros mais comuns

1. **Indexar `id`.** Já é o `rowid`; o índice é uma cópia ordenada do que já está ordenado.
2. **Confundir cardinalidade com necessidade.** A coluna pode ser seletiva e não ter consulta.
3. **Ler `SEARCH` e comemorar.** Em março, o `SEARCH` foi 51% mais lento que o `SCAN`.
4. **Achar que `SCAN` é sempre ruim.** `SCAN ... USING INDEX` entrega ordenado de graça.
5. **Errar a ordem do índice composto.** A coluna que aparece sozinha vem primeiro.
6. **Reescrever o filtro mudando a semântica.** `UPPER(x) = 'A'` e `x = 'a'` não são a mesma pergunta.
7. **Relatar ganho menor que o ruído da medição.**
8. **Indexar coluna booleana.** Salvo distribuição muito desigual — e aí, índice parcial.
9. **Esquecer de somar o custo** de todos os índices recomendados juntos.
