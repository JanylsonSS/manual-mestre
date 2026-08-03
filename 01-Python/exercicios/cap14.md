# Exercícios — Capítulo 01.14: Tuplas e desempacotamento

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap14.md`](gabaritos/cap14.md).

## Aquecimento

### A1 — Tupla ou não? `[Aquecimento · ~5 min · a vírgula manda]`

**Tarefa.** Diga o tipo de cada expressão: `(1)` · `(1,)` · `()` · `1, 2` · `("a", "b")` · `("a")`.

### A2 — Desempacotamento `[Aquecimento · ~10 min · previsão]`

**Tarefa.** Preveja os valores das etiquetas — ou o erro exato:

```python
a, b = (10, 20)
```

```python
x, y, z = (1, 2)
```

```python
p, q = [5, 6]
```

```python
a, b = 1, 2
a, b = b, a
```

```python
for i, letra in enumerate("ab", start=1):
    print(i, letra)
```

### A3 — Tupla ou lista? `[Aquecimento · ~5 min · registro × coleção]`

**Tarefa.** Classifique com 1 linha de justificativa: (1) um pedido com código/produto/valor/cidade; (2) os pedidos do dia; (3) as coordenadas de um ponto (x, y); (4) os itens de um carrinho em construção; (5) as cidades atendidas (fixas por contrato); (6) o par (quociente, resto) de uma divisão; (7) o histórico de preços de um produto; (8) o registro de uma venda lida do CSV.

### A4 — O que funciona? `[Aquecimento · ~10 min · limites da tupla]`

**Tarefa.** Sobre `t = ("PED-1", 100, "Campinas")`, quais funcionam e quais explodem (com qual mensagem)?

1. `t[0]`
2. `t[-1]`
3. `t[0:2]`
4. `t[1] = 200`
5. `t.append("novo")`
6. `len(t)` e `"Campinas" in t`

## Aplicação

### AP1 — Registros do lote `[Aplicação · ~20 min · listas viram tuplas]`

**Tarefa.** Pegue as `linhas_sujas` do 01.12 e produza `pedidos` como **lista de tuplas** validadas (código, produto, valor_centavos, cidade). O relatório usa desempacotamento — zero `campos[0]` no corpo do laço.

### AP2 — O carrinho vira nota `[Aplicação · ~20 min · o fluxo mutável→imutável]`

**Tarefa.** `carrinho_para_nota.py`: monte um carrinho (lista) recebendo 3 itens; feche com `nota = tuple(carrinho)`; imprima ambos; tente alterar a nota (linha comentada com a mensagem real de erro); prove que alterar o carrinho depois **não** afeta a nota (e explique por quê, em 2 linhas).

<details><summary>💡 Dica 1 (conceito)</summary>
`tuple(lista)` cria uma tupla NOVA com os mesmos itens — como a cópia rasa do 01.13. Se os itens forem imutáveis, a nota está realmente congelada.
</details>

### AP3 — Trocas e retornos `[Aplicação · ~20 min · desempacotamento aplicado]`

**Tarefa.** Quatro mini-exercícios em `desempacotando.py`: (a) trocar duas variáveis; (b) rotacionar três (`a, b, c = c, a, b`) e conferir; (c) usar `divmod` no cálculo do troco (quantas notas + resto, em uma linha por degrau); (d) reescrever um laço com `enumerate` usando tuplas explícitas (`for par in ...` + desempacotamento manual dentro) e comparar legibilidade.

## Desafio

### D1 — A nota fiscal da Aurora `[Desafio · ~45 min · o fluxo completo]`

**Tarefa.** Implemente o diagrama da seção 8: linhas sujas → esteira montando lista temporária → validação (código, valor, cidade atendida) → `tuple()` + append em `pedidos` (inválidos vão para `rejeitados` com motivo) → relatório desempacotado com totais. Ao final: bloco comentado com as 3 sabotagens que a tupla barra (com as mensagens reais) + reflexão de 5 linhas comparando com o `promessas_pagas.py` do 01.12.

<details><summary>💡 Dica 1 (conceito)</summary>
A lista temporária só existe durante a limpeza; a tupla nasce quando tudo está validado. Duas listas de saída: pedidos e rejeitados.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Rejeitados também são registros: `(linha_original, motivo)` — tupla de dois campos.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
for linha → campos = split/strip → laudos → if todos ok: pedidos.append(tuple(campos_convertidos)) else: rejeitados.append((linha, motivo)) → relatórios → sabotagens comentadas → reflexão.
</details>
