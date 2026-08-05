# Gabarito — Capítulo 04.09: Encapsulamento e properties

Leia depois de tentar. Enunciados em [`../cap09.md`](../cap09.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — Preveja a saída

| # | Resultado |
|---|---|
| 1 e 2 | `1 True` — `_A__y` **está** no `__dict__` |
| 3 | `AttributeError: can't set attribute 'v'` |
| 4 | **`(setter rodou)`** — o `__init__` passa pelo setter |
| 5 | `RecursionError` |
| 6 | `1 False` — não há `__dict__` |

**O item 4 é o que mais importa na prática.** `self.preco = 100` no `__init__` **aciona o setter** — e é por isso que a atribuição deve ir para o nome **público**. Se o `__init__` escrevesse `self._preco = 100`, a validação seria contornada na construção, e existiria um caminho para criar um objeto inválido.

**O item 5 é o erro mais comum ao escrever a primeira property:**

```python
@property
def x(self):
    return self.x        # chama a si mesmo, infinitamente
```

O getter de `x` lê `self.x`, que chama o getter de `x`. `RecursionError`. A correção é o underscore: `return self._x`. **A convenção `_nome` não é estética aqui — é o que evita a recursão.**

## A2 — Property ou não?

| # | Escolha | Por quê |
|---|---|---|
| 1 | **atributo simples** | sem validação, property é verbosidade com custo |
| 2 | **property** | validação: inteiro positivo |
| 3 | **property somente-leitura** | derivado, cálculo barato |
| 4 | **property somente-leitura** | idem |
| 5 | **método** — `buscar_dados_completos()` | ver abaixo |
| 6 | **property somente-leitura** | derivado da data |

**O item 5 é o único que não é property, e o motivo é o custo.** `cliente.dados_completos` parece um atributo — gratuito, instantâneo, seguro de acessar num laço. Se ele consulta o banco, a sintaxe **mente sobre o custo**, e alguém vai escrevê-lo dentro de um `for` sem perceber que está fazendo `n` consultas.

É o mesmo problema do `__len__` que faz I/O (04.05/D1) e do `do_banco` que abre conexão (04.08/A3.6). **A regra que unifica os três: a interface deve sugerir o custo.** Property para o barato; método com nome de verbo para o caro.

**Os itens 3, 4 e 6 são o caso ideal da property somente-leitura:** derivados baratos, que não podem ficar dessincronizados porque não são guardados.

## A3 — Ache o erro

| # | Erro | Sintoma |
|---|---|---|
| 1 | getter lê a si mesmo | `RecursionError` |
| 2 | setter atribui ao nome público | `RecursionError` |
| 3 | `__init__` escreve `self._preco` | contorna a validação |
| 4 | property que faz SQL | esconde custo (A2.5) |
| 5 | getter/setter que só repassa | verbosidade com ~45% de custo |
| 6 | `__slots__ = ("a")` | ver abaixo |

**Os itens 1 e 2 são o mesmo erro nos dois sentidos:** o getter que lê o nome público e o setter que escreve nele. Os dois entram em recursão, e a correção é sempre o `_`.

**O item 6 é a armadilha mais sutil do capítulo**, porque `__slots__ = ("a")` **funciona por acidente**:

```
class X: __slots__ = ("a")     # string "a", não tupla
x.a = 1   -> ok
x.ab = 1  -> AttributeError
```

`("a")` **não é uma tupla** — é a string `"a"` entre parênteses redundantes. O Python itera a string, e como ela tem um caractere, o resultado coincide com o esperado. Com dois caracteres, o erro aparece:

```
class Y: __slots__ = ("ab")
y.a  -> AttributeError    y.b -> AttributeError    y.ab -> ok
```

`"ab"` iterado dá `'a'` e `'b'`… e o Python cria um slot chamado `ab`? Não — ele aceita a string como um nome único. O comportamento é confuso o suficiente para justificar a regra: **sempre vírgula**. `__slots__ = ("a",)`.

## A4 — O que `__slots__` recusa

| # | Operação | Resultado |
|---|---|---|
| 1 | `s.x = 2` | ok — declarado |
| 2 | `s.y = 1` | `AttributeError: 'S' object has no attribute 'y'` |
| 3 | `del s.x` | **ok** — dá para apagar |
| 4 | `s.__dict__` | `AttributeError` — não existe |
| 5 | subclasse sem `__slots__` | **funciona** — ver abaixo |

**O item 5 é a armadilha que anula a proteção:**

```python
class T(S): pass          # sem __slots__
t = T()
t.qualquer = 1            # FUNCIONA
hasattr(t, "__dict__")    # True
```

**Uma subclasse que não declara `__slots__` recupera o `__dict__`** — e com ele, a capacidade de aceitar qualquer atributo. Toda a proteção da classe mãe desaparece na primeira subclasse distraída.

**O que isso significa para quem adotou `__slots__` por segurança:** a garantia é **local à classe**, não à hierarquia. Se a intenção é recusar atributos inventados, **toda** classe da cadeia precisa declarar `__slots__` — inclusive as vazias, com `__slots__ = ()`.

E se a intenção era economizar memória, o efeito é o mesmo: a subclasse sem slots volta a ter um dicionário por instância, e a economia evapora.

## AP1 — A validação tardia

**1 a 3.** A property da §6.3 resolve. Os 15 usos continuam escrevendo `produto.preco_centavos = x`, e agora `produto.preco_centavos = "89.90"` levanta `TypeError`.

**4.** Com `set_preco()`, mudariam **15 linhas** — mais os testes, mais qualquer código externo que use a classe. E o risco não é o trabalho: é **esquecer uma**. A que ficar para trás continua atribuindo direto, sem validação, e o bug sobrevive à correção.

**5. Existe caso em que `set_preco()` seria melhor?** Sim, dois.

**Quando a operação é cara ou tem efeito colateral.** `set_preco()` que grava no banco, dispara evento ou recalcula índices deveria ser um método — pelo argumento do A2.5: a sintaxe de atributo sugere gratuidade.

**Quando a operação precisa de mais de um argumento.** `definir_preco(valor, motivo, autorizado_por)` não cabe numa property, que recebe exatamente um valor. Tentar contornar passando uma tupla é pior que um método honesto.

**A regra:** property para atribuição simples com validação; método quando houver custo, efeito colateral ou mais de um parâmetro.

## AP2 — Derivados

**1.** Os três como property somente-leitura, calculando a partir de `self.itens`.

**3. A dessincronização, na versão que guarda:**

```python
pedido.itens.append(Item("Mouse", 8990))
pedido.total          # ainda o valor antigo — errado
```

O item entrou; o total não sabe. **Nenhum erro** — só um número errado, que segue para o relatório e para a nota fiscal.

É exatamente o problema do `total_centavos` derivável do 03.16/A3.5, e a conclusão é a mesma: **guardar derivado é cache, e cache pode divergir da fonte.**

**4. O recálculo:** um relatório que lê `total` mil vezes recalcula **mil vezes**. Com dez itens, é irrelevante. Com dez mil itens e mil leituras, são dez milhões de operações.

**5. Quando guardar se justifica** — e a resposta tem duas condições, não uma:

- o cálculo é **caro** (percorre milhares de itens, ou consulta o banco), **e**
- existe um **mecanismo** que garante a atualização: uma única função de escrita por onde tudo passa, ou invalidação explícita.

**Sem o mecanismo, é erro; com ele, é decisão** — a mesma frase do 03.16/A3.5.

E há um meio-termo que resolve a maioria dos casos: `functools.cached_property`, que calcula na primeira leitura e guarda. Ele tem o mesmo risco de divergir, com a vantagem de a invalidação ser explícita (`del pedido.total`).

## AP3 — Medindo `__slots__`

```
sem __slots__   37,6 MB · leitura de atributo: 13,0 ms
com __slots__   16,8 MB · leitura de atributo: 12,5 ms      (200 mil objetos)

atributo direto  72,7 ms por 1M leituras
property        105,4 ms por 1M leituras
```

**4. Para uma classe com 50 instâncias, qual otimização vale a pena? Nenhuma.**

A conta, com os números:

- **`__slots__`** economiza ~105 bytes por objeto. Com 50 instâncias: **5 KB**. Irrelevante.
- **Leitura de atributo** é ~2% mais rápida com slots. Com 50 objetos lidos algumas vezes: nanossegundos.
- **Evitar property** economiza 33 ns por leitura. Para importar, seriam necessários milhões de acessos.

**A resposta honesta é "nenhuma", e o exercício pede exatamente isso** — porque a tentação de aplicar as três "porque são otimizações" é o erro que o 03.14 documentou com outros números.

**O que vale a pena numa classe de 50 instâncias:** property **para validação**, que não é otimização — é correção. E `__slots__` se o objetivo for **recusar atributos inventados**, que também não é desempenho.

**A regra:** escolha por clareza e segurança; otimize depois de medir; e reconheça quando a medição diz "não faça nada".

## D1 — A conta bancária

```python
class Conta:
    def __init__(self, titular, saldo=0, limite=0):
        self.titular = titular          # passa pelo setter
        self._saldo = 0
        self.limite = limite            # passa pelo setter
        self._historico = []
        if saldo:
            self.depositar(saldo)       # entra pelo caminho autorizado

    @property
    def titular(self):
        return self._titular

    @titular.setter
    def titular(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("titular inválido: %r" % valor)
        self._titular = valor.strip()

    @property
    def limite(self):
        return self._limite

    @limite.setter
    def limite(self, valor):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("limite inválido: %r" % valor)
        self._limite = valor

    @property
    def saldo(self):                    # SEM setter — (b)
        return self._saldo

    @property
    def saldo_disponivel(self):
        return self._saldo + self._limite

    @property
    def historico(self):
        return tuple(self._historico)   # (c) cópia imutável

    def depositar(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("depósito inválido: %r" % valor)
        self._saldo += valor
        self._historico.append(("deposito", valor))

    def sacar(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("saque inválido: %r" % valor)
        if valor > self.saldo_disponivel:
            raise ValueError("saque de %d excede o disponível (%d)"
                             % (valor, self.saldo_disponivel))
        self._saldo -= valor
        self._historico.append(("saque", valor))
```

Os ataques, todos recusados:

```
saldo direto       -> AttributeError: can't set attribute 'saldo'
titular vazio      -> ValueError: titular inválido: '  '
limite negativo    -> ValueError: limite inválido: -1
depósito negativo  -> ValueError: depósito inválido: -5
saque > disponível -> ValueError: saque de 999999 excede o disponível (3000)
histórico          -> AttributeError: can't set attribute 'historico'
```

**(b) é a construção que vale registrar:** `saldo` tem **só getter**. Os métodos `depositar` e `sacar` escrevem em `self._saldo` — eles são o caminho autorizado, e a ausência de setter recusa todo o resto. **Não é preciso proibir nada explicitamente; é preciso não oferecer.**

**(d)** A mensagem inclui o disponível: `"saque de 999999 excede o disponível (3000)"`. Um erro que diz o valor limite poupa a próxima pergunta — o mesmo padrão das mensagens do 03.13.

**A pergunta 1 — o furo, e ele existe:**

```
c._saldo = -1000   ->   PASSOU. saldo agora é -1000.
```

**Não há como impedir.** Nem property, nem `__slots__` (que aceitaria `_saldo`, já que ele precisa ser declarado), nem name mangling — `_Conta__saldo` também é acessível.

**O que isso diz sobre encapsulamento em Python:** ele protege contra **engano**, não contra **intenção**. Quem escreve `conta._saldo = -1000` sabe que está violando o contrato — o underscore avisou. A linguagem confia que ninguém faz isso sem motivo, e aceita o custo.

**E onde a garantia realmente existe:** no banco. `CHECK (saldo_centavos >= 0)` (03.13) vale para **todos** os caminhos de escrita — inclusive o script que ignora a classe inteira e faz `UPDATE` direto. É a mesma conclusão da §9: property dá erro cedo e com boa mensagem; constraint garante o dado.

**A pergunta 2 — o custo da cópia.** `tuple(self._historico)` com 100 mil movimentações copia 100 mil referências a cada leitura de `conta.historico`. Num relatório que lê o histórico dentro de um laço, isso é O(n) por acesso.

Três saídas, e cada uma tem custo:

- **devolver um iterador** — não copia, não permite alterar, mas **esgota** (04.05) e não aceita `len()`;
- **`types.MappingProxyType` / uma tupla guardada** — exige manter a versão imutável sincronizada;
- **documentar que não se deve alterar** e devolver a lista — volta a ser convenção.

**A escolha que eu faria:** manter a cópia (correção acima de desempenho) e, se a medição mostrar que importa, acrescentar um método `iterar_historico()` que devolve o gerador — deixando a escolha para quem chama. É o padrão do 04.05/§12: **materialize por padrão, ofereça o preguiçoso quando pedirem.**

---

## Erros comuns

1. **Getter que lê o nome público.** `RecursionError` — use `self._x`.
2. **`__init__` escrevendo `self._x` direto.** Contorna a própria validação.
3. **`__slots__ = ("a")` sem vírgula.** Funciona por acaso com um nome; quebra com dois.
4. **Subclasse sem `__slots__`.** Recupera o `__dict__` e anula a proteção da mãe.
5. **Property que faz I/O.** A sintaxe de atributo mente sobre o custo.
6. **Getter/setter que só repassa.** Verbosidade com ~45% de custo por leitura.
7. **Guardar valor derivado sem mecanismo de atualização.** Dessincroniza em silêncio.
8. **Aplicar `__slots__` numa classe com 50 instâncias.** 5 KB economizados.
9. **Achar que property protege o dado.** Protege contra engano; a garantia é do banco.
