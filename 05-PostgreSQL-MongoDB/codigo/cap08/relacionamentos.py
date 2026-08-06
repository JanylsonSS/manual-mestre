"""Relacionamentos: navegar entre objetos, e o SQL que isso custa.

Oito cenas. A pergunta central é "quanto custa escrever um ponto?".

    [1] navegar de um lado para o outro
    [2] cada ponto é uma consulta
    [3] back_populates: os dois lados coerentes na MEMÓRIA
    [4] cascata do ORM e cascata do banco
    [5] muitos-para-muitos com tabela de associação
    [6] quando o vínculo tem atributo, ele vira classe
    [7] lazy="raise": transformar surpresa em erro
    [8] a ordem dentro da coleção

Uso:
    python codigo/laboratorio.py
    python codigo/cap08/relacionamentos.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import sqlalchemy as sa
from sqlalchemy import event
from sqlalchemy.orm import Session, raiseload

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from laboratorio import uri  # noqa: E402
from modelo import (Base, Cliente, Etiqueta, ItemPedido,  # noqa: E402
                    Pedido, Produto)

URI_SA = uri().replace("postgresql://", "postgresql+psycopg://", 1)
SQL_VISTO: list[str] = []


def linha(rotulo: str, valor: object) -> None:
    print("    %-38s %s" % (rotulo, valor))


def gravar_sql(engine: sa.Engine) -> None:
    @event.listens_for(engine, "before_cursor_execute")
    def _anotar(conn, cursor, comando, param, ctx, muitos):  # type: ignore[no-untyped-def]
        SQL_VISTO.append(" ".join(comando.split())[:74])


def cena_1_navegar(sessao: Session) -> None:
    print("[1] NAVEGAR DE UM LADO PARA O OUTRO")
    pedido = sessao.get(Pedido, 1)
    assert pedido is not None
    linha("o pedido:", pedido)
    linha("pedido.cliente:", pedido.cliente)
    linha("pedido.itens:", pedido.itens)
    linha("o produto do primeiro item:", pedido.itens[0].produto)
    linha("e de volta: cliente.pedidos:",
          [p.id for p in pedido.cliente.pedidos])
    linha("total do pedido (property):",
          "R$ %.2f" % (pedido.total_centavos / 100))
    print("    >>> quatro tabelas atravessadas com pontos. Nenhum JOIN")
    print("        escrito, e nenhum id manipulado à mão")
    print()


def cena_2_cada_ponto_custa(sessao: Session) -> None:
    print("[2] CADA PONTO É UMA CONSULTA")
    sessao.expunge_all()
    SQL_VISTO.clear()
    pedido = sessao.get(Pedido, 20)
    assert pedido is not None
    linha("get(Pedido, 20):", "%d consulta(s)" % len(SQL_VISTO))
    SQL_VISTO.clear()
    _ = pedido.cliente
    linha("ler .cliente:", "%d consulta(s)" % len(SQL_VISTO))
    for comando in SQL_VISTO:
        linha("", comando)
    SQL_VISTO.clear()
    itens = pedido.itens
    linha("ler .itens:", "%d consulta(s)" % len(SQL_VISTO))
    SQL_VISTO.clear()
    for item in itens:
        _ = item.produto.nome
    linha("ler .produto de %d itens:" % len(itens),
          "%d consulta(s)" % len(SQL_VISTO))
    linha("total para UM pedido:", "%d consultas" % (2 + 1 + len(itens)))
    SQL_VISTO.clear()
    print("    >>> o carregamento é PREGUIÇOSO: a coleção só vai ao banco")
    print("        quando alguém a lê. Num laço sobre muitos pedidos isso")
    print("        vira o problema N+1, que o 05.09 mede e resolve")
    print()


def cena_3_back_populates(sessao: Session) -> None:
    print("[3] back_populates: OS DOIS LADOS COERENTES NA MEMÓRIA")
    pedido = sessao.get(Pedido, 3)
    assert pedido is not None
    quantos_antes = len(pedido.itens)
    novo = ItemPedido(produto_id=9, quantidade=1,
                      preco_unitario_centavos=4990)
    linha("o item novo conhece o pedido?", novo.pedido)
    pedido.itens.append(novo)
    linha("depois do append, item.pedido:", novo.pedido)
    linha("e sem nenhum flush?", not sessao.new or novo in sessao.new)
    linha("itens antes / depois:", "%d / %d" % (quantos_antes,
                                                len(pedido.itens)))
    sessao.rollback()
    print("    >>> `back_populates` liga os dois atributos: mexer num")
    print("        atualiza o outro NA MEMÓRIA, antes de qualquer SQL. Sem")
    print("        ele, os dois lados discordam até você recarregar")
    print()


def cena_4_cascatas(engine: sa.Engine, sessao: Session) -> None:
    print("[4] CASCATA DO ORM E CASCATA DO BANCO")
    sessao.add(Cliente(id=950, nome="Cascata", cidade="Natal"))
    pedido = Pedido(id=950, cliente_id=950, data=sa.func.current_date(),
                    status="pendente")
    pedido.itens = [
        ItemPedido(produto_id=1, quantidade=1, preco_unitario_centavos=100),
        ItemPedido(produto_id=2, quantidade=2, preco_unitario_centavos=200),
    ]
    sessao.add(pedido)
    sessao.flush()
    linha("itens criados:", sessao.scalar(
        sa.select(sa.func.count()).select_from(ItemPedido)
        .where(ItemPedido.pedido_id == 950)))

    removido = pedido.itens.pop()
    sessao.flush()
    linha("depois de pop() na lista:", sessao.scalar(
        sa.select(sa.func.count()).select_from(ItemPedido)
        .where(ItemPedido.pedido_id == 950)))
    linha("o item removido virou:", "órfão, apagado pelo delete-orphan")
    linha("(id que existia:", "%s)" % removido.id)

    sessao.delete(pedido)
    sessao.flush()
    linha("depois de delete(pedido):", sessao.scalar(
        sa.select(sa.func.count()).select_from(ItemPedido)
        .where(ItemPedido.pedido_id == 950)))
    sessao.rollback()

    with engine.begin() as conexao:
        conexao.execute(sa.text(
            "INSERT INTO clientes (id, nome) VALUES (951, 'Cascata SQL')"))
        conexao.execute(sa.text(
            "INSERT INTO pedidos (id, cliente_id, data, status) "
            "VALUES (951, 951, current_date, 'pendente')"))
        conexao.execute(sa.text(
            "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, "
            "preco_unitario_centavos) VALUES (951, 1, 1, 100)"))
        conexao.execute(sa.text("DELETE FROM pedidos WHERE id = 951"))
        sobrou = conexao.execute(sa.text(
            "SELECT count(*) FROM itens_pedido WHERE pedido_id = 951")).scalar()
        linha("DELETE cru, sem ORM nenhum:", "sobraram %s itens" % sobrou)
        conexao.execute(sa.text("DELETE FROM clientes WHERE id = 951"))
    print("    >>> são DUAS cascatas independentes. `delete-orphan` é do")
    print("        ORM e vale para quem passa por ele; `ON DELETE CASCADE`")
    print("        é do banco e vale para todo mundo. Ter as duas é o certo")
    print()


def cena_5_muitos_para_muitos(sessao: Session) -> None:
    print("[5] MUITOS-PARA-MUITOS COM TABELA DE ASSOCIAÇÃO")
    sem_fio = Etiqueta(nome="sem-fio")
    promocao = Etiqueta(nome="promocao")
    fone = sessao.get(Produto, 1)
    mouse = sessao.get(Produto, 2)
    assert fone is not None and mouse is not None
    fone.etiquetas = [sem_fio, promocao]
    mouse.etiquetas.append(sem_fio)
    sessao.flush()

    linha("etiquetas do fone:", fone.etiquetas)
    linha("produtos da etiqueta sem-fio:", [p.id for p in sem_fio.produtos])
    linha("linhas na tabela de ligação:", sessao.scalar(
        sa.select(sa.func.count()).select_from(
            sa.table("produto_etiqueta"))))
    SQL_VISTO.clear()
    achados = sessao.scalars(
        sa.select(Produto).join(Produto.etiquetas)
        .where(Etiqueta.nome == "sem-fio")).all()
    linha("consultando por etiqueta:", [p.id for p in achados])
    for comando in SQL_VISTO[:1]:
        linha("o JOIN gerado:", comando)
    SQL_VISTO.clear()
    sessao.rollback()
    print("    >>> `secondary=` esconde a tabela de ligação: você trabalha")
    print("        com duas listas e nunca escreve a terceira tabela")
    print()


def cena_6_vinculo_com_atributo(sessao: Session) -> None:
    print("[6] QUANDO O VÍNCULO TEM ATRIBUTO, ELE VIRA CLASSE")
    pedido = sessao.get(Pedido, 1)
    assert pedido is not None
    for item in pedido.itens:
        linha("item %d:" % item.id,
              "%s x%d a R$ %.2f" % (item.produto.nome, item.quantidade,
                                    item.preco_unitario_centavos / 100))
    linha("um pedido tem produtos?", "sim, mas com quantidade e preço")
    linha("por isso itens_pedido é:", "classe (ItemPedido), não secondary")
    print("    >>> `secondary` serve quando a ligação é só uma ligação. Se")
    print("        ela guarda quantidade, preço ou data, vira entidade — e")
    print("        o preço unitário aqui é o do momento da compra (05.07/§9)")
    print()


def cena_7_lazy_raise(sessao: Session) -> None:
    print("[7] lazy='raise': TRANSFORMAR SURPRESA EM ERRO")
    sessao.expunge_all()
    pedido = sessao.scalars(
        sa.select(Pedido).where(Pedido.id == 4)
        .options(raiseload(Pedido.itens))).one()
    linha("o pedido carregou:", pedido)
    try:
        linha("lendo .itens:", pedido.itens)
    except Exception as erro:
        linha("lendo .itens:",
              "%s: %s" % (type(erro).__name__,
                          str(erro).split("\n")[0][:44]))
    print("    >>> `raiseload` faz a consulta preguiçosa VIRAR ERRO. É como")
    print("        se garante, num endpoint crítico, que ninguém acrescentou")
    print("        um ponto inocente no template")
    print()


def cena_8_ordem(sessao: Session) -> None:
    print("[8] A ORDEM DENTRO DA COLEÇÃO")
    sessao.expunge_all()
    pedido = sessao.get(Pedido, 20)
    assert pedido is not None
    linha("itens do pedido 20:", [i.id for i in pedido.itens])
    linha("declarado no modelo:", 'order_by="ItemPedido.id"')

    print("    -- e por que isso não é preciosismo --")
    crua = sa.text("SELECT id FROM itens_pedido WHERE pedido_id = 20")
    linha("sem ORDER BY, agora:", sessao.scalars(crua).all())
    sessao.execute(sa.text(
        "UPDATE itens_pedido SET quantidade = quantidade WHERE id = 28"))
    sessao.commit()
    linha("depois de um UPDATE no id 28:", sessao.scalars(crua).all())
    sessao.execute(sa.text(
        "UPDATE itens_pedido SET quantidade = quantidade WHERE id = 29"))
    sessao.commit()
    linha("depois de um UPDATE no id 29:", sessao.scalars(crua).all())
    linha("a posição física de cada linha:", sessao.execute(sa.text(
        "SELECT id, ctid::text FROM itens_pedido "
        "WHERE pedido_id = 20")).all())
    print("    >>> o MVCC (05.01/§6.3) não altera a linha: ele escreve uma")
    print("        versão NOVA no fim da tabela. Sem ORDER BY, a ordem que")
    print("        volta é a física — e ela muda a cada UPDATE, em silêncio")
    print()


def main() -> None:
    engine = sa.create_engine(URI_SA)
    gravar_sql(engine)
    try:
        Base.metadata.create_all(
            engine, tables=[Base.metadata.tables["etiquetas"],
                            Base.metadata.tables["produto_etiqueta"]])
        with Session(engine) as sessao:
            cena_1_navegar(sessao)
            cena_2_cada_ponto_custa(sessao)
            cena_3_back_populates(sessao)
            cena_4_cascatas(engine, sessao)
            cena_5_muitos_para_muitos(sessao)
            cena_6_vinculo_com_atributo(sessao)
            cena_7_lazy_raise(sessao)
            cena_8_ordem(sessao)
    finally:
        with engine.begin() as conexao:
            conexao.execute(sa.text("DROP TABLE IF EXISTS produto_etiqueta"))
            conexao.execute(sa.text("DROP TABLE IF EXISTS etiquetas"))
        engine.dispose()


if __name__ == "__main__":
    main()
