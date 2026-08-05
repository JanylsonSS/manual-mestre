# Exercícios — Capítulo 04.15: Pydantic

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap15.md`](gabaritos/cap15.md).

> Instale uma vez: `pip install pydantic pydantic-settings`.

## Aquecimento

### A1 — Passa ou não? `[Aquecimento · ~10 min]`

Dado o modelo:

```python
class P(BaseModel):
    preco_centavos: int = Field(gt=0)
    nome: str = Field(min_length=2)
    ativo: bool
    data: date
```

Para cada valor, diga se passa — e, se passar, **com que valor final**.

1. `preco_centavos="8990"` · 2. `preco_centavos=89.90` · 3. `preco_centavos=True` · 4. `preco_centavos=0`
5. `nome=42` · 6. `ativo="sim"` · 7. `ativo="yes"` · 8. `data="15/07/2026"`

### A2 — Preveja a saída `[Aquecimento · ~12 min]`

```python
# 1
class M1(BaseModel):
    nome: str
    tags: list[str] = []
a, b = M1(nome="a"), M1(nome="b")
a.tags.append("x")
a; b

# 2
class M2(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nome: str
M2(nome="Mouse", cor="preto")

# 3
class M3(BaseModel):
    valor: int
    @field_validator("valor")
    @classmethod
    def dobrar(cls, v: int) -> int:
        v * 2
M3(valor=5)

# 4
class M4(BaseModel):
    model_config = ConfigDict(frozen=True)
    nome: str
len({M4(nome="a"), M4(nome="a")})

# 5
class M5(BaseModel):
    a: int
    b: int
    @model_validator(mode="after")
    def a_menor_que_b(self) -> "M5":
        if self.a >= self.b:
            raise ValueError("a deve ser menor que b")
        return self
M5(a="10", b=5)

# 6
class M6(BaseModel):
    n: int
class Filho(M6):
    n: str
Filho(n=42)
```

### A3 — Ache o erro `[Aquecimento · ~15 min]`

Alguns falham na hora; **outros funcionam e estão errados**. Diga qual é qual.

```python
# 1
class Item(BaseModel):
    desconto: int = 0
    quantidade: int = 1
    preco: int = 1

    @field_validator("desconto")
    @classmethod
    def cabe(cls, v, info):
        total = info.data["quantidade"] * info.data["preco"]
        if v > total:
            raise ValueError("desconto maior que o total")
        return v

# 2
class Config(BaseModel):
    hosts: list[str] = []

# 3
class Cliente(BaseModel):
    nome: str
    observacao: str | None

# 4
class Produto(BaseModel):
    nome: str

    @field_validator("nome")
    @classmethod
    def limpar(cls, v: str) -> str:
        v.strip()

# 5
class Pedido(BaseModel):
    cliente: str
    total_centavos: int = Field(ge=0)

pedido = Pedido(cliente="Ana", total_centavos=5000)
pedido.total_centavos = -1

# 6
class Endereco(BaseModel):
    cep: str
```

### A4 — `Field`, validador ou config? `[Aquecimento · ~10 min]`

Para cada requisito, diga o que resolve — e, quando houver, o que **não** resolve.

1. O preço precisa ser maior que zero.
2. O SKU deve ser guardado sempre em maiúsculas.
3. O desconto não pode passar do total do item.
4. Um campo desconhecido no JSON deve gerar erro, não sumir.
5. O CEP tem oito dígitos, com ou sem hífen.
6. O objeto não deve poder ser alterado depois de criado.

---

## Aplicação

### AP1 — A refatoração `[Aplicação · ~20 min]`

Pegue a validação escrita à mão do mini projeto do 04.14 (a versão com `dict[str, object]` e um `isinstance` por campo) e substitua por um modelo Pydantic.

Requisitos: mesmo comportamento nos casos válidos; `extra="forbid"`; e um teste que passe um registro com **três** defeitos e mostre os três de uma vez.

**Conte as linhas antes e depois**, e responda: qual comportamento você **ganhou** sem pedir?

### AP2 — A fronteira aninhada `[Aplicação · ~25 min]`

Modele um `PedidoEntrada` com `cliente`, `data`, `endereco` (objeto) e `itens` (lista de objetos).

Requisitos: `extra="forbid"` em todos; CEP com oito dígitos, com ou sem hífen, normalizado para o formato com hífen; mínimo de um item; quantidade positiva; e um `@computed_field` com o total.

Depois, envie um JSON com defeitos em **três níveis** — um no pedido, um no endereço e um no segundo item — e imprima o `loc` de cada erro.

**A pergunta que importa:** o que o `loc` do erro do segundo item mostra, e por que essa tupla vale mais que a mensagem?

### AP3 — A configuração, finalmente `[Aplicação · ~20 min]`

Volte ao mini projeto do 04.13 (o `Config` com sete campos, treze linhas de conversão e validação) e reescreva-o com `BaseSettings`.

Requisitos: `env_prefix`; `Literal` para o nível de log; faixa da porta declarada; senha fora do `repr`; `extra="forbid"`; e nenhuma senha no código.

**Conte de novo as linhas**, e responda: as mensagens de erro melhoraram? Em quê, exatamente?

---

## Desafio

### D1 — A alfândega da Aurora `[Desafio · ~50 min]`

Construa a fronteira completa de um endpoint de criação de pedido, com **duas camadas**.

**Requisitos:**

- `PedidoEntrada`, `ItemEntrada`, `EnderecoEntrada` — modelos Pydantic com `extra="forbid"`.
- Validação: quantidade positiva, preço não-negativo, CEP de oito dígitos, mínimo um item, categoria entre as quatro da Aurora.
- Conversão explícita para `Pedido`, `ItemPedido`, `Endereco` — dataclasses **congeladas** (04.13).
- `processar(json_cru: str) -> Pedido | list[dict]` — devolve o pedido ou a lista de erros.
- `mypy --strict` limpo.

**As três perguntas que valem a nota:**

1. Onde ficou a fronteira? E o que aconteceria se o `Pedido` de dentro fosse o próprio modelo Pydantic?
2. Você validou alguma coisa **duas** vezes? Qual, e por quê?
3. "No máximo 50 unidades por item" é regra de validação ou regra de negócio? Decida pela pergunta: **essa regra pode mudar sem que o formato do dado mude?**

---

## Mini projeto

### MP — O importador de CSV `[Mini projeto · ~40 min]`

Um script que leia um CSV de produtos e produza `validos.json` e `rejeitados.json`.

**Requisitos:**

- Modelo com `extra="forbid"` e restrições em todos os campos.
- Cada linha rejeitada aparece no relatório com **número da linha, campo e mensagem**.
- Um validador de campo que converta preço em reais com vírgula (`"89,90"`) para centavos.
- Resumo final com a contagem por tipo de erro.

**O CSV de entrada deve ter, de propósito:** uma linha com preço vazio, uma com categoria inexistente, uma com coluna a mais, uma com quantidade negativa e uma perfeitamente válida.

**E a pergunta que fecha:** sua contagem por tipo de erro usou o campo `type` do `errors()` ou a mensagem em texto? Um dos dois é estável entre versões da biblioteca e o outro não. Descubra qual **antes** de escolher — e diga como descobriu.
