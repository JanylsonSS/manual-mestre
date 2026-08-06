# Gabarito — Capítulo 05.06: ORM, modelos declarativos

Leia depois de tentar. Enunciados em [`../cap06.md`](../cap06.md).

> Execução real: SQLAlchemy 2.0.51 contra PostgreSQL 16.2.

## A1 — Qual o DDL?

O DDL de todas as oito, gerado de uma vez:

```sql
CREATE TABLE t_a1 (
	id SERIAL NOT NULL,
	nome VARCHAR NOT NULL,
	apelido TEXT,
	criado_a TIMESTAMP WITHOUT TIME ZONE NOT NULL,
	criado_b TIMESTAMP WITH TIME ZONE NOT NULL,
	preco NUMERIC(12, 2) NOT NULL,
	ativo_a BOOLEAN NOT NULL,
	ativo_b BOOLEAN DEFAULT 'true' NOT NULL,
	PRIMARY KEY (id)
)
```

| # | Anotação | Coluna |
|---|---|---|
| 1 | `Mapped[str]` | `VARCHAR NOT NULL` |
| 2 | `Mapped[str \| None]` com `Text` | `TEXT` (aceita nulo) |
| 3 | `Mapped[datetime]` | `TIMESTAMP WITHOUT TIME ZONE NOT NULL` |
| 4 | com `DateTime(timezone=True)` | `TIMESTAMP WITH TIME ZONE NOT NULL` |
| 5 | `Mapped[Decimal]` com `Numeric(12,2)` | `NUMERIC(12, 2) NOT NULL` |
| 6 | `default=True` | `BOOLEAN NOT NULL` — **sem `DEFAULT`** |
| 7 | `server_default="true"` | `BOOLEAN DEFAULT 'true' NOT NULL` |
| 8 | `primary_key=True` em `Mapped[int]` | `SERIAL NOT NULL` |

**O par 6/7 é o exercício.** As duas linhas parecem equivalentes e produzem DDL diferente: o `default` do Python **não aparece no `CREATE TABLE`**. Um `INSERT` que não passe pelo ORM deixa a coluna sem valor — e como ela é `NOT NULL`, o `INSERT` falha.

**O 3 é o defeito que o próprio manual cometeu** (05.06/§6.3): `Mapped[datetime]` sozinho gera o tipo sem fuso.

**E o 8 merece nota:** `Mapped[int]` com `primary_key=True` vira `SERIAL`, ou seja, o SQLAlchemy assume que o banco gera o valor. Se a tabela real não tiver sequência, o `INSERT` do ORM falha com `null value in column "id"` — que foi exatamente o erro que apareceu ao escrever o 05.07.

## A2 — O que `create_all` faz?

| # | Situação | O que acontece | Avisa? |
|---|---|---|---|
| 1 | Tabela não existe | `CREATE TABLE` | — |
| 2 | Tabela idêntica | nada | não |
| 3 | Coluna nova no modelo | **nada** | **não** |
| 4 | Tipo mudou no modelo | **nada** | **não** |
| 5 | `Index` novo | **nada** | **não** |
| 6 | Coluna removida do modelo | **nada** | **não** |

Medido para os casos 3 e 5:

```
colunas no banco:                ['id', 'moeda', 'valor', 'observacao',
                                  'registrada_em']
depois de acrescentar 'fonte':   ['id', 'moeda', 'valor', 'observacao',
                                  'registrada_em']

índices declarados:              [('produtos_categoria_idx', ['categoria'])]
índices que existem no banco:    []
```

**A coluna "Avisa?" é a resposta inteira.** `create_all` verifica **existência de tabela** e nada mais. Cinco das seis situações são divergências silenciosas, e a única forma de descobri-las é a conferência do AP2 — ou uma falha em produção.

## A3 — Ache o erro

**1. `default=dt.datetime.now()` com parênteses.** A função foi **chamada na definição da classe**, e o valor congelou no instante do `import`. Todos os pedidos recebem a mesma data — a do momento em que o processo subiu. É o mesmo defeito do argumento padrão mutável do 04.01. Correção: `default=dt.datetime.now` (sem parênteses) ou, melhor, `server_default=func.now()` com `DateTime(timezone=True)`.

**2. `Mapped[str]` numa coluna que aceita nulo.** O modelo gera `NOT NULL` e o banco tem nulos. O `create_all` não corrige (A2.4), então a tabela continua aceitando — e o **`mypy` passa a mentir**: ele garante `str` e o valor chega `None`, produzindo `AttributeError` em `cliente.email.lower()`. Correção: `Mapped[str | None]`.

**3. `Mapped[float]` para preço.** `DOUBLE PRECISION` para dinheiro, o defeito do 05.03/§6.1. Correção: `Mapped[int]` de centavos, ou `Mapped[Decimal]` com `Numeric(12,2)`.

