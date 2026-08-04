# Gabarito — Capítulo 04.02: Funções como valores e lambdas

Leia depois de tentar. Enunciados em [`../cap02.md`](../cap02.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — Preveja a saída

| # | Resultado |
|---|---|
| 1 | `6 True` |
| 2 | `3` |
| 3 | `6 False` |
| 4 | `['a', 'bb', 'ccc']` |
| 5 | `[-1, 2, 3]` |
| 6 | `TypeError: len() takes exactly one argument (0 given)` |

**O item 3 é a distinção do capítulo em duas linhas.** `h = f(3)` guarda o **resultado** — o número 6 —, e `callable(6)` é `False`. Se você respondeu `True`, releu `h = f` no lugar de `h = f(3)`. O parêntese é o operador de chamada.

**O item 5 é o que ensina sobre `key`.** `sorted([3,-1,2], key=abs)` devolve `[-1, 2, 3]`, não `[1, 2, 3]`. A chave decide a **ordem**; o resultado contém os **elementos originais**. `abs` foi usado para comparar e desapareceu — é a caixa `E` do fluxograma da §8.

**O item 6 é o erro mais comum do capítulo, e a mensagem denuncia:** `len()` foi **chamada** na hora de montar o argumento, com zero argumentos. `key=len` (sem parênteses) é o correto.

## A2 — Escreva o `key`

| # | `key` | Resultado |
|---|---|---|
| 1 | `key=lambda p: -p["i"]` | `['Cid', 'Ana', 'Bia']` |
| 2 | `key=lambda p: (p["c"], -p["i"])` | `['Bia', 'Cid', 'Ana']` |
| 3 | `key=lambda s: (len(s), s)` | `['a', 'd', 'bb', 'cc']` |
| 4 | `key=str.lower` | `['abacaxi', 'Banana', 'Cereja']` |
| 5 | duas passadas — ver abaixo | |
| 6 | `key=lambda p: p["i"] <= 30` | os acima de 30 primeiro |

**O item 4 dispensa lambda.** `str.lower` já é uma função que recebe uma string e devolve outra — exatamente o contrato de `key`. Escrever `lambda s: s.lower()` funciona e é uma indireção a mais. **Métodos de classe usados como função solta (`str.lower`, `str.strip`) são `key` prontas.**

**O item 5 é o que o `-` não resolve.** `-"Ana"` é `TypeError: bad operand type for unary -: 'str'`. A saída são duas passadas, do critério **menos** importante para o mais:

```python
tmp = sorted(P, key=lambda p: p["n"], reverse=True)   # nome DESC (menos importante)
res = sorted(tmp, key=lambda p: p["c"])               # cidade ASC (mais importante)
# [('rj','Bia'), ('sp','Cid'), ('sp','Ana')]
```

**O item 6 usa um truque que vale registrar:** `False < True` em Python, porque booleanos são inteiros 0 e 1. Ordenar por `p["i"] <= 30` põe os `False` (acima de 30) primeiro. É idiomático e merece um comentário no código, porque não é evidente na leitura.

## A3 — `lambda` ou `def`?

| # | Escolha | Por quê |
|---|---|---|
| 1 | **lambda** (ou `itemgetter(2)`) | expressão curta, argumento descartável |
| 2 | **def** | três parâmetros e lógica condicional |
| 3 | **def** | ver abaixo |
| 4 | **def** | usada em cinco lugares — merece nome e docstring |
| 5 | **lambda** | uma linha, passada e descartada |
| 6 | **def** | ganhou nome; é um `def` pior |

**O item 3 parece caber num lambda** — `lambda v: 0 if v is None else v` — e a decisão certa é `def` mesmo assim, por dois motivos. Primeiro, essa regra é de **negócio** ("ausência conta como zero") e vai reaparecer; merece nome e um lugar. Segundo, ela tem um caso de borda que a versão de uma linha esconde: `0` e `""` não são `None`, mas `if not v` os trataria como se fossem. Um `def` com docstring documenta a diferença; um lambda espalhado em seis lugares a esquece em dois.

**O item 6 é o critério em forma pura.** `dobro = lambda x: x * 2` é sintaticamente válido e desaconselhado pelo PEP 8. O lambda existe para ser **anônimo**; nomeá-lo entrega o pior dos dois mundos — a limitação de uma expressão, sem a docstring nem o nome no traceback.

## A4 — Ache o erro

| # | Erro | Correção |
|---|---|---|
| 1 | chamou em vez de passar | `key=minha_funcao` |
| 2 | `key` recebe **um** elemento | `key=lambda x: x` ou `sorted(nums)` |
| 3 | `-` não funciona em texto | `reverse=True` |
| 4 | `filter` esgota | `list(...)` antes de reutilizar |
| 5 | `KeyError` não tratado | `.get()` com padrão, ou erro que liste as opções |
| 6 | imprimiu a função, não o resultado | `ACOES["salvar"]()` |

As mensagens reais:

```
2) TypeError: <lambda>() missing 1 required positional argument: 'b'
3) TypeError: bad operand type for unary -: 'str'
4) list(m) -> [2, 3] · list(m) de novo -> []
6) <function <lambda> at 0x...>
```

**O item 2 é um resquício de Python 2**, onde `sort` aceitava uma função de **comparação** de dois argumentos. Se você precisa mesmo comparar pares — ordenação por regra que não se expressa como chave —, existe `functools.cmp_to_key`. É raro e vale saber que existe.

**O item 4 é o único que não dá erro**, e por isso é o pior. A segunda leitura devolve `[]`, o programa segue, e o relatório sai vazio sem nenhuma pista.

## AP1 — O despacho

```python
OPERACOES = {
    "soma": lambda a, b: a + b,
    "sub":  lambda a, b: a - b,
    "mult": lambda a, b: a * b,
    "div":  lambda a, b: a / b,
    "pot":  lambda a, b: a ** b,
    "mod":  lambda a, b: a % b,
    "max":  max,
}

def calcular(operacao, a, b):
    funcao = OPERACOES.get(operacao)
    if funcao is None:
        raise ValueError(
            f"operação '{operacao}' inválida. Use: {', '.join(sorted(OPERACOES))}"
        )
    return funcao(a, b)
```

**Note o `"max": max`** — a função embutida entra direto, sem lambda. Envolvê-la em `lambda a, b: max(a, b)` seria uma indireção sem ganho.

**3. Acrescentando `"min"`:** na versão com dicionário, uma linha. Na cadeia de `if`, uma linha **e** a mensagem de erro do `else`, que lista as operações à mão e ficaria desatualizada — é justamente o que o item 2 elimina, porque a lista sai de `sorted(OPERACOES)`.

**4. Sobre o `None` em `div` e `mod`.** É má ideia, e por dois motivos.

Primeiro, `None` **não é um resultado de divisão** — é a ausência de resultado disfarçada de valor. Quem chamar `calcular("div", 1, 0) * 2` recebe `TypeError` numa linha que não tem nada a ver com o problema, e o rastro até a divisão por zero se perde.

Segundo, ele mascara um erro que o Python já reporta com precisão: `ZeroDivisionError: division by zero` diz exatamente o que aconteceu. Substituí-lo por `None` troca uma mensagem exata por um valor mudo.

**A alternativa:** deixar o `ZeroDivisionError` subir. Se o chamador quiser tratar, `try/except`; se quiser um padrão, que escolha o dele. **Uma função que decide sozinha engolir erros rouba do chamador a decisão de como reagir** — é a mesma lição do `except` largo no 01.21.

## AP2 — Ordenando a Aurora

```python
CRITERIOS = {
    "nome":           lambda p: p["nome"],
    "preco":          lambda p: p["preco_centavos"],
    "preco_desc":     lambda p: -p["preco_centavos"],
    "categoria":      lambda p: (p["categoria"], p["nome"]),
    "categoria_caro": lambda p: (p["categoria"], -p["preco_centavos"]),
    "ativos":         lambda p: (not p["ativo"], p["nome"]),
}

def ordenar(produtos, criterio="nome"):
    chave = CRITERIOS.get(criterio)
    if chave is None:
        raise ValueError(
            f"critério '{criterio}' desconhecido. Use: {', '.join(CRITERIOS)}"
        )
    return sorted(produtos, key=chave)
```

**O critério `"ativos"` usa o truque do booleano:** `not p["ativo"]` é `False` para os ativos, e `False < True`, então eles vêm primeiro. Dentro de cada grupo, ordena por nome.

**A medição:** um contador dentro do `key` mostra **12 chamadas para 12 produtos**. Confirma a §6.3 na escala do laboratório — e é a razão de uma `key` que consulta o banco fazer `n` consultas.

## AP3 — A estabilidade

**A regra, e ela é contraintuitiva: ordene do critério MENOS importante para o MAIS importante.**

```python
p1 = sorted(P, key=lambda x: x[2], reverse=True)   # nome DESC   (menos importante)
p2 = sorted(p1, key=lambda x: x[1])                # cargo ASC
p3 = sorted(p2, key=lambda x: x[0])                # cidade ASC  (mais importante)
```

```
('rj','dev','Cid')
('rj','qa','Bia')
('sp','dev','Zoe')
('sp','dev','Bia')
('sp','dev','Ana')
('sp','qa','Ana')
```

Cidade crescente; dentro dela, cargo crescente; dentro dele, nome **decrescente** (Zoe, Bia, Ana). Correto.

**Na ordem errada** — do mais importante para o menos — o resultado é lixo:

```
('sp','dev','Zoe')
('rj','dev','Cid')
('sp','dev','Bia')
```

A última ordenação **manda**, e as anteriores só sobrevivem nos empates dela.

**4. O que a estabilidade tem a ver.** Tudo. A garantia é: elementos com chaves iguais **mantêm a ordem relativa anterior**. Sem ela, cada nova ordenação embaralharia os empates e destruiria o trabalho da passada anterior — a técnica seria impossível. É por isso que a estabilidade não é detalhe de implementação: é uma **promessa documentada** do `sorted`, e código sério depende dela.

**3. O caso em que a tupla não resolve** é exatamente o do enunciado: `nome` decrescente. `-x[2]` é `TypeError` para texto, e não existe forma de inverter uma string dentro de uma tupla de chave. Passadas sucessivas com `reverse=True` são a única saída — ou uma classe que inverta a comparação, que é mais trabalho que duas linhas.

## D1 — O pipeline

```python
def aplicar(dados, *etapas):
    resultado, relatorio = dados, []
    for i, etapa in enumerate(etapas, 1):
        nome = getattr(etapa, "__name__", repr(etapa))
        antes = len(resultado)
        try:
            resultado = etapa(resultado)
        except Exception as erro:
            raise RuntimeError(f"etapa {i} ({nome}) falhou: {erro}") from erro
        relatorio.append((nome, antes, len(resultado)))
    return resultado, relatorio
```

Saída real:

```
resultado: [10, 20, 30]
  limpar     4 -> 3
  <lambda>   3 -> 3

erro: etapa 2 (<lambda>) falhou: list index out of range
```

**(a)** Zero etapas: o laço não roda, devolve `(dados, [])`.

**(c) — e aqui está o ponto do desafio.** `getattr(etapa, "__name__", repr(etapa))` funciona, e o resultado para um lambda é `<lambda>`:

```
<function limpar ...>  -> limpar
<function <lambda> ...> -> <lambda>
<method 'upper' of str> -> upper
```

A mensagem `etapa 2 (<lambda>) falhou` é **melhor que nada e pior que o necessário**: com três lambdas no pipeline, você sabe que foi a segunda — pelo número, não pelo nome. É a demonstração concreta do argumento da §6.5, e a conclusão prática: **etapas de pipeline devem ser `def` nomeados**, justamente porque vão aparecer em mensagens de erro.

O `raise ... from erro` preserva a exceção original no traceback (01.21) — sem ele, a causa real se perde.

**(b) e a decisão que a Dica 2 provoca.** `len(resultado)` pressupõe que toda etapa devolva algo dimensionável. Uma etapa que agregue para um número quebra o relatório. Duas saídas honestas: exigir coleções e documentar; ou `len(resultado) if hasattr(resultado, "__len__") else "—"`. **A primeira é melhor**, porque um pipeline cujas etapas mudam de tipo no meio é difícil de entender de qualquer forma — a restrição documenta uma boa prática em vez de contornar uma ruim.

**O fecho — onde o pipeline é pior.**

*Melhor:* o relatório por etapa sai de graça e é ouro para depurar transformação de dados; a sequência vira **dado**, montável a partir de configuração; e o tratamento de erro fica num lugar só.

*Pior:* uma linha de erro a mais entre você e o problema — o traceback aponta para dentro de `aplicar`, não para a linha que falhou; o depurador precisa entrar em duas funções; e a leitura exige saber o que `aplicar` faz. Quatro linhas sequenciais são lidas por qualquer pessoa, na hora.

**O critério:** o pipeline se paga quando as etapas **variam** — em número, em ordem, em configuração. Quando são sempre as mesmas quatro, ele é uma abstração que cobra e não entrega.

---

## Erros mais comuns

1. **`key=funcao()`** — chamou em vez de passar.
2. **Achar que `key` recebe dois elementos.** Recebe um.
3. **`-` em texto.** Só numérico; para texto, `reverse=True` ou duas passadas.
4. **Passadas na ordem errada.** Do menos importante para o mais.
5. **Consumir `map`/`filter` duas vezes.** A segunda vem vazia, sem erro.
6. **Engolir exceção devolvendo `None`.** Rouba do chamador a decisão.
7. **Lambda atribuído a nome.** É um `def` pior.
8. **Envolver função embutida em lambda.** `lambda a,b: max(a,b)` em vez de `max`.
