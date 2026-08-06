"""Python falando com o PostgreSQL — e a vulnerabilidade que isso abre.

A cena 1 é uma SQL injection FUNCIONANDO, contra uma tabela temporária
deste script. Ela existe porque ler sobre injection não ensina; ver a
tabela sumir, ensina.

    [1] a injection, em três ataques
    [2] o parâmetro, e por que ele não é escape de aspas
    [3] o que NÃO dá para parametrizar: nomes
    [4] tipos: o que vem e o que vai
    [5] o formato das linhas
    [6] transações: quem faz commit
    [7] inserir muito: laço, executemany, copy
    [8] erros com nome

Uso:
    python codigo/laboratorio.py
    python codigo/cap04/psycopg_demo.py
"""

from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

import psycopg
from psycopg import sql
from psycopg.rows import class_row, dict_row
from psycopg.types.json import Jsonb

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from laboratorio import uri  # noqa: E402

URI = uri()


def linha(rotulo: str, valor: object) -> None:
    print("    %-34s %s" % (rotulo, valor))


def preparar(cursor: psycopg.Cursor) -> None:
    cursor.execute("DROP TABLE IF EXISTS contas_teste")
    cursor.execute("""
        CREATE TABLE contas_teste (
            id    integer PRIMARY KEY,
            login text UNIQUE NOT NULL,
            senha text NOT NULL,
            papel text NOT NULL DEFAULT 'cliente'
        )
    """)
    cursor.executemany(
        "INSERT INTO contas_teste (id, login, senha, papel) "
        "VALUES (%s, %s, %s, %s)",
        [(1, "ana", "senha-da-ana", "cliente"),
         (2, "bruno", "senha-do-bruno", "cliente"),
         (3, "raiz", "senha-forte-do-admin", "admin")])
    cursor.connection.commit()


def cena_1_injection(cursor: psycopg.Cursor) -> None:
    print("[1] SQL INJECTION, FUNCIONANDO")

    def autenticar_vulneravel(login: str, senha: str) -> list[tuple]:
        # NUNCA escreva isto. Está aqui para ser atacado.
        comando = ("SELECT id, login, papel FROM contas_teste "
                   "WHERE login = '%s' AND senha = '%s'" % (login, senha))
        cursor.execute(comando)          # noqa: S608 — o defeito é o assunto
        return cursor.fetchall()

    linha("login honesto:", autenticar_vulneravel("ana", "senha-da-ana"))
    linha("senha errada:", autenticar_vulneravel("ana", "errada"))

    print("    -- ataque 1: entrar sem saber a senha --")
    resultado = autenticar_vulneravel("ana", "qualquer' OR '1'='1")
    linha("senha usada:", "qualquer' OR '1'='1")
    linha("entrou como:", resultado)

    print("    -- ataque 2: escolher DE QUEM é a conta --")
    resultado = autenticar_vulneravel("raiz'--", "nem tentei")
    linha("login usado:", "raiz'--")
    linha("entrou como:", resultado)

    print("    -- ataque 3: destruir --")
    linha("login usado:", "x'; DROP TABLE contas_teste; --")
    try:
        autenticar_vulneravel("x'; DROP TABLE contas_teste; --", "y")
        linha("houve exceção?", "não — o comando passou inteiro")
    except psycopg.Error as erro:
        linha("houve exceção?", str(erro).split("\n")[0])
    cursor.connection.commit()
    cursor.execute("SELECT to_regclass('contas_teste')")
    resultado_tabela = cursor.fetchone()
    linha("a tabela ainda existe?",
          resultado_tabela[0] if resultado_tabela else "NÃO — foi destruída")
    print("    >>> o ataque 3 mandou DOIS comandos numa chamada. O psycopg")
    print("        aceita isso quando NÃO há parâmetro, porque aí ele usa o")
    print("        protocolo simples do Postgres. Com parâmetro, o protocolo")
    print("        é outro e recusa mais de um comando (cena 2)")
    preparar(cursor)                     # reconstrói o que o ataque destruiu
    print()


