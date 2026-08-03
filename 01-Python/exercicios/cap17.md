# Exercícios — Capítulo 01.17: Compreensões

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap17.md`](gabaritos/cap17.md).

## Aquecimento

### A1 — Previsão `[Aquecimento · ~10 min · as três formas]`

**Tarefa.** Preveja a saída exata (com `valores = [3, 8, 15, 22]`):

1. `[v * 10 for v in valores]`
2. `[v for v in valores if v % 2 == 0]`
3. `[v if v > 10 else 0 for v in valores]`
4. `{v: v ** 2 for v in valores if v < 10}`
5. `{v % 3 for v in valores}`
6. `[c for c in "Aurora" if c.isupper()]`
7. `[len(p) for p in ["Fone", "Mouse", "Cabo"]]`
8. `{p[0] for p in ["Fone", "Mouse", "Cabo", "Fita"]}`

### A2 — Dobre o laço `[Aquecimento · ~10 min · laço → comprehension]`

**Tarefa.** Converta cada laço:

```python
# 1
dobros = []
for v in valores:
    dobros.append(v * 2)
```

```python
# 2
grandes = []
for v in valores:
    if v > 10:
        grandes.append(v)
```

```python
# 3
mapa = {}
for codigo, valor in pares:
    mapa[codigo] = valor
```

```python
# 4
iniciais = set()
for nome in nomes:
    iniciais.add(nome[0].upper())
```

### A3 — Desdobre a comprehension `[Aquecimento · ~10 min · o caminho inverso]`

**Tarefa.** Converta em laços explícitos:

1. `[int(t) for t in textos if t.isdigit()]`
2. `{c.strip().lower() for c in cidades_sujas}`
3. `{k: v * 2 for k, v in totais.items() if v > 100}`

### A4 — Filtro ou escolha? `[Aquecimento · ~5 min · a posição do if]`

**Tarefa.** Para cada intenção, escreva a comprehension correta (com `if` no fim ou `if/else` na frente):

1. "Só os valores positivos."
2. "Todos os valores, com os negativos virando zero."
3. "Só os produtos de Campinas."
4. "Todos os produtos, com o nome em maiúsculas se for de Campinas."

## Aplicação

### AP1 — A esteira em uma linha `[Aplicação · ~20 min · refatoração]`

**Tarefa.** Refatore a limpeza do lote (01.12) para comprehensions: `validos` (centavos int), `rejeitados` (textos que falharam), `canonicas` (cidades limpas) e `indice` (codigo → registro). Compare o total de linhas antes/depois em comentário.

### AP2 — As três formas `[Aplicação · ~20 min · escolhendo a saída]`

**Tarefa.** Do lote de registros (5 tuplas): (a) lista dos códigos com valor acima de R$ 100; (b) dicionário `codigo → cidade canônica`; (c) conjunto dos produtos distintos. Uma comprehension cada.

### AP3 — Refatoração reversa `[Aplicação · ~25 min · quando desdobrar]`

**Tarefa.** As três comprehensions abaixo são ilegíveis. Converta cada uma num laço legível (com nomes intermediários) e justifique em 1 linha o que melhorou:

```python
r1 = [f"{c}: R$ {v/100:.2f}" for c, p, v, cid in regs if v > 10000 and cid.strip().lower() in ("campinas", "santos") and "a" in p.lower()]
```

```python
r2 = {cid.strip().lower(): [p for c, p, v, cid2 in regs if cid2.strip().lower() == cid.strip().lower()] for c, p, v, cid in regs}
```

```python
r3 = [int(t.replace("R$", "").replace(".", "").replace(",", "").strip()) if t.strip() else 0 for t in textos_monetarios]
```

<details><summary>💡 Dica 1 (conceito)</summary>
Aplique os três testes: comprimento, quantidade de for/if, leitura em voz alta. A r2 tem uma comprehension DENTRO de outra — e é quadrática, além de ilegível.
</details>

## Desafio

### D1 — O júri da legibilidade `[Desafio · ~45 min · decidir, não aplicar]`

**Tarefa.** Cinco laços dos seus arquivos (01.12–01.16), cada um com: versão comprehension proposta, os três testes aplicados, e o veredito (dobra / permanece) com justificativa. Fecho: estatística e o padrão comum aos que resistiram (3 linhas).

<details><summary>💡 Dica 1 (conceito)</summary>
Os resistentes costumam fazer mais de uma coisa por volta: calcular E formatar E acumular em dois lugares.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Conte os caracteres da versão dobrada — o teste (a) é objetivo e resolve metade dos casos.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Por caso: origem, laço, comprehension, 3 testes, veredito, justificativa. Fecho com estatística e padrão.
</details>
