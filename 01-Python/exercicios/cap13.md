# Exercícios — Capítulo 01.13: Listas parte 2

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap13.md`](gabaritos/cap13.md).

## Aquecimento

### A1 — Previsão de aliasing `[Aquecimento · ~10 min · reamarrar × mutar]`

**Tarefa.** Preveja o estado final de TODAS as etiquetas em cada cena:

```python
# 1
a = [1, 2]
b = a
b.append(3)
```

```python
# 2
a = [1, 2]
b = a
b = [9, 9]
```

```python
# 3
s = "ab"
t = s
t = t + "c"
```

```python
# 4
a = [1, 2]
b = a.copy()
b.append(3)
```

```python
# 5
a = [[1], [2]]
b = a.copy()
b[0].append(99)
```

```python
# 6
a = [1, 2, 3]
b = a
a.sort(reverse=True)
```

### A2 — Contratos `[Aquecimento · ~5 min · muta ou devolve?]`

**Tarefa.** Classifique: `append` · `sorted` · `sort` · `copy` · `remove` · `count` · `reverse` · `pop` · `extend` · `index`.

### A3 — Rasa ou profunda? `[Aquecimento · ~10 min · o critério]`

**Tarefa.** Para cada estrutura, diga qual cirurgia é suficiente e por quê:

1. `["PED-1", "PED-2", "PED-3"]`
2. `[100, 200, 300]`
3. `[["PED-1", 100], ["PED-2", 200]]`
4. `[[1, 2], [3, 4], [5, 6]]` — e você só vai LER a cópia, nunca mutar. Muda a resposta?

### A4 — sort × sorted `[Aquecimento · ~5 min · preservar ou substituir]`

**Tarefa.** Para cada trecho: o que fica em cada variável, o que explode:

```python
p = [3, 1, 2]
q = p.sort()
```

```python
p = [3, 1, 2]
q = sorted(p)
```

```python
p = [3, 1, 2]
p.sort()
print(p[0])
```

```python
p = [3, 1, 2]
q = p.sort()
print(q[0])
```

## Aplicação

### AP1 — Autópsia do fantasma `[Aplicação · ~20 min · diagnóstico]`

**Contexto.** O script abaixo (relatório da Aurora) tem 3 bugs de aliasing:

```python
vendas = [4990, 12990, 46990, 899]
backup = vendas
top = vendas
top.sort(reverse=True)
baratas = vendas
baratas.remove(46990)

print("backup:", backup)
print("top 2:", top[:2])
print("vendas originais:", vendas)
```

**Tarefa.** Rode, diagnostique cada bug com `is`, explique em 1 linha cada, e corrija — as três "visões" devem existir sem que `vendas` mude.

### AP2 — Ordenações do relatório `[Aplicação · ~20 min · preservando a original]`

**Tarefa.** Dada `produtos = [["Teclado", 34900], ["fone", 46990], ["Mouse", 8990]]`: produza (a) top 3 por valor decrescente, (b) ordem alfabética por nome ignorando caixa, (c) a lista invertida — sem alterar `produtos` (prove imprimindo-a ao final de cada visão).

<details><summary>💡 Dica 1 (conceito)</summary>
Ordenar por um campo de sublista exige key — mas `key=` com função própria só chega no 04.02. Solução de hoje: monte uma lista auxiliar com o campo na frente, ou ordene por nome com key=str.lower após extrair os nomes. Documente a limitação.
</details>

### AP3 — A matriz que não era `[Aplicação · ~20 min · a pegadinha construída]`

**Tarefa.** Construa `errada = [[0] * 3] * 3` e `certa = []` + for/append de listas novas. Prove a diferença: mute `[0][0]` nas duas e imprima; use `is` entre as linhas de cada uma. Escreva a explicação com suas palavras (3–4 linhas).

## Desafio

### D1 — O livro-caixa imutável `[Desafio · ~50 min · integridade de histórico]`

**Tarefa.** Lista `vendas` (cada item: `[produto, valor_centavos, cidade]`) que só cresce. Produza 4 visões sem alterá-la: top 3 por valor, alfabética por produto, só Campinas, ordem inversa de chegada — cada uma com prova de integridade (`is` + print da original). Depois, o bloco de sabotagem: uma versão com `sort()` no lugar, demonstrando o dano às outras visões. Conclua em 5 linhas por que histórico não se muta.

<details><summary>💡 Dica 1 (conceito)</summary>
4 visões = 4 listas novas: sorted, sorted com key, filtro (for+append), fatia [::-1].
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
A sabotagem fica mais didática se você rodar "as 4 visões", depois o sort() destrutivo, depois "as 4 visões" de novo — a diferença aparece na visão que dependia da ordem de chegada.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
vendas → 4 blocos de visão (cada um com prova) → bloco sabotagem → 4 visões de novo → conclusão comentada.
</details>
