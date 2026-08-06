# Exercícios — Capítulo 05.04: Python + Postgres com psycopg

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap04.md`](gabaritos/cap04.md).

> Suba o laboratório antes: `python codigo/laboratorio.py`.

## Aquecimento

### A1 — Vulnerável ou não? `[Aquecimento · ~12 min]`

```python
# 1
cursor.execute("SELECT * FROM produtos WHERE id = %s", (id_produto,))

# 2
cursor.execute(f"SELECT * FROM produtos WHERE id = {id_produto}")

# 3
cursor.execute("SELECT * FROM produtos WHERE nome = '%s'" % nome)

# 4
cursor.execute("SELECT * FROM produtos WHERE id = %s" % id_produto)

# 5
cursor.execute("SELECT * FROM %s" % tabela)   # tabela vem de uma lista fixa

# 6
cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(tabela)))

# 7
cursor.execute("SELECT * FROM produtos WHERE nome LIKE %s", ("%" + termo + "%",))

# 8
cursor.execute("SELECT * FROM produtos ORDER BY " + coluna)
```

Para cada um: vulnerável, seguro, ou "depende"? Se depender, de quê?

### A2 — Preveja o resultado `[Aquecimento · ~12 min]`

```python
# 1
cursor.execute("SELECT %s", ("ana",))            # e o tipo devolvido?
# 2
cursor.execute("SELECT %s", ({"a": 1},))
# 3
cursor.execute("SELECT %s::numeric = 19.90", (0.1 + 19.8,))
# 4
cursor.execute("SELECT count(*) FROM produtos WHERE id = %s", ("1"))
# 5
with psycopg.connect(URI) as c:
    with c.cursor() as k:
        k.execute("UPDATE produtos SET ativo = false WHERE id = 1")
# o produto 1 continua ativo?
# 6
cursor.execute("SELECT now()::timestamptz")      # e o tzinfo?
```

### A3 — Ache o erro `[Aquecimento · ~15 min]`

```python
# 1
def buscar(termo):
    cursor.execute("SELECT * FROM produtos WHERE nome ILIKE '%" + termo + "%'")
    return cursor.fetchall()

# 2
def salvar_total(total: float):
    cursor.execute("INSERT INTO vendas (total) VALUES (%s)", (total,))

# 3
def listar(ordem):
    cursor.execute(sql.SQL("SELECT * FROM produtos ORDER BY {}")
                   .format(sql.Identifier(ordem)))

# 4
def criar(email):
    try:
        cursor.execute("INSERT INTO clientes (email) VALUES (%s)", (email,))
    except psycopg.Error:
        return {"erro": "erro interno"}

# 5
def importar(linhas):
    for linha in linhas:                     # 400 mil linhas
        cursor.execute("INSERT INTO carga VALUES (%s, %s)", linha)

# 6
def conectar():
    logger.info("conectando em %s", os.environ["DATABASE_URL"])
    return psycopg.connect(os.environ["DATABASE_URL"])
```

### A4 — Qual `row_factory`? `[Aquecimento · ~8 min]`

1. Um script de uma linha que conta registros.
2. Um endpoint que devolve JSON.
3. Uma função que calcula frete a partir do produto.
4. Um relatório com 40 colunas.
5. Uma comparação entre duas linhas campo a campo.
6. Uma carga que só passa dados adiante para outro sistema.

---

## Aplicação

### AP1 — Conserte a camada de acesso `[Aplicação · ~30 min]`

Pegue as seis funções do A3 e reescreva todas.

**Requisitos:** nenhuma f-string perto de SQL; `Decimal` onde o banco tem `numeric`; erro de integridade traduzido; e nenhum segredo no log.

**A pergunta que fecha:** a função 1 usa `ILIKE` com `%` em volta. Depois de parametrizada, onde ficam os sinais de porcentagem — no SQL ou no valor? E por quê?

### AP2 — Filtros opcionais com ordenação `[Aplicação · ~30 min]`

Uma função `listar_produtos(categoria=None, preco_max=None, ordenar_por="nome", ordem="asc")`.

**Requisitos:** filtros que só entram quando presentes; ordenação por lista branca; `ASC`/`DESC` validado; e `LIMIT`/`OFFSET` parametrizados.

**A pergunta que separa:** por que `ASC`/`DESC` não pode ir em `sql.Identifier`? Qual o instrumento certo?

### AP3 — Meça as três inserções `[Aplicação · ~25 min]`

Reproduza a medição da §6.7 na sua máquina, com 20 mil linhas.

**Requisitos:** os três métodos; `TRUNCATE` entre eles; e a confirmação de que os três inseriram a mesma quantidade.

**As duas perguntas:** o seu `copy` foi quantas vezes mais rápido? E o que acontece com o tempo do laço se você tirar o `commit` do fim e comitar linha a linha?

---

## Desafio

### D1 — Repositório tipado `[Desafio · ~60 min]`

Um `RepositorioProdutos` com `buscar`, `listar`, `criar` e `atualizar`.

**Requisitos:**

- Devolve dataclasses, não tuplas nem dicionários.
- Traduz `UniqueViolation` e `ForeignKeyViolation` em exceções de domínio.
- `Decimal` para valores monetários, em toda a fronteira.
- A conexão entra pelo construtor — o repositório não a cria.
- Testes que provem a tradução de erro.

**As três perguntas que valem a nota:**

1. Quais erros do banco você traduziu e quais deixou subir? Justifique a linha divisória.
2. O repositório faz `commit`? Argumente pelos dois lados.
3. Como você testa a tradução de `UniqueViolation` sem depender de dado deixado por outro teste?

---

## Mini projeto

### MP — O importador do fornecedor `[Mini projeto · ~50 min]`

Um CSV com 200 mil produtos, alguns inválidos.

**Requisitos:**

- Carga com `COPY`.
- Validação, já que `COPY` é tudo-ou-nada.
- Arquivo de rejeitados com o número da linha e o motivo.
- Relatório final: aceitas, rejeitadas, tempo.
- Rodar duas vezes não duplicar nada.

**E a pergunta que fecha:** você escolheu validar em Python antes, ou carregar numa tabela de escala com tudo em `text` e validar com SQL? Descreva um cenário em que a sua escolha é a pior das duas.
