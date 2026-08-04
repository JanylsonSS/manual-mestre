# Gabarito — Capítulo 04.04: Decoradores

Leia depois de tentar. Enunciados em [`../cap04.md`](../cap04.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — Preveja a saída

| # | Resultado |
|---|---|
| 1 | `None` |
| 2 | `TypeError: 'NoneType' object is not callable` |
| 3 | `(rodou)` aparece **na importação**, antes de qualquer chamada |
| 4 | **1 vez** — três chamadas, uma decoração |
| 5 | `__name__` e `__doc__` **sobrevivem** aos dois níveis |
| 6 | `<x>V</x>` |

**O item 1 é o erro mais cruel do capítulo.** `def dentro(*a): f(*a)` chama a função e **descarta** o resultado. Não há erro, não há aviso: `soma(1, 2)` passa a devolver `None`. Toda função decorada assim vira um buraco silencioso, e o sintoma aparece longe da causa.

**O item 2 é o mesmo esquecimento um nível acima**, e é muito mais gentil: o decorador devolve `None`, o nome da função vira `None`, e a primeira chamada estoura com uma mensagem clara. **Falhar alto é melhor que devolver `None`** — é a mesma lição do 03.11.

**O item 4 é o que mais organiza o modelo mental.** O decorador rodou **uma** vez, para três chamadas. Ele não é executado a cada invocação; ele já foi executado, na importação.

**O item 5 confirma que `wraps` é transitivo.** Cada nível copia os metadados do que envolve, então uma pilha de decoradores todos com `wraps` preserva o nome original até o topo. Um único nível sem `wraps` no meio quebra a cadeia dali para cima.

## A2 — Com ou sem parênteses?

| # | Correto? | Por quê |
|---|---|---|
| 1 | **não** | `wraps` é fábrica: exige `@functools.wraps(f)` |
| 2 | **sim** | `lru_cache` aceita as duas formas |
| 3 | **sim** | forma com argumento |
| 4 | **não** | `meu_decorador()` chamado sem a função → `TypeError` |
| 5 | **não** | `repetir` é fábrica: precisa de `@repetir(3)` |
| 6 | **sim** | `app.rota(...)` devolve o decorador |

A mensagem do item 4:

```
TypeError: erro_sem_parenteses() missing 1 required positional argument: 'f'
```

**O item 2 é a exceção que confunde.** `functools.lru_cache` aceita **as duas formas** porque foi escrito para isso (desde o Python 3.8) — é o truque do AP2.3. A maioria dos decoradores não aceita, e supor que aceitam produz o erro do item 4 ou, pior, um decorador que recebe a função onde esperava um argumento.

**A regra:** se o decorador tem argumentos, `@dec(...)`. Se não tem, `@dec`. Aceitar as duas exige código extra e deliberado.

## A3 — Ache o erro

| # | Erro | Consequência |
|---|---|---|
| 1 | sem `wraps` | introspecção e registro por nome quebram |
| 2 | não devolve `envolvida` | `'NoneType' object is not callable` |
| 3 | `envolvida` não devolve | a função passa a devolver `None`, **em silêncio** |
| 4 | `envolvida(self, *args)` | só funciona em métodos; `*args` já cobre `self` |
| 5 | abre arquivo no corpo | acontece na **importação**, para toda função decorada |
| 6 | `@cache` acima de `@autenticar` | **falha de segurança** |

**O item 4 merece explicação.** Escrever `def envolvida(self, *args, **kwargs)` num decorador genérico o amarra a métodos. Não é necessário: `self` chega como o primeiro posicional e `*args` o absorve naturalmente. Um decorador escrito com `*args, **kwargs` funciona em funções **e** métodos sem alteração.

**O item 6 é o único que não é um bug de programação, é de arquitetura.** Com `@cache` por fora, a segunda requisição ao mesmo recurso devolve o resultado cacheado **sem passar pela autenticação** — qualquer pessoa recebe o dado de quem pediu antes. A ordem correta é autenticar por fora, cachear por dentro.

## A4 — A ordem

| # | Resultado | Mais interno |
|---|---|---|
| 1 | `@maiuscula` sobre `@exclamar` → `"OI!"` | `exclamar` |
| 2 | `@exclamar` sobre `@maiuscula` → `"OI!"` | `maiuscula` |
| 3 | `@cronometrar` sobre `@cache` | `cache` — **mede o acerto de cache** |
| 4 | `@cache` sobre `@cronometrar` | `cronometrar` — **não mede o acerto** |
| 5 | o `__name__` **original** chega ao topo | — |

**Os itens 1 e 2 dão o mesmo resultado por acaso** — maiúscula e exclamação comutam. É uma armadilha proposital: a ordem sempre importa conceitualmente, mas nem sempre o resultado difere, e testar com um caso que comuta não prova nada.

**Os itens 3 e 4 são a diferença que importa.** Com `@cronometrar` por fora, o tempo medido inclui os acertos de cache — que são quase zero — e a média desaba, escondendo o custo real da função. Com `@cache` por fora, o cronômetro só roda quando há cálculo de verdade, e a média reflete o custo real.

**Nenhum dos dois é universalmente certo:** o primeiro responde "quanto o chamador espera?", o segundo, "quanto custa calcular?". São perguntas diferentes, e escolher a ordem é escolher a pergunta.

## AP1 — Os três clássicos

```python
def registrar(funcao):
    @functools.wraps(funcao)
    def envolvida(*args, **kwargs):
        print(f"-> {funcao.__name__}({args}, {kwargs})")
        resultado = funcao(*args, **kwargs)
        print(f"<- {funcao.__name__} = {resultado!r}")
        return resultado
    return envolvida


def cronometrar(funcao):
    @functools.wraps(funcao)
    def envolvida(*args, **kwargs):
        inicio = time.perf_counter()
        try:
            return funcao(*args, **kwargs)
        finally:
            print(f"   {funcao.__name__}: {(time.perf_counter()-inicio)*1000:.2f} ms")
    return envolvida


def retentar(funcao):
    @functools.wraps(funcao)
    def envolvida(*args, **kwargs):
        ultima = None
        for tentativa in range(1, 4):
            try:
                return funcao(*args, **kwargs)
            except Exception as erro:
                ultima = erro
                print(f"   tentativa {tentativa} falhou: {erro}")
        raise ultima          # preserva a exceção ORIGINAL
    return envolvida
```

**O `raise ultima` é a decisão que importa.** Levantar uma exceção nova (`RuntimeError("falhou 3 vezes")`) descartaria a informação sobre **por que** falhou — timeout? permissão? dado inválido? Quem trata a exceção precisa dessa distinção, e um decorador que a apaga rouba do chamador a capacidade de reagir corretamente.

**A ordem de empilhamento, e a resposta pedida:**

```python
@registrar
@cronometrar
@retentar
def instavel(): ...
```

De fora para dentro: `registrar` vê a chamada **e** o resultado final (depois das retentativas); `cronometrar` mede o tempo total, incluindo as falhas; `retentar` fica colado na função. Se `retentar` ficasse por fora, o log e o cronômetro rodariam **três vezes** — o que é uma escolha defensável (você vê cada tentativa) e uma pergunta diferente.

## AP2 — Com argumentos

```python
def retentar(vezes=3, espera=0.1):
    def decorador(funcao):
        @functools.wraps(funcao)
        def envolvida(*args, **kwargs):
            for tentativa in range(1, vezes + 1):
                try:
                    return funcao(*args, **kwargs)
                except Exception as erro:
                    if tentativa == vezes:
                        raise
                    time.sleep(espera)
        return envolvida
    return decorador
```

**O `raise` sem argumento** relança a exceção corrente preservando o traceback — melhor que `raise erro`, que reinicia o rastro.

**3. O decorador que funciona com e sem parênteses.** O truque é receber a função como **primeiro parâmetro opcional** e os argumentos como keyword-only:

```python
def cronometrar(funcao=None, *, limite_ms=None):
    def decorador(f):
        @functools.wraps(f)
        def envolvida(*a, **k):
            inicio = time.perf_counter()
            try:
                return f(*a, **k)
            finally:
                ms = (time.perf_counter() - inicio) * 1000
                if limite_ms is None or ms > limite_ms:
                    print(f"    {f.__name__}: {ms:.2f} ms")
        return envolvida
    return decorador if funcao is None else decorador(funcao)
```

```
sem parênteses:        a: 1.09 ms
com limite alto:       (nada, como esperado)
com parênteses vazios: c: 1.02 ms
```

**Como a detecção funciona:** `@cronometrar` (sem parênteses) chama `cronometrar(a_funcao)` — então `funcao` não é `None`, e devolvemos o resultado já decorado. `@cronometrar(limite_ms=100)` chama `cronometrar(limite_ms=100)` — `funcao` é `None`, e devolvemos o decorador para o `@` aplicar em seguida.

**O `*` na assinatura não é decoração:** ele impede `@cronometrar(100)`, que passaria `100` como `funcao` e produziria um erro incompreensível. É o keyword-only do 04.01 evitando um erro que só apareceria em tempo de execução.

**É assim que `functools.lru_cache` aceita as duas formas** (A2.2) — e vale saber que a maioria dos decoradores não faz isso, porque o código extra raramente compensa.

## AP3 — O que `wraps` salva

| Perda | Sem `wraps` | Com `wraps` |
|---|---|---|
| `__name__` | `envolvida` | `calcular2` |
| `__doc__` | `None` | a docstring real |
| `inspect.signature` | `(*a, **k)` | `(x, y)` |
| `repr()` | `<function sem.<locals>.envolvida at 0x…>` | `<function calcular2 at 0x…>` |

**A que quebra um programa de verdade** é o `__name__`, quando alguém o usa como chave:

```python
REGISTRO = {}
def registrar(f):
    REGISTRO[f.__name__] = f
    return f

@registrar
@sem_wraps
def rota_a(): pass

@registrar
@com_wraps
def rota_b(): pass

list(REGISTRO)      # ['envolvida', 'rota_b']
```

**A rota foi registrada com o nome errado.** Com duas rotas nessa situação, a segunda **sobrescreve** a primeira — as duas se chamam `envolvida` — e uma delas desaparece do roteador sem nenhum erro. É exatamente o tipo de falha que leva horas para diagnosticar, porque o sintoma ("a rota /x não existe") não aponta para a causa.

E a mesma coisa vale para `inspect.signature` num framework de injeção: FastAPI lê a assinatura para saber o que passar, encontra `(*args, **kwargs)`, e não consegue injetar nada.

**O aviso do enunciado, confirmado.** O traceback é **idêntico**:

```
SEM wraps: ['<module>', 'envolvida', 'quebra_a']
COM wraps: ['<module>', 'envolvida', 'quebra_b']
```

Os dois mostram três frames, e os dois mostram `envolvida` no meio. **`wraps` copia atributos da função (`__name__`, `__doc__`); o traceback lê o nome do objeto de código (`__code__.co_name`)**, que é imutável e continua sendo `envolvida`. Copiar `__code__` faria a função decorada **ser** a original, o que anularia a decoração.

A conclusão: use `wraps` sempre — mas pelos motivos certos. Repetir "melhora o traceback" é propagar uma crença que um teste de trinta segundos desmente.

## D1 — O registro de rotas

```python
class Aplicacao:
    def __init__(self):
        self.rotas = {}
        self.antes = []

    def rota(self, caminho, metodo="GET"):
        def decorador(funcao):
            self.rotas[(metodo, caminho)] = funcao
            return funcao                       # INALTERADA
        return decorador

    def antes_de_tudo(self, funcao):
        self.antes.append(funcao)
        return funcao

    def despachar(self, metodo, caminho, *args, **kwargs):
        chave = (metodo, caminho)
        if chave not in self.rotas:
            disponiveis = ", ".join(f"{m} {c}" for m, c in sorted(self.rotas))
            raise KeyError(
                f"rota {metodo} {caminho} não registrada. Existem: {disponiveis}"
            )
        for gancho in self.antes:
            gancho(metodo, caminho)
        return self.rotas[chave](*args, **kwargs)
```

```
GET  /usuarios -> ['ana', 'bruno']
POST /usuarios -> criado carla
a função continua normal? ['ana', 'bruno'] · __name__: listar
rota inexistente -> 'rota GET /x não registrada. Existem: GET /usuarios, POST /usuarios'
```

**(d) A chave é uma tupla `(metodo, caminho)`** — a regra que não cabe numa "coluna" só, como o `UNIQUE(pedido_id, produto_id)` do 03.13.

**(c) A mensagem lista as rotas registradas**, gerada do próprio dicionário — o mesmo padrão do despacho do 04.02, e pelo mesmo motivo: a lista nunca fica desatualizada.

**A pergunta que fecha — por que devolver a função inalterada.**

Porque o **efeito desejado é o registro**, não a modificação. `@app.rota` não precisa fazer nada quando a função é chamada; precisa fazer algo quando ela é **definida**. Devolver a original tem três vantagens concretas:

- **`listar()` continua funcionando** fora do roteador — dá para chamá-la e testá-la diretamente, sem passar por `despachar`;
- **`__name__` é preservado de graça**, sem precisar de `wraps` (não há envelope para mentir);
- **custo zero por chamada** — nenhuma camada extra.

**O que mudaria se envolvesse.** Você ganharia a possibilidade de fazer coisas por requisição — validar entrada, medir tempo, tratar exceção e devolver um erro formatado. É por isso que frameworks reais **fazem** envolver: o `@app.get` do FastAPI faz muito mais que registrar.

O custo é o esperado: `listar()` chamada diretamente passaria pela camada extra (que pode nem fazer sentido fora de uma requisição), e `wraps` viraria obrigatório.

**O critério, e ele resume o capítulo:** envolva quando precisar agir **a cada chamada**; devolva inalterada quando o efeito acontece **na definição**. Registro é definição. Log, cache e autenticação são chamada.

---

## Erros comuns

1. **Esquecer o `return` dentro de `envolvida`.** A função passa a devolver `None`, em silêncio.
2. **Esquecer de devolver `envolvida`.** `'NoneType' object is not callable`.
3. **Achar que o decorador roda a cada chamada.** Roda uma vez, na definição.
4. **`@dec()` num decorador sem argumentos.** `missing 1 required positional argument`.
5. **Levantar exceção nova no `@retentar`.** Apaga a causa real.
6. **Testar ordem de empilhamento com operações que comutam.** Não prova nada.
7. **`@cache` acima de `@autenticar`.** Falha de segurança.
8. **Repetir que `wraps` melhora o traceback.** Não melhora — melhora nome, doc, assinatura e registro.
9. **Envolver quando só era preciso registrar.**
