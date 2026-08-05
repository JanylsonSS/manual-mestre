# Gabarito — Capítulo 04.10: Herança

Leia depois de tentar. Enunciados em [`../cap10.md`](../cap10.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — Preveja a saída

| # | Resultado |
|---|---|
| 1 | `'A.g -> B.f'` |
| 2 | **`'C'`** |
| 3 | `F E E` |
| 4 | `['i'] ['i']` |
| 5 | `'Ola de K'` |
| 6 | `'L()'` |

**Os itens 1 e 5 têm a mesma causa, e é a mais importante do capítulo:** `self` é sempre a instância **real**, não a classe onde o código foi escrito.

Em `A.g`, o `self.f()` resolve pelo MRO de `type(self)`, que é `B` — então roda `B.f`. Em `J.cumprimentar`, `type(self).__name__` é `'K'`. **A mãe chama a versão da filha sem saber que a filha existe** — é exatamente isso que polimorfismo significa, e é o que faz o padrão *template method* do mini projeto funcionar.

**O item 2 é a armadilha da ordem.** `self.x = "D"` roda primeiro; depois `super().__init__()` roda `self.x = "C"` e **sobrescreve**. O resultado é `'C'`, não `'D'`.

É a razão de `super()` vir **primeiro**: a mãe inicializa, a filha ajusta. Invertido, a mãe desfaz o trabalho da filha — e o defeito é silencioso.

**O item 6 é sutil e vale registrar:** `M` herda `__repr__` de `L`, e o texto devolvido é `"L()"` — **fixo**, com o nome errado para `M`. Um `__repr__` herdado que cita o nome da classe literalmente mente sobre subclasses. A correção é `type(self).__name__`, e é o assunto do 04.12.

## A2 — Leia o MRO

| # | MRO |
|---|---|
| 1 | `[W, Y, Z, X, object]` |
| 2 | `[S, R, Q, P, object]` |
| 3 | `TypeError` |
| 4 | linear: `[C, B, A, object]` |
| 5 | `[U, object]` — duas |

**O item 2 mostra a regra da linearização:** `S(R, P)` não pode pôr `P` logo depois de `S`, porque `R` (e `Q`) dependem de `P` estar **depois** delas. O C3 resolve como `[S, R, Q, P]`.

**O item 3 é a inversão que quebra:** `T(P, R)` pede `P` antes de `R`, contradizendo o MRO de `R`, que exige `P` depois. O Python recusa **na definição da classe**, o que é bom — o erro aparece na importação, não em produção.

**O item 5 é uma checagem útil:** toda classe herda de `object`, mesmo sem declarar. `object` é sempre o último do MRO.

## A3 — Ache o erro

| # | Erro | Consequência |
|---|---|---|
| 1 | sem `super().__init__()` | objeto sem os atributos da mãe |
| 2 | usa atributo da mãe antes do `super()` | `AttributeError` |
| 3 | `type() is` | rejeita subclasses válidas |
| 4 | copia o corpo da mãe | diverge quando a mãe mudar |
| 5 | `Kit(Fisico, Digital)` | hierarquia estourando (D1) |
| 6 | herança por reúso | "todo fornecedor é um restaurante"? |

**O item 2, medido:**

```python
class ComPropRuim(Base):
    def __init__(self, n):
        self.calculado = self.n * 2      # `n` ainda NÃO existe
        super().__init__(n)
```

```
AttributeError: 'ComPropRuim' object has no attribute 'n'
```

**É o item A1.2 com consequência pior.** Lá, a ordem invertida sobrescrevia um valor em silêncio; aqui, ela quebra alto. A regra é a mesma: `super().__init__()` **primeiro**.

**O item 6 é o erro conceitual mais caro da lista.** Herdar `Restaurante` para criar `Fornecedor` porque os dois têm CNPJ e endereço confunde **ter os mesmos campos** com **ser do mesmo tipo**. O sintoma aparece depois: `Fornecedor` herda `servir_prato()`, e alguém eventualmente chama.

O teste que pega isso antes: *"todo fornecedor é um restaurante?"* Não. A relação é "os dois são **pessoas jurídicas**" — e a saída é uma base comum `PessoaJuridica`, ou composição.

## A4 — Herdar, substituir ou estender?

| # | Ação | Por quê |
|---|---|---|
| 1 | **estender** | quer o da mãe **mais** algo → `super()` |
| 2 | **substituir** | zero não tem relação com o cálculo da mãe |
| 3 | **herdar** | nada a fazer |
| 4 | **estender** | `super().__init__()` + os campos novos |
| 5 | **substituir** | o preço vem dos itens, não do campo |
| 6 | **estender** | envolve o resultado da mãe |

**O item 5 merece uma ressalva.** Se `Kit.preco_centavos` **ignora** completamente o da mãe, isso é um sinal de alerta: a filha não está especializando, está **contradizendo**. Vale perguntar se `Kit` é mesmo um `Produto`, ou se é uma **coleção** de produtos — o que seria composição.

**A regra que orienta os seis:** estender quando o comportamento da mãe faz parte da resposta; substituir quando não faz; herdar quando o da mãe já serve. **Substituir muitos métodos é sinal de que a herança está errada.**

## AP1 — A hierarquia da Aurora

```python
class Produto:
    def __init__(self, nome, preco_centavos):
        self.nome = nome
        self.preco_centavos = preco_centavos

    def descrever(self):
        return "%s: R$ %.2f" % (self.nome, self.preco_centavos / 100)

    def frete_centavos(self):
        return 2000


class ProdutoFisico(Produto):
    def __init__(self, nome, preco_centavos, peso_kg):
        super().__init__(nome, preco_centavos)
        self.peso_kg = peso_kg

    def frete_centavos(self):
        return int(self.peso_kg * 500)


class ProdutoDigital(Produto):
    def __init__(self, nome, preco_centavos, tamanho_mb):
        super().__init__(nome, preco_centavos)
        self.tamanho_mb = tamanho_mb

    def frete_centavos(self):
        return 0

    def descrever(self):
        return "%s (%d MB)" % (super().descrever(), self.tamanho_mb)


def total_com_frete(produtos):
    return sum(p.preco_centavos + p.frete_centavos() for p in produtos)
```

**4.** `total_com_frete` não menciona nenhuma subclasse. Ela chama `p.frete_centavos()` e cada objeto responde por si — é polimorfismo, e é o que o A1.1 demonstrou mecanicamente.

**5. Se surgir `ProdutoImportado`: nada muda em `total_com_frete`.** Escreve-se a classe nova com o seu `frete_centavos()`, e a função existente passa a funcionar com ela sem uma linha alterada.

**É esse o teste de uma boa hierarquia:** acrescentar um tipo não exige tocar em quem consome. Se exigir, o consumidor está verificando tipo em algum lugar — e é o AP3.

## AP2 — O diamante

```
D().quem(): D -> B -> C -> A
MRO de D:   [D, B, C, A, object]
```

**4. `A.__init__` roda exatamente UMA vez:**

```
ordem: D -> B -> C -> A
A rodou 1 vez
```

E o contraste que prova o valor de `super()` — a mesma hierarquia chamando as mães **pelo nome**:

```python
class D2(B2, C2):
    def __init__(self):
        B2.__init__(self)
        C2.__init__(self)
```

```
ordem: D -> B -> A -> C -> A
A rodou 2 vezes      <<< o problema do diamante
```

**`A.__init__` roda duas vezes.** Numa classe que abre conexão, incrementa contador ou aloca recurso, isso é um defeito real — e é exatamente o problema que o C3 e o `super()` foram criados para resolver.

**5. Como o `super()` de `B` chega em `C`.** `super()` sem argumentos é `super(B, self)`, onde `self` é uma instância de `D`. Ele procura no MRO de **`type(self)`** — que é `[D, B, C, A, object]` — a partir da posição **seguinte** a `B`. O próximo é `C`.

**`B` não conhece `C`, e não precisa.** A ordem é uma propriedade da instância, não do código de `B`. É o que torna mixins possíveis: uma classe pode chamar `super()` sem saber quem virá depois.

## AP3 — Polimorfismo × `isinstance`

**1. A versão polimórfica** é a do AP1: cada classe implementa `frete_centavos()`, e a função só chama.

**2. O quarto tipo:** na versão polimórfica, uma classe nova e **zero** alterações. Na versão com `isinstance`, uma classe nova **mais** um `elif` — e o `elif` precisa entrar na **posição certa**, que é o item 3.

**3. A armadilha da ordem, medida:**

```python
class Importado(Fisico): ...     # Importado É um Fisico

# ordem A: Fisico primeiro
if isinstance(p, Fisico):     return int(p.peso_kg * 500)    # 1000
if isinstance(p, Importado):  return 5000                    # nunca roda

# ordem B: Importado primeiro
if isinstance(p, Importado):  return 5000                    # 5000
if isinstance(p, Fisico):     return int(p.peso_kg * 500)
```

```
Fisico primeiro:    1000     <<< o ramo de Importado nunca roda
Importado primeiro: 5000
```

**A subclasse precisa vir antes da mãe, sempre** — e nada avisa quando a ordem está errada. Um `elif` acrescentado no fim da cadeia por uma subclasse silenciosamente nunca executa.

**4. Existe caso em que `isinstance` é melhor?** Sim, e vale reconhecer dois.

**Quando você não controla as classes.** Tratar `int`, `str` e `list` de formas diferentes numa função de serialização exige verificar tipo — você não pode acrescentar métodos a `int`.

**Quando o comportamento pertence ao consumidor, não ao objeto.** Como formatar um produto para HTML não é responsabilidade do produto; pôr `para_html()` em toda classe de domínio polui o modelo com preocupações de apresentação. Aí `isinstance` — ou, melhor, `functools.singledispatch` — é honesto.

**A regra:** o comportamento é do objeto → polimorfismo. O comportamento é de quem consome, ou as classes não são suas → verificação de tipo, com a subclasse antes da mãe.

## D1 — A hierarquia que estoura

**A hierarquia inicial: 6 classes** (`Produto` + 5 tipos).

**(a) O kit misto.** `Kit` já existe, mas um kit com digitais e físicos precisa calcular frete só sobre os físicos. Se `Kit` herda de `Produto`, ele precisa de um `frete_centavos()` que **inspeciona os itens** — e aí aparece o primeiro `isinstance`. **Total: 6 classes, 1 `isinstance`.**

**(b) Assinatura digital.** `AssinaturaDigital(Assinatura, ProdutoDigital)` — herança múltipla. Funciona, e o MRO precisa ser verificado. **Total: 7 classes.**

**(c) Serviço com material físico.** `ServicoComEntrega(Servico, ProdutoFisico)`. **Total: 8 classes** — e agora existem três classes cujo nome é a **junção** de duas características.

**O ponto exato de ruptura é (b).** Não é (c), e o motivo é preciso: em (b) apareceu a **primeira classe cuja existência decorre de uma combinação**, não de uma especialização. `AssinaturaDigital` não é "um tipo mais específico de assinatura" — é "assinatura **e** digital ao mesmo tempo".

**O sinal contável:** com 3 características que se combinam livremente, a herança precisa de até 8 classes; a composição precisa de 3 objetos de política.

**A versão com composição a partir dali:**

```python
class PoliticaFrete:
    def calcular(self, produto):
        raise NotImplementedError


class FreteGratis(PoliticaFrete):
    def calcular(self, produto):
        return 0


class FretePorPeso(PoliticaFrete):
    def __init__(self, por_kg=500):
        self.por_kg = por_kg

    def calcular(self, produto):
        return int(produto.peso_kg * self.por_kg)


class Produto:
    def __init__(self, nome, preco_centavos, politica_frete=None):
        self.nome = nome
        self.preco_centavos = preco_centavos
        self.politica_frete = politica_frete or FreteGratis()

    def frete_centavos(self):
        return self.politica_frete.calcular(self)
```

Agora um kit misto é **um `Produto`** com a política adequada. Nenhuma classe nova.

**A solução híbrida, que é a que eu entregaria:** manter `ProdutoDigital` e `ProdutoFisico` como subclasses — são especializações genuínas, com campos próprios — **e** extrair frete e devolução para políticas. Herança para o eixo "que tipo de coisa é"; composição para os eixos "como se comporta em X".

**O fecho — por que "prefira composição a herança" é útil e incompleto.**

É útil porque corrige o viés dominante: a maioria das pessoas alcança herança primeiro, e a maioria das hierarquias de mais de dois níveis se arrepende.

É **incompleto** por três razões. Primeiro, ele não diz **quando** — e a resposta ("a partir do segundo eixo de variação") é o que faltava. Segundo, ele ignora que composição custa: `produto.politica_frete.calcular(produto)` é mais indireto que `produto.frete()`, e para dois tipos com uma diferença isso é complexidade sem retorno. Terceiro, frameworks inteiros são construídos sobre herança — `BaseModel`, `APIView`, `TestCase` — e ali ela é a resposta certa, porque o framework define o esqueleto e você preenche as diferenças.

**A versão completa do conselho:** herança para especialização num eixo; composição quando os eixos se multiplicam; e a decisão vem da contagem de combinações, não de uma preferência.

---

## Erros comuns

1. **`super()` depois do código da filha.** A mãe sobrescreve (A1.2) ou o atributo ainda não existe (A3.2).
2. **Achar que a mãe chama a versão dela.** `self` é sempre a instância real.
3. **`__repr__` herdado com o nome fixo.** Mente sobre subclasses.
4. **Chamar mães pelo nome em herança múltipla.** `A.__init__` roda duas vezes.
5. **`isinstance` com a mãe antes da subclasse.** O ramo da subclasse nunca roda.
6. **Cadeia de `isinstance` para comportamento que pertence ao objeto.**
7. **Herdar por campos em comum.** "Todo X é um Y?" resolve.
8. **Filha que substitui quase todos os métodos.** A herança está errada.
9. **Converter tudo em composição desde o início.** Para dois tipos, herança é melhor.