def cena_2_parametro(cursor: psycopg.Cursor) -> None:
    print("[2] O PARÂMETRO")

    def autenticar_segura(login: str, senha: str) -> list[tuple]:
        cursor.execute(
            "SELECT id, login, papel FROM contas_teste "
            "WHERE login = %s AND senha = %s", (login, senha))
        return cursor.fetchall()

    linha("login honesto:", autenticar_segura("ana", "senha-da-ana"))
    linha("ataque 1:", autenticar_segura("ana", "qualquer' OR '1'='1"))
    linha("ataque 2:", autenticar_segura("raiz'--", "nem tentei"))
    linha("ataque 3:",
          autenticar_segura("x'; DROP TABLE contas_teste; --", "y"))
    print("    >>> nenhum ataque devolveu linha, e nada foi destruído:")
    print("        o texto inteiro virou VALOR, e valor não vira comando")

    print("    -- o erro que parece proteção e não é --")
    perigoso = ("SELECT count(*) FROM contas_teste WHERE login = '%s'"
                % "ana' OR '1'='1")
    linha("com aspas em volta do %s:", perigoso[-46:])
    cursor.execute(perigoso)
    resultado = cursor.fetchone()
    linha("linhas devolvidas:", resultado[0] if resultado else None)
    print("    >>> pôr aspas em volta e formatar com %% é a MESMA coisa que")
    print("        concatenar. O parâmetro do psycopg não usa aspas")

    print("    -- parâmetro nomeado --")
    cursor.execute(
        "SELECT login FROM contas_teste WHERE papel = %(papel)s",
        {"papel": "admin"})
    resultado = cursor.fetchone()
    linha("por nome:", resultado[0] if resultado else None)
    print()


def cena_3_identificadores(cursor: psycopg.Cursor) -> None:
    print("[3] O QUE NÃO DÁ PARA PARAMETRIZAR: NOMES")
    try:
        cursor.execute("SELECT count(*) FROM %s", ("contas_teste",))
    except psycopg.Error as erro:
        cursor.connection.rollback()
        linha("tabela como parâmetro:", str(erro).split("\n")[0])

    consulta = sql.SQL("SELECT count(*) FROM {}").format(
        sql.Identifier("contas_teste"))
    cursor.execute(consulta)
    resultado = cursor.fetchone()
    linha("com sql.Identifier:", resultado[0] if resultado else None)
    linha("o SQL gerado:", consulta.as_string(cursor))

    maldoso = sql.SQL("SELECT count(*) FROM {}").format(
        sql.Identifier('contas_teste"; DROP TABLE contas_teste; --'))
    linha("nome maldoso, escapado:", maldoso.as_string(cursor)[:70])
    print("    >>> Identifier põe aspas duplas e dobra as internas: o nome")
    print("        inteiro vira UM identificador, por esquisito que seja")
    print()


def cena_4_tipos(cursor: psycopg.Cursor) -> None:
    print("[4] TIPOS: O QUE VEM E O QUE VAI")
    cursor.execute("""
        SELECT '{"a": 1}'::jsonb,
               now()::timestamptz,
               19.90::numeric(6,2),
               ARRAY['a','b'],
               gen_random_uuid(),
               NULL::text,
               true
    """)
    resultado = cursor.fetchone()
    if resultado is None:
        return
    nomes = ["jsonb", "timestamptz", "numeric", "array", "uuid", "null",
             "boolean"]
    for nome, valor in zip(nomes, resultado):
        linha("%s ->" % nome, "%-34r %s" % (valor, type(valor).__name__))
    print("    -- e no sentido contrário --")
    try:
        cursor.execute("SELECT pg_typeof(%s)", ({"a": 1},))
    except psycopg.Error as erro:
        cursor.connection.rollback()
        linha("dict cru vira:", str(erro).split("\n")[0])
    cursor.execute("SELECT pg_typeof(%s), pg_typeof(%s), pg_typeof(%s)",
                   (Jsonb({"a": 1}), Decimal("19.90"), [1, 2, 3]))
    linha("Jsonb, Decimal, list viram:", cursor.fetchone())
    print("    -- a armadilha do float, em quatro passos --")
    linha("1. o Python calcula 0.1 + 19.8:", repr(0.1 + 19.8))
    cursor.execute("SELECT pg_typeof(%s)", (0.1 + 19.8,))
    resultado = cursor.fetchone()
    linha("2. o psycopg manda como:", resultado[0] if resultado else None)
    cursor.execute("SELECT %s::text", (0.1 + 19.8,))
    resultado = cursor.fetchone()
    linha("3. e o banco recebe:", resultado[0] if resultado else None)
    cursor.execute("SELECT (%s::numeric)::text, %s::numeric = 19.90",
                   (0.1 + 19.8, 0.1 + 19.8))
    resultado = cursor.fetchone()
    linha("4. convertido para numeric:",
          "%s   (= 19.90? %s)" % (resultado[0], resultado[1])
          if resultado else None)
    print("    >>> o passo 4 ENGANA: a conversão para numeric arredonda e o")
    print("        erro some. Uma comparação isolada passa. O que não passa")
    print("        é a soma — e é lá que o problema aparece em produção:")
    cursor.execute("SELECT sum(%s::float8) = 100.00::float8 "
                   "FROM generate_series(1, 10000)", (0.01,))
    resultado = cursor.fetchone()
    linha("0.01 somado 10 mil vezes = 100?",
          resultado[0] if resultado else None)
    cursor.execute("SELECT sum(%s::numeric) = 100.00 "
                   "FROM generate_series(1, 10000)", (Decimal("0.01"),))
    resultado = cursor.fetchone()
    linha("o mesmo com Decimal/numeric:",
          resultado[0] if resultado else None)
    print()


