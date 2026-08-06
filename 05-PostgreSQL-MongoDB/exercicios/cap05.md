# Exercícios — Capítulo 05.05: SQLAlchemy, visão geral e Core

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap05.md`](gabaritos/cap05.md).

> `pip install "SQLAlchemy>=2.0"`, e suba o laboratório: `python codigo/laboratorio.py`.

## Aquecimento

### A1 — Grava ou não grava? `[Aquecimento · ~10 min]`

```python
# 1
with engine.connect() as c:
    c.execute(text("UPDATE produtos SET ativo = false WHERE id = 1"))

# 2
with engine.begin() as c:
    c.execute(text("UPDATE produtos SET ativo = false WHERE id = 1"))

# 3
with engine.connect() as c:
    c.execute(text("UPDATE produtos SET ativo = false WHERE id = 1"))
    c.commit()

# 4
with engine.begin() as c:
    c.execute(text("UPDATE produtos SET ativo = false WHERE id = 1"))
    raise RuntimeError("erro")

# 5
c = engine.connect()
c.execute(text("UPDATE produtos SET ativo = false WHERE id = 1"))
c.close()

# 6
with psycopg.connect(URI) as c:
    c.cursor().execute("UPDATE produtos SET ativo = false WHERE id = 1")
```

### A2 — Preveja o estado do pool `[Aquecimento · ~10 min]`

Com `pool_size=3, max_overflow=2, pool_timeout=5`:

1. Quantas conexões existem logo depois de `create_engine`?
2. Depois de três `connect()` simultâneos?
3. Depois de cinco?
4. No sexto?
5. Ao devolver as cinco, quantas ficam guardadas?
6. Com quatro instâncias da aplicação, quantas conexões o banco pode receber?

### A3 — Ache o erro `[Aquecimento · ~12 min]`

```python
# 1
def listar():
    engine = sa.create_engine(URI)
    with engine.connect() as c:
        return c.execute(text("SELECT * FROM produtos")).all()

# 2
with engine.connect() as c:
    c.execute("SELECT 1")

# 3
with engine.connect() as c:
    r = c.execute(text("SELECT id FROM produtos"))
    print(len(r.all()), r.all()[0])

# 4
engine = sa.create_engine(URI, pool_size=100, max_overflow=100)

# 5
engine = sa.create_engine("postgresql://user:senha@host/banco")

# 6
with engine.connect() as c:
    c.execute(text(f"SELECT * FROM produtos WHERE nome = '{nome}'"))
```

### A4 — `text()` ou expressão? `[Aquecimento · ~8 min]`

1. Um `SELECT` com três `JOIN` e uma janela.
2. Um filtro opcional que só entra às vezes.
3. Um `INSERT ... ON CONFLICT DO UPDATE`.
4. Uma contagem com `WHERE` fixo.
5. Uma consulta que precisa rodar em PostgreSQL e SQLite.
6. Um `CREATE INDEX CONCURRENTLY`.

---

## Aplicação

### AP1 — Meça o pool `[Aplicação · ~25 min]`

Reproduza a medição da §3 com três cenários: abrindo de verdade, com pool, e na mesma conexão.

**As duas perguntas:** os seus três números guardam a mesma proporção? E o que muda se você apontar para um Postgres em outra máquina (ou num contêiner com rede)?

### AP2 — Dimensione o pool `[Aplicação · ~20 min]`

Um serviço com quatro instâncias, cada uma com 8 processos, atrás de um Postgres com `max_connections = 100`. As requisições duram 30 ms, e 20 ms delas são banco.

Escolha `pool_size`, `max_overflow` e `pool_timeout`, **e justifique cada número**. Inclua na conta as conexões de migração, do administrador e do painel de monitoramento.

**A pergunta que fecha:** o que acontece se você errar para mais? E para menos? Os dois erros têm sintomas diferentes — descreva os dois.

### AP3 — Do SQL para o Core `[Aplicação · ~30 min]`

Traduza três consultas do módulo 03 para expressões do Core, e imprima o SQL gerado de cada uma:

1. Receita por categoria (03.06).
2. Clientes sem pedido (03.08).
3. O produto mais vendido de cada mês (03.10).

**A pergunta que separa:** qual das três você deixaria em `text()`, e por quê?

---

## Desafio

### D1 — O pool sob pressão `[Desafio · ~50 min]`

Um programa que dispara N threads contra um pool de tamanho conhecido e reporta a curva de espera.

**Requisitos:**

- Pool com tamanho configurável.
- Cada thread mede quanto esperou para obter a conexão e quanto durou a consulta.
- Uma consulta deliberadamente lenta (`pg_sleep`) misturada com rápidas.
- Relatório com mínimo, mediana, p95 e máximo da espera.

**As três perguntas que valem a nota:**

1. A partir de quantas threads a espera deixa de ser zero? Bate com o limite do pool?
2. Como a consulta lenta afeta a espera das rápidas? Meça.
3. O que muda ao dobrar `pool_size`? E ao dobrar `max_overflow`? Por que os efeitos são diferentes?

---

## Mini projeto

### MP — A camada de acesso em Core `[Mini projeto · ~40 min]`

A camada de dados da Aurora, sem ORM.

**Requisitos:**

- Uma engine de módulo, a partir de variável de ambiente.
- Funções que recebem `Connection` e não a criam.
- Expressões do Core; `text()` só onde justificado por escrito.
- `fechar()` que chama `dispose()`.
- Um teste que prove que `criar_pedido` e `baixar_estoque` acontecem juntos ou não acontecem.

**E a pergunta que fecha:** por que as funções recebem `Connection` e não `Engine`? Descreva o que ficaria impossível na outra escolha.
