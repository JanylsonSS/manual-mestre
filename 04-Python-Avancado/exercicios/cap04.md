# Exercícios — Capítulo 04.04: Decoradores

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap04.md`](gabaritos/cap04.md).

## Aquecimento

### A1 — Preveja a saída `[Aquecimento · ~10 min]`

```python
# 1 — o decorador esqueceu o return DENTRO de `dentro`
def d1(f):
    def dentro(*a): f(*a)
    return dentro
@d1
def soma(a, b): return a + b
soma(1, 2)

# 2 — o decorador esqueceu de devolver `dentro`
def d2(f):
    def dentro(*a): return f(*a)
@d2
def x(): return 1
x()

# 3 — print no corpo do decorador
def d3(f):
    print("(rodou)")
    return f
@d3
def y(): return 1
# quando "(rodou)" aparece?

# 4 — contador global no decorador; a função é chamada 3 vezes
# quantas vezes o decorador rodou?

# 5 — dois @wraps empilhados: __name__ e __doc__ sobrevivem?

# 6 — @marcar("x") sobre uma função que devolve "V"
```

### A2 — Com ou sem parênteses? `[Aquecimento · ~10 min]`

Para cada uso, diga se está correto e por quê:

1. `@functools.wraps` (sem parênteses)
2. `@functools.lru_cache` (sem parênteses)
3. `@functools.lru_cache(maxsize=32)`
4. `@meu_decorador()` — onde `meu_decorador(f)` recebe a função
5. `@repetir` — onde `repetir(vezes)` é uma fábrica
6. `@app.rota("/x")`

### A3 — Ache o erro `[Aquecimento · ~10 min]`

1. Decorador sem `functools.wraps`.
2. Decorador que não devolve `envolvida`.
3. `envolvida` que não devolve o resultado.
4. `envolvida(self, *args)` num decorador genérico.
5. Decorador que abre um arquivo de log no próprio corpo.
6. `@cache` empilhado **acima** de `@autenticar`.

### A4 — A ordem `[Aquecimento · ~10 min]`

Para cada empilhamento, diga o resultado e qual decorador é o mais interno:

1. `@maiuscula` sobre `@exclamar` numa função que devolve `"oi"`
2. `@exclamar` sobre `@maiuscula` na mesma
3. `@cronometrar` sobre `@cache` — o tempo medido inclui o acerto de cache?
4. `@cache` sobre `@cronometrar` — e agora?
5. `@wraps`-ados três níveis: qual `__name__` chega ao topo?

## Aplicação

### AP1 — Os três clássicos `[Aplicação · ~20 min]`

Escreva, todos com `wraps`:

1. `@registrar` — imprime nome, argumentos e resultado.
2. `@cronometrar` — imprime o tempo, **inclusive** quando a função levanta exceção.
3. `@retentar` — tenta 3 vezes antes de desistir, com a exceção original preservada.

Teste os três numa função que falha nas duas primeiras chamadas e funciona na terceira. **A pergunta:** em que ordem você os empilharia, e por quê?

### AP2 — Com argumentos `[Aplicação · ~25 min]`

Converta os três do AP1 em versões parametrizadas: `@registrar(nivel="INFO")`, `@cronometrar(limite_ms=100)` (avisa só se estourar), `@retentar(vezes=3, espera=0.1)`.

1. Nomeie explicitamente os três níveis em cada um.
2. Faça `@retentar(vezes=3)` e `@retentar()` funcionarem.
3. **O desafio extra:** faça `@cronometrar` funcionar **com e sem** parênteses. Descubra como detectar os dois casos.

### AP3 — O que `wraps` salva `[Aplicação · ~20 min]`

**Tarefa.** Demonstre, com saída impressa, as **quatro** perdas de omitir `functools.wraps`:

1. `__name__`
2. `__doc__`
3. `inspect.signature`
4. `repr(funcao)`

Para cada uma: mostre o valor sem `wraps`, com `wraps`, e escreva uma frase sobre a consequência prática.

**E a parte que vale o exercício.** Uma dessas perdas quebra um programa de verdade; as outras três só o tornam desagradável. Descubra qual, construindo o caso: empilhe um decorador `@registrar` (que guarda a função num dicionário usando `f.__name__` como chave) **acima** de um decorador sem `wraps`, e olhe as chaves do dicionário.

**Um aviso, para você não perder tempo:** o traceback de uma exceção levantada **dentro** da função é idêntico com e sem `wraps`. Verifique isso — e explique por quê. A resposta diz algo sobre o que `wraps` copia e o que ele não consegue copiar.

## Desafio

### D1 — O registro de rotas `[Desafio · ~50 min]`

Construa um mini roteador:

```python
app = Aplicacao()

@app.rota("/usuarios", metodo="GET")
def listar(): return ["ana", "bruno"]

app.despachar("GET", "/usuarios")
```

- **(a)** o decorador **registra** e devolve a função **inalterada**;
- **(b)** `despachar` encontra e chama, repassando argumentos;
- **(c)** rota inexistente levanta erro **listando as registradas**;
- **(d)** o mesmo caminho com métodos diferentes convive;
- **(e)** um `@app.antes` cujas funções rodam antes de toda rota;
- **(f)** prove que `listar()` continua funcionando normalmente fora do roteador.

**A pergunta que fecha:** por que o decorador devolve a função inalterada em vez de um envelope? O que mudaria — para melhor e para pior — se ele envolvesse?

<details><summary>💡 Dica 1 (conceito)</summary>
A chave do dicionário precisa distinguir método e caminho: uma tupla `(metodo, caminho)` resolve (03.13 — a regra que não cabe numa coluna só).
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
`app.rota(...)` é um **método** que devolve um decorador — ou seja, os três níveis do §6.4, com o primeiro sendo um método que já tem acesso a `self`.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`class Aplicacao` com `self.rotas = {}` → `def rota(self, caminho, metodo="GET")` devolvendo `decorador(funcao)` que faz `self.rotas[(metodo, caminho)] = funcao; return funcao` → `despachar` com `KeyError` informativo.
</details>
