# Gabarito — Capítulo 04.14: Type hints

Leia depois de tentar. Enunciados em [`../cap14.md`](../cap14.md).

> Toda saída abaixo é execução real, no Python 3.10 com mypy.

## A1 — Leia a assinatura

| # | Promete | Obriga quem chama a |
|---|---|---|
| 1 | recebe lista de inteiros, devolve um inteiro | — |
| 2 | recebe texto, devolve `Produto` **ou nada** | **verificar `is None`** antes de usar |
| 3 | recebe `Produto`, **não devolve nada** | não usar o retorno (é `None`) |
| 4 | agrupa produtos por uma chave de texto | — |
| 5 | recebe uma função `int → str` e uma lista de int | passar função com essa assinatura exata |
| 6 | devolve **exatamente dois** inteiros | desempacotar em duas variáveis |
| 7 | nada. `Any` desliga a verificação | — (e é o problema) |
| 8 | devolve tupla de floats de **tamanho variável** | não presumir quantos |

**As três que ensinam mais.**

O **2** é o único que muda o código de quem chama: `X | None` transfere a obrigação da guarda para o chamador, e o verificador cobra.

O **3** contradiz a intuição de que anotar `-> None` é inútil. Sem essa anotação, a função inteira sai do radar do verificador (§6.8) — `-> None` não é enfeite, é o que a coloca em verificação.

E o **6** contra o **8**: `tuple[int, int]` é tamanho fixo, `tuple[float, ...]` é tamanho variável. Confundir os dois é o erro mais comum com tuplas.

## A2 — Escreva a anotação

```python
def dobrar(n: int) -> int: ...
def nomes(produtos: list[Produto]) -> list[str]: ...
def contar(texto: str) -> dict[str, int]: ...
def primeiro(itens: list[T]) -> T | None: ...
def formatar(centavos: int) -> str: ...
def imprimir(mensagem: str) -> None: ...
def par_impar(numeros: list[int]) -> tuple[list[int], list[int]]: ...
def cronometrar(funcao: Callable[..., T], *args: object) -> tuple[T, float]: ...
```

```
mypy --strict -> Success: no issues found in 1 source file
```

**O 4 e o 8 exigem uma peça nova: `TypeVar`.**

```python
T = TypeVar("T")
```

`primeiro(itens: list[str]) -> str | None` funcionaria para textos e obrigaria a escrever uma cópia por tipo. `T` diz "o que entrar, sai" — e a conferência é real:

```
primeiro([Produto("Mouse")]) atribuído a `int | None` ->
error: Incompatible types in assignment (expression has type "Produto | None", variable has type "int | None")
```

O verificador sabe que aquela chamada específica devolve `Produto | None`, embora a assinatura não mencione `Produto` em lugar nenhum.

No **8**, `Callable[..., T]` são as reticências literais: "aceita qualquer assinatura, e devolve `T`". É a anotação honesta para uma função de repasse (04.01), que de fato não sabe o que vai receber. E `*args: object` anota **cada item** de `args`, não a tupla.

O **6** é a armadilha do lote: `print` devolve `None`, então a função devolve `None`, e a anotação é `-> None`.

## A3 — Passa nos dois?

| # | `mypy` aceita? | `python` roda? | O que acontece de fato |
|---|---|---|---|
| 1 | **não** | **sim** | imprime `20.0` — um float onde a assinatura promete int |
| 2 | **não** | **sim** | imprime `None` onde a assinatura promete `str` |
| 3 | **sim** | **não** | `TypeError: can only concatenate str (not "int") to str` |
| 4 | **não** | **não** | `TypeError: unsupported operand type(s) for -: 'int' and 'str'` |
| 5 | **sim** | **não** | `NameError: name 'Produto' is not defined` |
| 6 | **não** | **sim** | imprime `13`, corretamente |

**Os quatro pares acontecem, e cada um ensina uma coisa diferente.**

**1 e 2 — o verificador pega, o interpretador não.** São os defeitos silenciosos: `20.0` e `None` circulam com aparência de resultado e quebram em outro arquivo, mais tarde. É a justificativa da ferramenta em estado puro.

**3 — o verificador passa e o programa quebra.** `Any` apagou a verificação (§6.4), e o `preco: int` aceitou uma string sem conferência. Note que a anotação `preco: int` estava lá, certa, e não serviu para nada — porque o que estava do outro lado era `Any`.