def cena_5_formato_das_linhas(conexao: psycopg.Connection) -> None:
    print("[5] O FORMATO DAS LINHAS")
    consulta = ("SELECT id, nome, preco_centavos FROM produtos "
                "WHERE id = 1")
    with conexao.cursor() as cursor:
        cursor.execute(consulta)
        linha("padrão (tupla):", cursor.fetchone())
    with conexao.cursor(row_factory=dict_row) as cursor:
        cursor.execute(consulta)
        linha("dict_row:", cursor.fetchone())

    @dataclass
    class Produto:
        id: int
        nome: str
        preco_centavos: int

        def reais(self) -> str:
            return "R$ %.2f" % (self.preco_centavos / 100)

    with conexao.cursor(row_factory=class_row(Produto)) as cursor:
        cursor.execute(consulta)
        produto = cursor.fetchone()
    linha("class_row(Produto):", produto)
    linha("e ele tem comportamento:", produto.reais() if produto else None)
    print("    >>> class_row exige que os nomes das colunas batam com os")
    print("        campos. É a ponte para as dataclasses do 04.13")
    print()


def cena_6_transacoes() -> None:
    print("[6] TRANSAÇÕES: QUEM FAZ COMMIT")
    with psycopg.connect(URI) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("UPDATE contas_teste SET papel = 'x' WHERE id = 1")
    with psycopg.connect(URI) as conexao, conexao.cursor() as cursor:
        cursor.execute("SELECT papel FROM contas_teste WHERE id = 1")
        resultado = cursor.fetchone()
    linha("depois do with, sem commit:", resultado[0] if resultado else None)
    print("    >>> o `with` da CONEXÃO faz commit ao sair sem exceção.")
    print("        Isso surpreende quem espera o contrário")

    try:
        with psycopg.connect(URI) as conexao, conexao.cursor() as cursor:
            cursor.execute("UPDATE contas_teste SET papel = 'y' WHERE id = 1")
            raise RuntimeError("algo deu errado no meio")
    except RuntimeError as erro:
        linha("exceção:", erro)
    with psycopg.connect(URI) as conexao, conexao.cursor() as cursor:
        cursor.execute("SELECT papel FROM contas_teste WHERE id = 1")
        resultado = cursor.fetchone()
    linha("depois da exceção:", resultado[0] if resultado else None)

    with psycopg.connect(URI) as conexao:
        with conexao.transaction():
            with conexao.cursor() as cursor:
                cursor.execute(
                    "UPDATE contas_teste SET papel = 'z' WHERE id = 1")
            try:
                with conexao.transaction():
                    with conexao.cursor() as cursor:
                        cursor.execute("UPDATE contas_teste SET papel = 'w' "
                                       "WHERE id = 1")
                    raise ValueError("desfaz só a parte de dentro")
            except ValueError:
                pass
    with psycopg.connect(URI) as conexao, conexao.cursor() as cursor:
        cursor.execute("SELECT papel FROM contas_teste WHERE id = 1")
        resultado = cursor.fetchone()
    linha("transação aninhada:", resultado[0] if resultado else None)
    print("    >>> conexao.transaction() aninhado vira SAVEPOINT: a parte")
    print("        de dentro desfaz sem derrubar a de fora")
    print()


