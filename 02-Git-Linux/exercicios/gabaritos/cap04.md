# Gabaritos — Capítulo 02.04

Abra somente após tentativa honesta.

## A1 — Previsão de pipes

1. `21` (20 registros + cabeçalho) — e é *useless use of cat*: `wc -l vendas.csv` faz o mesmo.
2. `20` (pula o cabeçalho).
3. O número de linhas com "campinas" em qualquer caixa — **atenção:** se o cabeçalho contivesse a palavra, ele entraria na conta.
4. A lista de cidades **distintas** (uma por linha), em ordem alfabética — incluindo o texto do cabeçalho (`cidade`), porque não foi pulado.
5. A cidade com mais ocorrências, com sua contagem (uma linha).
6. Os códigos dos 3 primeiros registros (uma coluna).

**Erro esperado:** esquecer que o cabeçalho entra nos itens 3 e 4 — motivo pelo qual `tail -n +2` abre quase todo pipe sobre CSV.
**Critério:** 6/6 com a observação do cabeçalho.

## A2 — Redirecionamento

1. Tela: nada. Arquivo: a listagem. 2. Tela: **a mensagem de erro** (stderr). Arquivo: vazio (foi truncado na abertura!). 3. Tela: nada de stdout (não houve); arquivo `erros.txt`: a mensagem. 4. Tela: nada; arquivo: listagem **e** erros juntos. 5. `log.txt` com **1 linha** (cada execução truncou a anterior). 6. `log.txt` com **3 linhas**.

**Critério:** 6/6; os itens 2 e 5 são os que ensinam.

## A3 — Flags do grep

1. `-i` · 2. `-n` · 3. `-v` · 4. `-c` · 5. `-r` · 6. `-l`.

**Critério:** 6/6.

## A4 — Monte o pipe

1. `tail -n +2 vendas.csv | wc -l`
2. `tail -n +2 vendas.csv | cut -d';' -f2 | sort | uniq -c | sort -rn | head -3`
3. `grep -c WARN app.log`
4. `grep ERROR app.log | tail -5`

**Critério:** 4/4; o item 2 com `tail -n +2` e as quatro estações.

## AP1 — Investigação do CSV

Referências (arquivo do 01.22/01.25, 13 registros):

1. `tail -n +2 dados/vendas.csv | wc -l` → 13
2. `grep -ci campinas dados/vendas.csv` → 4
3. `tail -n +2 dados/vendas.csv | cut -d';' -f4 | tr -d ' ' | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn`
4. `tail -n +2 dados/vendas.csv | sort -t';' -k3 -rn | head -5 | cut -d';' -f1,3` (ordena pela coluna 3 numericamente)
5. `grep ';$' dados/vendas.csv` → a linha da `Cadeira Ergonômica` (cidade vazia = termina com `;`)
6. `tail -n +2 dados/vendas.csv | cut -d';' -f2 | sort -u | wc -l`
7. `grep -rln "calcular_frete" --include="*.py" .`
8. `find 01-Python/codigo -type f -exec ls -lh {} \; | sort -k5 -rh | head -1` (ou `ls -lhS` dentro de cada pasta)

**Critério:** ≥ 6/8 com o comando registrado; o item 5 (usar `;$` para achar campo vazio no fim) é o mais engenhoso.

## AP2 — Análise de log

Referências: (a) `cut -d' ' -f3 app.log | sort | uniq -c | sort -rn`; (b) `grep ERROR app.log | tail -5`; (c) `grep ERROR app.log | cut -d' ' -f2 | cut -d':' -f1,2 | sort | uniq -c`; (d) `grep ERROR app.log | grep timeout`; (e) `grep -v INFO app.log`.

**Critério:** 5 análises funcionando sobre o log criado por você.

## AP3 — Relatório redirecionado

Referência de estrutura:

```bash
{
  echo "RELATÓRIO — $(date +%Y-%m-%d)"
  echo "Registros: $(tail -n +2 vendas.csv | wc -l)"
  echo ""
  echo "Por cidade:"
  tail -n +2 vendas.csv | cut -d';' -f4 | tr -d ' ' | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn
} > relatorio_terminal.txt
```

**Erro esperado:** usar `>` em cada linha (cada uma truncaria a anterior — sobraria só a última); a solução é o bloco `{ ... } >` ou `>>` a partir da segunda.
**Critério:** arquivo gerado por bloco único, com as três seções.

## D1 — O investigador de incidentes

**Referências:** (a) `wc -l app.log`; (b) `grep -c ERROR app.log`; (c) `grep ERROR app.log | cut -d' ' -f4- | sort | uniq -c | sort -rn | head -3`; (d) `grep ERROR app.log | cut -d' ' -f2 | cut -d':' -f1,2 | sort | uniq -c | sort -rn | head -1`; (e) `grep ERROR app.log | grep timeout`; (f) `grep -vc INFO app.log`.

**Reflexão esperada:** o terminal vence quando a pergunta é **pontual, exploratória e sobre texto** — a resposta sai em segundos e o custo de errar é zero (refazer o pipe não custa nada). O Python passa a ser a ferramenta certa quando: a lógica tem regras de negócio (validação, conversões, cálculos com decisão), o processo **roda repetidamente** e precisa ser mantido/testado, ou o resultado alimenta outro sistema (JSON, banco). Critério prático: *investigar com terminal; produzir com Python*.

**Critério de "está bom":** 6 respostas com um pipe cada; arquivo de diagnóstico montado com `>>`; reflexão com o critério explícito e um exemplo de cada lado.
