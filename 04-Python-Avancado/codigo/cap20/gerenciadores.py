"""Context managers: o que precisa acontecer mesmo quando dá errado.

Este arquivo abre a Caixa-preta 2 do 04.12 — `__enter__` e `__exit__`.

Seis cenas:
    [1] o problema, e o `try/finally` que o resolve escrevendo demais
    [2] o protocolo: `__enter__` e `__exit__`
    [3] `__exit__` devolvendo `True` ENGOLE a exceção
    [4] `@contextmanager` — e o `try/finally` que não pode faltar dentro
    [5] o `with` do `sqlite3` NÃO fecha a conexão
    [6] `ExitStack`, `suppress`, `closing` e o custo de cada forma

Uso:
    python codigo/cap20/gerenciadores.py
    mypy --strict codigo/cap20/gerenciadores.py
"""

import contextlib
import sqlite3
import tempfile
import timeit
from collections.abc import Iterator
from pathlib import Path
from types import TracebackType


# ---------------------------------------------------------------
# [2] O protocolo, escrito à mão. `__enter__` devolve o que vai
#     para o `as`; `__exit__` recebe a exceção — ou três `None`.
# ---------------------------------------------------------------
class Cronometro:
    """Mede quanto tempo o bloco levou, mesmo se ele falhar."""

    def __init__(self, rotulo: str) -> None:
        self.rotulo = rotulo
        self.ms = 0.0
        self._inicio = 0.0

    # `-> "Cronometro"` entre aspas: a classe ainda não terminou de
    # existir quando a anotação é avaliada (04.14 §6.6). No Python
    # 3.11+ existe `typing.Self`, que diz o mesmo sem repetir o nome.
    def __enter__(self) -> "Cronometro":
        # perf_counter, e não datetime.now() — 04.18 §6.8.
        self._inicio = timeit.default_timer()
        return self

    def __exit__(self, tipo: type[BaseException] | None,
                 valor: BaseException | None,
                 rastro: TracebackType | None) -> None:
        self.ms = (timeit.default_timer() - self._inicio) * 1000
        estado = "falhou (%s)" % tipo.__name__ if tipo else "ok"
        print("    %-14s %6.2f ms · %s" % (self.rotulo, self.ms, estado))
        # Devolver None (falso) deixa a exceção seguir. Ver cena [3].


# ---------------------------------------------------------------
# [3] O mesmo protocolo, com uma linha diferente — e um efeito
#     que quase ninguém espera.
# ---------------------------------------------------------------
class Engole:
    """Errado de propósito: `__exit__` devolve True."""

    def __enter__(self) -> "Engole":
        return self

    def __exit__(self, tipo: type[BaseException] | None,
                 valor: BaseException | None,
                 rastro: TracebackType | None) -> bool:
        return True                      # <- a exceção SOME


# ---------------------------------------------------------------
# [4] A versão curta. O `try/finally` de dentro não é enfeite.
# ---------------------------------------------------------------
@contextlib.contextmanager
def transacao(nome: str) -> Iterator[str]:
    print("    BEGIN", nome)
    try:
        yield nome
    except Exception:
        print("    ROLLBACK", nome)
        raise
    else:
        print("    COMMIT", nome)
    finally:
        print("    fim", nome)


@contextlib.contextmanager
def frouxo() -> Iterator[None]:
    """Errado de propósito: sem `try`, a limpeza não roda em erro."""
    print("    abriu")
    yield
    print("    fechou")


def cena_1_o_problema() -> None:
    print("[1] O PROBLEMA")
    pasta = Path(tempfile.mkdtemp(prefix="cap20-"))
    caminho = pasta / "dados.txt"

    # A versão escrita à mão. Correta, e com duas linhas de cerimônia
    # para cada linha de trabalho.
    arquivo = open(caminho, "w", encoding="utf-8")
    try:
        arquivo.write("mouse;8990\n")
    finally:
        arquivo.close()

    with open(caminho, encoding="utf-8") as leitura:
        print("    escrito e lido:", leitura.read().strip())
    print("    o `with` faz o mesmo que o try/finally, em uma linha")
    print("    >>> e a garantia é a mesma: fecha mesmo se o corpo falhar")
    print()


