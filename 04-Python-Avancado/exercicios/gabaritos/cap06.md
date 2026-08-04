# Gabarito — Capítulo 04.06: Geradores e `yield`

Leia depois de tentar. Enunciados em [`../cap06.md`](../cap06.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — Preveja a saída

| # | Impresso | Devolvido |
|---|---|---|
| 1 | **nada** | um objeto `generator` |
| 2 | `A` | `1` |
| 3 | `A`, `B`, `C` | `[1, 2]` |
| 4 | — | `[1]` |
| 5 | — | `[0, 1]` |
| 6 | — | `[2, 4]` e depois `[]` |

**O item 1 é a armadilha central.** `x = g1()` não imprime `A` — não imprime nada. A função não começou a rodar. É o mecanismo por trás da validação tardia do AP2.

**O item 3 mostra a ordem completa:** `list()` consome tudo, então os três `print` saem **antes** de o valor `[1, 2]` aparecer. O `C` sai porque a função continua depois do último `yield` até terminar.

**O item 4:** `return "ignorado"` encerra o gerador. O valor **não** vai para a lista — a saída é `[1]`. O `yield 2` depois do `return` é inalcançável.

**O item 5:** `return` dentro do laço encerra na segunda iteração, depois de já ter cedido o `1`. Resultado `[0, 1]`.

**Sobre o valor do `return`, que o A4.5 retoma:** ele não some. Vira o argumento do `StopIteration`:

```python
g = com_valor(); next(g)
next(g)     # StopIteration, e e.value == 99
```

O `for` e o `list()` capturam o `StopIteration` e **descartam** o `.value`. Ele só é útil em `yield from`, que o repassa — mecanismo que sustenta as corrotinas.

## A2 — Lista ou gerador?

| # | Escolha | Por quê |
|---|---|---|
| 1 | **lista** | 12 itens, três passadas — gerador esgotaria |
| 2 | **gerador** | 20 GB não cabem |
| 3 | **gerador** | consome 10 de milhões; a preguiça evita o resto |
| 4 | **`set`** | ver abaixo |
| 5 | **depende** | ver abaixo |
| 6 | **gerador** | limite só conhecido em execução |

**O item 4 é uma pegadinha, e a resposta não é nenhuma das duas.** "Testado com `in` muitas vezes" pede um **conjunto**: `in` num `set` é O(1); numa lista, O(n); e num gerador, O(n) **e destrutivo** — o primeiro teste consome o gerador, e todos os seguintes dão `False`. É o esgotamento produzindo uma resposta errada em vez de vazia.

**O item 5 depende de quem consome.** Se o JSON é montado de uma vez (`json.dumps(list(...))`), materializar é inevitável. Se a resposta é enviada em streaming, o gerador permite começar a responder antes de a consulta terminar — que é como APIs devolvem resultados grandes.

**O item 6 é o caso em que gerador é a única saída razoável:** o limite vem em execução, então não há como saber quantos itens produzir. Um gerador infinito com `takewhile` resolve; uma lista exigiria adivinhar um teto.

## A3 — Converta

```python
def pares(n):
    for x in range(n):
        if x % 2 == 0:
            yield x


def linhas(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        yield from arquivo


def concatenar(a, b):
    yield from a
    yield from b


def primeiros(iteravel, n):
    for posicao, item in enumerate(iteravel):
        if posicao >= n:
            return
        yield item


def pares_texto(dicionario):
    for chave, valor in dicionario.items():
        yield "%s=%s" % (chave, valor)
```

**O que muda para quem chama — e são quatro coisas:**

1. **não dá para usar `len()`** nem índice;
2. **só serve uma vez** — a segunda passada vem vazia;
3. **o resultado só existe quando consumido** — um `print` do retorno mostra `<generator object ...>`;
4. **exceções aparecem no consumo**, não na chamada.

**O item 2 tem uma sutileza que vale registrar.** A versão com `with` **é melhor** que `return open(caminho).readlines()`, porque fecha o arquivo. Mas o `with` só fecha quando o gerador termina ou é coletado — se alguém abandonar o gerador no meio, o arquivo fica aberto até a coleta de lixo. É a caixa-preta 2 do capítulo.

## A4 — Ache o erro

| # | Erro | Sintoma real |
|---|---|---|
| 1 | validação na primeira linha | erro só no primeiro `next()` |
| 2 | `len(g)` | `TypeError: object of type 'generator' has no len()` |
| 3 | `list(infinito())` | trava até esgotar a memória |
| 4 | sem `with` | arquivo aberto indefinidamente |
| 5 | `return 99` esperando chegar ao `for` | vira `StopIteration.value`, descartado |
| 6 | mesmo gerador para duas funções | a segunda recebe vazio |

A saída do item 1:

```
gen = val("/nao/existe")   -> criou sem erro, tipo: generator
list(gen)                  -> FileNotFoundError: /nao/existe
```

**O `try/except` em volta da chamada não pega nada** — e é isso que torna o erro caro: quem escreveu o tratamento acha que está protegido.

## AP1 — O pipeline

Medido sobre 100 mil linhas, quatro etapas:

```
listas     resultado=42856857150 ·  431,0 ms · pico  24,24 MB
geradores  resultado=42856857150 ·  281,0 ms · pico   0,03 MB
```

**4. A conclusão que contraria a intuição: a versão com geradores foi mais RÁPIDA.**

O senso comum diz que geradores são mais lentos, porque cada valor custa uma retomada de quadro. E **é verdade**, isolando a iteração:

```
sum(lista)              8,8 ms
sum(x for x in lista)  38,4 ms      <- 4,4x mais lento
```

Mas num **pipeline**, a versão com listas paga algo que a com geradores não paga: **alocar quatro listas de 100 mil elementos**. Alocação e coleta de lixo custam mais que a retomada de quadro, e a conta se inverte.

E o cruzamento existe — medido com etapas puras, sem I/O:

```
1 etapa:  listas 17,8 ms · geradores 17,1 ms
2 etapas: listas 41,5 ms · geradores 27,0 ms   <- geradores ganham
4 etapas: listas 49,8 ms · geradores 51,3 ms   <- empatam
```

**A lição, e ela vale além deste exercício:** "geradores são mais lentos" e "geradores são mais rápidos" são ambos falsos como regra. O que existe é um cruzamento que depende do número de etapas, do tamanho dos dados e do custo de cada transformação. **Só a medição decide** — e é o mesmo que o 03.14 concluiu sobre índices.

## AP2 — A validação

**1 e 2.** O `try/except` em volta da chamada não pega:

```python
try:
    g = ler("inexistente.txt")     # nada acontece aqui
except FileNotFoundError:
    print("não pega")               # nunca executa
list(g)                             # o erro estoura AQUI
```

**3. A correção — duas funções:**

```python
def ler(caminho):
    """Função NORMAL: valida e devolve o gerador."""
    if not os.path.exists(caminho):
        raise FileNotFoundError(caminho)     # dispara na CHAMADA
    return _ler_linhas(caminho)


def _ler_linhas(caminho):
    """O gerador de verdade, privado."""
    with open(caminho, encoding="utf-8") as arquivo:
        yield from arquivo
```

`ler` não tem `yield`, então é uma função comum: o corpo roda na chamada, e o `raise` acontece onde se espera. Ela devolve o gerador de `_ler_linhas`, e quem chama não percebe a diferença.

**4.** Agora o `try/except` funciona, porque o erro acontece dentro da chamada.

**5. Por que a linguagem foi projetada assim.** Executar até o primeiro `yield` na chamada parece resolver — e criaria um problema pior: um gerador que abre arquivo, conecta ou reserva recurso passaria a fazê-lo **no momento da criação**, mesmo que ninguém o consuma.

Isso quebraria o caso mais valioso: `g = ler_arquivo_gigante(caminho)` seria caro mesmo se você desistisse. **Preguiça total é mais simples de raciocinar que preguiça parcial**, e a linguagem escolheu a regra sem exceção: nada roda até alguém pedir.

O preço é a armadilha da validação — e o padrão de duas funções é o preço pago de volta.

## AP3 — Infinitos

```python
def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def primos():
    n = 2
    while True:
        if all(n % d for d in range(2, int(n ** 0.5) + 1)):
            yield n
        n += 1
```

```
fib 10:      [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
primos 8:    [2, 3, 5, 7, 11, 13, 17, 19]
```

**2. `islice` contra `takewhile`** — e a diferença é o critério de parada:

```
islice(fib(), 10)                      -> os 10 PRIMEIROS
takewhile(lambda x: x < 100, fib())    -> [0,1,1,2,3,5,8,13,21,34,55,89]
```

`islice` para por **quantidade**; `takewhile` para por **condição**. Nos infinitos, `takewhile` é a escolha certa quando o critério é sobre o valor — e é perigoso se a condição puder voltar a ser verdadeira depois, porque ele para no **primeiro** falso e não retoma.

**3. A composição:**

```python
primos_de_fib = (x for x in fib() if eh_primo(x))
list(itertools.islice(primos_de_fib, 5))     # [2, 3, 5, 13, 89]
```

Dois infinitos compostos, e nada trava — porque `islice` limita o consumo. **É o argumento mais forte a favor de preguiça:** essa composição não tem versão materializada.

**4. `list(primos())` sem executar.** Ele nunca termina. O gerador produz primos indefinidamente e `list` os acumula até a memória acabar — o processo é morto pelo sistema operacional, ou trava a máquina com *swap* antes disso.

**Por que executar seria má ideia:** não é um erro rápido, é uma degradação lenta. Num notebook, o sistema fica sem resposta antes de o Python falhar. **A regra: um gerador infinito só se consome com limite** — `islice`, `takewhile`, `zip` com algo finito, ou `break`.

## D1 — O leitor de CSV

```python
class LeitorCSV:
    def __init__(self, caminho, tamanho=100, pular_invalidas=False):
        self.caminho = caminho
        self.tamanho = tamanho
        self.pular_invalidas = pular_invalidas
        self.descartadas = 0
        self.cabecalho = self._ler_cabecalho()

    def _ler_cabecalho(self):
        with open(self.caminho, encoding="utf-8") as arquivo:
            return next(arquivo).rstrip("\n").split(",")

    def __iter__(self):
        self.descartadas = 0                      # zera a cada passada
        esperado = len(self.cabecalho)
        bloco = []
        with open(self.caminho, encoding="utf-8") as arquivo:
            next(arquivo)                          # pula o cabeçalho
            for linha in arquivo:
                campos = linha.rstrip("\n").split(",")
                if len(campos) != esperado:
                    if self.pular_invalidas:
                        self.descartadas += 1
                        continue
                    raise ValueError(
                        "linha com %d campos, esperado %d: %r"
                        % (len(campos), esperado, linha[:60])
                    )
                bloco.append(campos)
                if len(bloco) == self.tamanho:
                    yield bloco
                    bloco = []
            if bloco:
                yield bloco                        # (a) o último, menor
```

**(b)** O cabeçalho é lido no `__init__`, por uma função **normal** — que é o padrão do AP2 aplicado: a validação (arquivo existe? tem cabeçalho?) acontece na construção, não no primeiro `next()`.

**(c)** `self.descartadas` é um atributo do objeto, zerado a cada `__iter__`. É a solução da Dica 2 — a mesma do 04.03/D1 e do 04.04, porque geradores, como closures, não expõem variáveis internas.

**A comparação honesta — e o caso em que as duas classes ganham.**

| | Duas classes (04.05) | Gerador (04.06) |
|---|---|---|
| Linhas | ~35 | ~20 |
| Legibilidade | o `__next__` explicita o estado | o `for` esconde o estado |
| Estado inspecionável | `iterador._posicao` | **não** |
| Dois iteradores | independentes | independentes |
| Pausar e retomar externamente | possível | possível |

**O caso concreto em que a versão com classes é melhor: quando você precisa inspecionar ou manipular a posição.**

Um leitor com retomada — "continue do bloco 47, onde a execução anterior falhou" — precisa de `iterador.posicao = 47`. Com gerador, o estado está no quadro congelado, inacessível de fora. Você teria que reprojetar a interface (aceitar `inicio=47` e pular no laço), o que funciona e é **outra** solução, não a mesma.

Casos reais em que isso pesa: processamento com *checkpoint*, leitores que reportam progresso ("bloco 47 de 200"), e depuração de pipeline — onde parar num ponto e olhar o estado é exatamente o que se quer.

**A conclusão que o desafio pede:** geradores ganham em concisão quase sempre, e perdem quando o **estado da iteração** é parte da interface. Reduzir 35 linhas a 20 é bom; perder acesso à posição é um custo — e escolher sem saber que ele existe é o que o exercício quer evitar.

---

## Erros comuns

1. **Esperar `print` na chamada da função geradora.** Nada roda até o `next()`.
2. **Achar que `return valor` chega ao `for`.** Vira `StopIteration.value`, descartado.
3. **Gerador para coleção testada com `in` muitas vezes.** Esgota e passa a responder `False`.
4. **`try/except` em volta da chamada.** O erro só aparece no consumo.
5. **`list()` num infinito.** Não é erro rápido — é degradação até o sistema travar.
6. **Envolver lista existente em expressão geradora.** 4,4x mais lento, sem economia.
7. **Supor que geradores são sempre mais lentos.** Num pipeline de 2 etapas, foram 35% mais rápidos.
8. **Escolher gerador sem notar que perde acesso à posição.**
