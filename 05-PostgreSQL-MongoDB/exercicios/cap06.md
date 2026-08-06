# Exercícios — Capítulo 05.06: ORM, modelos declarativos

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap06.md`](gabaritos/cap06.md).

## Aquecimento

### A1 — Qual o DDL? `[Aquecimento · ~12 min]`

Escreva a coluna que cada linha gera, no PostgreSQL:

```python
# 1
nome: Mapped[str]
# 2
apelido: Mapped[str | None] = mapped_column(Text)
# 3
criado_em: Mapped[dt.datetime]
# 4
criado_em: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True))
# 5
preco: Mapped[Decimal] = mapped_column(Numeric(12, 2))
# 6
ativo: Mapped[bool] = mapped_column(default=True)
# 7
ativo: Mapped[bool] = mapped_column(server_default="true")
# 8
id: Mapped[int] = mapped_column(primary_key=True)
```

### A2 — O que `create_all` faz? `[Aquecimento · ~10 min]`

Em cada situação, diga o que acontece e se há aviso:

1. A tabela não existe.
2. A tabela existe, idêntica ao modelo.
3. Você acrescentou uma coluna ao modelo.
4. Você mudou o tipo de uma coluna no modelo.
5. Você acrescentou um `Index` ao `__table_args__`.
6. Você removeu uma coluna do modelo.

### A3 — Ache o erro `[Aquecimento · ~12 min]`

```python
# 1
class Pedido(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    criado_em: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now())

# 2
class Cliente(Base):
    __tablename__ = "clientes"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(Text, unique=True)
    # (o banco tem clientes sem e-mail)

# 3
class Produto(Base):
    __tablename__ = "produtos"
    id: Mapped[int] = mapped_column(primary_key=True)
    preco: Mapped[float]

# 4
if Produto.ativo == True:
    print("tem produto ativo")

# 5
sessao.scalars(select(Produto).where(Produto.preco > 100))
# (preco é uma @property)

# 6
class Item(Base):
    __tablename__ = "itens"
    id: Mapped[int] = mapped_column(primary_key=True)
    quantidade: Mapped[int] = mapped_column(CheckConstraint("quantidade > 0"))
```

### A4 — `default`, `server_default` ou os dois? `[Aquecimento · ~8 min]`

1. Data de criação de um pedido.
2. Um `uuid` gerado pela aplicação.
3. `ativo = true` num cadastro.
4. Um contador que começa em zero e é somado por outro serviço.
5. Um campo `versao` usado para bloqueio otimista.
6. Um `slug` derivado do nome, calculado em Python.

---

## Aplicação

### AP1 — Modele um schema dado `[Aplicação · ~30 min]`

Escreva os modelos para: `fornecedores` (id, nome, cnpj único, ativo), `notas_fiscais` (id, fornecedor, número, emitida em, valor total) e `itens_nota` (id, nota, descrição, quantidade, valor unitário).

**Requisitos:** tipos corretos para dinheiro e para instantes; restrições nomeadas; `NOT NULL` decidido pela anotação; e o DDL impresso e conferido.

### AP2 — A conferência como teste `[Aplicação · ~25 min]`

Escreva `test_modelos_batem_com_o_banco` comparando **nomes e tipos**.

**Requisitos:** compilar os dois lados com o mesmo dialeto; falhar com mensagem que diga qual coluna e qual diferença; e cobrir também colunas que existem no banco e não no modelo.

**A pergunta que fecha:** o que o seu teste **não** detecta? Liste ao menos três divergências possíveis que passam.

### AP3 — Conserte o modelo divergente `[Aplicação · ~20 min]`

Dado um banco com `criado_em timestamptz`, `preco numeric(12,2)` e `email text NULL`, e um modelo com `Mapped[dt.datetime]`, `Mapped[float]` e `Mapped[str]`, conserte as três — e descreva o sintoma que cada divergência produziria em produção.

---

## Desafio

### D1 — Convenção de nomes `[Desafio · ~45 min]`

Aplique uma `naming_convention` ao `MetaData` e faça todas as restrições ganharem nome previsível.

**Requisitos:** convenção para `ix`, `uq`, `ck`, `fk` e `pk`; o DDL antes e depois; e a lista de restrições cujo nome mudou.

**As três perguntas:**

1. Por que restrição sem nome é um problema que só aparece na primeira migração?
2. O que acontece ao adotar a convenção num banco que **já** tem tabelas criadas?
3. A convenção do `ck` usa `%(constraint_name)s`. O que isso exige de quem escreve o `CheckConstraint`?

---

## Mini projeto

### MP — O catálogo com JSONB `[Mini projeto · ~40 min]`

Una este capítulo com o 05.03: a tabela `produtos` com coluna `atributos jsonb`.

**Requisitos:** `Mapped[dict[str, Any]]` mapeado para `JSONB`; `CHECK` de `jsonb_typeof`; índice GIN declarado; e a conferência do AP2 passando.

**E a pergunta que fecha:** o modelo passou a usar um tipo específico do PostgreSQL. Quando isso é aceitável e quando não é? Dê um exemplo concreto de cada caso.