**4. `if Produto.ativo == True`.** Medido:

```
Produto.ativo == True      bool = False    tipo = BinaryExpression
Produto.nome != 'x'        bool = True
Produto.id > 5             bool -> TypeError: Boolean value of this clause
                                             is not defined
```

**O `if` nunca entra**, porque o `__bool__` da expressão compara identidade. Com `!=` ele sempre entraria. Só os operadores de ordem falham alto.

**5. Filtrar por `@property`.** `preco` não é coluna e não existe para o banco. O erro é de compilação da consulta. Correção: filtrar por `preco_centavos`, ou usar `hybrid_property`.

**6. `CheckConstraint` dentro de `mapped_column`.** Este **funciona**, e é o item que quebra a expectativa:

```sql
quantidade INTEGER NOT NULL CHECK (quantidade > 0)
```

O `CHECK` sai como restrição **de coluna**, sem nome. O defeito não é sintático: é a ausência de nome (D1) e a impossibilidade de escrever uma restrição que envolva duas colunas. Correção: `__table_args__` com `name=`.

## A4 — `default`, `server_default` ou os dois?

| # | Caso | Escolha |
|---|---|---|
| 1 | Criação de pedido | **`server_default=func.now()`** |
| 2 | `uuid` da aplicação | **`default`** — quem gera é o Python |
| 3 | `ativo = true` | **os dois** |
| 4 | Contador somado por outro serviço | **`server_default="0"`** |
| 5 | `versao` para bloqueio otimista | **os dois**, e `version_id_col` |
| 6 | `slug` calculado em Python | **`default`** |

**O 4 é o critério em estado puro:** o valor precisa existir para quem escreve **por fora**, e só `server_default` alcança esse caminho.

**E o 2 é o inverso:** se a regra de geração está em Python (um `uuid` com prefixo, por exemplo), `server_default` não tem como reproduzi-la.

**O 3 pede os dois** porque `ativo` é o tipo de campo que aparece em migração de carga: `INSERT INTO clientes (id, nome) SELECT ...` precisa de um padrão do servidor, e o código Python fica mais legível com o padrão declarado ali também.

## AP1 — Modele um schema dado

O ponto do exercício está em três decisões, e não no volume de código:

```python
class NotaFiscal(Base):
    __tablename__ = "notas_fiscais"

    id: Mapped[int] = mapped_column(primary_key=True)
    fornecedor_id: Mapped[int] = mapped_column(ForeignKey("fornecedores.id"))
    numero: Mapped[str] = mapped_column(Text)
    emitida_em: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True))
    valor_total_centavos: Mapped[int]

    __table_args__ = (
        UniqueConstraint("fornecedor_id", "numero",
                         name="uq_notas_fornecedor_numero"),
        CheckConstraint("valor_total_centavos >= 0",
                        name="ck_notas_valor_nao_negativo"),
    )
```

**O `numero` é `text` e não `integer`** — nota fiscal tem zeros à esquerda e às vezes série junto, e ninguém soma número de nota. É o mesmo raciocínio do CPF no 05.03/A1.

**A unicidade é composta:** o número se repete entre fornecedores diferentes. Declarar `unique=True` só em `numero` recusaria notas legítimas.

**E `cnpj` é `text` com `CHECK` de formato**, pelo mesmo motivo do `numero`.

## AP2 — A conferência como teste

```python
def test_modelos_batem_com_o_banco(engine):
    inspetor = sa.inspect(engine)
    problemas = []
    for modelo in (Cliente, Produto, Pedido, ItemPedido):
        tabela = modelo.__tablename__
        no_banco = {c["name"]: c["type"].compile(engine.dialect)
                    for c in inspetor.get_columns(tabela)}
        no_modelo = {c.name: c.type.compile(engine.dialect)
                     for c in modelo.__table__.columns}
        for nome in set(no_banco) | set(no_modelo):
            if nome not in no_modelo:
                problemas.append("%s.%s só no banco" % (tabela, nome))
            elif nome not in no_banco:
                problemas.append("%s.%s só no modelo" % (tabela, nome))
            elif no_banco[nome] != no_modelo[nome]:
                problemas.append("%s.%s: banco=%s modelo=%s"
                                 % (tabela, nome, no_banco[nome],
                                    no_modelo[nome]))
    assert not problemas, "\n".join(problemas)
```

**Compilar os dois lados com o mesmo dialeto é obrigatório**, e a primeira versão do capítulo errou nisso: `str(tipo)` de um lado e `compile()` do outro geraram uma divergência falsa entre `TIMESTAMP` e `TIMESTAMP WITH TIME ZONE`.

**A pergunta que fecha: o que este teste não detecta?** Ao menos cinco coisas:

1. **`NOT NULL`** — a nulidade não está sendo comparada, e o A3.2 é exatamente esse caso.
2. **Restrições `CHECK`** — o modelo pode declarar uma que o banco não tem.
3. **Índices** — a §6.7 mostrou um índice declarado e ausente.
4. **Sequência de identidade** — foi o erro que derrubou o 05.07.
5. **`server_default`** — presente no modelo e ausente na coluna.

**A conclusão honesta é que a conferência é uma rede com furos grandes**, e o instrumento que fecha todos eles é o `alembic revision --autogenerate` do 05.10, comparando `MetaData` com o banco.

## AP3 — Conserte o modelo divergente

| Divergência | Sintoma em produção |
|---|---|
| `Mapped[datetime]` contra `timestamptz` | Grava e lê convertendo em silêncio: um `datetime` ciente vira ingênuo na ida, e comparar dois registros de fusos diferentes dá diferença de horas — o defeito do 04.18 entrando pelo modelo. |
| `Mapped[float]` contra `numeric(12,2)` | O `psycopg` devolve `Decimal` e o `mypy` promete `float`. As contas passam a misturar os dois, e `Decimal + float` levanta `TypeError` — em produção, na primeira soma. |
| `Mapped[str]` contra `text NULL` | O `mypy` garante `str` e o valor chega `None`. `cliente.email.lower()` quebra com `AttributeError` no primeiro cliente sem e-mail. |

**Os três sintomas têm a mesma forma:** o modelo faz uma promessa que o banco não cumpre, e a quebra acontece longe da declaração.

## D1 — Convenção de nomes

```python
conv = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=conv)
```

O DDL que sai:

```sql
CREATE TABLE t_conv (
	id SERIAL NOT NULL,
	email TEXT NOT NULL,
	qtd INTEGER NOT NULL,
	dados JSONB NOT NULL,
	CONSTRAINT pk_t_conv PRIMARY KEY (id),
	CONSTRAINT ck_t_conv_qtd_positiva CHECK (qtd > 0),
	CONSTRAINT uq_t_conv_email UNIQUE (email)
)
```

**1. Por que só aparece na primeira migração.** Enquanto você só cria tabelas, o nome não importa: o `CREATE TABLE` funciona com ou sem ele. O problema surge quando o Alembic precisa **remover** uma restrição — `ALTER TABLE ... DROP CONSTRAINT ?` exige o nome, e o gerado pelo PostgreSQL depende da ordem das colunas e pode diferir entre ambientes.

**2. Adotar num banco que já existe.** A convenção afeta apenas objetos **novos**. As restrições existentes mantêm os nomes antigos, e o modelo passa a discordar do banco em algo que a conferência do AP2 nem olha. A correção é uma migração de renomeação, escrita à mão, com um `ALTER TABLE ... RENAME CONSTRAINT` por objeto — e o nome antigo precisa ser lido do banco de cada ambiente.

**3. O que `%(constraint_name)s` exige.** Que todo `CheckConstraint` seja declarado **com `name=`**. Sem isso, o SQLAlchemy levanta erro ao montar o nome — o que é uma boa notícia: a convenção transforma "esqueci de nomear" em falha imediata, em vez de nome gerado silenciosamente.

## MP — O catálogo com JSONB

```python
class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(Text)
    categoria: Mapped[str] = mapped_column(Text)
    preco_centavos: Mapped[int]
    atributos: Mapped[dict[str, Any]] = mapped_column(
        JSONB, nullable=False, server_default="{}")

    __table_args__ = (
        CheckConstraint("jsonb_typeof(atributos) = 'object'",
                        name="ck_produtos_atributos_objeto"),
        Index("ix_produtos_atributos", "atributos",
              postgresql_using="gin"),
    )
```

`Mapped[dict[str, Any]]` **não** vira `JSONB` sozinho: sem `mapped_column(JSONB)` o SQLAlchemy não sabe qual dos tipos JSON usar, e o `JSONB` vem do dialeto `sqlalchemy.dialects.postgresql`.

**A pergunta que fecha: quando o tipo específico é aceitável?**

**É aceitável** quando o banco é uma decisão de longo prazo e o recurso não tem substituto — que é o caso do `JSONB` com índice GIN. Trocar de banco nessa situação exigiria remodelar de qualquer forma, e fingir portabilidade só custa desempenho.

**Não é aceitável** quando o mesmo modelo precisa rodar em SQLite nos testes e PostgreSQL em produção. Aí o `JSONB` quebra a suíte — e a saída é `JSON().with_variant(JSONB, "postgresql")`, que usa o tipo genérico em SQLite e o específico no Postgres.

**O exemplo concreto de cada lado:** um sistema interno que roda em Postgres há oito anos e vai continuar — use `JSONB` sem culpa. Uma biblioteca distribuída que os usuários apontam para o banco deles — não use, ou use com variante.
