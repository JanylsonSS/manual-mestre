"""Os tipos que o Postgres tem e o SQLite não tinha.

Oito cenas, todas comparando com o módulo 03 — porque a pergunta do
capítulo é "o que eu ganho ao declarar o tipo certo?".

    [1] dinheiro: numeric contra double precision
    [2] o que o SQLite aceitava e o Postgres recusa
    [3] json e jsonb: o que cada um guarda
    [4] consultar dentro do JSONB
    [5] o índice GIN, medido em 200 mil linhas
    [6] arrays
    [7] UUID
    [8] datas, horas e o que timestamptz NÃO guarda

Uso:
    python codigo/laboratorio.py
    python codigo/cap03/tipos.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import psycopg

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from laboratorio import uri  # noqa: E402

URI = uri()


def linha(rotulo: str, valor: object) -> None:
    print("    %-38s %s" % (rotulo, valor))


def um(cursor: psycopg.Cursor, sql: str) -> object:
    cursor.execute(sql)
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None


def cena_1_dinheiro(cursor: psycopg.Cursor) -> None:
    print("[1] DINHEIRO: numeric CONTRA double precision")
    linha("0.1 + 0.2 em double precision:",
          um(cursor, "SELECT 0.1::float8 + 0.2::float8"))
    linha("0.1 + 0.2 em numeric:",
          um(cursor, "SELECT 0.1::numeric + 0.2::numeric"))
    linha("são iguais a 0.3? (float8)",
          um(cursor, "SELECT 0.1::float8 + 0.2::float8 = 0.3::float8"))
    linha("são iguais a 0.3? (numeric)",
          um(cursor, "SELECT 0.1::numeric + 0.2::numeric = 0.3::numeric"))
    linha("soma de 0.01 dez mil vezes (float8):",
          um(cursor, "SELECT sum(0.01::float8) FROM generate_series(1, 10000)"))
    linha("a mesma soma em numeric:",
          um(cursor, "SELECT sum(0.01::numeric) FROM generate_series(1, 10000)"))
    print("    >>> por isso preço vira numeric(12,2) — ou integer de centavos,")
    print("        que é o que a Aurora usa desde o módulo 03")
    print()


def cena_2_o_que_o_postgres_recusa(cursor: psycopg.Cursor) -> None:
    print("[2] O QUE O SQLite ACEITAVA E O POSTGRES RECUSA")
    cursor.execute("DROP TABLE IF EXISTS rigor")
    cursor.execute("CREATE TEMP TABLE rigor (n integer, d date)")
    # O commit é necessário: cada INSERT abaixo falha, e o rollback que
    # limpa a transação levaria junto o CREATE TABLE se ele ainda
    # estivesse pendente. A primeira versão deste script não commitava, e
    # as três últimas linhas da cena diziam 'relation "rigor" does not
    # exist' — um erro do script disfarçado de erro de tipo.
    cursor.connection.commit()
    for descricao, sql in [
        ("texto numa coluna integer",
         "INSERT INTO rigor (n) VALUES ('abacaxi')"),
        ("data inexistente",
         "INSERT INTO rigor (d) VALUES ('2026-02-30')"),
        ("integer estourado",
         "INSERT INTO rigor (n) VALUES (3000000000)"),
        ("data ambígua aceita",
         "INSERT INTO rigor (d) VALUES ('2026-03-04')"),
    ]:
        try:
            cursor.execute(sql)
            linha(descricao, "aceito -> %s" % um(
                cursor, "SELECT coalesce(d::text, n::text) FROM rigor "
                        "ORDER BY ctid DESC LIMIT 1"))
        except psycopg.Error as erro:
            cursor.connection.rollback()
            linha(descricao, str(erro).split("\n")[0])
    print("    >>> no SQLite os três primeiros entravam: o tipo era uma")
    print("        sugestão. Aqui ele é uma promessa que o banco cumpre")
    print()


def cena_3_json_e_jsonb(cursor: psycopg.Cursor) -> None:
    print("[3] json E jsonb: O QUE CADA UM GUARDA")
    entrada = '{"b": 1,   "a": 2, "b": 3}'
    linha("entrada:", entrada)
    linha("guardado como json:", um(cursor, "SELECT '%s'::json" % entrada))
    linha("guardado como jsonb:", um(cursor, "SELECT '%s'::jsonb" % entrada))
    linha("tamanho em bytes (json):",
          um(cursor, "SELECT pg_column_size('%s'::json)" % entrada))
    linha("tamanho em bytes (jsonb):",
          um(cursor, "SELECT pg_column_size('%s'::jsonb)" % entrada))
    try:
        cursor.execute("SELECT '%s'::json = '%s'::json" % (entrada, entrada))
    except psycopg.Error as erro:
        cursor.connection.rollback()
        linha("json = json:", str(erro).split("\n")[0])
    linha("jsonb = jsonb:",
          um(cursor, "SELECT '%s'::jsonb = '%s'::jsonb" % (entrada, entrada)))
    print("    >>> jsonb reordena as chaves, descarta os espaços, fica com a")
    print("        ÚLTIMA chave repetida — e ganha comparação e índice. E,")
    print("        para um objeto pequeno, ocupa MAIS bytes que o json")
    print()


def cena_4_consultar_dentro(cursor: psycopg.Cursor) -> None:
    print("[4] CONSULTAR DENTRO DO JSONB")
    cursor.execute("""
        CREATE TEMP TABLE catalogo (
            id     integer PRIMARY KEY,
            nome   text NOT NULL,
            attrs  jsonb NOT NULL
        )
    """)
    cursor.execute("""
        INSERT INTO catalogo VALUES
        (1, 'Fone Bluetooth XZ-9',
            '{"cor": "preto", "bateria_h": 30, "tags": ["anc", "usb-c"]}'),
        (2, 'Monitor 24 polegadas',
            '{"cor": "preto", "polegadas": 24, "tags": ["ips", "hdmi"]}'),
        (3, 'Mousepad Grande',
            '{"cor": "cinza", "tags": ["tecido"]}')
    """)
    linha("-> devolve jsonb:", um(cursor, "SELECT attrs -> 'cor' FROM catalogo "
                                          "WHERE id = 1"))
    linha("->> devolve text:", um(cursor, "SELECT attrs ->> 'cor' FROM catalogo "
                                          "WHERE id = 1"))
    linha("chave que não existe:",
          um(cursor, "SELECT attrs ->> 'peso' FROM catalogo WHERE id = 1"))
    linha("@> (contém):",
          um(cursor, "SELECT count(*) FROM catalogo "
                     "WHERE attrs @> '{\"cor\": \"preto\"}'"))
    linha("? (tem a chave):",
          um(cursor, "SELECT count(*) FROM catalogo WHERE attrs ? 'polegadas'"))
    linha("dentro de um array:",
          um(cursor, "SELECT count(*) FROM catalogo "
                     "WHERE attrs -> 'tags' @> '[\"anc\"]'"))
    linha("comparar número exige cast:",
          um(cursor, "SELECT nome FROM catalogo "
                     "WHERE (attrs ->> 'bateria_h')::int > 20"))
    cursor.execute("SELECT jsonb_object_keys(attrs) FROM catalogo WHERE id = 2")
    linha("as chaves do produto 2:", [c[0] for c in cursor.fetchall()])
    print("    >>> a seta dupla é a que você usa em WHERE e comparação;")
    print("        a simples é para continuar navegando")
    print()


def cena_5_indice_gin(cursor: psycopg.Cursor) -> None:
    print("[5] O ÍNDICE GIN, MEDIDO EM 200 MIL LINHAS")
    cursor.execute("DROP TABLE IF EXISTS eventos")
    cursor.execute("CREATE TABLE eventos (id bigserial PRIMARY KEY, "
                   "corpo jsonb NOT NULL)")
    inicio = time.perf_counter()
    cursor.execute("""
        INSERT INTO eventos (corpo)
        SELECT jsonb_build_object(
            'tipo',    (ARRAY['clique','compra','visita','erro'])[1 + i % 4],
            'usuario', 1 + i % 5000,
            'origem',  (ARRAY['web','app','api'])[1 + i % 3])
        FROM generate_series(1, 200000) AS i
    """)
    cursor.connection.commit()
    linha("carga de 200 mil linhas:",
          "%.0f ms" % ((time.perf_counter() - inicio) * 1000))

    seletiva = ("SELECT count(*) FROM eventos "
                "WHERE corpo @> '{\"usuario\": 4242, \"tipo\": \"compra\"}'")
    ampla = ("SELECT count(*) FROM eventos "
             "WHERE corpo @> '{\"tipo\": \"compra\", \"origem\": \"api\"}'")

    def medir(consulta: str) -> tuple[float, object]:
        cursor.execute(consulta)          # aquece
        cursor.fetchone()
        inicio = time.perf_counter()
        cursor.execute(consulta)
        alvo = cursor.fetchone()
        return (time.perf_counter() - inicio) * 1000, alvo[0] if alvo else None

    def plano(consulta: str) -> str:
        cursor.execute("EXPLAIN (COSTS OFF) " + consulta)
        return " / ".join(l[0].strip() for l in cursor.fetchall()[:3])

    ms_sel_sem, casos_sel = medir(seletiva)
    ms_amp_sem, casos_amp = medir(ampla)
    linha("consulta SELETIVA casa:", "%s linhas" % casos_sel)
    linha("  sem índice:", "%.1f ms — %s" % (ms_sel_sem, plano(seletiva)))
    linha("consulta AMPLA casa:", "%s linhas" % casos_amp)
    linha("  sem índice:", "%.1f ms — %s" % (ms_amp_sem, plano(ampla)))

    inicio = time.perf_counter()
    cursor.execute("CREATE INDEX eventos_corpo_gin ON eventos USING gin (corpo)")
    cursor.connection.commit()
    linha("criar o índice GIN:",
          "%.0f ms" % ((time.perf_counter() - inicio) * 1000))
    cursor.execute("ANALYZE eventos")
    ms_sel_com, _ = medir(seletiva)
    ms_amp_com, _ = medir(ampla)
    linha("SELETIVA com índice:", "%.1f ms — %s" % (ms_sel_com, plano(seletiva)))
    linha("  ganho:", "%.0fx" % (ms_sel_sem / max(ms_sel_com, 0.001)))
    linha("AMPLA com índice:", "%.1f ms — %s" % (ms_amp_com, plano(ampla)))
    linha("  ganho:", "%.1fx" % (ms_amp_sem / max(ms_amp_com, 0.001)))
    linha("tamanho da tabela:",
          um(cursor, "SELECT pg_size_pretty(pg_relation_size('eventos'))"))
    linha("tamanho do índice GIN:",
          um(cursor, "SELECT pg_size_pretty("
                     "pg_relation_size('eventos_corpo_gin'))"))
    cursor.execute("DROP TABLE eventos")
    cursor.connection.commit()
    print()


def cena_6_arrays(cursor: psycopg.Cursor) -> None:
    print("[6] ARRAYS")
    linha("literal:", um(cursor, "SELECT ARRAY['anc', 'usb-c', 'bluetooth']"))
    linha("primeiro elemento (base 1!):",
          um(cursor, "SELECT (ARRAY['a','b','c'])[1]"))
    linha("índice 0 devolve:",
          um(cursor, "SELECT (ARRAY['a','b','c'])[0]"))
    linha("contém:", um(cursor, "SELECT ARRAY['a','b'] @> ARRAY['b']"))
    linha("qualquer um:", um(cursor, "SELECT 'b' = ANY (ARRAY['a','b'])"))
    cursor.execute("SELECT unnest(ARRAY['anc','usb-c'])")
    linha("unnest vira linhas:", [c[0] for c in cursor.fetchall()])
    linha("array_agg junta linhas:",
          um(cursor, "SELECT array_agg(DISTINCT categoria ORDER BY categoria) "
                     "FROM produtos"))
    linha("tamanho:", um(cursor, "SELECT cardinality(ARRAY['a','b','c'])"))
    print("    >>> array de texto resolve etiqueta sem tabela extra. O preço")
    print("        é não ter chave estrangeira: nada garante que 'anc' existe")
    print()


def cena_7_uuid(cursor: psycopg.Cursor) -> None:
    print("[7] UUID")
    linha("gerar:", um(cursor, "SELECT gen_random_uuid()"))
    linha("tamanho de um uuid:", um(cursor, "SELECT pg_column_size(gen_random_uuid())"))
    linha("tamanho de um bigint:", um(cursor, "SELECT pg_column_size(1::bigint)"))
    linha("tamanho do mesmo uuid como text:",
          um(cursor, "SELECT pg_column_size(gen_random_uuid()::text)"))
    try:
        cursor.execute("SELECT 'nao-e-uuid'::uuid")
    except psycopg.Error as erro:
        cursor.connection.rollback()
        linha("uuid inválido:", str(erro).split("\n")[0])
    print("    >>> 16 bytes contra 8 do bigint — e contra 40 se você guardar")
    print("        como texto, que é o erro mais comum com UUID")
    print()


def cena_8_datas(cursor: psycopg.Cursor) -> None:
    print("[8] DATAS, HORAS E O QUE timestamptz NÃO GUARDA")
    cursor.execute("SET TIME ZONE 'America/Sao_Paulo'")
    linha("fuso da sessão:", um(cursor, "SHOW TimeZone"))
    cursor.execute("CREATE TEMP TABLE quando (com timestamptz, sem timestamp)")
    cursor.execute("INSERT INTO quando VALUES "
                   "('2026-08-06 15:00:00-03', '2026-08-06 15:00:00-03')")
    linha("timestamptz lido em São Paulo:", um(cursor, "SELECT com FROM quando"))
    linha("timestamp  lido em São Paulo:", um(cursor, "SELECT sem FROM quando"))
    cursor.execute("SET TIME ZONE 'Asia/Tokyo'")
    linha("timestamptz lido em Tóquio:", um(cursor, "SELECT com FROM quando"))
    linha("timestamp  lido em Tóquio:", um(cursor, "SELECT sem FROM quando"))
    cursor.execute("SET TIME ZONE 'America/Sao_Paulo'")
    print("    >>> o timestamptz NÃO guarda o fuso: ele guarda o instante em")
    print("        UTC e mostra no fuso de quem lê. O timestamp não guarda")
    print("        instante nenhum — é um número de calendário e relógio")

    linha("date - date (dias corridos):",
          um(cursor, "SELECT '2026-08-06'::date - '2026-06-02'::date"))
    linha("age(), como o banco escreve:",
          um(cursor, "SELECT age('2026-08-06'::date, "
                     "'2026-06-02'::date)::text"))
    linha("age(), como o psycopg entrega:",
          um(cursor, "SELECT age('2026-08-06'::date, '2026-06-02'::date)"))
    linha("31 de janeiro + 1 mês:",
          um(cursor, "SELECT '2026-01-31'::date + interval '1 month'"))
    linha("somar:", um(cursor, "SELECT '2026-08-06'::date + interval '45 days'"))
    linha("truncar no mês:",
          um(cursor, "SELECT date_trunc('month', '2026-08-06 15:32'::timestamp)"))
    linha("extrair:", um(cursor, "SELECT extract(dow FROM '2026-08-06'::date)"))
    cursor.execute("""
        SELECT date_trunc('month', data)::date AS mes, count(*)
        FROM pedidos GROUP BY 1 ORDER BY 1
    """)
    for mes, quantos in cursor.fetchall():
        linha("pedidos em %s:" % mes, quantos)
    print("    >>> date_trunc é o GROUP BY por mês que no módulo 03 precisou")
    print("        de strftime — e que aqui continua sendo uma data de verdade")
    print()


def main() -> None:
    with psycopg.connect(URI) as conexao:
        with conexao.cursor() as cursor:
            cena_1_dinheiro(cursor)
            cena_2_o_que_o_postgres_recusa(cursor)
            cena_3_json_e_jsonb(cursor)
            cena_4_consultar_dentro(cursor)
            cena_5_indice_gin(cursor)
            cena_6_arrays(cursor)
            cena_7_uuid(cursor)
            cena_8_datas(cursor)


if __name__ == "__main__":
    main()