**5 — o verificador passa e o programa nem carrega.** O `-> Produto` sem aspas é avaliado enquanto a classe está sendo definida, e o nome ainda não existe (§6.6). O mypy resolve a referência adiante sem dificuldade; o interpretador não. **É o caso que prova que passar no verificador não é o mesmo que rodar** — e a correção é `-> "Produto"` ou `from __future__ import annotations`.

**6 — o verificador reclama e o programa está certo.** `maior([1, 2, 3])` nunca devolve `None`, e o `+ 10` é seguro. Mas o verificador olha a **assinatura**, não a chamada, e a assinatura admite `None`. Ele não está com defeito: está apontando que a função é insegura para outras entradas. Três saídas legítimas: uma guarda, um `assert`, ou aceitar que aqui o apontamento é excessivo e escrever `# type: ignore[operator]` com o motivo. **A escolha é sua — e é essa a habilidade do D1.**

## A4 — Qual construção?

| # | Situação | Anotação |
|---|---|---|
| 1 | busca que às vezes não acha | `-> Cliente \| None` |
| 2 | função que transforma centavos em texto | `Callable[[int], str]` |
| 3 | objeto com `salvar`, sem herança | `Protocol` |
| 4 | três números, nesta ordem | `tuple[int, int, int]` |
| 5 | JSON de formato variável | `Any` — e é o sinal de que falta validação |
| 6 | devolve outro objeto da própria classe | `-> "Produto"`, ou `from __future__ import annotations` |

**Sobre o 5.** `Any` é a resposta tecnicamente correta e é também um aviso: você acabou de declarar que aquele dado não é conferido por ninguém. `dict[str, Any]` é um meio-termo honesto — diz que é um dicionário de chaves de texto e admite não saber os valores. A saída de verdade é validar na fronteira, que é o 04.15.

**Sobre o 4.** `tuple[int, int, int]` e não `list[int]`: a lista não fixa a quantidade nem a ordem, e "mínimo, médio, máximo" depende das duas coisas. Se os três tiverem nomes, uma dataclass diz mais.

## AP1 — Tipar o que já existe

As assinaturas do `geradores.py` anotadas:

```python
def contar_narrando() -> Iterator[int]: ...
def naturais() -> Iterator[int]: ...
def limpar(linhas: Iterable[str]) -> Iterator[str]: ...
def numerar(linhas: Iterable[str], inicio: int = 1) -> Iterator[tuple[int, str]]: ...
def cabecalho_e_corpo(linhas: Iterable[str]) -> Iterator[str]: ...
```

**(1) `naturais()`, que nunca termina, é `Iterator[int]`.** A anotação descreve **o que ele produz**, não quantos — e é por isso que ela funciona igualmente bem para o gerador infinito e para o que produz três itens. Não existe `Iterator` "finito" ou "infinito" no vocabulário de tipos: essa distinção é do domínio, e vai no docstring.

`Generator[int, None, None]` também está correto e diz mais (o que ele recebe via `send` e o que devolve no `return`). Como nenhum gerador do 04.06 usa `send`, `Iterator[int]` é a anotação honesta — não prometa precisão que você não usa.

**(2) A anotação de `limpar` muda o entendimento, sim.** Escrever `linhas: Iterable[str]` em vez de `list[str]` documenta o achado central do 04.06: a função aceita **qualquer** iterável, inclusive outro gerador, e é isso que permite encadear estágios sem materializar nada. `list[str]` teria funcionado e teria mentido — o verificador passaria a recusar exatamente o uso que o capítulo defende.

**A regra que sai daí:** anote parâmetros com o tipo **mais geral** que a função aceita (`Iterable`), e retornos com o **mais específico** que ela garante (`Iterator`, `list`).

## AP2 — A união com None, completa

```python
def buscar_produto(catalogo: Catalogo, nome: str) -> Produto | None:
    for produto in catalogo:
        if produto.nome == nome:
            return produto
    return None

def preco_formatado(catalogo: Catalogo, nome: str) -> str:
    produto = buscar_produto(catalogo, nome)
    if produto is None:
        return "produto não encontrado"
    return "R$ %.2f" % (produto.preco_centavos / 100)

def aplicar_desconto(catalogo: Catalogo, nome: str, porcento: int) -> Produto | None:
    produto = buscar_produto(catalogo, nome)
    if produto is None:
        return None
    novo = produto.preco_centavos * (100 - porcento) // 100
    return replace(produto, preco_centavos=novo)

def preco_obrigatorio(catalogo: Catalogo, nome: str) -> Produto:
    produto = buscar_produto(catalogo, nome)
    if produto is None:
        raise ProdutoNaoEncontrado(nome)
    return produto
```

