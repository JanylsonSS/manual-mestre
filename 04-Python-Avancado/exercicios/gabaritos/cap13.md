# Gabarito — Capítulo 04.13: Dataclasses

Leia depois de tentar. Enunciados em [`../cap13.md`](../cap13.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — O que foi gerado?

| Declaração | `__init__` | `__repr__` | `__eq__` | `__hash__` | `__lt__` |
|---|---|---|---|---|---|
| `@dataclass` | sim | sim | sim | **`None`** (bloqueado) | não |
| `frozen=True` | sim | sim | sim | **sim** | não |
| `order=True` | sim | sim | sim | `None` | **sim** |
| `frozen=True, order=True` | sim | sim | sim | sim | sim |
| `eq=False` | sim | sim | **não** | herdado (identidade) | não |
| `init=False` | **não** | sim | sim | `None` | não |
| `slots=True` | sim | sim | sim | `None` | não |
| classe comum | não | não | não | herdado | não |

**Três coisas que a tabela ensina.**

A coluna do `__hash__` tem **três** estados, não dois: gerado, herdado e **`None`**. `None` não significa ausente — significa **bloqueado**, e é o que produz `unhashable type`.

`eq=False` é o único caso em que o hash de identidade sobrevive. E o resultado é coerente com isso:

```
eq=False -> {SemEq(1), SemEq(1)} tem 2 elementos <- identidade, não valor
```

E `order=True` sozinho **não** é permitido sem igualdade:

```
@dataclass(order=True, eq=False) -> ValueError: eq must be true if order is true
```

Faz sentido: ordenar exige saber quando dois objetos empatam.

**Nota sobre `unsafe_hash=True`:** existe, gera `__hash__` numa classe mutável, e o nome é o aviso. Use `frozen=True`; se você precisa de `unsafe_hash`, tem um objeto mutável servindo de chave, que é o problema do 04.12/F3.

## A2 — Preveja a saída

| # | Resultado |
|---|---|
| 1 | `A(x=1)` · `['x']` · **`True`** |
| 2 | `{B(itens=(1, 2))}` — **um** elemento |
| 3 | `[C(ativo=False, nome='Alfa'), C(ativo=True, nome='Beta'), C(ativo=True, nome='Zeta')]` |
| 4 | `D(nome='a', tags={'x'})` e `D(nome='b', tags=set())` |
| 5 | `False` · `'G(valor=1)'` |

**O item 1 é a armadilha central do capítulo.** `y = 0` não tem anotação, então não é campo: não aparece no `repr`, `fields(A)` só lista `x`, e o `__eq__` **ignora `y`** — dois objetos com `y` valendo 0 e 99 são iguais.

O item 2 mostra o par que funciona: `frozen` devolve o hash, `tuple` é hasheável, e dois objetos iguais viram um.

**O item 3 tem uma sutileza:** `ativo` é o primeiro campo declarado, então é o primeiro critério — e `False < True` em Python, porque `bool` é subclasse de `int`. Ordenar por um booleano é legítimo e quase nunca é o que se queria.

O item 4 é `default_factory` funcionando: conjuntos separados.

**O item 5 tem duas respostas úteis.** `F(1) == G(1)` é `False` porque o `__eq__` gerado exige `outro.__class__ is self.__class__` — mais estrito que o `isinstance` do 04.12. E `repr(G(1))` mostra `G`, não `F`: o `__repr__` gerado usa `__qualname__` da instância, que é a correção que o 04.10/A1.6 pediu à mão.

## A3 — Ache o erro

**1. `itens: list = []` — falha na hora.**

```
ValueError: mutable default <class 'list'> for field itens is not allowed: use default_factory
```

É a armadilha do 04.01, detectada na definição da classe. Correção: `field(default_factory=list)`.

**2. `TAXA: float = 0.15` — funciona, e está errado.** A constante virou campo:

```
campos: ['nome', 'TAXA']
Produto('Mouse', 0.5) -> Produto(nome='Mouse', TAXA=0.5)
```

Qualquer chamador pode passar outra taxa, e duas leituras do mesmo produto com taxas diferentes ficam desiguais. Correção: `TAXA: ClassVar[float] = 0.15`.

**3. `frozen` com `__post_init__` que atribui — falha na hora.**

```
FrozenInstanceError: cannot assign to field 'email'
```

O `__setattr__` congelado vale também para dentro da classe. Correção: `object.__setattr__(self, "email", self.email.lower())`.

**4. `total` como campo — funciona, e é o erro mais sutil dos seis.** Três problemas de uma vez:

```
Item(2, 100, 12345) -> Item(quantidade=2, preco_unitario=100, total=200)
```

O `__init__` **aceita** `total=12345` e o `__post_init__` o descarta em silêncio. Além disso, `total` entra no `__eq__`, então alguém que atribua `item.total = 999` torna dois itens idênticos desiguais. E o valor pode ficar dessincronizado dos outros campos a qualquer momento.

Correção: `@property`, como no 04.09 — o que se calcula não se armazena. Se o valor precisar mesmo ser campo (por vir do banco, por exemplo), use `field(init=False, compare=False)`.

**5. Herança — falha na hora.**

```
TypeError: non-default argument 'tamanho_mb' follows default argument
```

`Base.ativo` tem default, então todo campo da filha precisa de default. Correção: `tamanho_mb: int = 0`, ou tirar o default de `ativo`.

**6. `Chave` como chave de dicionário — falha na hora.**

```
TypeError: unhashable type: 'Chave'
```

`@dataclass` sem `frozen` bloqueia o hash. Correção: `@dataclass(frozen=True)`.

**A leitura que vale mais que os seis:** os defeitos 2 e 4 **funcionam**. São os caros — o que falha na definição você conserta em trinta segundos.

## A4 — Qual opção atende?

| # | Requisito | Resposta |
|---|---|---|
| 1 | Servir de chave em dicionário | `frozen=True` |
| 2 | Token fora do log | `field(repr=False)` |
| 3 | Contadores diferentes, objetos iguais | `field(compare=False)` |
| 4 | Identificador calculado, não passado | `field(init=False)` + `__post_init__` |
| 5 | 5 milhões de objetos | `slots=True` |
| 6 | Lista vazia por pedido | `field(default_factory=list)` |

**O que não resolve, e por quê.**

No **1**, `unsafe_hash=True` também gera o hash e é a resposta errada: ela mantém o objeto mutável, e mutar um campo do hash faz o objeto sumir do dicionário (04.12/F3).

No **2**, tornar o campo `_token` não adianta — o `@dataclass` não olha para o sublinhado, e o campo continua no `repr`.

No **5**, `namedtuple` também economiza e é imutável, mas perde `__post_init__`, defaults por campo e mutabilidade parcial. E `slots=True` tem um custo próprio: nenhuma subclasse pode acrescentar atributos sem redeclarar `__slots__` (04.09).

No **6**, `itens: list = []` é o erro do A3.1.

## AP1 — A refatoração

```python
@dataclass
class Endereco:
    rua: str
    numero: str
    cidade: str
    cep: str
    complemento: str = field(default="", compare=False)
```

**15 linhas viraram 7** — e o nome de cada campo, que aparecia até quatro vezes, aparece uma.

**Sobre o defeito.** O `__eq__` original ignora `complemento`. Não dá para saber se foi intenção ou esquecimento **e é exatamente esse o problema**: no código manual, as duas coisas têm a mesma aparência.

Ao converter, você é obrigado a decidir — e a decisão fica escrita. `compare=False` diz "de propósito"; a ausência dele diz "todos os campos contam". A refatoração transformou uma ambiguidade em uma declaração:

```
complementos diferentes, iguais? True <- compare=False preserva o comportamento original
```

Se a resposta certa fosse "era esquecimento", remova o `field(...)` e deixe `complemento: str = ""`. O ponto é que agora há uma escolha visível onde antes havia uma omissão.

## AP2 — O `field()`

```python
@dataclass
class Usuario:
    email: str
    nome: str
    senha_hash: str = field(repr=False)
    ultimo_acesso: object = field(default=None, compare=False)
    tentativas_login: int = field(default=0, compare=False)
    permissoes: set = field(default_factory=set)

    def __post_init__(self):
        self.email = self.email.strip().lower()
        if "@" not in self.email:
            raise ValueError("e-mail inválido: %r" % self.email)
```

```
repr: Usuario(email='ana@aurora.com', nome='Ana', ultimo_acesso=None, tentativas_login=0, permissoes=set())
senha no repr? False
tentativas 0 x 7, iguais? True
permissoes separadas: {'admin'} set()
sem @ -> ValueError: e-mail inválido: 'ana'
```

**Três detalhes que decidem a nota.**

`senha_hash: str = field(repr=False)` **não tem default** — `field()` sem `default` mantém o campo obrigatório. Dá para ajustar um campo sem torná-lo opcional.

O `__post_init__` normaliza **antes** de validar. Invertida, a ordem faria `" ANA@X.COM "` passar na checagem do `@` e ficar guardado com espaços.

E `permissoes` fica **dentro** do `==`, ao contrário de `tentativas_login`: dois usuários com permissões diferentes são usuários diferentes. A distinção entre acessório e essencial é de domínio, não de tipo.

## AP3 — Congelar de verdade

**Os dois problemas:**

```
(a) conteúdo mudou: CestaRuim(dono='Ana', produtos=['Mouse'])
(b) em set -> TypeError: unhashable type: 'list'
```

`frozen=True` recusa `cesta.produtos = [...]` e não tem nada a dizer sobre `cesta.produtos.append(...)`. Reatribuir e mutar continuam sendo coisas distintas.

**A correção:**

```python
@dataclass(frozen=True)
class Cesta:
    dono: str
    produtos: tuple = ()
```

```
corrigida: Cesta(dono='Ana', produtos=('Mouse', 'Teclado'))
append -> 'tuple' object has no attribute 'append'
em set: 1 elemento
```

**E a pergunta final — um objeto mutável dentro da tupla.** Depende do que ele é:

```
tupla com dataclass mutável dentro -> hash: unhashable type: 'ProdutoMutavel'
tupla com classe comum dentro      -> hash funciona
```

Se for outra dataclass mutável, o hash falha e o erro aparece — o Python protege você de novo. Se for uma classe comum, ela é hasheável por **identidade**, o hash funciona e a imutabilidade é uma ficção: mutar o objeto de dentro não muda o hash (então ele não some do `set`), mas duas cestas com produtos equivalentes e distintos comparam como **diferentes**.

A regra que sai daí: **`frozen` garante uma camada.** Para valer em profundidade, tudo lá dentro precisa ser imutável também — e a única forma de saber é olhar.

## D1 — O catálogo da Aurora

O esqueleto, contra o banco real do módulo 03:

```python
@dataclass(frozen=True, slots=True)
class Produto:
    id: int
    nome: str
    categoria: str
    preco_centavos: int
    ativo: bool = True
    codigo_fornecedor: str = field(default="", repr=False)
    CATEGORIAS: ClassVar[tuple] = ("acessorios", "audio", "perifericos", "video")

    def __post_init__(self):
        if self.preco_centavos < 0:
            raise ValueError("preco negativo: %d" % self.preco_centavos)
        if self.categoria not in self.CATEGORIAS:
            raise ValueError("categoria desconhecida: %r" % self.categoria)


def carregar_produtos(conexao):
    consulta = "SELECT id, nome, categoria, preco_centavos, ativo FROM produtos"
    return [Produto(id=i, nome=n, categoria=c, preco_centavos=p, ativo=bool(a))
            for i, n, c, p, a in conexao.execute(consulta)]
```

```
carregados: 12
primeiro: Produto(id=1, nome='Fone Bluetooth XZ-9', categoria='audio', preco_centavos=46990, ativo=True)
set com todos: 12
total do pedido: 50880
categoria fora da lista -> categoria desconhecida: 'mobiliario'
quantidade zero -> quantidade deve ser positiva: 0
```

Note o `bool(a)`: o SQLite devolve `1`, e a anotação `ativo: bool` **não converte nada** (§6.2). Quem converte é você, na fronteira. Esse trabalho manual é o que o 04.15 automatiza.

**As três perguntas.**

**(1) `list` ou `tuple`.** Se `Pedido` for mutável — que é o caso, pois um pedido em montagem recebe itens —, `list` está certo e o pedido não é hasheável, o que também está certo: um pedido tem identidade própria (o número), não é um valor. Se você quisesse `Pedido` congelado, `tuple` seria obrigatória, e acrescentar um item passaria a ser `replace(pedido, itens=pedido.itens + (novo,))` — mais seguro e mais incômodo. A escolha é entre entidade e valor, e o campo apenas registra a decisão.

**(2) `asdict`?** Não, por dois motivos — e o segundo é mais forte que o desempenho.

O primeiro é o custo: `asdict` faz cópia profunda e leva **533,1 ms** contra 16,7 ms da montagem à mão em 100 mil chamadas (§13). Num laço de 100 mil pedidos, é meio segundo contra 17 ms.

O segundo é que **`asdict` só enxerga campos**:

```
asdict do pedido: {'cliente': 'Ana', 'data': '2026-07-15', 'itens': [...]}
```

`total_centavos` **não está lá** — é `@property`. Uma serialização baseada em `asdict` entregaria ao consumidor um JSON sem o total, e o defeito só apareceria do outro lado da API. Escreva `para_json` à mão, ou some as propriedades explicitamente.

`asdict` continua ótimo para depurar, para teste e para volume baixo, onde a cópia profunda é uma garantia útil.

**(3) Por que o SKU não cabe no `__post_init__`.** Porque validar que um SKU existe exige **consultar o catálogo** — o objeto precisaria de acesso ao banco para se construir. Três consequências: criar um `ItemPedido` viraria I/O (o problema do 04.09 sobre esconder custo atrás de sintaxe barata); testar a classe exigiria um banco; e montar mil itens faria mil consultas.

`__post_init__` é para **invariantes locais** — o que se verifica olhando só para os campos do objeto. Regra que depende do mundo externo vai para a camada que já tem a conexão: um `validar_pedido(pedido, repositorio)` ou o próprio serviço que monta o pedido. É a mesma fronteira que o módulo 11 chama de separação entre domínio e infraestrutura.

## MP — O leitor de configuração

O esqueleto:

```python
@dataclass(frozen=True)
class Config:
    host: str = "localhost"
    porta: int = 5432
    banco: str = "aurora"
    usuario: str = "aurora"
    senha: str = field(default="", repr=False)
    nivel_log: str = "INFO"
    timeout_s: float = 5.0

    NIVEIS: ClassVar[tuple] = ("DEBUG", "INFO", "WARNING", "ERROR")

    def __post_init__(self):
        if not 1 <= self.porta <= 65535:
            raise ValueError("porta fora da faixa: %d" % self.porta)
        if self.nivel_log not in self.NIVEIS:
            raise ValueError("nível de log desconhecido: %r" % self.nivel_log)

    @classmethod
    def do_ambiente(cls):
        return cls(
            host=os.environ.get("AURORA_HOST", "localhost"),
            porta=int(os.environ.get("AURORA_PORTA", "5432")),
            banco=os.environ.get("AURORA_BANCO", "aurora"),
            usuario=os.environ.get("AURORA_USUARIO", "aurora"),
            senha=os.environ.get("AURORA_SENHA", ""),
            nivel_log=os.environ.get("AURORA_NIVEL_LOG", "INFO"),
            timeout_s=float(os.environ.get("AURORA_TIMEOUT", "5")),
        )
```

**Onde estão as decisões.** `frozen=True` porque configuração lida uma vez não deve mudar em execução. `senha` com `repr=False` porque um `print(config)` num handler de erro despeja a senha no log — e o valor vem do ambiente, nunca do código (§18.3 da spec). `do_ambiente` é `@classmethod` e não `@staticmethod` pelo motivo do 04.08: `cls` faz uma subclasse `ConfigTeste.do_ambiente()` devolver o tipo certo.

**A contagem que interessa:** sete linhas de conversão dentro de `do_ambiente` (`int(...)`, `float(...)`, os `get` com default) mais seis linhas de validação no `__post_init__` — **treze linhas para sete campos**, e elas crescem linearmente. Com quinze campos, são quase trinta.

Repare também no que **não** foi verificado: `host` pode ser vazio, `banco` pode conter espaços, `timeout_s` pode ser negativo. Cada regra nova é mais um `if`.

Guarde os treze. No 04.15, os mesmos sete campos com as mesmas conversões e as mesmas faixas cabem na **declaração** de cada campo, e a mensagem de erro sai pronta, dizendo qual campo e qual valor. Essa diferença — treze linhas de `if` contra sete declarações — é o argumento inteiro a favor do Pydantic, e você o terá medido você mesmo antes de ouvi-lo.
