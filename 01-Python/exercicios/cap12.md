# Exercícios — Capítulo 01.12: Listas — parte 1

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap12.md`](gabaritos/cap12.md).

## Aquecimento

### A1 — A régua transfere `[Aquecimento · ~10 min · índices e fatias]`

**Tarefa.** Sobre `pedidos = ["PED-1", "PED-2", "PED-3", "PED-4", "PED-5"]`, preveja:

1. `pedidos[0]`
2. `pedidos[-2]`
3. `pedidos[1:3]`
4. `pedidos[2:]`
5. `len(pedidos[1:4])`
6. `"PED-3" in pedidos`
7. `pedidos[5]`
8. `pedidos[3:99]`

### A2 — Mutação e append `[Aquecimento · ~10 min · o poder novo]`

**Tarefa.** Preveja o estado final da lista em cada sequência (e o que cada operação devolve):

```python
valores = [100, 200, 300]
valores[1] = 250
valores.append(400)
```

```python
fila = []
fila.append("Ana")
fila.append("Bia")
fila[0] = "Ana Paula"
```

```python
itens = [1, 2, 3]
resultado = itens.append(4)
# o que há em itens? e em resultado?
```

```python
letras = list("sol")
letras[0] = "S"
letras.append("!")
# e a string "sol" original?
```

### A3 — Os três padrões `[Aquecimento · ~5 min · classificação]`

**Tarefa.** Classifique cada laço (acumular / filtrar / transformar / combinação):

1. `for v in valores: total += v`
2. `for t in textos: numeros.append(int(t))`
3. `for v in valores: (if v > 100) grandes.append(v)`
4. `for t in textos: (if t.isdigit()) numeros.append(int(t))`
5. `for c in codigo: (if c == "-") hifens += 1`

### A4 — String × lista `[Aquecimento · ~5 min · os dois contratos]`

**Tarefa.** Para cada par, diga qual funciona, qual explode (ou silencia) e por quê:

1. `s[0] = "X"` vs. `lista[0] = "X"`
2. `s = s.upper()` vs. `lista = lista.append(x)`
3. `s + "!"` vs. `lista + [item]`
4. `for c in s` vs. `for item in lista`

## Aplicação

### AP1 — O caixa ganha memória `[Aplicação · ~20 min · lista + métricas]`

**Tarefa.** Evolua o `caixa_do_dia.py` (01.10/AP2): cada valor válido entra numa lista `valores`; no fechamento: total, quantidade, ticket médio, **maior** e **menor** (acumuladores no for — sem `max`/`min` prontos), com o caixa vazio protegido por truthiness.

### AP2 — Filtrar e transformar o lote `[Aplicação · ~25 min · a linha de produção]`

**Contexto.** O lote do dia chegou com defeitos:

```python
lote = ["46990", "12990", "abc", "899", "", "34900"]
```

**Tarefa.** Produza: `validos` (centavos int — filtro `isdigit` + transformação), `rejeitados` (os textos que falharam, com `repr`), e o relatório: N válidos somando R$ X; N rejeitados listados.

### AP3 — Enumerate no recibo `[Aplicação · ~20 min · posição + item]`

**Tarefa.** Dada uma lista de valores em centavos, imprima o recibo: linhas `N. R$ V (acumulado: R$ A)` via enumerate + acumulador, e o destaque final "último item: ..." com `[-1]` — protegido para a lista vazia.

## Desafio

### D1 — Caixa da Aurora v3 `[Desafio · ~50 min · fechamento com histograma]`

**Tarefa.** Fila de atendimento (while + insistência) registrando valores numa lista; fechamento com: total, quantidade, ticket médio, maior, menor, quantos acima de R$ 500, e o histograma horizontal (`"#" * (valor // 10_000)` por linha, numerado via enumerate). Recibo formatado e alinhado.

<details><summary>💡 Dica 1 (conceito)</summary>
Maior/menor: inicialize com o primeiro da lista (valores[0]) DEPOIS de garantir que ela não está vazia — a ordem dos guardas importa.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Camadas testáveis: fila → lista → métricas → histograma. Transcrição de uma sessão com 4 pedidos no comentário final.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
while fila → append → fechamento: if valores: for das métricas → for numero, v in enumerate(valores, 1): print(f"{numero:>2}. {'#' * (v // 10_000)}") → else: vazio.
</details>