```
mypy --strict -> Success: no issues found in 1 source file

R$ 89.90 · produto não encontrado
Produto(nome='Mouse', preco_centavos=8091) · None
preco_obrigatorio('Mesa') -> ProdutoNaoEncontrado: Mesa
```

Removendo a guarda de `preco_formatado`:

```
error: Item "None" of "Produto | None" has no attribute "preco_centavos"  [union-attr]
```

**As três estratégias, e a que vai numa API pública.**

`preco_formatado` **absorve** a ausência e devolve texto. Serve para exibição, e só: o texto "produto não encontrado" é indistinguível de um nome de produto para quem chama.

`aplicar_desconto` **propaga** a ausência. É a mais composável e a mais honesta — mas note que ela empurra a guarda para o próximo, e uma cadeia de quatro funções `| None` produz quatro `if`.

`preco_obrigatorio` **levanta exceção**. É a que se usa numa API pública, e por dois motivos: a assinatura fica `-> Produto`, sem `| None`, de modo que ninguém precisa de guarda no caminho feliz; e a ausência vira um evento com nome, tipo e rastreamento, em vez de um `None` que se confunde com "achei e o valor é vazio".

**O critério geral:** ausência **esperada** (o produto pode não existir e isso é normal) → `| None`. Ausência **excepcional** (o produto deveria existir; se não existe, algo está errado) → exceção. E note que `ProdutoNaoEncontrado` herda de `LookupError`, não de `Exception` solta — a hierarquia certa permite que quem chama capture por categoria.

## AP3 — `Protocol` nas políticas de frete

```python
@runtime_checkable
class PoliticaFrete(Protocol):
    def calcular(self, produto: Produto) -> Centavos: ...


class FreteGratis:                       # não herda de nada
    def calcular(self, produto: Produto) -> Centavos:
        return 0
```

A política escrita errada, e o que o verificador diz:

```
error: Argument 1 to "cobrar" has incompatible type "FreteErrado"; expected "PoliticaFrete"
note: Following member(s) of "FreteErrado" have conflicts:
note:     Expected:
note:         def calcular(self, produto: Produto) -> int
note:     Got:
note:         def calcular(self, produto: Produto) -> str
```

O diagnóstico mostra **os dois lados**, e é isso que faz o `Protocol` valer o trabalho: o erro do 04.11 (uma política com a assinatura errada entrando no sistema em silêncio) passa a ser detectado antes de rodar.

**A pergunta sobre o híbrido.** O `Produto.frete_centavos` do 04.11 aceita objeto com `calcular` **ou** função. A anotação é uma união:

```python
Frete = PoliticaFrete | Callable[[Produto], Centavos]
```

E ela expõe o custo daquele projeto: quem consome precisa **distinguir os dois casos em execução**, com `isinstance` ou `hasattr`. Escrever a anotação tornou visível uma decisão que estava escondida no `if hasattr(politica, "calcular")` — e a pergunta que ela levanta é se a flexibilidade valia a bifurcação. Aceitar só o `Protocol` custa três linhas a mais em quem passa uma função, e devolve uma assinatura sem união.

**E aqui aparece uma limitação que vale mais que o exercício.** Para usar `isinstance` com um `Protocol`, ele precisa de `@runtime_checkable` — sem isso, tanto o verificador quanto o interpretador recusam:

```
error: Only @runtime_checkable protocols can be used with instance and class checks  [misc]
TypeError: Instance and class checks can only be used with @runtime_checkable protocols
```

Com o decorador, funciona. Mas veja o que ele confere:

```
runtime_checkable confere assinatura? True
```

**`True` para a `FreteErrado`** — a classe cujo `calcular` devolve `str`. Em execução, `isinstance` verifica apenas que o **método existe**, não que a assinatura bate. O verificador estático pega; a checagem em execução não.

A lição é a do capítulo inteiro, agora do lado avesso: as duas conferências são diferentes e nenhuma substitui a outra.

