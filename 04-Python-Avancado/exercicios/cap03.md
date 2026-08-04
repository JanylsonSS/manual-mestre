# Exercícios — Capítulo 04.03: Closures e fábricas

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap03.md`](gabaritos/cap03.md).

## Aquecimento

### A1 — Preveja a saída `[Aquecimento · ~10 min]`

```python
# 1
def f1():
    fs = []
    for i in range(3): fs.append(lambda: i * 10)
    return [f() for f in fs]

# 2
def f2(): return [(lambda: i)() for i in range(3)]

# 3
def f3(n):
    def g(): return n
    n = 99
    return g()

# 4
def f4():
    x = 10
    def g(): x = 20; return x
    g(); return x

# 5
def f5():
    x = 10
    def g():
        nonlocal x; x = 20; return x
    g(); return x

# 6
from functools import partial
fs = [partial(lambda i: i, i) for i in range(3)]
[f() for f in fs]
```

**O item 3 é o mais importante.** Depois de responder, explique **por que** em uma linha.

### A2 — Precisa de `nonlocal`? `[Aquecimento · ~10 min]`

Para cada função interna, diga se `nonlocal` é necessário:

1. `def g(): return contador`
2. `def g(): contador += 1`
3. `def g(): lista.append(1)` — com `lista = []` fora
4. `def g(): lista = [1]` — idem
5. `def g(): d["chave"] = 1` — com `d = {}` fora
6. `def g(): return contador + 1`

**A pergunta que fecha:** os itens 3 e 4 parecem iguais e são opostos. Por quê?

### A3 — O que a célula guarda `[Aquecimento · ~10 min]`

Para cada caso, diga o que `__code__.co_freevars` e `__closure__[n].cell_contents` mostram:

1. `def fab(a, b): def inner(): return a + b; return inner` → `fab(1, 2)`
2. Uma closure que não usa nenhuma variável externa.
3. Uma closure sobre uma **lista** que é modificada depois de a closure ser criada.
4. Duas closures da mesma fábrica, criadas com argumentos diferentes.
5. Uma closure com `nonlocal`, antes e depois de três chamadas.

### A4 — Closure ou classe? `[Aquecimento · ~10 min]`

1. Um contador que só incrementa.
2. Um contador que incrementa, lê e zera.
3. Uma função de validação com dois limites fixos.
4. Uma conexão com banco que abre, consulta e fecha.
5. Um `key=` especializado para `sorted`.
6. Um acumulador que soma e devolve a média ao final.

## Aplicação

### AP1 — As fábricas `[Aplicação · ~20 min]`

Escreva três fábricas de validadores: `entre(minimo, maximo)`, `tamanho_maximo(n)`, `um_de(*opcoes)`. Cada uma devolve uma função de um valor para `bool`.

1. Combine-as: `validar(valor, *regras)` devolvendo a lista de regras violadas.
2. Faça a mensagem de erro dizer **qual** regra falhou — o que exige que a função interna tenha nome.
3. Reescreva uma delas com `functools.partial` e compare.
4. **A decisão:** em qual das três `partial` é suficiente, e por quê?

### AP2 — Os filtros da Aurora `[Aplicação · ~25 min]`

Implemente os filtros combináveis da §9 (`preco_minimo`, `da_categoria`, `apenas_ativos`) e `filtrar(produtos, *filtros)`.

1. Acrescente dois filtros novos sem tocar em `filtrar`.
2. Monte a lista de filtros a partir de um dicionário de configuração.
3. Escreva a versão com `if` e compare as duas em: linhas, legibilidade, e facilidade de acrescentar o sétimo filtro.
4. **A pergunta da §9:** os filtros do seu caso são conhecidos em tempo de escrita ou de execução? Escolha a versão com base nisso, não em preferência.

### AP3 — O contador completo `[Aplicação · ~20 min]`

**Tarefa.** Estenda o contador em closure para suportar: incrementar, **ler sem incrementar**, zerar, e definir um valor.

1. Implemente devolvendo um dicionário de funções.
2. Implemente com uma classe.
3. Compare as duas em linhas, legibilidade e facilidade de estender.
4. **A conclusão que o exercício quer:** em que ponto exato a closure deixou de ser a escolha certa?

## Desafio

### D1 — O memoizador `[Desafio · ~45 min]`

Escreva `memoizar(funcao, limite=None)` que devolva uma versão com cache em closure.

- **(a)** argumentos já vistos devolvem o resultado guardado;
- **(b)** o cache mora na closure, **não** numa global;
- **(c)** expõe `acertos` e `erros`;
- **(d)** com `limite`, descarta o mais antigo ao encher;
- **(e)** **meça** `fib(30)` com e sem cache.

**As duas perguntas do fecho:** (1) por que argumentos precisam ser hasháveis, e o que acontece com uma lista? (2) O `functools.lru_cache` da biblioteca padrão faz isso — quando escrever o seu se justifica?

<details><summary>💡 Dica 1 (conceito)</summary>
`cache = {}` na função externa; `nonlocal` só é necessário para os **contadores** (números), não para o dicionário — mutar não exige, reatribuir exige. É o A2 aplicado.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para (c): a closure não tem como expor variáveis. Uma saída é anexar um atributo à função envolvida (`envolvida.estatisticas = ...`) — o 04.01 mostrou que funções aceitam atributos.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`def memoizar(f, limite=None)` → `cache = {}` → `def envolvida(*args)` → checar `args in cache` → calcular, guardar, devolver → anexar atributo → `return envolvida`. Para (d): `cache.pop(next(iter(cache)))` remove o mais antigo, já que dicionários preservam ordem de inserção.
</details>
