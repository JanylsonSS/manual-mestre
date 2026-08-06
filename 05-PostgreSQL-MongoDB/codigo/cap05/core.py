"""SQLAlchemy Core: a engine, o pool e o SQL montado por objetos.

Oito cenas. A pergunta que elas respondem é "o que eu ganho em relação
ao psycopg do 05.04?" — e a resposta principal não é sintaxe: é o pool.

    [1] a engine não conecta
    [2] connect() e begin(): quem faz commit
    [3] SQL cru, com parâmetro
    [4] o pool, medido contra o psycopg
    [5] o pool cheio, e o que acontece então
    [6] refletir um schema que já existe
    [7] SQL montado por objetos
    [8] o que volta: Row, mappings, scalars

Uso:
    python codigo/laboratorio.py
    python codigo/cap05/core.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import psycopg
import sqlalchemy as sa
from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from laboratorio import uri  # noqa: E402

URI = uri()
# O SQLAlchemy precisa saber qual driver usar; o psycopg 3 é "postgresql+psycopg".
URI_SA = URI.replace("postgresql://", "postgresql+psycopg://", 1)


def linha(rotulo: str, valor: object) -> None:
    print("    %-36s %s" % (rotulo, valor))


def cena_1_engine_nao_conecta() -> None:
    print("[1] A ENGINE NÃO CONECTA")
    inicio = time.perf_counter()
    engine = sa.create_engine(
        "postgresql+psycopg://ninguem:errado@host.que.nao.existe:5432/nada")
    ms = (time.perf_counter() - inicio) * 1000
    linha("create_engine com URL inválida:", "%.2f ms, sem erro" % ms)
    linha("o que ela é:", type(engine).__name__)
    linha("o pool que ela criou:", type(engine.pool).__name__)
    try:
        engine.connect()
    except sa.exc.OperationalError as erro:
        linha("só ao conectar:", str(erro.orig).split("\n")[0][:52])
    engine.dispose()
    print("    >>> a engine é uma FÁBRICA de conexões com um pool dentro,")
    print("        não uma conexão. Ela se cria uma vez, no início do")
    print("        programa, e vive enquanto ele viver")
    print()


def cena_2_commit(engine: sa.Engine) -> None:
    print("[2] connect() E begin(): QUEM FAZ COMMIT")
    with engine.connect() as conexao:
        conexao.execute(text("UPDATE produtos SET preco_centavos = 1 "
                             "WHERE id = 12"))
    with engine.connect() as conexao:
        valor = conexao.execute(text("SELECT preco_centavos FROM produtos "
                                     "WHERE id = 12")).scalar()
    linha("depois de connect() sem commit:", valor)

    with engine.begin() as conexao:
        conexao.execute(text("UPDATE produtos SET preco_centavos = 13901 "
                             "WHERE id = 12"))
    with engine.connect() as conexao:
        valor = conexao.execute(text("SELECT preco_centavos FROM produtos "
                                     "WHERE id = 12")).scalar()
    linha("depois de begin():", valor)
    with engine.begin() as conexao:
        conexao.execute(text("UPDATE produtos SET preco_centavos = 13900 "
                             "WHERE id = 12"))
    print("    >>> o OPOSTO do psycopg (05.04/§6.6), onde o `with` da")
    print("        conexão comita. Aqui connect() descarta e begin() comita")
    print()


def cena_3_sql_cru(engine: sa.Engine) -> None:
    print("[3] SQL CRU, COM PARÂMETRO")
    with engine.connect() as conexao:
        try:
            conexao.execute("SELECT 1")           # type: ignore[arg-type]
        except Exception as erro:
            linha("string pura:", str(erro).split("\n")[0][:64])
        alvo = conexao.execute(
            text("SELECT nome FROM produtos WHERE categoria = :cat "
                 "ORDER BY id LIMIT 1"), {"cat": "audio"}).scalar()
        linha("com text() e :cat", alvo)
        maldoso = conexao.execute(
            text("SELECT count(*) FROM produtos WHERE categoria = :cat"),
            {"cat": "audio' OR '1'='1"}).scalar()
        linha("com um valor hostil:", maldoso)
    print("    >>> o SQLAlchemy 2.0 RECUSA string pura, e isso é proteção:")
    print("        text() marca 'eu sei que isto é SQL literal'. O parâmetro")
    print("        continua sendo parâmetro, com a proteção do 05.04")
    print()


def cena_4_pool(engine: sa.Engine) -> None:
    print("[4] O POOL, MEDIDO CONTRA O psycopg")
    repeticoes = 30

    inicio = time.perf_counter()
    for _ in range(repeticoes):
        conexao = psycopg.connect(URI)
        with conexao.cursor() as cursor:
            cursor.execute("SELECT 1")
        conexao.close()
    ms_abrindo = (time.perf_counter() - inicio) * 1000

    with engine.connect() as conexao:          # aquece o pool
        conexao.execute(text("SELECT 1"))
    inicio = time.perf_counter()
    for _ in range(repeticoes):
        with engine.connect() as conexao:
            conexao.execute(text("SELECT 1"))
    ms_pool = (time.perf_counter() - inicio) * 1000

    conexao = psycopg.connect(URI)
    inicio = time.perf_counter()
    for _ in range(repeticoes):
        with conexao.cursor() as cursor:
            cursor.execute("SELECT 1")
    ms_mesma = (time.perf_counter() - inicio) * 1000
    conexao.close()

    linha("abrindo de verdade a cada vez:",
          "%7.1f ms (%.2f ms cada)" % (ms_abrindo, ms_abrindo / repeticoes))
    linha("pegando do pool a cada vez:",
          "%7.1f ms (%.2f ms cada)" % (ms_pool, ms_pool / repeticoes))
    linha("a MESMA conexão, sem soltar:",
          "%7.1f ms (%.2f ms cada)" % (ms_mesma, ms_mesma / repeticoes))
    linha("ganho do pool:", "%.1fx" % (ms_abrindo / max(ms_pool, 0.001)))
    linha("quanto falta para o teto:",
          "%.1fx" % (ms_pool / max(ms_mesma, 0.001)))
    linha("estado do pool:", engine.pool.status())
    print("    >>> `with engine.connect()` NÃO abre uma conexão: pega uma")
    print("        emprestada, e sair do bloco devolve em vez de fechar. O")
    print("        que sobra de custo é o ROLLBACK que ele manda ao devolver")
    print("    >>> e aqui o laboratório SUBESTIMA o ganho: a conexão é por")
    print("        soquete Unix, na mesma máquina. Numa rede, o que some é")
    print("        a viagem de ida e volta do handshake, não microssegundos")
    print()


def cena_5_pool_cheio() -> None:
    print("[5] O POOL CHEIO")
    engine = sa.create_engine(URI_SA, pool_size=2, max_overflow=1,
                              pool_timeout=2)
    abertas = []
    try:
        for numero in range(1, 5):
            inicio = time.perf_counter()
            try:
                abertas.append(engine.connect())
                linha("conexão %d:" % numero,
                      "obtida em %.0f ms — %s"
                      % ((time.perf_counter() - inicio) * 1000,
                         engine.pool.status()))
            except sa.exc.TimeoutError as erro:
                linha("conexão %d:" % numero,
                      "%s" % str(erro).split("\n")[0][:66])
    finally:
        for conexao in abertas:
            conexao.close()
        engine.dispose()
    print("    >>> pool_size=2 mais max_overflow=1 dão TRÊS. A quarta espera")
    print("        pool_timeout segundos e desiste. Sem timeout, ela")
    print("        esperaria para sempre — e o sintoma seria 'o site travou'")
    print()


def cena_7_sql_por_objetos(engine: sa.Engine, metadados: sa.MetaData) -> None:
    print("[7] SQL MONTADO POR OBJETOS")
    produtos = metadados.tables["produtos"]
    itens = metadados.tables["itens_pedido"]

    consulta = (
        sa.select(produtos.c.categoria,
                  sa.func.sum(itens.c.quantidade
                              * itens.c.preco_unitario_centavos)
                  .label("receita"))
        .join_from(itens, produtos, itens.c.produto_id == produtos.c.id)
        .where(produtos.c.ativo.is_(True))
        .group_by(produtos.c.categoria)
        .order_by(sa.desc("receita")))

    linha("o SQL gerado:", "")
    for pedaco in str(consulta.compile(engine)).split("\n"):
        print("        " + pedaco)
    with engine.connect() as conexao:
        for categoria, receita in conexao.execute(consulta):
            linha("  %s:" % categoria, "R$ %.2f" % (receita / 100))
    print("    >>> os `.c` são as COLUNAS refletidas. Um erro de nome falha")
    print("        em Python, antes de virar SQL — e o `label` é o que")
    print("        permite ordenar por uma expressão")
    print()


def cena_6_refletir(engine: sa.Engine) -> sa.MetaData:
    print("[6] REFLETIR UM SCHEMA QUE JÁ EXISTE")
    metadados = sa.MetaData()
    inicio = time.perf_counter()
    metadados.reflect(bind=engine)
    ms = (time.perf_counter() - inicio) * 1000
    linha("reflect() levou:", "%.0f ms" % ms)
    linha("tabelas encontradas:", sorted(metadados.tables))
    produtos = metadados.tables["produtos"]
    linha("colunas de produtos:",
          [(c.name, str(c.type)) for c in produtos.columns])
    linha("chaves estrangeiras vistas:",
          sorted(str(f.column) for f in
                 metadados.tables["itens_pedido"].foreign_keys))
    print("    >>> reflect lê o catálogo do 05.01 e monta os objetos. É como")
    print("        se ataca um banco herdado sem escrever modelo nenhum")
    print()
    return metadados


def cena_8_o_que_volta(engine: sa.Engine) -> None:
    print("[8] O QUE VOLTA")
    consulta = text("SELECT id, nome, preco_centavos FROM produtos "
                    "WHERE id <= 2 ORDER BY id")
    with engine.connect() as conexao:
        primeira = conexao.execute(consulta).first()
        linha("first() ->", "%r  %s" % (primeira, type(primeira).__name__))
        linha("por nome:", primeira.nome if primeira else None)
        linha("desempacotando:", tuple(primeira) if primeira else None)

        mapeadas = conexao.execute(consulta).mappings().all()
        linha("mappings().all() ->", mapeadas[0])
        escalares = conexao.execute(
            text("SELECT nome FROM produtos WHERE id <= 2 ORDER BY id")
        ).scalars().all()
        linha("scalars().all() ->", escalares)

        resultado = conexao.execute(consulta)
        resultado.all()
        linha("all() uma segunda vez:", resultado.all())
    print("    >>> Row é tupla E objeto com atributos. E o resultado é um")
    print("        CURSOR: consumido uma vez, a segunda devolve vazio")
    print()


def main() -> None:
    engine = sa.create_engine(URI_SA)
    try:
        cena_1_engine_nao_conecta()
        cena_2_commit(engine)
        cena_3_sql_cru(engine)
        cena_4_pool(engine)
        cena_5_pool_cheio()
        metadados = cena_6_refletir(engine)
        cena_7_sql_por_objetos(engine, metadados)
        cena_8_o_que_volta(engine)
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