## D1 — O verificador no seu código

Não há gabarito de números — eles dependem do seu código. Há gabarito de **método**, e o critério de correção é a classificação.

Rodando `mypy` sobre o `codigo/` do módulo 04 deste manual, o resultado é:

```
cap07/objetos.py:54: error: Need type annotation for "tags"  [var-annotated]
cap01/assinaturas.py:93: error: "sleep" does not return a value  [func-returns-value]
cap01/assinaturas.py:114: error: Unexpected keyword argument "dados" for "relatorio"  [call-arg]
cap01/assinaturas.py:115: error: Too many positional arguments for "relatorio"  [call-arg]
```

**Quatro apontamentos, quatro corretos, quatro propositais** — todos são código escrito para demonstrar um erro acontecendo. A classificação é "código proposital" nos quatro casos, e a ação é `# type: ignore[codigo]` com o motivo:

```python
relatorio(dados=[1, 2])  # type: ignore[call-arg]  # erro proposital: demonstra positional-only
```

**O que isso ensina, e é o ponto do desafio:** um verificador que aponta código deliberado **não está com defeito**. Ele não tem acesso à sua intenção. Duas reações são igualmente ruins — obedecer a todos os apontamentos (você mutilaria as demonstrações) e ignorar todos (você perderia os defeitos reais no meio).

**Sobre a terceira pergunta**, a das linhas mudadas sem melhorar o código: espere um número diferente de zero, e não o trate como fracasso. Anotar `dict[str, list[tuple[int, str]]]` numa variável local que existia bem sem anotação é custo puro. Se esse número for grande em relação aos defeitos reais encontrados, `--strict` não é o ajuste certo **para aquele projeto** — e a resposta madura é essa, não "tipagem é boa" nem "tipagem é burocracia".

**Um cuidado de método:** conte os apontamentos **antes** de mexer em qualquer coisa. Corrigir enquanto lê destrói o denominador, e sem ele a terceira pergunta não tem resposta.

## MP — A biblioteca tipada

O esqueleto:

```python
Centavos = int
TabelaDePrecos = dict[str, Centavos]

class PoliticaPreco(Protocol):
    def aplicar(self, base: Centavos) -> Centavos: ...

def carregar(registros: list[dict[str, object]]) -> list[Produto]: ...
def buscar(catalogo: list[Produto], nome: str) -> Produto | None: ...
def por_categoria(catalogo: list[Produto], categoria: str) -> list[Produto]: ...
def total(catalogo: list[Produto]) -> Centavos: ...
def formatar(centavos: Centavos) -> str: ...
```

**A resposta que interessa é a última pergunta**, e ela costuma sair torta na primeira tentativa.

Quase todo mundo escreve `list[dict[str, Any]]` para os registros que vêm do JSON. E aí a `carregar` fica assim:

```python
def carregar(registros: list[dict[str, Any]]) -> list[Produto]:
    return [Produto(r["nome"], r["preco_centavos"], r["categoria"]) for r in registros]
```

`mypy --strict` **aceita**, e o requisito "sem `Any`" foi violado. Pior: essa função constrói `Produto` com o que vier —

```
mypy --strict -> Success: no issues found in 1 source file
python        -> [Produto(nome='Mouse', preco_centavos='8990', categoria='perifericos')]
```

— um `Produto` com o preço em **texto**, porque o valor veio de um formulário. O verificador aprovou, e o defeito vai aparecer na primeira soma.

Trocar para `list[dict[str, object]]` cumpre o requisito e **quebra o código**, de propósito, uma vez por campo:

```
error: Argument 1 to "Produto" has incompatible type "object"; expected "str"   [arg-type]
error: Argument 2 to "Produto" has incompatible type "object"; expected "int"   [arg-type]
error: Argument 3 to "Produto" has incompatible type "object"; expected "str"   [arg-type]
```

Agora o verificador está exigindo o que faltava: uma conversão explícita, com verificação, de cada campo. Escrevê-la à mão custa uma dúzia de linhas por classe e cresce com cada campo novo — foi o mesmo trabalho manual que o mini projeto do 04.13 mediu em treze linhas.

**Guarde as duas versões.** A do `Any` passa no verificador e não confere nada; a do `object` confere e é verbosa. O 04.15 apresenta a terceira, que confere e cabe na declaração — e você vai chegar lá tendo tentado as outras duas.
