# Gabarito — Capítulo 04.12: Métodos especiais (dunder)

Leia depois de tentar. Enunciados em [`../cap12.md`](../cap12.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — Qual dunder?

| # | Operação | Método |
|---|---|---|
| 1 | `print(objeto)` | `__str__` (com `__repr__` de reserva) |
| 2 | `[objeto]` no console | `__repr__` |
| 3 | `len(objeto)` | `__len__` |
| 4 | `objeto[2]` | `__getitem__` |
| 5 | `for x in objeto` | `__iter__`, ou `__getitem__` |
| 6 | `"a" in objeto` | `__contains__`, ou `__iter__`, ou `__getitem__` |
| 7 | `objeto1 + objeto2` | `__add__`, com `__radd__` de reserva |
| 8 | `if objeto:` | `__bool__`, ou `__len__`, ou sempre `True` |

**Os itens 5, 6 e 8 têm mais de uma resposta**, e é isso que ensinam: o Python tenta os métodos **em ordem**, e cai num padrão quando nenhum existe. Saber a cadeia explica comportamentos que de outro modo pareceriam arbitrários — sobretudo o item 8, cujo padrão é `True`.

## A2 — Preveja a saída

| # | Resultado |
|---|---|
| 1 | `True`, `True`, **`TypeError`** |
| 2 | **`True`** — `__bool__` ganha |
| 3 | `[0, 10, 20]` e `True` |
| 4 | `'D!'` |
| 5 | `True` e **`True`** |
| 6 | `False` e **`True`** |

**O item 1 mostra os três comportamentos de uma vez.** `==` funciona (há `__eq__`), `in` numa **lista** funciona (ela usa `==`), e `set` falha — porque `set` usa **hash**, e ele foi apagado. É a §6.2 em três operações.

**O item 2:** com os dois presentes, `__bool__` tem prioridade. `__len__` só é consultado quando `__bool__` não existe.

**O item 4 é sutil:** f-strings usam `__str__`, que **cai no `__repr__`** quando não existe. Por isso `f"{D()}"` dá `'D!'`. É mais uma razão para implementar `__repr__` sempre.

**O item 5 é a reflexão em ação.** `1 == E()` também dá `True`: o Python tenta `int.__eq__(1, E())`, que devolve `NotImplemented`, e então tenta `E().__eq__(1)`, que devolve `True`. **A comparação é comutativa por construção da linguagem**, mesmo quando você só implementou um lado.

**O item 6 fecha a cadeia:** com `NotImplemented` dos dois lados, o Python cai na comparação de **identidade**. Dois objetos diferentes dão `False`; o mesmo objeto dá `True`.

## A3 — Ache o erro

| # | Erro | Sintoma |
|---|---|---|
| 1 | `__eq__` sem `isinstance` | `AttributeError: 'str' object has no attribute 'n'` |
| 2 | `__repr__` com nome fixo | subclasse mostra o nome da mãe |
| 3 | campo do hash mutável | o objeto **some** do `set` |
| 4 | só `__str__` | `repr` continua inútil |
| 5 | `__add__` devolvendo `False` | erro de tipo passa em silêncio |
| 6 | `__len__` com I/O | esconde custo |

**O item 1, medido:** comparar com uma string quebra com `AttributeError` — e o erro aparece **dentro** do seu `__eq__`, o que confunde quem depura. A correção é `NotImplemented`, que produz `False` limpo ou `TypeError` claro.

**O item 2:**

```
class Err2Filha(Err2): pass
repr(Err2Filha())  ->  'Produto()'
```

É o 04.10/A1.6 de novo: `type(self).__name__` resolve.

**O item 3 é o mais instrutivo, e a saída é inquietante:**

```
antes de mutar:  x in conjunto -> True
x.n = 2
depois de mutar: x in conjunto -> False      <<< sumiu
mas está lá:     1 elemento
```

**O objeto está no conjunto e o conjunto diz que não está.** Ao mudar o campo que entra no hash, ele passa a ser procurado num balde diferente daquele onde foi guardado. Não há erro, não há aviso — só um dado que desaparece.

**A regra que sai daí:** implemente `__hash__` **só** em objetos que você trata como imutáveis. É a justificativa do `frozen=True` do 04.13.

## A4 — Vale a pena?

| # | Classe | Implementar | **Não** implementar |
|---|---|---|---|
| 1 | `Produto` | `__repr__`, `__eq__`, `__hash__`, `__lt__` | operadores aritméticos |
| 2 | `ConexaoBanco` | `__repr__`, `__enter__`/`__exit__` (04.20) | `__eq__`, `__hash__` |
| 3 | `Vetor2D` | `__repr__`, `__eq__`, `__add__`, `__mul__`, `__abs__` | `__len__` |
| 4 | `Pedido` | `__repr__`, `__len__`, `__iter__` | `__add__` |
| 5 | `Config` | `__repr__`, `__getitem__` | `__eq__`, operadores |
| 6 | `Temperatura` | tudo do D1 | — |

**O item 2 é o que mais se erra.** Comparar conexões por valor não faz sentido: duas conexões ao mesmo banco são recursos **diferentes**. Igualdade por identidade (o padrão) é a correta, e implementar `__eq__` aqui criaria confusão.

**O item 3 tem uma pegadinha:** `__len__` num `Vetor2D` é tentador — "o comprimento do vetor" —, e seria **errado**, porque `len()` precisa devolver um inteiro não-negativo e o comprimento de um vetor é um float. O dunder certo é `__abs__`, e `abs(vetor)` lê melhor.

**O item 4:** `Pedido + Pedido` não tem significado previsível (somar os itens? os totais?). É o critério da §6.7 — se quem conhece o domínio não prevê o resultado, use um método.

## AP1 — O `Produto` completo

```python
@functools.total_ordering
class Produto:
    def __init__(self, nome, preco_centavos):
        self.nome = nome
        self.preco_centavos = preco_centavos

    def __repr__(self):
        return "%s(nome=%r, preco_centavos=%d)" % (
            type(self).__name__, self.nome, self.preco_centavos)

    def __str__(self):
        return "%s — R$ %.2f" % (self.nome, self.preco_centavos / 100)

    def __eq__(self, outro):
        if not isinstance(outro, Produto):
            return NotImplemented
        return (self.nome, self.preco_centavos) == (outro.nome, outro.preco_centavos)

    def __lt__(self, outro):
        if not isinstance(outro, Produto):
            return NotImplemented
        return self.preco_centavos < outro.preco_centavos

    def __hash__(self):
        return hash((self.nome, self.preco_centavos))

    def __format__(self, spec):
        if spec == "curto":
            return self.nome
        return format(str(self), spec)
```

**4.** A subclasse vazia mostra o próprio nome, porque o `__repr__` usa `type(self).__name__`.

**5. `__format__` vale a pena?** Em geral, **não** — e reconhecer isso é a resposta.

`f"{produto:curto}"` economiza pouco sobre `produto.nome`, e cria um vocabulário privado (`"curto"`, `"longo"`) que ninguém descobre sem ler a implementação. `__format__` se justifica quando há **muitas** variações de apresentação usadas em templates, ou quando você precisa suportar especificadores padrão (`f"{valor:>10.2f}"`).

**Para uma classe de domínio com duas formas de exibição, `__str__` mais um método `resumo()` é mais honesto** — porque o método é descobrível por autocompletar e o especificador não.

## AP2 — A coleção

```python
class Catalogo:
    def __init__(self, produtos=None):
        self._produtos = list(produtos or [])

    def __len__(self):
        return len(self._produtos)

    def __getitem__(self, indice):
        if isinstance(indice, slice):
            return Catalogo(self._produtos[indice])     # (3) devolve Catalogo
        return self._produtos[indice]

    def __add__(self, outro):
        if not isinstance(outro, Catalogo):
            return NotImplemented
        return Catalogo(self._produtos + outro._produtos)

    def __repr__(self):
        return "Catalogo(%d produtos)" % len(self._produtos)
```

**3. O fatiamento devolvendo `Catalogo`** exige distinguir índice de fatia — `isinstance(indice, slice)`. Sem isso, `catalogo[0:2]` devolve uma lista, e o resultado de fatiar um `Catalogo` deixa de ser um `Catalogo`, quebrando o encadeamento.

**5. `__repr__` de 500 produtos deve mostrar os 500? Não.**

Três razões: um `repr` de 500 linhas torna a depuração **pior**, não melhor; ele aparece em tracebacks e logs, poluindo tudo; e coleções embutidas fazem o mesmo (`<generator object>`, e o `numpy` abrevia com `...`).

**A convenção que funciona:** mostrar o tipo, a contagem e, se couber, os dois ou três primeiros. `Catalogo(500 produtos: Mouse, Teclado, …)`.

## AP3 — O `Dinheiro`

**3. Removendo `__rmul__`:**

```
dinheiro * 3   ->  funciona
3 * dinheiro   ->  TypeError: unsupported operand type(s) for *: 'int' and 'Dinheiro'
```

O Python tenta `int.__mul__(3, dinheiro)`, que não sabe lidar com o tipo, e depois `Dinheiro.__rmul__` — que não existe. **A assimetria confunde**, porque multiplicação é comutativa no domínio.

**5. As duas divisões — e são casos diferentes:**

- **`dinheiro / dinheiro`** deveria devolver um **número puro** (uma razão). R$ 100 ÷ R$ 50 = 2 — duas vezes, não "R$ 2". É `__truediv__` devolvendo `float`.
- **`dinheiro / 2`** deveria devolver **`Dinheiro`**. Metade de R$ 100 são R$ 50.

**O mesmo operador com dois tipos de retorno**, decidido pelo tipo do operando direito. É legítimo, e precisa ser documentado — porque o leitor não adivinha.

E há a decisão de arredondamento: R$ 0,05 dividido por 3 não tem representação exata em centavos. **Dinheiro dividido precisa de uma política de arredondamento explícita**, e ignorá-la é como o `CAST` sem `ROUND` do 03.12.

## D1 — A `Temperatura`

```python
@functools.total_ordering
class Temperatura:
    __slots__ = ("_celsius",)
    ZERO_ABSOLUTO = -273.15

    def __init__(self, celsius):
        if celsius < self.ZERO_ABSOLUTO:
            raise ValueError("abaixo do zero absoluto: %s < %s"
                             % (celsius, self.ZERO_ABSOLUTO))
        object.__setattr__(self, "_celsius", float(celsius))

    def __setattr__(self, nome, valor):
        raise AttributeError("Temperatura é imutável (tentou %s)" % nome)

    @property
    def celsius(self):
        return self._celsius

    def __repr__(self):
        return "Temperatura(%r)" % self._celsius

    def __str__(self):
        return "%.1f °C" % self._celsius

    def __eq__(self, outro):
        if isinstance(outro, Temperatura):
            return self._celsius == outro._celsius
        if isinstance(outro, (int, float)):
            return self._celsius == outro
        return NotImplemented

    def __lt__(self, outro):
        if isinstance(outro, Temperatura):
            return self._celsius < outro._celsius
        if isinstance(outro, (int, float)):
            return self._celsius < outro
        return NotImplemented

    def __add__(self, outro):
        valor = outro._celsius if isinstance(outro, Temperatura) else outro
        if not isinstance(valor, (int, float)):
            return NotImplemented
        return Temperatura(self._celsius + valor)

    __radd__ = __add__

    def __hash__(self):
        return hash(self._celsius)

    def __bool__(self):
        return self._celsius != self.ZERO_ABSOLUTO

    def para_fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    @classmethod
    def de_fahrenheit(cls, fahrenheit):
        return cls((fahrenheit - 32) * 5 / 9)
```

Saída real:

```
repr: Temperatura(20.0) · str: 20.0 °C
t + 5: 25.0 °C · 5 + t: 25.0 °C
t < 25: True · 25 < t: False · t > 15: True
sorted: [Temperatura(10.0), Temperatura(20.0), Temperatura(30.0)]
set com dois iguais: 1
bool(zero absoluto): False
de_fahrenheit(212): 100.0 °C
imutável -> AttributeError: Temperatura é imutável (tentou _celsius)
Temperatura(-300) -> ValueError: abaixo do zero absoluto: -300 < -273.15
```

**(d) A imutabilidade** é feita com `__slots__` mais `__setattr__` que recusa — e `object.__setattr__` no `__init__` para contornar a própria proibição uma vez. É trabalhoso, e é exatamente isso que `@dataclass(frozen=True)` resolve no 04.13.

**Os três casos de borda:**

**1. `t1 - t2` devolve temperatura ou diferença?** Rigorosamente, uma **diferença** — 20 °C − 15 °C são 5 **graus de diferença**, não "5 °C". A distinção importa porque diferenças se somam livremente (5 + 5 = 10 graus de diferença) enquanto temperaturas não (20 °C + 20 °C não são 40 °C em nenhum sentido físico útil).

Bibliotecas sérias de unidades (`pint`, `astropy.units`) fazem essa distinção e criam um tipo `DeltaTemperatura`. **A implementação acima simplifica e devolve `Temperatura`** — e a resposta certa do exercício é **dizer que simplificou**, não fingir que não há questão.

**2. `t < 5` funciona?** Sim, na implementação acima — comparar com número é conveniente. E `5 < t` também, por reflexão: o Python tenta `int.__lt__`, recebe `NotImplemented`, e chama `Temperatura.__gt__` (gerado por `total_ordering`).

O argumento **contra** aceitar números: `t == 20` é ambíguo — 20 °C? °F? A escolha depende de quanto você valoriza conveniência contra explicitude, e as duas são defensáveis.

**3. `Temperatura(-300)`** deve levantar `ValueError` — está abaixo do zero absoluto, que é fisicamente impossível. É validação no construtor, o mesmo princípio do 04.09: **o objeto não deve conseguir existir num estado inválido.**

---

## Erros comuns

1. **`__eq__` sem `isinstance`.** `AttributeError` dentro do seu método.
2. **`__eq__` sem `__hash__`.** Sai de `set` e de chaves de dicionário.
3. **Mutar o campo do hash.** O objeto some do conjunto, sem erro.
4. **Só `__str__`.** O `repr` continua inútil, e listas o usam.
5. **`__repr__` com nome fixo.** Mente em subclasses.
6. **Devolver `False` em vez de `NotImplemented`.**
7. **Esquecer a versão reflexiva.** `3 * x` falha e `x * 3` funciona.
8. **`__len__` num `Vetor2D`.** É `__abs__`; `len` exige inteiro.
9. **`__repr__` que despeja 500 itens.** Piora a depuração.
