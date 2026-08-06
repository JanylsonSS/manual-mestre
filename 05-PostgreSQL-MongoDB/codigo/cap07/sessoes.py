"""A sessão: o que ela guarda, o que ela decide e quando ela manda SQL.

Nove cenas. A pergunta central é "por que `produto.preco = 1` grava sem
eu chamar UPDATE — e por que às vezes não grava?".

    [1] o mapa de identidade
    [2] os quatro estados de um objeto
    [3] o que é sujo, e como a sessão sabe
    [4] flush e commit são coisas diferentes
    [5] autoflush: a consulta que grava antes de perguntar
    [6] o commit que expira tudo
    [7] o objeto que sai da sessão
    [8] rollback: o que acontece na memória
    [9] uma sessão por unidade de trabalho

Uso:
    python codigo/laboratorio.py
    python codigo/cap07/sessoes.py
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import sqlalchemy as sa
from sqlalchemy import event, inspect
from sqlalchemy.orm import Session

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from laboratorio import uri  # noqa: E402
from modelo import Cliente, Pedido, Produto  # noqa: E402

URI_SA = uri().replace("postgresql://", "postgresql+psycopg://", 1)
SQL_VISTO: list[str] = []


def linha(rotulo: str, valor: object) -> None:
    print("    %-38s %s" % (rotulo, valor))


def gravar_sql(engine: sa.Engine) -> None:
    """Anota todo comando que sai — é o instrumento do 05.09."""

    @event.listens_for(engine, "before_cursor_execute")
    def _anotar(conn, cursor, comando, param,  # type: ignore[no-untyped-def]
                ctx, muitos):
        SQL_VISTO.append(" ".join(comando.split())[:88])


def mostrar_sql(titulo: str = "SQL emitido") -> None:
    if not SQL_VISTO:
        linha(titulo + ":", "(nenhum)")
    for comando in SQL_VISTO:
        linha(titulo + ":", comando)
        titulo = " " * len(titulo)
    SQL_VISTO.clear()


def estado(objeto: object) -> str:
    situacao = inspect(objeto)
    for nome in ("transient", "pending", "persistent", "deleted", "detached"):
        if getattr(situacao, nome):
            return nome
    return "?"


def cena_1_mapa_de_identidade(sessao: Session) -> None:
    print("[1] O MAPA DE IDENTIDADE")
    SQL_VISTO.clear()
    primeiro = sessao.get(Produto, 1)
    linha("primeira busca:", primeiro)
    segundo = sessao.get(Produto, 1)
    linha("segunda busca:", segundo)
    linha("é o MESMO objeto?", primeiro is segundo)
    linha("quantos SELECT foram emitidos?", len(SQL_VISTO))
    terceiro = sessao.scalars(
        sa.select(Produto).where(Produto.id == 1)).one()
    linha("por select(), é o mesmo?", terceiro is primeiro)
    linha("objetos na sessão:", len(sessao.identity_map))
    SQL_VISTO.clear()
    print("    >>> a sessão guarda um objeto por chave primária. Pedir duas")
    print("        vezes não traz duas cópias — e `is` responde True, o que")
    print("        significa que alterar um altera 'os dois'")
    print()


def cena_2_estados(sessao: Session) -> None:
    print("[2] OS QUATRO ESTADOS DE UM OBJETO")
    novo = Cliente(id=901, nome="Teste Estados", cidade="Sao Paulo")
    linha("recém-criado:", estado(novo))
    sessao.add(novo)
    linha("depois de add():", estado(novo))
    sessao.flush()
    linha("depois de flush():", estado(novo))
    sessao.expunge(novo)
    linha("depois de expunge():", estado(novo))
    sessao.rollback()
    print("    >>> transitório (a sessão não conhece), pendente (conhece e")
    print("        ainda não mandou), persistente (existe no banco desta")
    print("        transação) e destacado (existe e a sessão soltou)")
    print()


def cena_3_sujo(sessao: Session) -> None:
    print("[3] O QUE É SUJO, E COMO A SESSÃO SABE")
    produto = sessao.get(Produto, 2)
    assert produto is not None
    linha("antes de mexer, dirty:", set(sessao.dirty))
    produto.preco_centavos = 9990
    linha("depois de mexer, dirty:", {p.id for p in sessao.dirty})
    situacao = inspect(produto).attrs.preco_centavos
    linha("valor antigo guardado:", situacao.history.deleted)
    linha("valor novo:", situacao.history.added)
    sessao.rollback()
    linha("depois do rollback:", sessao.get(Produto, 2).preco_centavos)
    print("    >>> ninguém chamou UPDATE. A sessão instrumentou o atributo")
    print("        (05.06/§7) e anotou o valor anterior — é assim que ela")
    print("        sabe o que mudou, e é o que ela chama de unit of work")
    print()


def cena_4_flush_e_commit(sessao: Session) -> None:
    print("[4] flush E commit SÃO COISAS DIFERENTES")
    SQL_VISTO.clear()
    novo = Pedido(cliente_id=1, data=dt.date(2026, 8, 6),
                  status="pendente")
    sessao.add(novo)
    linha("id antes do flush:", novo.id)
    sessao.flush()
    linha("id depois do flush:", novo.id)
    mostrar_sql("no flush")
    linha("a transação ainda está aberta?", sessao.in_transaction())
    sessao.rollback()
    linha("depois do rollback, o id:", novo.id)
    linha("e o estado:", estado(novo))
    print("    >>> flush MANDA o SQL e não fecha a transação; commit fecha.")
    print("        O id vem do banco no flush — e some no rollback, porque")
    print("        aquele INSERT deixou de existir")
    print()


def cena_5_autoflush(sessao: Session) -> None:
    print("[5] AUTOFLUSH: A CONSULTA QUE GRAVA ANTES DE PERGUNTAR")
    SQL_VISTO.clear()
    sessao.add(Cliente(id=902, nome="Autoflush", cidade="Recife"))
    linha("um cliente pendente, sem flush:", "")
    quantos = sessao.scalar(
        sa.select(sa.func.count()).select_from(Cliente))
    linha("COUNT nomeando a CLASSE:", quantos)
    mostrar_sql("emitido")
    sessao.rollback()

    sessao.add(Cliente(id=903, nome="Autoflush", cidade="Recife"))
    SQL_VISTO.clear()
    quantos = sessao.scalar(
        sa.select(sa.func.count()).select_from(Cliente.__table__))
    linha("COUNT nomeando a TABELA:", quantos)
    mostrar_sql("emitido")
    sessao.rollback()
    print("    >>> a MESMA pergunta, na MESMA sessão, com duas respostas.")
    print("        Nomear a classe é comando do ORM e dispara o autoflush;")
    print("        nomear `__table__` é comando do Core, e ele não dispara")
    print("    >>> o autoflush existe para a consulta enxergar o que está")
    print("        pendente. O efeito colateral é um SELECT que falha com")
    print("        erro de INSERT — e é o que assusta quem não espera")
    print()


def cena_6_expire_on_commit(engine: sa.Engine) -> None:
    print("[6] O COMMIT QUE EXPIRA TUDO")
    with Session(engine) as sessao:
        produto = sessao.get(Produto, 3)
        assert produto is not None
        sessao.commit()
        SQL_VISTO.clear()
        linha("ler um atributo depois do commit:", produto.nome)
        linha("quantos SELECT isso custou?", len(SQL_VISTO))
        mostrar_sql("recarga")

    with Session(engine, expire_on_commit=False) as sessao:
        produto = sessao.get(Produto, 3)
        assert produto is not None
        sessao.commit()
        SQL_VISTO.clear()
        linha("com expire_on_commit=False:", produto.nome)
        linha("quantos SELECT isso custou?", len(SQL_VISTO))
    print("    >>> por padrão o commit marca todo objeto como vencido, e o")
    print("        próximo acesso a um atributo dispara um SELECT. É correto")
    print("        (o dado pode ter mudado) e é uma consulta que ninguém viu")
    print()


def cena_7_objeto_fora_da_sessao(engine: sa.Engine) -> None:
    print("[7] O OBJETO QUE SAI DA SESSÃO")
    with Session(engine) as sessao:
        produto = sessao.get(Produto, 4)
        assert produto is not None
    linha("fechada SEM commit, estado:", estado(produto))
    try:
        linha("lendo um atributo fora:", produto.nome)
    except Exception as erro:
        linha("lendo um atributo fora:",
              "%s: %s" % (type(erro).__name__,
                          str(erro).split("\n")[0][:44]))

    with Session(engine) as sessao:
        comitado = sessao.get(Produto, 4)
        assert comitado is not None
        sessao.commit()
    linha("fechada COM commit, estado:", estado(comitado))
    try:
        linha("lendo um atributo fora:", comitado.nome)
    except Exception as erro:
        linha("lendo um atributo fora:",
              "%s: %s" % (type(erro).__name__,
                          str(erro).split("\n")[0][:44]))

    with Session(engine, expire_on_commit=False) as sessao:
        outro = sessao.get(Produto, 4)
        assert outro is not None
        sessao.commit()
    linha("com expire_on_commit=False:", outro.nome)
    print("    >>> o DetachedInstanceError NÃO vem de fechar a sessão: vem")
    print("        de o commit ter VENCIDO o objeto e não haver mais quem")
    print("        o recarregue. Fechar sem comitar deixa os valores lá")
    print()


def cena_8_rollback(engine: sa.Engine) -> None:
    print("[8] ROLLBACK: O QUE ACONTECE NA MEMÓRIA")
    with Session(engine) as sessao:
        produto = sessao.get(Produto, 5)
        assert produto is not None
        original = produto.preco_centavos
        produto.preco_centavos = 1
        linha("na memória, antes do rollback:", produto.preco_centavos)
        sessao.rollback()
        linha("na memória, depois:", produto.preco_centavos)
        linha("o valor original era:", original)
        linha("estado do objeto:", estado(produto))
    print("    >>> o rollback também desfaz a MEMÓRIA: os objetos voltam a")
    print("        vencer e recarregam do banco. É o oposto do que a")
    print("        intuição diz, e é o comportamento certo")
    print()


def cena_9_uma_sessao_por_trabalho(engine: sa.Engine) -> None:
    print("[9] UMA SESSÃO POR UNIDADE DE TRABALHO")
    with Session(engine) as sessao:
        with sessao.begin():
            pedido = Pedido(cliente_id=1,
                            data=dt.date(2026, 8, 6),
                            status="pendente")
            sessao.add(pedido)
            sessao.flush()
            linha("pedido criado com id:", pedido.id)
            criado = pedido.id
        linha("depois do with, gravado?", sessao.get(Pedido, criado)
              is not None)
        sessao.execute(sa.delete(Pedido).where(Pedido.id == criado))
        sessao.commit()

    try:
        with Session(engine) as sessao:
            with sessao.begin():
                sessao.add(Pedido(cliente_id=1,
                                  data=dt.date(2026, 8, 6),
                                  status="INVENTADO"))
    except sa.exc.IntegrityError as erro:
        linha("status fora do CHECK:", type(erro.orig).__name__)
    with Session(engine) as sessao:
        linha("pedidos ao final:",
              sessao.scalar(sa.select(sa.func.count())
                            .select_from(Pedido.__table__)))
    print("    >>> `with sessao.begin()` comita ao sair e desfaz na exceção.")
    print("        É o mesmo desenho do engine.begin() do 05.05, agora com")
    print("        os objetos junto")
    print()


def main() -> None:
    engine = sa.create_engine(URI_SA)
    gravar_sql(engine)
    try:
        with Session(engine) as sessao:
            cena_1_mapa_de_identidade(sessao)
            cena_2_estados(sessao)
            cena_3_sujo(sessao)
            cena_4_flush_e_commit(sessao)
            cena_5_autoflush(sessao)
        cena_6_expire_on_commit(engine)
        cena_7_objeto_fora_da_sessao(engine)
        cena_8_rollback(engine)
        cena_9_uma_sessao_por_trabalho(engine)
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
