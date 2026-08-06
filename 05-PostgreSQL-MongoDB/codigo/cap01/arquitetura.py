"""O que muda quando o banco vira um servidor.

Todas as cenas comparam com o SQLite do módulo 03 — porque a diferença
entre os dois **é** o conteúdo do capítulo.

Seis cenas:
    [1] quem está rodando: os processos do servidor
    [2] onde eu estou: database, schema, role, search_path
    [3] duas conexões escrevendo — o que no SQLite dava "database is locked"
    [4] leitura sem espera (MVCC), e a trava que existe: a mesma LINHA
    [5] o custo de abrir uma conexão
    [6] o que o servidor sabe sobre si mesmo

Uso:
    python codigo/laboratorio.py          # uma vez, para criar o banco
    python codigo/cap01/arquitetura.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import psycopg

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from laboratorio import uri  # noqa: E402

URI = uri()


def mostrar(sql: str, indentacao: str = "    ", limite: int = 8) -> None:
    """Roda uma consulta e imprime como tabela."""
    with psycopg.connect(URI) as conexao, conexao.cursor() as cursor:
        cursor.execute(sql)
        colunas = [d.name for d in cursor.description or []]
        linhas = cursor.fetchall()
    if colunas:
        print(indentacao + " | ".join(colunas))
        print(indentacao + "-" * (len(" | ".join(colunas))))
    for linha in linhas[:limite]:
        print(indentacao + " | ".join(str(valor)[:38] for valor in linha))


def cena_1_processos() -> None:
    print("[1] QUEM ESTÁ RODANDO")
    mostrar("""
        SELECT pid, backend_type, state
        FROM pg_stat_activity
        ORDER BY pid
    """)
    print("    >>> um processo por CONEXÃO (client backend), mais os que")
    print("        cuidam do banco sozinhos. No SQLite não há processo")
    print("        nenhum: a biblioteca roda DENTRO do seu programa")
    print()


def cena_2_onde_estou() -> None:
    print("[2] ONDE EU ESTOU")
    mostrar("""
        SELECT current_database() AS banco,
               current_user       AS role,
               current_schema()   AS schema
    """)
    print("    -- os databases que existem --")
    mostrar("SELECT datname FROM pg_database ORDER BY 1")
    print("    -- os schemas DENTRO deste database --")
    mostrar("SELECT nspname FROM pg_namespace ORDER BY 1")
    print("    -- onde o Postgres procura uma tabela sem prefixo --")
    mostrar("SHOW search_path")
    print("    >>> três níveis: servidor > database > schema > tabela.")
    print("        No SQLite, um arquivo É o banco inteiro")
    print()


def cena_3_duas_conexoes() -> None:
    print("[3] DUAS CONEXÕES ESCREVENDO AO MESMO TEMPO")
    primeira = psycopg.connect(URI)
    segunda = psycopg.connect(URI)
    try:
        with primeira.cursor() as cursor:
            cursor.execute("UPDATE produtos SET preco_centavos = preco_centavos + 1 "
                           "WHERE id = 1")
        print("    A alterou o produto 1 (sem commit)")
        with segunda.cursor() as cursor:
            cursor.execute("UPDATE produtos SET preco_centavos = preco_centavos + 1 "
                           "WHERE id = 2")
        print("    B alterou o produto 2 — e NÃO houve erro")
        print("    >>> no SQLite (03.15) isto dava 'database is locked'")
    finally:
        primeira.rollback()
        segunda.rollback()
        primeira.close()
        segunda.close()
    print()


def cena_4_mvcc_e_trava() -> None:
    print("[4] LEITURA SEM ESPERA, E A TRAVA QUE EXISTE")
    escritora = psycopg.connect(URI)
    leitora = psycopg.connect(URI)
    try:
        with escritora.cursor() as cursor:
            cursor.execute("UPDATE produtos SET preco_centavos = 1 WHERE id = 1")
        with leitora.cursor() as cursor:
            cursor.execute("SELECT preco_centavos FROM produtos WHERE id = 1")
            linha = cursor.fetchone()
        print("    A alterou o produto 1 para 1; B lê e recebe:",
              linha[0] if linha else None)
        print("    >>> o valor ANTIGO, sem esperar. Cada transação enxerga")
        print("        uma versão coerente do banco — é o MVCC")

        print("    -- e agora B tenta alterar a MESMA linha --")
        with leitora.cursor() as cursor:
            cursor.execute("SET lock_timeout = '300ms'")
            inicio = time.perf_counter()
            try:
                cursor.execute("UPDATE produtos SET preco_centavos = 2 WHERE id = 1")
            except psycopg.errors.LockNotAvailable as erro:
                ms = (time.perf_counter() - inicio) * 1000
                print("    B esperou %.0f ms e desistiu: %s"
                      % (ms, str(erro).split("\n")[0]))
        print("    >>> a trava é da LINHA, não do banco — e ela tem prazo")
    finally:
        escritora.rollback()
        leitora.rollback()
        escritora.close()
        leitora.close()
    print()


def cena_5_custo_da_conexao() -> None:
    print("[5] O CUSTO DE ABRIR UMA CONEXÃO")
    inicio = time.perf_counter()
    for _ in range(20):
        psycopg.connect(URI).close()
    ms_conexoes = (time.perf_counter() - inicio) * 1000

    conexao = psycopg.connect(URI)
    inicio = time.perf_counter()
    for _ in range(20):
        with conexao.cursor() as cursor:
            cursor.execute("SELECT 1")
    ms_consultas = (time.perf_counter() - inicio) * 1000
    conexao.close()

    print("    20 conexões novas:            %6.1f ms (%.1f ms cada)"
          % (ms_conexoes, ms_conexoes / 20))
    print("    20 consultas na mesma conexão: %6.1f ms (%.2f ms cada)"
          % (ms_consultas, ms_consultas / 20))
    print("    >>> abrir custa ~%.0fx mais que usar. É por isso que existe"
          % (ms_conexoes / max(ms_consultas, 0.001)))
    print("        pool de conexões (05.05) — e por que abrir uma por")
    print("        requisição derruba um servidor web")
    print()


def cena_6_o_que_o_servidor_sabe() -> None:
    print("[6] O QUE O SERVIDOR SABE SOBRE SI MESMO")
    mostrar("""
        SELECT table_name, (SELECT count(*) FROM information_schema.columns c
                            WHERE c.table_name = t.table_name) AS colunas
        FROM information_schema.tables t
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    mostrar("""
        SELECT pg_size_pretty(pg_database_size(current_database())) AS tamanho_do_banco
    """)
    print("    >>> `information_schema` é padrão SQL e existe em todos os")
    print("        bancos; `pg_catalog` é o do Postgres e sabe mais")


def main() -> None:
    cena_1_processos()
    cena_2_onde_estou()
    cena_3_duas_conexoes()
    cena_4_mvcc_e_trava()
    cena_5_custo_da_conexao()
    cena_6_o_que_o_servidor_sabe()


if __name__ == "__main__":
    main()
