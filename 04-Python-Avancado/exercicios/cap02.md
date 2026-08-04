# Exercícios — Capítulo 04.02: Funções como valores e lambdas

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap02.md`](gabaritos/cap02.md).

## Aquecimento

### A1 — Preveja a saída `[Aquecimento · ~10 min]`

Dado `def f(x): return x * 2`:

1. `g = f; print(g(3), g is f)`
2. `print([f, len, str][1]("abc"))`
3. `h = f(3); print(h, callable(h))`
4. `sorted(["bb", "a", "ccc"], key=len)`
5. `sorted([3, -1, 2], key=abs)`
6. `sorted(["b", "a"], key=len())` — **cuidado**

### A2 — Escreva o `key` `[Aquecimento · ~10 min]`

Sobre `pessoas = [{"n": ..., "c": ..., "i": ...}]` (nome, cidade, idade), escreva o `key` para:

1. idade **decrescente**
2. cidade crescente, idade decrescente
3. tamanho do nome, e nomes de mesmo tamanho em ordem alfabética
4. ordem alfabética **ignorando maiúsculas**
5. cidade crescente, nome **decrescente** — o `-` não serve aqui
6. os que têm idade acima de 30 primeiro, depois o resto

### A3 — `lambda` ou `def`? `[Aquecimento · ~10 min · decida e justifique]`

1. Extrair o terceiro campo de uma tupla, para um `key=`.
2. Calcular o frete conforme peso, região e se é cliente premium.
3. Devolver `0` quando o valor for `None`, e o valor caso contrário.
4. Uma função guardada num dicionário de despacho, usada em cinco lugares.
5. Um *callback* de uma linha, passado a `map`.
6. `dobro = lambda x: x * 2`

### A4 — Ache o erro `[Aquecimento · ~10 min]`

1. `sorted(dados, key=minha_funcao())`
2. `sorted(nums, key=lambda a, b: a - b)`
3. `sorted(nomes, key=lambda s: -s)`
4. `resultado = filter(lambda x: x > 1, nums)` — usado duas vezes
5. `acao = ACOES[comando]` sem tratamento quando `comando` não existe
6. `print(ACOES["salvar"])` esperando executar a ação

## Aplicação

### AP1 — O despacho `[Aplicação · ~20 min]`

Converta esta função em despacho por dicionário:

```python
def calcular(operacao, a, b):
    if operacao == "soma": return a + b
    elif operacao == "sub": return a - b
    elif operacao == "mult": return a * b
    elif operacao == "div": return a / b if b else None
    elif operacao == "pot": return a ** b
    elif operacao == "mod": return a % b if b else None
    elif operacao == "max": return max(a, b)
    else: raise ValueError("operação inválida")
```

1. Escreva a versão com dicionário.
2. A mensagem de erro deve **listar as operações válidas**, gerada do próprio dicionário.
3. Acrescente `"min"` nas duas versões e compare o que foi preciso tocar.
4. **A pergunta que fecha:** `div` e `mod` devolvem `None` quando `b` é zero. Isso é boa ideia? Argumente e proponha alternativa.

### AP2 — Ordenando a Aurora `[Aplicação · ~25 min]`

Sobre os produtos do banco do módulo 03 (ou uma lista de dicionários equivalente), implemente seis ordenações: por nome; por preço; por preço decrescente; por categoria e depois nome; por categoria e depois preço decrescente; ativos primeiro, depois por nome.

Depois: monte um dicionário `CRITERIOS` com os seis, escreva `ordenar(produtos, criterio)` que o consulte, e faça a mensagem de erro listar as opções. **Meça** quantas vezes o `key` roda para 12 produtos, com um contador.

### AP3 — A estabilidade `[Aplicação · ~20 min]`

**Tarefa.** Ordene uma lista de pessoas por **três** critérios — cidade crescente, cargo crescente, nome decrescente — **sem usar tupla como chave**, apenas passadas sucessivas.

1. Descubra a ordem correta das passadas e explique a regra.
2. Prove que funciona comparando com a versão de tupla (onde couber).
3. Mostre um caso em que a tupla **não** resolve e as passadas resolvem.
4. Explique o que a garantia de estabilidade tem a ver com isso.

## Desafio

### D1 — O pipeline `[Desafio · ~45 min]`

Escreva `aplicar(dados, *etapas)` que passe `dados` por cada função em sequência.

- **(a)** zero etapas devolve os dados inalterados;
- **(b)** acumula um relatório: quantos itens entraram e saíram de **cada** etapa;
- **(c)** exceção numa etapa interrompe o pipeline com mensagem que **nomeia a etapa** — e resolver isso exige lidar com o `<lambda>`;
- **(d)** use-o nas vendas da Aurora: filtrar concluídas → converter centavos → agrupar por cidade → ordenar por total.

**Fecho:** em que o pipeline é melhor, e em que é pior, que quatro linhas sequenciais? Responda em 5 linhas, sem defender o pipeline por padrão.

<details><summary>💡 Dica 1 (conceito)</summary>
Para (c): `getattr(etapa, "__name__", repr(etapa))` devolve o nome quando existe. Para lambdas, `__name__` é `<lambda>` — e é justamente aí que o exercício quer que você chegue.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
O relatório de (b) pressupõe que cada etapa devolva algo com `len()`. E se uma devolver um número? Decida: exigir coleções, ou tratar o caso — e documente a decisão.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`resultado = dados` → laço sobre `etapas` com `enumerate` → `try/except` registrando o nome → acumular `(nome, antes, depois)` → devolver `(resultado, relatorio)`.
</details>
