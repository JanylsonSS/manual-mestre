"""O N+1, medido — e as estratégias que o resolvem.

Este é o capítulo em que quase tudo é contar consultas. O instrumento é
o registrador do 05.07/§10, agora com cronômetro junto.

    [1] o N+1, em consultas e em milissegundos
    [2] as três estratégias, lado a lado
    [3] joinedload multiplica linhas — e o unique() obrigatório
    [4] joinedload com LIMIT: o erro que o SQLAlchemy evita
    [5] contains_eager: quando VOCÊ escreve o JOIN
    [6] trazer só o que vai usar
    [7] não carregar nada: agregar no banco
    [8] o custo de virar objeto

Uso:
    python codigo/laboratorio.py
    python codigo/cap09/carregamento.py

ATENÇÃO: este script SEMEIA 2000 pedidos e 10000 itens, porque as
medições precisam de volume. Os vinte pedidos do módulo 03 continuam
intactos (a semeadura só cria itens para `id > 20`), mas as contagens
totais mudam. Para voltar ao estado original, rode `laboratorio.py` de
novo — ele recria as tabelas do zero.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy.orm import (Session, contains_eager, joinedload, load_only,
                            selectinload, subqueryload)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from laboratorio import uri  # noqa: E402
from modelo import Cliente, ItemPedido, Pedido, Produto  # noqa: E402

URI = uri()
URI_SA = URI.replace("postgresql://", "postgresql+psycopg://", 1)
SQL_VISTO: list[str] = []

PEDIDOS_EXTRA = 2000
ITENS_POR_PEDIDO = 5


def linha(rotulo: str, valor: object) -> None:
    print("    %-40s %s" % (rotulo, valor))


def gravar_sql(engine: sa.Engine) -> None:
    @event.listens_for(engine, "before_cursor_execute")
    def _anotar(conn, cursor, comando, param, ctx, muitos):  # type: ignore[no-untyped-def]
        SQL_VISTO.append(" ".join(comando.split())[:70])


def semear(engine: sa.Engine) -> None:
    """Cria volume para as medições, sem tocar nos dados do módulo 03."""
    with engine.begin() as conexao:
        ja = conexao.execute(sa.text(
            "SELECT count(*) FROM pedidos")).scalar() or 0
        if ja > PEDIDOS_EXTRA:
            return
        conexao.execute(sa.text("""
            INSERT INTO pedidos (cliente_id, data, status)
            SELECT 1 + mod(i, 8),
                   DATE '2026-01-01' + mod(i, 200),
                   (ARRAY['pago','pendente','cancelado'])[1 + mod(i, 3)]
            FROM generate_series(1, :quantos) AS i
        """), {"quantos": PEDIDOS_EXTRA})
        conexao.execute(sa.text("""
            INSERT INTO itens_pedido (pedido_id, produto_id, quantidade,
                                      preco_unitario_centavos)
            SELECT p.id, 1 + mod(p.id + j, 12), 1 + mod(j, 3), 1000 + j * 37
            FROM pedidos p
            CROSS JOIN generate_series(1, :itens) AS j
            WHERE p.id > 20
        """), {"itens": ITENS_POR_PEDIDO})


def medir(rotulo: str, funcao) -> tuple[int, float]:  # type: ignore[no-untyped-def]
    SQL_VISTO.clear()
    inicio = time.perf_counter()
    funcao()
    ms = (time.perf_counter() - inicio) * 1000
    quantas = len(SQL_VISTO)
    linha(rotulo, "%5d consulta(s)   %8.1f ms" % (quantas, ms))
    SQL_VISTO.clear()
    return quantas, ms


def cena_1_o_n_mais_um(engine: sa.Engine) -> None:
    print("[1] O N+1, EM CONSULTAS E EM MILISSEGUNDOS")
    linha("pedidos no banco:", "")

    def ingenuo() -> None:
        with Session(engine) as sessao:
            total = 0
            for pedido in sessao.scalars(
                    sa.select(Pedido).where(Pedido.status == "pago")
                    .limit(300)):
                for item in pedido.itens:
                    total += item.subtotal_centavos
            linha("  soma calculada:", "R$ %.2f" % (total / 100))

    medir("laço ingênuo sobre 300 pedidos:", ingenuo)
    print("    >>> uma consulta para os pedidos e uma para os itens de cada")
    print("        um. O código não tem nada de errado à vista: ele lê")
    print("        `pedido.itens`, que é exatamente o que o 05.08 ensinou")
    print()


def cena_2_tres_estrategias(engine: sa.Engine) -> None:
    print("[2] AS TRÊS ESTRATÉGIAS, LADO A LADO")

    def rodar(opcao) -> None:  # type: ignore[no-untyped-def]
        with Session(engine) as sessao:
            consulta = (sa.select(Pedido)
                        .where(Pedido.status == "pago").limit(300))
            if opcao is not None:
                consulta = consulta.options(opcao)
            total = 0
            for pedido in sessao.scalars(consulta).unique():
                for item in pedido.itens:
                    total += item.subtotal_centavos

    medir("sem opção (preguiçoso):", lambda: rodar(None))
    medir("joinedload:", lambda: rodar(joinedload(Pedido.itens)))
    medir("selectinload:", lambda: rodar(selectinload(Pedido.itens)))
    medir("subqueryload:", lambda: rodar(subqueryload(Pedido.itens)))
    print("    >>> joinedload traz tudo num JOIN só; selectinload faz uma")
    print("        segunda consulta com IN (...); subqueryload repete a")
    print("        consulta original dentro de uma subconsulta")
    print()


def cena_3_joinedload_multiplica(engine: sa.Engine) -> None:
    print("[3] joinedload MULTIPLICA LINHAS — E O unique() OBRIGATÓRIO")
    with Session(engine) as sessao:
        consulta = (sa.select(Pedido).where(Pedido.id.in_([1, 2, 3]))
                    .options(joinedload(Pedido.itens)))
        try:
            sessao.scalars(consulta).all()
        except Exception as erro:
            linha("sem unique():",
                  "%s: %s" % (type(erro).__name__,
                              str(erro).split("\n")[0][:46]))
        obtidos = sessao.scalars(consulta).unique().all()
        linha("com unique(), pedidos:", [p.id for p in obtidos])
        linha("itens de cada um:", [len(p.itens) for p in obtidos])
        cru = sessao.execute(sa.text(
            "SELECT count(*) FROM pedidos p JOIN itens_pedido i "
            "ON i.pedido_id = p.id WHERE p.id IN (1,2,3)")).scalar()
        linha("linhas que o JOIN devolveu:", cru)
    print("    >>> o JOIN devolve uma linha por ITEM, e o mesmo pedido")
    print("        aparece repetido. O `unique()` é obrigatório em 2.0 —")
    print("        antes era silencioso, e a contagem saía errada")
    print()


def cena_4_joinedload_com_limite(engine: sa.Engine) -> None:
    print("[4] joinedload COM LIMIT: O ERRO QUE O SQLAlchemy EVITA")
    with Session(engine) as sessao:
        SQL_VISTO.clear()
        obtidos = sessao.scalars(
            sa.select(Pedido).order_by(Pedido.id).limit(3)
            .options(joinedload(Pedido.itens))).unique().all()
        linha("pedidos pedidos:", 3)
        linha("pedidos recebidos:", len(obtidos))
        for comando in SQL_VISTO:
            if "anon" in comando or "LIMIT" in comando:
                linha("o SQL gerado:", comando)
        SQL_VISTO.clear()
    print("    >>> um LIMIT 3 sobre o JOIN cortaria no meio dos ITENS e")
    print("        traria menos de 3 pedidos. O SQLAlchemy embrulha a")
    print("        consulta numa subconsulta e aplica o LIMIT lá dentro")
    print()


def cena_5_contains_eager(engine: sa.Engine) -> None:
    print("[5] contains_eager: QUANDO VOCÊ ESCREVE O JOIN")
    with Session(engine) as sessao:
        SQL_VISTO.clear()
        obtidos = sessao.scalars(
            sa.select(Pedido)
            .join(Pedido.itens)
            .where(Pedido.id.in_([1, 2, 3]), ItemPedido.quantidade >= 2)
            .options(contains_eager(Pedido.itens))).unique().all()
        for pedido in obtidos:
            linha("pedido %d:" % pedido.id,
                  "%d item(ns) com quantidade >= 2"
                  % len(pedido.itens))
        linha("consultas emitidas:", len(SQL_VISTO))
        SQL_VISTO.clear()
        completo = sessao.get(Pedido, 1)
        assert completo is not None
        sessao.expire(completo)
        linha("o pedido 1 tem, de verdade:", "%d itens"
              % len(sessao.get(Pedido, 1).itens))
    print("    >>> ATENÇÃO: a coleção ficou FILTRADA. `contains_eager` diz")
    print("        'preencha com o que veio no meu JOIN', e o que veio foi")
    print("        só o que passou no WHERE. É poderoso e é uma armadilha")
    print()


def cena_6_so_o_necessario(engine: sa.Engine) -> None:
    print("[6] TRAZER SÓ O QUE VAI USAR")
    with Session(engine) as sessao:
        SQL_VISTO.clear()
        sessao.scalars(sa.select(Produto).limit(5)).all()
        linha("select(Produto):", SQL_VISTO[0] if SQL_VISTO else "")
        SQL_VISTO.clear()
        sessao.expunge_all()
        sessao.scalars(
            sa.select(Produto).limit(5)
            .options(load_only(Produto.nome))).all()
        linha("com load_only(nome):", SQL_VISTO[0] if SQL_VISTO else "")
        SQL_VISTO.clear()
        sessao.expunge_all()
        nomes = sessao.scalars(sa.select(Produto.nome).limit(5)).all()
        linha("select(Produto.nome):", SQL_VISTO[0] if SQL_VISTO else "")
        linha("e o que volta:", nomes[:2])
        SQL_VISTO.clear()
    print("    >>> `load_only` traz menos colunas e ainda constrói o objeto;")
    print("        `select(Produto.nome)` não constrói objeto nenhum e")
    print("        devolve texto. São coisas diferentes, com custos diferentes")
    print()


def cena_7_agregar_no_banco(engine: sa.Engine) -> None:
    print("[7] NÃO CARREGAR NADA: AGREGAR NO BANCO")

    def em_python() -> None:
        with Session(engine) as sessao:
            total = 0
            for pedido in sessao.scalars(
                    sa.select(Pedido).where(Pedido.status == "pago")
                    .limit(300).options(selectinload(Pedido.itens))):
                total += pedido.total_centavos
            linha("  total (Python):", "R$ %.2f" % (total / 100))

    def no_banco() -> None:
        with Session(engine) as sessao:
            alvo = sa.select(Pedido.id).where(
                Pedido.status == "pago").limit(300).subquery()
            total = sessao.scalar(
                sa.select(sa.func.sum(ItemPedido.quantidade
                                      * ItemPedido.preco_unitario_centavos))
                .where(ItemPedido.pedido_id.in_(sa.select(alvo.c.id))))
            linha("  total (SQL):", "R$ %.2f" % ((total or 0) / 100))

    medir("somando em Python:", em_python)
    medir("somando no banco:", no_banco)
    print("    >>> a pergunta era um NÚMERO, e a versão de cima trouxe")
    print("        milhares de objetos para chegar nele. A otimização que")
    print("        mais rende é não carregar")
    print()


def cena_8_custo_de_virar_objeto(engine: sa.Engine) -> None:
    print("[8] O CUSTO DE VIRAR OBJETO")
    quantos = 5000

    def orm() -> None:
        with Session(engine) as sessao:
            objetos = sessao.scalars(
                sa.select(ItemPedido).limit(quantos)).all()
            _ = sum(i.quantidade for i in objetos)

    def nucleo() -> None:
        with engine.connect() as conexao:
            linhas = conexao.execute(sa.text(
                "SELECT id, pedido_id, produto_id, quantidade, "
                "preco_unitario_centavos FROM itens_pedido LIMIT %d"
                % quantos)).all()
            _ = sum(linha[3] for linha in linhas)

    _, ms_orm = medir("%d linhas como objetos:" % quantos, orm)
    _, ms_nucleo = medir("%d linhas como tuplas:" % quantos, nucleo)
    linha("razão:", "%.1fx" % (ms_orm / max(ms_nucleo, 0.001)))
    print("    >>> a mesma consulta, o mesmo banco. A diferença é construir")
    print("        objetos, instrumentar atributos e registrá-los no mapa de")
    print("        identidade — o preço do que o 05.07 e o 05.08 dão de graça")
    print()


def main() -> None:
    engine = sa.create_engine(URI_SA)
    try:
        semear(engine)
        gravar_sql(engine)
        with engine.connect() as conexao:
            print("    (base de medição: %s pedidos, %s itens)\n" % (
                conexao.execute(sa.text("SELECT count(*) FROM pedidos"))
                .scalar(),
                conexao.execute(sa.text("SELECT count(*) FROM itens_pedido"))
                .scalar()))
        cena_1_o_n_mais_um(engine)
        cena_2_tres_estrategias(engine)
        cena_3_joinedload_multiplica(engine)
        cena_4_joinedload_com_limite(engine)
        cena_5_contains_eager(engine)
        cena_6_so_o_necessario(engine)
        cena_7_agregar_no_banco(engine)
        cena_8_custo_de_virar_objeto(engine)
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
