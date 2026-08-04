# Gabarito — Capítulo 04.01: `*args`, `**kwargs` e assinaturas

Leia depois de tentar. Enunciados em [`../cap01.md`](../cap01.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — Preveja a saída

| # | Resultado |
|---|---|
| 1 | `(1, [], (), None, {})` |
| 2 | `(1, 2, (3, 4), 5, {'x': 6})` |
| 3 | `[1, 2, 3] [1, 2, 3] [1, 2, 3]` — **as três iguais** |
| 4 | `(1,) (2,)` |
| 5 | `0 1 3` |
| 6 | `TypeError: f5() got multiple values for argument 'a'` |

**O item 3 é o mais instrutivo do exercício, e quase ninguém acerta.** A previsão comum é
`[1] [1,2] [1,2,3]` — errado. A saída é `[1,2,3]` **três vezes**.

O motivo tem duas partes. Primeiro, o default mutável: as três chamadas compartilham a mesma
lista. Segundo, e é o que engana: o `print` **avalia todos os argumentos antes de imprimir
qualquer um**. Quando a impressão começa, as três chamadas já aconteceram e as três referências
apontam para a mesma lista, agora com três elementos. Você não vê a evolução — vê o estado final,
três vezes.

**O item 4 é o contraste que ensina.** `acc=()` é uma **tupla**, imutável. `acc + (x,)` não
modifica nada: cria uma tupla nova. O default original continua vazio para sempre, e cada chamada
é independente. **É a prova de que o problema não é "default", é "default mutável"** — e a razão
de a regra prática ser sobre mutabilidade, não sobre valores padrão.

**O item 5, três chamadas e três respostas:** `f4()` recebe zero posicionais → tupla vazia → `0`.
`f4([1,2,3])` recebe **um** argumento, que por acaso é uma lista → `1`. `f4(*[1,2,3])` espalha a
lista em três posicionais → `3`. A diferença entre as duas últimas é exatamente o `*`.

**O item 6:** `f5(1, a=2)` tenta preencher `a` duas vezes — uma posicionalmente, outra por nome.
`**kwargs` não "salva" nesse caso, porque o Python resolve os parâmetros nomeados **antes** de
juntar o resto.

## A2 — Empacota ou espalha?

| # | Operação | O que acontece |
|---|---|---|
| 1 | **empacota** | os posicionais viram a tupla `n` |
| 2 | **espalha** | `[1,2,3]` vira três argumentos |
| 3 | **empacota** | os nomeados viram o dicionário `opcoes` |
| 4 | **espalha** | vira `conectar(host="local")` |
| 5 | **empacota** | `a = 1`, `resto = [2, 3]` — **e vira lista, não tupla** |
| 6 | **espalha** | vira `print("a", "b", sep="-")` → `a-b` |

**O item 5 é a mesma sintaxe num terceiro contexto:** desempacotamento em atribuição. Empacota o
que sobra — e note que aqui o resultado é **`list`**, não `tuple` como em `*args`. É uma
inconsistência real da linguagem, e vale saber para não errar num `isinstance`.

**A regra que unifica os seis:** `*` do lado **esquerdo** (definição, atribuição) junta; do lado
**direito** (chamada) espalha.

## A3 — Ache o erro

| # | Válida? | Mensagem |
|---|---|---|
| 1 | **sim** | `a` vira keyword-only obrigatório |
| 2 | não | `SyntaxError: non-default argument follows default argument` |
| 3 | não | `SyntaxError: invalid syntax` |
| 4 | **sim** | `a` só posicional, `b` só nomeado |
| 5 | não | `SyntaxError: invalid syntax` |
| 6 | **sim, e é a pegadinha** | ver abaixo |

**O item 1 surpreende quem espera erro.** `def g(*args, a, b=1)` é válida: tudo depois de `*args`
é keyword-only, e `a` é obrigatório **por nome**. `g(1, 2)` falha com `missing 1 required
keyword-only argument: 'a'`; `g(1, 2, a=3)` funciona.

**Os itens 3 e 5 falham pela mesma razão:** `**kwargs` tem de ser o **último**. Nada vem depois
dele, porque ele existe justamente para absorver todo o resto.

**O item 6 é o ponto do exercício.** `def g(a, b=[], c={})` é sintaticamente perfeita e
semanticamente uma bomba: dois defaults mutáveis. **O Python não avisa** — nenhum erro, nenhum
aviso, nem com `-W all`. Ferramentas de análise estática (`ruff`, `pylint`) pegam; o interpretador
não. É a razão de este ser um dos primeiros avisos que qualquer linter de Python emite.

## A4 — Como chamar?

Assinatura: `(a, /, b, c=3, *, d, e=5)`

| # | Chamada | Resultado |
|---|---|---|
| 1 | `h(1, 2, d=4)` | `(1, 2, 3, 4, 5)` |
| 2 | `h(1, b=2, d=4)` | `(1, 2, 3, 4, 5)` |
| 3 | `h(a=1, b=2, d=4)` | `TypeError` — `a` é positional-only |
| 4 | `h(1, 2, 3, 4)` | `TypeError` — `d` só por nome |
| 5 | `h(1, 2, 3, d=4, e=6)` | `(1, 2, 3, 4, 6)` |

**O menor conjunto aceito: `h(1, 2, d=4)`** — dois posicionais e um nomeado. `a` e `b` são
obrigatórios (sem default) e `d` é obrigatório **e** keyword-only. `c` e `e` têm padrão.

**A leitura que vale levar:** a assinatura comunica quatro categorias distintas de parâmetro —
obrigatório-posicional, flexível, opcional, e obrigatório-nomeado — e o leitor descobre isso
**sem abrir o corpo da função**. É esse o argumento a favor de usar `/` e `*` com intenção.

## AP1 — O repasse

```python
def cronometrar(f, *args, **kwargs):
    inicio = time.perf_counter()
    resultado = f(*args, **kwargs)
    return resultado, (time.perf_counter() - inicio) * 1000


def repetir(f, vezes, *args, **kwargs):
    return [f(*args, **kwargs) for _ in range(vezes)]


def com_padrao(f, padrao, *args, **kwargs):
    try:
        return f(*args, **kwargs)
    except Exception:
        return padrao
```

```
com_padrao(int, -1, 'abc') -> -1
com_padrao(int, -1, '42')  -> 42
```

**A pergunta que fecha o exercício.** `vezes` precisa vir **antes** de `*args` porque, depois
dele, tudo é keyword-only. Se fosse `def repetir(f, *args, vezes, **kwargs)`, a chamada seria
`repetir(sorted, [3,1,2], vezes=3)` — o que até funciona, e cria um problema real: **se a função
envolvida tiver ela mesma um parâmetro chamado `vezes`, os dois colidem.** O nome do seu
parâmetro passa a competir com o namespace de quem você envolve.

É por isso que funções de repasse costumam usar nomes improváveis ou apenas posicionais — e é a
mesma razão pela qual decoradores bem escritos evitam acrescentar parâmetros nomeados (04.04).

**Sobre o `except Exception` em (3):** ele é largo de propósito aqui, porque a função existe para
absorver qualquer falha. Em código de produção, capturar `Exception` sem relançar é o
anti-padrão do 01.21 — a versão honesta registra o erro antes de devolver o padrão.

## AP2 — Refatorando

**1. As chamadas originais:**

```python
gerar_relatorio(vendas, "csv", False, "valor", 10, True, True, "saida.csv")
gerar_relatorio(vendas, "texto", True, "nome", None, False, False, None)
```

Ilegíveis. Os três booleanos no meio são indistinguíveis, e trocar dois deles não dá erro — dá um
relatório errado.

**2. A assinatura refatorada:**

```python
def gerar_relatorio(dados, /, formato="texto", *,
                    incluir_zeros=False, ordenar_por="nome",
                    limite=None, mostrar_total=True,
                    exportar=False, caminho=None):
    ...
```

**3. As chamadas novas:**

```python
gerar_relatorio(vendas, "csv", ordenar_por="valor", limite=10,
                exportar=True, caminho="saida.csv")
gerar_relatorio(vendas, incluir_zeros=True)
```

A segunda encolheu de oito argumentos para dois, porque os defaults cobrem o caso comum. **A
chamada passou a mencionar só o que foge do padrão** — que é a informação que interessa a quem lê.

**4. Acrescentando `agrupar_por`.** Na versão original, o parâmetro novo precisa ir **no fim**,
senão quebra todas as chamadas existentes — e o fim é onde ele fica pior posicionado
semanticamente, longe de `ordenar_por`. Na versão refatorada, ele entra **em qualquer lugar**
depois do `*`, porque a ordem dos keyword-only é irrelevante para o chamador. Zero chamadas
quebradas.

**5. A decisão sobre `**extras`.**

*A favor:* absorve opções futuras sem alterar a assinatura; útil se a função repassa as opções a
outra função que evolui por conta própria.

*Contra:* `ordernar_por="valor"`, com a letra trocada, é **absorvido em silêncio** e o relatório
sai ordenado por `nome`. Sem `**extras`, o Python diria `unexpected keyword argument
'ordernar_por'` — e um erro alto na primeira execução vale mais que um relatório sutilmente
errado descoberto semanas depois.

**A escolha justificada: não.** Esta função é o ponto final, não um repasse — ela não entrega as
opções a mais ninguém. `**kwargs` se justifica quando você **repassa**; aqui, ele só compraria
tolerância a erro de digitação. **A flexibilidade que não serve a um repasse é quase sempre
flexibilidade contra você.**

## AP3 — A armadilha

**1. Lista:**

```python
def registrar(item, historico=[]):
    historico.append(item); return historico
```

Persiste. Correção: `historico=None` e `if historico is None: historico = []`.

**2. Dicionário:**

```python
def contar(chave, contagens={}):
    contagens[chave] = contagens.get(chave, 0) + 1
    return contagens
```

Três chamadas com chaves diferentes devolvem um dicionário com as três. Mesmo remédio.

**3. Chamada de função:**

```python
def criar_evento(nome, em=datetime.datetime.now()):
    return nome, em
```

Todas as chamadas trazem o instante da **importação do módulo**. Correção: `em=None` e
`em = em or datetime.datetime.now()`.

**O extra — inspecionando `__defaults__`:**

```python
registrar.__defaults__          # ([],)      antes
registrar("a"); registrar("b")
registrar.__defaults__          # (['a','b'],)  depois
```

**O default está guardado num atributo do objeto-função, e ele mudou.** Isso encerra a discussão
sobre "por que isso acontece": não há regra oculta nem comportamento especial de parâmetros. A
lista é um objeto comum, referenciado por um atributo comum, e `append` a modifica como
modificaria qualquer outra (01.13).

E é a mesma constatação que abre o próximo capítulo: **funções têm atributos porque são objetos.**

## D1 — O registrador

```python
def registrar(evento, *detalhes, nivel="INFO", destino=None, **contexto):
    mensagem = evento
    if detalhes:
        mensagem += " | " + " | ".join(str(d) for d in detalhes)
    if contexto:
        mensagem += " · " + " · ".join(f"{k}={v}" for k, v in contexto.items())

    linha = f"[{nivel}] {mensagem}"
    if destino is None:
        print(linha)
    else:
        with open(destino, "a", encoding="utf-8") as arquivo:
            arquivo.write(linha + "\n")
    return linha
```

**(a) As chamadas, com a saída real:**

```
registrar("banco conectado")
    [INFO] banco conectado

registrar("consulta lenta", "SELECT * FROM eventos", nivel="WARN")
    [WARN] consulta lenta | SELECT * FROM eventos

registrar("falha", "timeout", "tentativa 3", nivel="ERRO", host="db01", ms=5000)
    [ERRO] falha | timeout | tentativa 3 · host=db01 · ms=5000
```

**(b) e (c) — e aqui está a parte que importa.**

A chamada que **recusa** é `registrar()`:

```
TypeError: registrar() missing 1 required positional argument: 'evento'
```

Só isso. **A assinatura quase não recusa nada** — e descobrir isso é mais valioso que o erro.

Veja o que ela aceita calada:

```
registrar("falha", "ERRO")
    [INFO] falha | ERRO          <<< "ERRO" virou DETALHE, nao nivel
```

Quem quis passar o nível posicionalmente não recebe erro: o valor é absorvido por `*detalhes`, a
linha sai com `[INFO]`, e um alerta crítico vai para o log como informação de rotina.

E o item (c):

```
registrar("teste", contexto={"a": 1})
    [INFO] teste · contexto={'a': 1}
```

`contexto` **não** é um parâmetro que se possa preencher — é o nome interno do `**`. Passá-lo por
nome cria uma chave chamada `contexto` dentro dele. Não há colisão nem erro; há uma chave com um
nome infeliz.

**(d) Por que `nivel` e `destino` são keyword-only.** Justamente por causa de (b): se fossem
posicionais, `registrar("falha", "ERRO")` seria ambíguo entre "um detalhe" e "o nível". O `*`
elimina a ambiguidade **na definição**, e a documenta na assinatura. O preço é que a forma errada
não dá erro — ela cai em `*detalhes`, que aceita qualquer coisa.

**A lição completa:** `*args` compra flexibilidade e **paga com detecção de erro**, exatamente
como `**kwargs` no AP2. Numa API em que confundir nível com detalhe seja grave, a assinatura certa
não tem `*detalhes` — tem `detalhes: list = None`, que recusa o argumento extra.

**O fecho.** A assinatura comunica quatro coisas sem que ninguém leia o corpo: `evento` é
obrigatório e vem primeiro; existem detalhes opcionais em número livre; `nivel` e `destino` são
opções com padrão, e precisam ser nomeadas; e há espaço aberto para contexto arbitrário. Quem lê
`registrar("falha", "timeout", nivel="ERRO", host="db01")` entende a chamada inteira sem
documentação. **A assinatura é a primeira linha de documentação de qualquer função — e a única
que o interpretador verifica.**

---

## Erros mais comuns

1. **Prever `[1] [1,2] [1,2,3]` no A1.3.** O `print` avalia tudo antes de imprimir.
2. **Achar que todo default é problema.** Tupla e imutáveis são seguros.
3. **Confundir `f4([1,2,3])` com `f4(*[1,2,3])`.** Um argumento contra três.
4. **Esperar que `def g(*args, a)` seja erro.** É válida: `a` vira keyword-only obrigatório.
5. **Pôr `**kwargs` antes do fim.** Ele tem de ser o último.
6. **Confiar no interpretador para pegar default mutável.** Só o linter pega.
7. **Nomear parâmetros de função de repasse** com nomes prováveis — colidem com os da envolvida.
8. **Achar que `*args` só traz flexibilidade.** Ele absorve argumentos errados em silêncio.
