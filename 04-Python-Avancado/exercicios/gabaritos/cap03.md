# Gabarito — Capítulo 04.03: Closures e fábricas

Leia depois de tentar. Enunciados em [`../cap03.md`](../cap03.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — Preveja a saída

| # | Resultado | Por quê |
|---|---|---|
| 1 | `[20, 20, 20]` | uma célula, três funções; `i` acaba em 2 |
| 2 | `[0, 1, 2]` | **chamado dentro do laço** — ver abaixo |
| 3 | `99` | ver abaixo |
| 4 | `10` | `x = 20` criou uma local; a externa não mudou |
| 5 | `20` | `nonlocal` alcançou a externa |
| 6 | `[0, 1, 2]` | `partial` amarra o **valor** no momento da criação |

**O item 2 é a prova do mecanismo.** O mesmo lambda, a mesma célula — e o resultado é `[0,1,2]`. A diferença é **quando** a função é chamada: dentro do laço, `i` ainda vale o da iteração. Isso mostra que o problema não é "o lambda captura errado"; é que a leitura acontece tarde.

**O item 3 é o mais importante, e é a demonstração mais limpa do capítulo.** `g` foi criada com `n` valendo 1; depois `n = 99`; `g()` devolve **99**. A closure não fotografou o valor na criação — ela lê a célula na chamada. Se você respondeu `1`, seu modelo mental é "a closure copia", e é exatamente o modelo que produz surpresa no item 1.

**Os itens 4 e 5, lado a lado**, são o `nonlocal` em uma linha: sem ele, a atribuição cria uma variável nova e a externa fica intacta (`10`); com ele, alcança a externa (`20`).

## A2 — Precisa de `nonlocal`?

| # | Operação | Precisa? | Resultado sem |
|---|---|---|---|
| 1 | `return contador` | **não** | `5` |
| 2 | `contador += 1` | **sim** | `UnboundLocalError` |
| 3 | `lista.append(1)` | **não** | `[1]` — funcionou |
| 4 | `lista = [1]` | **sim** (se quiser afetar a externa) | externa continua `[9]` |
| 5 | `d["k"] = 1` | **não** | `{'k': 1}` — funcionou |
| 6 | `return contador + 1` | **não** | `6` |

**A pergunta que fecha — por que 3 e 4 são opostos.** A distinção não é sobre listas: é sobre **mutar** contra **reatribuir**.

- `lista.append(1)` **muta o objeto** que a variável referencia. A variável não muda de alvo, então não há atribuição, então não há necessidade de declaração.
- `lista = [1]` **reatribui a variável** a um objeto novo. É uma atribuição — e qualquer atribuição torna o nome local à função inteira.

**A regra completa em uma frase: `nonlocal` é sobre a variável, não sobre o objeto.** Mutar o objeto (`append`, `d[k] = v`, `obj.attr = x`) nunca exige; reatribuir a variável (`=`, `+=`, `-=`) sempre exige.

É o mesmo aliasing do 01.13, e explica por que `+=` numa lista é ambíguo: `lista += [1]` muta **e** reatribui, e funciona sem `nonlocal` por acidente da implementação de listas — motivo suficiente para evitá-lo em closure.

## A3 — O que a célula guarda

| # | `co_freevars` | `cell_contents` |
|---|---|---|
| 1 | `('a', 'b')` | `1` e `2` |
| 2 | `()` | `__closure__` é `None` |
| 3 | `('lst',)` | **reflete a mutação**: `[1, 2, 3]` |
| 4 | iguais | valores diferentes — células diferentes |
| 5 | `('n',)` | muda a cada chamada |

**O item 2 é uma checagem útil:** uma função sem variáveis livres tem `__closure__ is None`. Não é uma tupla vazia — é `None`. É como se detecta programaticamente se uma função é closure.

**O item 3 é o que mais surpreende.** A célula guarda a **referência** à lista, não uma cópia. Criar a closure e depois fazer `L.append(3)` faz a closure ver `[1,2,3]`. É coerente com tudo o que o capítulo diz — a closure guarda a variável, e a variável aponta para um objeto mutável.

**A consequência prática:** capturar um mutável numa closure e modificá-lo depois é uma fonte de bug difícil de rastrear, porque o efeito aparece longe da causa. Se o valor precisa ser congelado, copie na criação: `def inner(lst=list(lst))` ou `copia = list(lst)` antes do `def`.

## A4 — Closure ou classe?

| # | Escolha | Por quê |
|---|---|---|
| 1 | **closure** | uma operação, estado mínimo |
| 2 | **classe** | três operações sobre o mesmo estado |
| 3 | **closure** (ou `partial`) | função especializada, sem estado mutável |
| 4 | **classe** | ciclo de vida — e um *context manager* (04.20) |
| 5 | **closure** | é literalmente o caso do `itemgetter` |
| 6 | **depende** | ver abaixo |

**O item 6 é o interessante.** Um acumulador que soma e devolve a média no fim tem **duas** operações — o que sugere classe. Mas se a leitura acontece uma vez só, no fim, uma closure que devolve o par `(somar, media)` resolve sem cerimônia.

**O critério afiado:** não é o número de operações, é se elas precisam ser chamadas **em ordem arbitrária e repetidamente**. Duas operações com um fluxo fixo (acumula muitas vezes, lê uma) cabem numa closure. Duas operações intercaladas livremente pedem um objeto.

## AP1 — As fábricas

```python
def entre(minimo, maximo):
    def validar(valor):
        return minimo <= valor <= maximo
    validar.__name__ = f"entre({minimo}, {maximo})"
    return validar


def tamanho_maximo(n):
    def validar(valor):
        return len(valor) <= n
    validar.__name__ = f"tamanho_maximo({n})"
    return validar


def um_de(*opcoes):
    def validar(valor):
        return valor in opcoes
    validar.__name__ = f"um_de{opcoes}"
    return validar


def validar(valor, *regras):
    return [r.__name__ for r in regras if not r(valor)]
```

**O item 2 revela algo que o 04.02 preparou:** para a mensagem dizer *qual* regra falhou, a função interna precisa de nome — e `def validar(valor)` dentro de todas as três daria o **mesmo** nome. A solução é reescrever `__name__` na fábrica, incluindo os argumentos capturados. É possível porque funções aceitam atributos (04.01).

**3 e 4 — onde `partial` é suficiente.** Em `tamanho_maximo`: `partial(lambda n, v: len(v) <= n, n)` faz o mesmo. Em `entre`, também. **`partial` não serve em `um_de`**, porque `*opcoes` precisa ser empacotado, e porque ali há a lógica extra de montar o nome.

A regra: **`partial` é suficiente quando a fábrica só amarra argumentos.** Se há qualquer lógica na criação — validar os limites, pré-calcular, nomear —, a fábrica se justifica.

## AP2 — Os filtros da Aurora

A implementação está na §9 do capítulo. As respostas que importam:

**1.** Dois filtros novos: duas funções novas, **zero** alterações em `filtrar`.

**2.** A montagem por configuração é onde a arquitetura se paga:

```python
CONSTRUTORES = {
    "preco_minimo": preco_minimo,
    "categoria": da_categoria,
    "ativos": lambda _: apenas_ativos(),
}

def montar(config):
    return [CONSTRUTORES[chave](valor) for chave, valor in config.items()]

filtros = montar({"preco_minimo": 10000, "categoria": "audio"})
filtrar(produtos, *filtros)
```

**3. A comparação honesta:** a versão com `if` tem ~8 linhas e é lida por qualquer pessoa. A versão com fábricas tem ~20 e exige entender closures. Para o sétimo filtro: `if` cresce em dois lugares (parâmetro e bloco); fábrica cresce em um (uma função nova).

**4. A resposta certa depende do seu caso, e é isso que o exercício ensina.** Se os filtros vêm de um formulário com três caixas fixas, a versão com `if` é melhor — mais curta, mais direta, e o programa **sabe** quais filtros existem. Se vêm de uma configuração que o usuário edita, ou de uma API que aceita filtros arbitrários, a versão com fábricas é a única que não exige alterar código a cada pedido novo.

**Escolher a arquitetura flexível para um problema fixo é pagar complexidade por uma flexibilidade que ninguém vai usar.** É a mesma conclusão do pipeline no 04.02/D1, e vai reaparecer no 04.11.

## AP3 — O contador completo

**Com dicionário de funções:**

```python
def contador(inicio=0):
    n = inicio
    def incrementar(passo=1):
        nonlocal n
        n += passo
        return n
    def ler(): return n
    def zerar():
        nonlocal n
        n = 0
    def definir(valor):
        nonlocal n
        n = valor
    return {"inc": incrementar, "ler": ler, "zerar": zerar, "definir": definir}

c = contador()
c["inc"](); c["ler"]()      # 1
```

**Com classe:**

```python
class Contador:
    def __init__(self, inicio=0):
        self.n = inicio
    def incrementar(self, passo=1):
        self.n += passo
        return self.n
    def ler(self): return self.n
    def zerar(self): self.n = 0
    def definir(self, valor): self.n = valor

c = Contador()
c.incrementar(); c.ler()    # 1
```

**3 e 4 — o ponto exato em que a closure deixou de servir.** Foi na **segunda** operação. Com uma, a closure é mais curta e clara. Com quatro:

- a chamada vira `c["inc"]()` em vez de `c.incrementar()` — pior de ler e sem verificação: `c["incr"]()` dá `KeyError` em tempo de execução, enquanto `c.incr()` dá `AttributeError` com uma mensagem que sugere o nome certo;
- cada função precisa repetir `nonlocal n`;
- não há como imprimir o contador de forma útil, nem compará-lo com outro (04.12);
- o dicionário não documenta nada — não há docstring de classe nem de método visível.

**O que o exercício quer que você conclua:** o dicionário de funções **é** um objeto, montado à mão, sem as facilidades que a linguagem já oferece. Quando você se pega construindo um, a linguagem está pedindo uma classe — e o 04.07 dá o vocabulário para aceitá-la sem culpa.

## D1 — O memoizador

```python
import functools

def memoizar(funcao, limite=None):
    cache = {}
    acertos = erros = 0

    @functools.wraps(funcao)
    def envolvida(*args):
        nonlocal acertos, erros
        if args in cache:
            acertos += 1
            return cache[args]
        erros += 1
        resultado = funcao(*args)
        if limite and len(cache) >= limite:
            cache.pop(next(iter(cache)))       # o mais antigo (dict preserva ordem)
        cache[args] = resultado
        return resultado

    envolvida.estatisticas = lambda: (acertos, erros)
    return envolvida
```

**A medição:**

```
fib(30) sem cache: 316.4 ms · com cache: 0.0702 ms · 4507x
estatísticas (acertos, erros): (28, 31)
```

**Quatro mil e quinhentas vezes.** E note as estatísticas: 31 cálculos reais para `fib(30)`, contra os 2,7 milhões de chamadas da versão ingênua. O ganho não é o cache ser rápido — é a recursão deixar de recalcular a mesma subárvore.

**(b) e o A2 aplicado:** `cache` é **mutado** (`cache[args] = ...`), então **não** precisa de `nonlocal`. `acertos` e `erros` são **reatribuídos** (`+= 1`), então precisam. Quem declarou `nonlocal cache` não errou o resultado, mas não entendeu a regra.

**(c) — como expor estatísticas de dentro de uma closure.** Não há como; variáveis livres não são acessíveis de fora por nome. A saída é **anexar um atributo** à função devolvida (04.01). É exatamente o que `functools.lru_cache` faz com `cache_info()`.

**As duas perguntas do fecho.**

**(1) Por que hasháveis.** O cache é um dicionário, e chaves de dicionário precisam ser hasháveis. `args` é uma tupla — hasheável **se** todos os elementos forem. Com uma lista dentro:

```
TypeError: unhashable type: 'list'
```

A mensagem é clara, e o erro acontece na primeira chamada. É um limite honesto: memoizar funções que recebem coleções mutáveis exige converter (`tuple(lista)`) e aceitar o custo de copiar.

**(2) Quando escrever o seu.** Quase nunca. `functools.lru_cache` faz tudo isto, é implementado em C, trata `**kwargs`, é seguro entre threads e vem com `cache_info()` e `cache_clear()`. Escrever o seu se justifica em três casos: a chave precisa ser calculada de forma diferente (só um dos argumentos); a expiração é por **tempo**, não por tamanho; ou o cache precisa ser compartilhado ou persistido.

**E a razão de o exercício existir mesmo assim:** depois de escrever este, `@lru_cache` deixa de ser uma linha mágica. Você sabe que há um dicionário numa closure, contadores com `nonlocal`, e um atributo anexado à função — que é precisamente o que o próximo capítulo formaliza.

---

## Erros comuns

1. **Achar que a closure copia o valor.** O A1.3 devolve 99.
2. **Confundir mutar com reatribuir.** `append` não precisa de `nonlocal`; `=` precisa.
3. **`nonlocal` num dicionário mutado.** Desnecessário — e revela o mal-entendido.
4. **Capturar mutável e modificá-lo depois.** A closure vê a mudança.
5. **Esperar `__closure__ == ()`** para função sem variáveis livres. É `None`.
6. **Dicionário de funções com quatro entradas.** Já era uma classe.
7. **Escolher arquitetura flexível para problema fixo.**
8. **Memoizar função que recebe lista.** `unhashable type: 'list'`.
