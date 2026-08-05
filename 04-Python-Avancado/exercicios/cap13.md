# Exercícios — Capítulo 04.13: Dataclasses

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap13.md`](gabaritos/cap13.md).

## Aquecimento

### A1 — O que foi gerado? `[Aquecimento · ~10 min]`

Para cada declaração, diga **quais** destes existem na classe: `__init__`, `__repr__`, `__eq__`, `__hash__`, `__lt__`.

1. `@dataclass`
2. `@dataclass(frozen=True)`
3. `@dataclass(order=True)`
4. `@dataclass(frozen=True, order=True)`
5. `@dataclass(eq=False)`
6. `@dataclass(init=False)`
7. `@dataclass(slots=True)`
8. Uma classe comum, sem decorador

### A2 — Preveja a saída `[Aquecimento · ~10 min]`

```python
# 1
@dataclass
class A:
    x: int
    y = 0
a1, a2 = A(1), A(1)
a2.y = 99
A(1);  [f.name for f in fields(A)];  a1 == a2

# 2
@dataclass(frozen=True)
class B:
    itens: tuple = ()
{B((1, 2)), B((1, 2))}

# 3
@dataclass(order=True)
class C:
    ativo: bool
    nome: str
sorted([C(True, "Zeta"), C(False, "Alfa"), C(True, "Beta")])

# 4
@dataclass
class D:
    nome: str
    tags: set = field(default_factory=set)
d1, d2 = D("a"), D("b")
d1.tags.add("x")
d1;  d2

# 5
@dataclass
class F:
    valor: int = 0
class G(F):
    pass
F(1) == G(1);  repr(G(1))
```

### A3 — Ache o erro `[Aquecimento · ~12 min]`

Cada trecho tem um defeito. Alguns falham na hora; **outros funcionam e estão errados** — diga qual é qual.

```python
# 1
@dataclass
class Carrinho:
    itens: list = []

# 2
@dataclass
class Produto:
    nome: str
    TAXA: float = 0.15          # constante da classe

# 3
@dataclass(frozen=True)
class Cliente:
    email: str
    def __post_init__(self):
        self.email = self.email.lower()

# 4
@dataclass
class Item:
    quantidade: int
    preco_unitario: int
    total: int = 0
    def __post_init__(self):
        self.total = self.quantidade * self.preco_unitario

# 5
@dataclass
class Base:
    nome: str
    ativo: bool = True

@dataclass
class Digital(Base):
    tamanho_mb: int

# 6
@dataclass
class Chave:
    a: int

cache = {Chave(1): "resultado"}
```

### A4 — Qual opção atende? `[Aquecimento · ~10 min]`

Para cada requisito, diga qual parâmetro do decorador ou de `field()` resolve — e, quando houver, qual **não** resolve e por quê.

1. O objeto precisa servir de chave num dicionário.
2. O token de autenticação não pode aparecer no log.
3. Duas leituras do mesmo produto com contadores diferentes devem ser iguais.
4. O identificador interno é calculado, e ninguém deve passá-lo na criação.
5. Serão criados 5 milhões de objetos e a memória é apertada.
6. A lista de itens começa vazia em cada pedido.

---

## Aplicação

### AP1 — A refatoração `[Aplicação · ~20 min]`

Converta para `@dataclass`, preservando o comportamento:

```python
class Endereco:
    def __init__(self, rua, numero, cidade, cep, complemento=""):
        self.rua = rua
        self.numero = numero
        self.cidade = cidade
        self.cep = cep
        self.complemento = complemento

    def __repr__(self):
        return "Endereco(%r, %r, %r, %r, %r)" % (
            self.rua, self.numero, self.cidade, self.cep, self.complemento)

    def __eq__(self, outro):
        if not isinstance(outro, Endereco):
            return NotImplemented
        return (self.rua == outro.rua and self.numero == outro.numero
                and self.cidade == outro.cidade and self.cep == outro.cep)
```

Conte as linhas antes e depois. E responda: **a versão original tem um defeito** — o `__eq__` ignora um campo. Isso foi intencional ou esquecimento? Ao converter, o que você faz com ele?

### AP2 — O `field()` `[Aplicação · ~25 min]`

Escreva um `Usuario` com: `email`, `nome`, `senha_hash`, `ultimo_acesso` (padrão `None`), `tentativas_login` (padrão 0) e `permissoes` (conjunto vazio por padrão).

Requisitos: `senha_hash` fora do `__repr__`; `tentativas_login` e `ultimo_acesso` fora do `__eq__`; `permissoes` com valor inicial próprio em cada objeto; e `__post_init__` que normalize o e-mail para minúsculas e recuse e-mail sem `@`.

Depois, prove com código que dois usuários com o mesmo e-mail e tentativas diferentes são iguais, e que `repr(usuario)` não contém a senha.

### AP3 — Congelar de verdade `[Aplicação · ~20 min]`

Esta classe **parece** imutável:

```python
@dataclass(frozen=True)
class Cesta:
    dono: str
    produtos: list = field(default_factory=list)
```

Escreva um teste que demonstre os dois problemas: (a) o conteúdo muda; (b) o objeto não entra num `set`.

Depois corrija e mostre que a versão corrigida passa nos dois casos. Ao final, responda: e se um dos produtos dentro da tupla for, ele mesmo, um objeto mutável?

---

## Desafio

### D1 — O catálogo da Aurora `[Desafio · ~50 min]`

Modele `Produto`, `ItemPedido` e `Pedido` como dataclasses e escreva as duas pontas do fluxo: carregar do banco (módulo 03) e serializar para JSON.

**Requisitos:**

- `Produto` e `ItemPedido` congelados e **hasheáveis de verdade** — teste pondo-os num `set`.
- `Pedido` mutável, com `cliente`, `data`, `itens` e `total_centavos` **derivado**.
- Validação no `__post_init__`: quantidade positiva, preço não-negativo, categoria entre as quatro da Aurora.
- `codigo_fornecedor` fora do `__repr__`.
- `carregar_produtos(conexao)` que devolva `list[Produto]` a partir de um `SELECT` na tabela `produtos`.
- `para_json(pedido)` que devolva uma string JSON.

**As três perguntas que valem a nota:**

1. `Pedido.itens` deve ser `list` ou `tuple`? O que muda se `Pedido` for congelado?
2. `para_json` usa `asdict`? Consulte a §13 do capítulo e decida para um laço de 100 mil pedidos.
3. Validar que o SKU existe no catálogo **não** cabe no `__post_init__`. Por quê, e onde cabe?

---

## Mini projeto

### MP — O leitor de configuração `[Mini projeto · ~40 min]`

Um `Config` congelado com `host`, `porta`, `banco`, `usuario`, `senha`, `nivel_log` e `timeout_s`, todos com default sensato.

**Requisitos:**

- Construtor alternativo `Config.do_ambiente()` (04.08) lendo variáveis de ambiente.
- `__post_init__` que recuse porta fora de 1–65535 e `nivel_log` fora de `DEBUG/INFO/WARNING/ERROR`.
- `senha` fora do `__repr__` — e um teste que prove isso.
- Conversão explícita: variável de ambiente é string; `porta` e `timeout_s` são números.
- Nenhuma senha no código (§18.3 da spec): tudo vem do ambiente.

**Ao final, conte as linhas gastas só em conversão e validação.** Guarde o número: o 04.15 faz isso com uma declaração por campo, e essa comparação é o argumento a favor do Pydantic.