def cena_2_protocolo() -> None:
    print("[2] O PROTOCOLO — __enter__ E __exit__")
    with Cronometro("soma") as relogio:
        total = sum(range(200_000))
    print("    resultado:", total, "· guardado no objeto:", round(relogio.ms, 2), "ms")

    try:
        with Cronometro("com erro"):
            raise ValueError("algo deu errado no meio")
    except ValueError:
        print("    >>> o __exit__ rodou ANTES de a exceção subir,")
        print("        e recebeu o tipo dela nos argumentos")
    print()


def cena_3_engolir() -> None:
    print("[3] __exit__ DEVOLVENDO True ENGOLE A EXCEÇÃO")
    with Engole():
        raise ValueError("erro grave")
    print("    o programa CONTINUOU — a exceção sumiu sem rastro")
    print("    >>> devolva None (ou nada). `return True` é para quem")
    print("        quer suprimir de propósito, como o contextlib.suppress")
    print()


def cena_4_contextmanager() -> None:
    print("[4] @contextmanager")
    with transacao("t1") as nome:
        print("    usando", nome)
    try:
        with transacao("t2"):
            raise RuntimeError("falhou no meio")
    except RuntimeError:
        pass

    print("    -- e o que acontece sem o try de dentro --")
    try:
        with frouxo():
            raise ValueError("x")
    except ValueError:
        print("    >>> 'fechou' NÃO apareceu: o recurso vazou")

    print("    -- um gerador não pode ser reutilizado --")
    gerenciador = transacao("reuso")
    with gerenciador:
        pass
    try:
        with gerenciador:
            pass
    except (AttributeError, RuntimeError) as erro:
        print("    segunda vez ->", type(erro).__name__ + ":", erro)
    print()


def cena_5_sqlite() -> None:
    print("[5] O `with` DO sqlite3 NÃO FECHA A CONEXÃO")
    conexao = sqlite3.connect(":memory:")
    conexao.execute("CREATE TABLE t (a INTEGER)")
    conexao.commit()

    with conexao:
        conexao.execute("INSERT INTO t VALUES (1)")

    conexao.execute("SELECT 1")            # ainda funciona!
    print("    depois do `with`, a conexão continua aberta")

    try:
        with conexao:
            conexao.execute("INSERT INTO t VALUES (2)")
            raise ValueError("falhou no meio")
    except ValueError:
        pass
    total = conexao.execute("SELECT count(*) FROM t").fetchone()[0]
    print("    linhas após o rollback automático:", total, "(o 2 não entrou)")
    print("    >>> ele gerencia a TRANSAÇÃO, não a conexão (03.15).")
    print("        Para fechar: contextlib.closing(sqlite3.connect(...))")
    conexao.close()
    print()


def cena_6_contextlib_e_custo() -> None:
    print("[6] ExitStack, suppress — E O CUSTO DE CADA FORMA")
    pasta = Path(tempfile.mkdtemp(prefix="cap20-"))
    with contextlib.ExitStack() as pilha:
        arquivos = [pilha.enter_context(open(pasta / ("f%d.txt" % i), "w",
                                             encoding="utf-8"))
                    for i in range(3)]
        print("    dentro do with, fechados?", [a.closed for a in arquivos])
    print("    depois,                fechados?", [a.closed for a in arquivos])
    print("    >>> ExitStack é para quando a QUANTIDADE só se sabe rodando")

    with contextlib.suppress(FileNotFoundError):
        (pasta / "nao-existe.txt").unlink()
    print("    suppress: o arquivo não existia e o programa seguiu")

    preparo = (
        "import contextlib\n"
        "class Vazio:\n"
        "    def __enter__(self): return self\n"
        "    def __exit__(self, *a): return None\n"
        "@contextlib.contextmanager\n"
        "def vazio_gerador():\n"
        "    yield\n"
        "vazio = Vazio()\n")
    print("    -- entrar e sair 1 milhão de vezes --")
    for rotulo, trecho in [("nada", "pass"),
                           ("with (classe)", "with vazio: pass"),
                           ("with (@contextmanager)", "with vazio_gerador(): pass")]:
        segundos = min(timeit.repeat(trecho, preparo, number=1_000_000, repeat=3))
        print("       %-24s %7.1f ms" % (rotulo, segundos * 1000))
    print("    >>> o gerador é ~6× mais caro para entrar e sair.")
    print("        Irrelevante para um arquivo; relevante num laço quente")


def main() -> None:
    cena_1_o_problema()
    cena_2_protocolo()
    cena_3_engolir()
    cena_4_contextmanager()
    cena_5_sqlite()
    cena_6_contextlib_e_custo()


if __name__ == "__main__":
    main()
