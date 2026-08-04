# Gabarito — Capítulo 04.05: Iteráveis e iteradores

Leia depois de tentar. Enunciados em [`../cap05.md`](../cap05.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — Esgota ou não?

| # | Objeto | `__next__` | Classificação |
|---|---|---|---|
| 1 | `[1,2,3]` | `False` | iterável |
| 2 | `{"a":1}` | `False` | iterável |
| 3 | `"abc"` | `False` | iterável |
| 4 | `range(3)` | `False` | iterável |
| 5 | `map(str,[1])` | **`True`** | **iterador — esgota** |
| 6 | `zip([1],[2])` | **`True`** | **iterador — esgota** |
| 7 | `enumerate([1])` | **`True`** | **iterador — esgota** |
| 8 | `{1,2}` | `False` | iterável |

**A pergunta que fecha.** `range` e `map` são os dois preguiçosos — nenhum materializa os valores. A diferença é que `range` **não guarda posição**: ele guarda início, fim e passo, e produz um iterador novo a cada `for`. `map` guarda a posição em si mesmo, e por isso só serve uma vez.

**Preguiça e esgotamento são independentes**, e essa é a frase a levar: preguiça é sobre *quando* os valores são produzidos; esgotamento é sobre *quantas vezes* o objeto serve.

## A2 — Preveja a saída

| # | Resultado |
|---|---|
| 1 | `[(1,3), (2,4)]` e depois `[]` |
| 2 | `2` e depois `0` |
| 3 | `[0,1,2]` e `[0,1,2]` |
| 4 | **`[3]`** |
| 5 | `2` e depois `0` |
| 6 | os 9 pares — funciona |

**O item 4 é o mais instrutivo do exercício.** O `for` consumiu o `1` e o `2`; o `break` saiu do laço **sem devolver nada ao iterador**. `list(it)` continua de onde parou: `[3]`.

Não é `[1,2,3]` (o iterador não reinicia) nem `[]` (ele não foi esgotado). É a demonstração mais direta de que **o iterador é uma posição**, e que sair do `for` não a altera.

Isso tem um uso real: consumir o cabeçalho de um arquivo com `next(f)` e depois `for linha in f` para o resto — o iterador lembra que a primeira linha já foi.

**O item 6 funciona** porque `lista` é iterável: cada `for` pede um iterador novo. Com um iterador no lugar da lista, o resultado seria muito diferente — é o AP1.4.

## A3 — O `for` à mão

```python
# 1
iterador = iter([1, 2, 3])
while True:
    try:
        x = next(iterador)
    except StopIteration:
        break
    print(x)
```

Os itens 2 e 3 são idênticos em estrutura — é o ponto do exercício. **O mesmo código percorre lista, string e `dict.items()`**, porque os três cumprem o mesmo protocolo.

**O item 4:** `sum` faz exatamente isso internamente, acumulando em vez de imprimir.

**O item 5** é o padrão "pegue o primeiro sem materializar": `next(iter(x))` cria um iterador, tira um valor e descarta o resto. Em `next(iter(arquivo))` isso lê **uma** linha de um arquivo de 10 GB. Com `x[0]` numa lista funcionaria também, mas `next(iter(...))` funciona em **qualquer** iterável — inclusive conjuntos e geradores, que não aceitam índice.

**Um detalhe do item 3 que vale registrar:** `dict.items()` é **iterável**, não iterador — duas passadas funcionam. E é uma *view*: ela **reflete alterações** feitas no dicionário depois de criada.

```
duas passadas: [('a',1), ('b',2)]  [('a',1), ('b',2)]
depois de d["c"]=3: [('a',1), ('b',2), ('c',3)]
```

## A4 — Ache o erro

| # | Erro | Sintoma |
|---|---|---|
| 1 | `__next__` sem `StopIteration` | laço infinito |
| 2 | `__iter__` devolve `self` com posição própria | ver abaixo |
| 3 | `len` num iterador | `TypeError: object of type 'map' has no len()` |
| 4 | remover durante o `for` | ver abaixo |
| 5 | `__iter__` devolve lista | `TypeError: iter() returned non-iterator of type 'list'` |
| 6 | mesmo gerador para duas funções | a segunda recebe vazio |

**O item 2 tem dois sintomas, e o segundo é pior:**

```
1ª passada: [1, 2, 3]   ·   2ª passada: []
fors aninhados sobre [1,2]: [(1, 2)]
```

A segunda passada vazia já é ruim. Mas os `for` aninhados devolvendo **um** par em vez de quatro é o defeito difícil de diagnosticar: o laço interno consome o que o externo ia visitar, e o resultado é uma fração silenciosa do esperado.

**O item 4 é o erro que engana porque às vezes funciona:**

```
[1,2,3,4,5] -> [1,3,5]   esperado [1,3,5]   visitou [1,2,4]   OK (por acaso)
[1,2,4,5]   -> [1,4,5]   esperado [1,5]     visitou [1,2,5]   ERRADO
[2,4,6]     -> [4]       esperado []        visitou [2,6]     ERRADO
```

Remover durante a iteração faz o índice **pular** elementos: ao remover a posição 1, o que era a posição 2 vira 1, e o `next` seguinte pede a 2 — pulando um item. Com `[2,4,6]`, remover todos os pares deixa `[4]`.

**E o primeiro caso "funciona"** — o que torna o bug perigoso: testado com a lista errada, ele passa. **A correção:** itere sobre uma cópia (`for x in lista[:]`) ou, melhor, construa uma lista nova por compreensão.

**O item 5 é uma mensagem que vale conhecer:** `iter() returned non-iterator of type 'list'`. O Python **verifica** que `__iter__` devolveu algo com `__next__`. Uma lista não tem, e o erro é específico e claro.

## AP1 — O iterável

A implementação correta está na §6.5 do capítulo. O que o exercício acrescenta:

**3. O teste dos dois iteradores** é o que distingue um iterável de verdade:

```python
a, b = iter(playlist), iter(playlist)
next(a), next(b), next(a)     # 'm1', 'm1', 'm2'
```

Os dois começam do início e avançam separadamente. Uma implementação com uma classe só daria `'m1', 'm2', 'm3'` — os dois compartilhando a mesma posição.

**4. Os dois sintomas da versão errada**, lado a lado:

```
1ª passada: ['m1','m2','m3']   2ª passada: []
[(a,b) for a in p for b in p]: [('m1','m2')]
```

**A regra que sai daí:** se dois `for` aninhados sobre o mesmo objeto não produzem `n²` pares, o objeto é um iterador disfarçado de coleção.

## AP2 — O bug do relatório

**1. Onde o erro aparece contra onde está a causa.** O `ZeroDivisionError` estoura na linha do `return`; a causa é o `sum` **duas linhas acima**, que consumiu o gerador. Essa distância é o que torna o bug caro — o traceback aponta para uma divisão que está correta.

**2 e 3. As três correções e o custo medido** (100 mil linhas):

| Correção | Pico de memória | Legibilidade |
|---|---|---|
| materializar (`list`) | alto — a lista inteira | melhor |
| uma passada só | baixo — constante | pior |
| reabrir o arquivo | baixo | média, e duas leituras de disco |

**4. A decisão.** Para 5 MB: **materializar**. A memória é irrelevante e o código fica direto — otimizar aqui é resolver um problema que não existe. Para 5 GB: **uma passada**, porque é a única que cabe. Reabrir quase nunca compensa: paga I/O, que é a operação mais cara das três, para economizar linhas.

**A pergunta que resolve o caso geral:** *quantas vezes vou percorrer isto, e cabe na memória?* Duas percorridas e cabe → materialize. Não cabe → reestruture para uma passada.

## AP3 — `itertools`

```
tee -> a: [1,2,3,4]  b: [1,2,3,4]      (as duas cópias funcionam)
islice(range(100), 2, 5): [2, 3, 4]
chain([1], [2,3]): [1, 2, 3]
```

**2. O custo do `tee`, medido.** Consumindo **só** a cópia `a` de um gerador de 200 mil elementos:

```
pico: 9.0 MB
```

`tee` guardou os 200 mil valores num buffer interno, porque a cópia `b` ainda não os leu. **Ele não duplica o iterador; ele bufferiza o que uma cópia já consumiu e a outra não.**

**5. Quando `tee` é pior que `list()`.** Exatamente aí: se você consome uma cópia inteiramente antes de tocar na outra, `tee` guarda tudo na memória **e** paga a indireção do buffer — enquanto `list()` guardaria o mesmo tanto, de forma mais simples e mais rápida de percorrer.

**`tee` compensa quando as cópias avançam mais ou menos juntas** (por exemplo, comparando cada elemento com o seguinte), porque aí o buffer fica pequeno. É uma ferramenta específica, não um "list() preguiçoso".

**3 e 4 são os casos em que `itertools` brilha:** `islice(arquivo, 100, 110)` lê 110 linhas de um arquivo de qualquer tamanho e para; `chain(a, b, c)` percorre três arquivos como um só, sem concatenar nada em memória.

## D1 — O leitor de blocos

```python
class Blocos:
    def __init__(self, caminho, tamanho=100):
        if tamanho < 1:
            raise ValueError("tamanho deve ser >= 1")
        self.caminho = caminho
        self.tamanho = tamanho
        self._contagem = None            # só depois da primeira passada

    def __iter__(self):
        return IteradorDeBlocos(self)    # reabre a cada passada

    def __len__(self):
        if self._contagem is None:
            raise TypeError(
                "len() indisponível antes da primeira passada: contar exigiria "
                "ler o arquivo inteiro, que é justamente o que esta classe evita. "
                "Percorra uma vez, ou use sum(1 for _ in blocos)."
            )
        return self._contagem


class IteradorDeBlocos:
    def __init__(self, dono):
        self._dono = dono
        self._arquivo = open(dono.caminho, encoding="utf-8")
        self._blocos = 0

    def __iter__(self):
        return self

    def __next__(self):
        bloco = []
        for linha in self._arquivo:
            bloco.append(linha.rstrip("\n"))
            if len(bloco) == self._dono.tamanho:
                break
        if not bloco:
            self._arquivo.close()
            self._dono._contagem = self._blocos     # guarda para o __len__
            raise StopIteration
        self._blocos += 1
        return bloco                                 # (c) o último pode ser menor
```

**(a)** `__iter__` cria um iterador novo, que **abre o arquivo de novo** — daí a segunda passada funcionar.

**(b)** O `for linha in self._arquivo` aproveita que o arquivo **é um iterador** (§6.3): as linhas chegam uma a uma, e só `tamanho` delas ficam vivas por vez.

**(e2) — testar que a memória não cresce sem arquivo gigante.** Meça com `tracemalloc` percorrendo um arquivo de 50 mil linhas com `tamanho=10` e com `tamanho=10000`. Se o pico crescer proporcionalmente ao **bloco** e não ao **arquivo**, a preguiça funciona. Um arquivo modesto resolve: o que se testa é a **relação**, não o valor absoluto.

**(1) Por que `__len__` é um problema.** `len()` precisa de resposta **imediata e barata** — é a expectativa de quem escreve `if len(x) > 0`. Contar blocos exige ler o arquivo inteiro, que é exatamente o que a classe existe para evitar. Um `__len__` que faz I/O transforma uma operação que parece gratuita numa leitura de disco escondida.

**O que a biblioteca padrão faz:** não implementa `__len__` em iteradores, ponto. `len(map(...))` dá `TypeError: object of type 'map' has no len()`, e quem quiser contar escreve `sum(1 for _ in it)` — explicitamente, sabendo que consome. **Ausência é melhor que uma implementação que mente sobre o custo.**

A implementação acima escolhe um meio-termo defensável: `len()` funciona **depois** que a informação já foi obtida de graça, e levanta um erro explicativo antes. É honesto, mas há um argumento forte para não ter `__len__` nenhum — a inconsistência ("às vezes funciona") é ela mesma uma armadilha.

**(2) Se alguém apagar o arquivo entre duas passadas**, o `open` do próximo `__iter__` levanta `FileNotFoundError`. **A responsabilidade é do chamador**, e essa é a resposta certa: a classe não pode garantir que um recurso externo continue existindo, e tentar (copiando o arquivo, segurando o descritor aberto) trocaria um erro claro por um comportamento surpreendente. O que a classe **deve** fazer é falhar de forma legível — que é o que acontece.

---

## Erros comuns

1. **Prever `[]` ou `[1,2,3]` no A2.4.** É `[3]` — o iterador é uma posição.
2. **Achar que preguiçoso implica esgotável.** `range` desmente.
3. **Testar remoção durante `for` com uma lista que funciona por acaso.**
4. **Uma classe só para iterável e iterador.** Dois sintomas: segunda passada vazia e aninhamento quebrado.
5. **`__iter__` devolvendo lista.** O Python verifica e recusa.
6. **Usar `tee` como "list() preguiçoso".** Ele bufferiza tudo se as cópias não avançam juntas.
7. **Implementar `__len__` que faz I/O.** Esconde custo onde ninguém espera.
8. **Reabrir arquivo para economizar memória** quando materializar resolveria.