def cena_7_inserir_muito(conexao: psycopg.Connection) -> None:
    print("[7] INSERIR MUITO: LAÇO, executemany, copy")
    quantidade = 20000
    dados = [(i, "linha %d" % i) for i in range(quantidade)]
    with conexao.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS carga")
        cursor.execute("CREATE TABLE carga (id integer, texto text)")
        conexao.commit()

        inicio = time.perf_counter()
        for registro in dados:
            cursor.execute("INSERT INTO carga VALUES (%s, %s)", registro)
        conexao.commit()
        ms_laco = (time.perf_counter() - inicio) * 1000

        cursor.execute("TRUNCATE carga")
        conexao.commit()
        inicio = time.perf_counter()
        cursor.executemany("INSERT INTO carga VALUES (%s, %s)", dados)
        conexao.commit()
        ms_many = (time.perf_counter() - inicio) * 1000

        cursor.execute("TRUNCATE carga")
        conexao.commit()
        inicio = time.perf_counter()
        with cursor.copy("COPY carga (id, texto) FROM STDIN") as copia:
            for registro in dados:
                copia.write_row(registro)
        conexao.commit()
        ms_copy = (time.perf_counter() - inicio) * 1000

        cursor.execute("SELECT count(*) FROM carga")
        resultado = cursor.fetchone()
        linha("linhas ao final:", resultado[0] if resultado else None)
        linha("laço com execute:", "%7.0f ms" % ms_laco)
        linha("executemany:", "%7.0f ms  (%.1fx)"
              % (ms_many, ms_laco / max(ms_many, 0.001)))
        linha("copy:", "%7.0f ms  (%.1fx)"
              % (ms_copy, ms_laco / max(ms_copy, 0.001)))
        cursor.execute("DROP TABLE carga")
        conexao.commit()
    print()


def cena_8_erros_com_nome(cursor: psycopg.Cursor) -> None:
    print("[8] ERROS COM NOME")
    tentativas = [
        ("login repetido",
         "INSERT INTO contas_teste (id, login, senha) "
         "VALUES (99, 'ana', 'x')"),
        ("chave estrangeira",
         "INSERT INTO itens_pedido (id, pedido_id, produto_id, quantidade, "
         "preco_unitario_centavos) VALUES (999, 9999, 1, 1, 100)"),
        ("restrição CHECK",
         "INSERT INTO produtos (id, nome, categoria, preco_centavos) "
         "VALUES (99, 'x', 'y', -1)"),
        ("coluna que não existe",
         "SELECT coluna_inventada FROM contas_teste"),
    ]
    for descricao, comando in tentativas:
        try:
            cursor.execute(comando)
        except psycopg.Error as erro:
            cursor.connection.rollback()
            linha(descricao, "%s / SQLSTATE %s"
                  % (type(erro).__name__, erro.sqlstate))
    print("    >>> cada erro tem CLASSE própria e código SQLSTATE. Tratar")
    print("        UniqueViolation é diferente de tratar psycopg.Error")
    print()


def main() -> None:
    with psycopg.connect(URI) as conexao:
        with conexao.cursor() as cursor:
            preparar(cursor)
            cena_1_injection(cursor)
            cena_2_parametro(cursor)
            cena_3_identificadores(cursor)
            cena_4_tipos(cursor)
        cena_5_formato_das_linhas(conexao)
    cena_6_transacoes()
    with psycopg.connect(URI) as conexao:
        cena_7_inserir_muito(conexao)
        with conexao.cursor() as cursor:
            cena_8_erros_com_nome(cursor)
            cursor.execute("DROP TABLE IF EXISTS contas_teste")
            conexao.commit()


if __name__ == "__main__":
    main()
