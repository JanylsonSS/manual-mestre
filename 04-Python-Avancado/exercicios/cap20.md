# Exercícios — Capítulo 04.20: Context managers

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap20.md`](gabaritos/cap20.md).

## Aquecimento

### A1 — A saída roda? `[Aquecimento · ~10 min]`

Dado este gerenciador, diga se `__exit__` roda em cada situação:

```python
class R:
    def __enter__(self): return self
    def __exit__(self, *a): print("saiu"); return None
```

1. O bloco termina normalmente.
2. O bloco faz `return`.
3. O bloco faz `break` dentro de um `for`.
4. O bloco levanta `ValueError`.
5. O bloco chama `sys.exit(3)`.
6. O bloco chama `os._exit(3)`.
7. O bloco entra num laço infinito e alguém aperta Ctrl-C.
8. O próprio `__enter__` levanta uma exceção.

### A2 — Preveja a saída `[Aquecimento · ~12 min]`

```python
# 1
class A:
    def __enter__(self): print("entra"); return 42
    def __exit__(self, *a): print("sai"); return None
with A() as x:
    print(x)

# 2
class B:
    def __enter__(self): return self
    def __exit__(self, *a): return True
with B():
    raise ValueError("some?")
print("cheguei aqui?")

# 3
with A(), A():
    print("corpo")

# 4
@contextlib.contextmanager
def g():
    print("antes")
    yield
    print("depois")
try:
    with g():
        raise RuntimeError()
except RuntimeError:
    print("peguei")

# 5
cm = g()
with cm: pass
with cm: pass

# 6
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE t (a)")
with con:
    con.execute("INSERT INTO t VALUES (1)")
print(con.execute("SELECT 1").fetchone())
```

### A3 — Ache o erro `[Aquecimento · ~12 min]`

```python
# 1
class Conexao:
    def __enter__(self):
        self.con = abrir()
        return self.con
    def __exit__(self, tipo, valor, rastro):
        self.con.close()
        return True

# 2
@contextlib.contextmanager
def bloqueio(trava):
    trava.acquire()
    yield
    trava.release()

# 3
arquivo = open("dados.csv")
with arquivo:
    processar(arquivo)
with arquivo:
    processar(arquivo)

# 4
def carregar(caminhos):
    abertos = []
    try:
        for c in caminhos:
            abertos.append(open(c))
        return [a.read() for a in abertos]
    finally:
        for a in abertos:
            a.close()

# 5
with sqlite3.connect("aurora.db") as con:
    con.execute("INSERT INTO pedidos VALUES (...)")

# 6
class Timer:
    def __enter__(self):
        self.inicio = datetime.now()
    def __exit__(self, *a):
        print(datetime.now() - self.inicio)
```

### A4 — Classe ou gerador? `[Aquecimento · ~10 min]`

Para cada caso, diga qual forma escolher e por quê.

1. Abrir e fechar uma conexão de banco.
2. Medir o tempo de um bloco e **guardar** o valor para uso posterior.
3. Silenciar um `FileNotFoundError` específico.
4. Abrir uma quantidade de arquivos que só se sabe em execução.
5. Um gerenciador que entra e sai dentro de um laço de dez milhões.
6. Mudar o diretório de trabalho e restaurá-lo.

---

## Aplicação

### AP1 — O cronômetro `[Aplicação · ~20 min]`

Escreva o `Cronometro` da §6.1 como classe, tipado, e teste-o.

Requisitos: guarda a duração em `self.ms`, acessível **depois** do bloco; funciona quando o bloco falha; usa `perf_counter` (04.18); e é **reutilizável** — o mesmo objeto pode entrar em dois `with`.

O teste do caso de erro é o que importa: verifique que `ms` foi preenchido **e** que a exceção subiu.

### AP2 — O estado restaurado `[Aplicação · ~25 min]`

Escreva `variavel_de_ambiente(nome, valor)`, que define uma variável e a restaura ao sair.

Requisitos: funciona quando a variável **já existia** (restaura o valor antigo) e quando **não existia** (remove); restaura em caso de exceção; e é tipado.

**A parte que separa** é o segundo caso. Escreva o teste que o cobre — e note que ele falha em quase toda primeira implementação.

### AP3 — A conexão certa `[Aplicação · ~20 min]`

Escreva um `banco(caminho)` que abra uma conexão SQLite, garanta `PRAGMA foreign_keys = ON` e a **feche** ao sair.

Requisitos: fecha mesmo em erro; e permite usar `with conexao:` por dentro, para transações.

Depois, **prove** as duas coisas: que a conexão está fechada depois do bloco (tente usá-la e capture o erro) e que uma transação interna faz `ROLLBACK` quando o corpo falha.

---

## Desafio

### D1 — A operação instrumentada `[Desafio · ~50 min]`

Construa `operacao(nome, **contexto)` — o gerenciador da §9 — e use-o para instrumentar um processamento em lote.

**Requisitos:**

- `INFO` na entrada e na saída, com duração por `perf_counter`.
- `log.exception` e relançamento em caso de erro.
- Contexto no `extra` em **todas** as mensagens.
- Aninhamento coerente.
- `mypy --strict` limpo.

**O teste que prova:** processe 5 itens, o terceiro falhando. Confira no log que os 5 têm entrada, que 4 têm saída, e que o terceiro tem o rastro.

**As três perguntas que valem a nota:**

1. Seu gerenciador é reutilizável? Teste usando o **mesmo objeto** em dois `with` e explique o resultado.
2. Aninhe duas `operacao` e faça a interna falhar. **Quantas mensagens de erro aparecem no log — e quantas deveriam?** Corrija.
3. O que o seu `__exit__` devolve? O que aconteceria se devolvesse `True`?

---

## Mini projeto

### MP — A caixa de ferramentas `[Mini projeto · ~40 min]`

Um módulo `contextos.py` com cinco gerenciadores tipados e testados:

- `cronometro(rotulo)` — mede e registra, mesmo em erro.
- `pasta_temporaria()` — cria e apaga, inclusive o conteúdo.
- `variavel_de_ambiente(nome, valor)` — define e **restaura**.
- `nivel_de_log(logger, nivel)` — muda e restaura.
- `banco(caminho)` — abre, aplica `PRAGMA foreign_keys = ON`, fecha.

Cada um com teste que verifique o estado **depois** do bloco, no caminho feliz **e** com exceção.

**E a pergunta que fecha:** três dos cinco precisam guardar o estado anterior para restaurá-lo. Um deles tem um caso de borda que os outros não têm — a diferença entre "o valor era outro" e "o valor **não existia**".

Qual é, e como o seu código distingue os dois? Testar isso exige um caso específico; escreva-o.
