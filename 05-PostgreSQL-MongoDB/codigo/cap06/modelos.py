"""Modelos declarativos: a classe É a tabela.

Sete cenas. A pergunta central é "o que a anotação de tipo do 04.14
passa a decidir quando ela está dentro de um modelo?".

    [1] a classe e a tabela que ela descreve
    [2] a anotação decide NOT NULL
    [3] o DDL que sai de cada classe
    [4] default do Python e default do servidor
    [5] create_all: o que ele faz e o que ele NÃO faz
    [6] o modelo confere contra o banco de verdade
    [7] restrições e índices declarados na classe

Uso:
    python codigo/laboratorio.py
    python codigo/cap06/modelos.py
"""

from __future__ import annotations

import datetime as dt
import sys
from decimal import Decimal
from pathlib import Path

import sqlalchemy as sa
from sqlalchemy.schema import CreateTable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from laboratorio import uri  # noqa: E402
from modelo import Base, Cliente, Cotacao, ItemPedido, Pedido, Produto  # noqa: E402

URI_SA = uri().replace("postgresql://", "postgresql+psycopg://", 1)


def linha(rotulo: str, valor: object) -> None:
    print("    %-36s %s" % (rotulo, valor))


def cena_1_classe_e_tabela() -> None:
    print("[1] A CLASSE E A TABELA QUE ELA DESCREVE")
    linha("Produto.__tablename__:", Produto.__tablename__)
    linha("Produto.__table__ é um:", type(Produto.__table__).__name__)
    linha("colunas:", [c.name for c in Produto.__table__.columns])
    linha("Produto.nome é um:", type(Produto.nome).__name__)
    linha("e Produto.nome == 'x' vira:",
          str(Produto.nome == "x"))
    linha("tabelas registradas na Base:", sorted(Base.metadata.tables))
    print("    >>> a classe não guarda dados: ela DESCREVE a tabela. E o")
    print("        atributo de classe é uma expressão SQL, o que faz")
    print("        `Produto.nome == 'x'` virar um WHERE em vez de um bool")
    print()


def cena_2_anotacao_decide() -> None:
    print("[2] A ANOTAÇÃO DECIDE NOT NULL")
    for modelo, campo in [(Cliente, "nome"), (Cliente, "email"),
                          (Produto, "preco_centavos"), (Cotacao, "observacao")]:
        coluna = modelo.__table__.columns[campo]
        anotacao = modelo.__annotations__.get(campo, "?")
        linha("%s.%s" % (modelo.__name__, campo),
              "%-22s -> %s %s" % (anotacao, coluna.type,
                                  "NULL" if coluna.nullable else "NOT NULL"))
    print("    >>> `Mapped[str]` vira NOT NULL e `Mapped[str | None]` aceita")
    print("        nulo. A anotação do 04.14, que o Python ignora e o mypy")
    print("        lê, aqui vira restrição no banco")
    print()


def cena_3_ddl(engine: sa.Engine) -> None:
    print("[3] O DDL QUE SAI DE CADA CLASSE")
    for pedaco in str(CreateTable(Cotacao.__table__).compile(engine)).split(
            "\n"):
        if pedaco.strip():
            print("        " + pedaco.rstrip())
    print("    >>> `Mapped[Decimal]` com Numeric(12,4) virou NUMERIC(12, 4),")
    print("        e `registrada_em` só saiu WITH TIME ZONE porque o modelo")
    print("        declara DateTime(timezone=True): `Mapped[datetime]`")
    print("        sozinho produz o tipo SEM fuso, que o 05.03/§6.8 desaconselha")
    print()


def cena_4_defaults(engine: sa.Engine) -> None:
    print("[4] DEFAULT DO PYTHON E DEFAULT DO SERVIDOR")
    coluna_ativo = Produto.__table__.columns["ativo"]
    linha("Produto.ativo default (Python):", coluna_ativo.default)
    linha("Produto.ativo server_default:",
          coluna_ativo.server_default.arg if coluna_ativo.server_default
          else None)
    coluna_data = Cotacao.__table__.columns["registrada_em"]
    linha("Cotacao.registrada_em default:", coluna_data.default)
    linha("... e server_default:",
          str(coluna_data.server_default.arg) if coluna_data.server_default
          else None)
    with engine.begin() as conexao:
        conexao.execute(sa.text(
            "INSERT INTO cotacoes (id, moeda, valor) "
            "VALUES (1, 'USD', 5.4321)"))
        alvo = conexao.execute(sa.text(
            "SELECT registrada_em FROM cotacoes WHERE id = 1")).scalar()
    linha("INSERT cru, sem passar pelo ORM:", alvo)
    print("    >>> só o server_default alcança quem escreve por fora do")
    print("        Python — migração, script de carga, outro serviço. O")
    print("        default do Python só vale para objetos criados pelo ORM")
    print()


def cena_5_create_all(engine: sa.Engine) -> None:
    print("[5] create_all: O QUE ELE FAZ E O QUE NÃO FAZ")
    inspetor = sa.inspect(engine)
    linha("cotacoes existe agora?", inspetor.has_table("cotacoes"))
    linha("colunas no banco:",
          [c["name"] for c in inspetor.get_columns("cotacoes")])

    Cotacao.__table__.append_column(
        sa.Column("fonte", sa.Text(), nullable=True))
    Base.metadata.create_all(engine)          # rodando de novo
    inspetor = sa.inspect(engine)
    linha("depois de acrescentar 'fonte':",
          [c["name"] for c in inspetor.get_columns("cotacoes")])
    print("    >>> create_all cria o que FALTA e NÃO altera o que existe.")
    print("        A coluna nova está no modelo e não está no banco — e o")
    print("        programa vai falhar ao consultá-la, sem aviso nenhum.")
    print("        É essa lacuna que o Alembic (05.10) preenche")
    print()


def cena_6_conferir_contra_o_banco(engine: sa.Engine) -> None:
    print("[6] O MODELO CONFERE CONTRA O BANCO DE VERDADE")
    inspetor = sa.inspect(engine)
    for modelo in (Cliente, Produto, Pedido, ItemPedido):
        do_banco = {c["name"] for c in
                    inspetor.get_columns(modelo.__tablename__)}
        do_modelo = {c.name for c in modelo.__table__.columns}
        estado = "iguais" if do_banco == do_modelo else "DIVERGEM: %s" % (
            do_banco ^ do_modelo)
        linha("%s (%d colunas)" % (modelo.__tablename__, len(do_modelo)),
              "nomes %s" % estado)

    print("    -- e agora comparando os TIPOS, e não os nomes --")
    for modelo in (Cliente, Produto, Pedido, ItemPedido):
        tipos_banco = {c["name"]: c["type"].compile(engine.dialect)
                       for c in inspetor.get_columns(modelo.__tablename__)}
        for coluna in modelo.__table__.columns:
            no_banco = tipos_banco[coluna.name]
            no_modelo = coluna.type.compile(engine.dialect)
            if no_banco != no_modelo:
                linha("%s.%s" % (modelo.__tablename__, coluna.name),
                      "banco=%s  modelo=%s" % (no_banco, no_modelo))
    print("    >>> os modelos descrevem as MESMAS tabelas do laboratório,")
    print("        que são as mesmas do módulo 03. Nada de schema novo")
    print()


def cena_7_restricoes(engine: sa.Engine) -> None:
    print("[7] RESTRIÇÕES E ÍNDICES DECLARADOS NA CLASSE")
    for restricao in sorted(Produto.__table__.constraints,
                            key=lambda r: type(r).__name__):
        linha(type(restricao).__name__, restricao.name)
    linha("índices declarados:",
          [(i.name, [c.name for c in i.columns])
           for i in Produto.__table__.indexes])
    inspetor = sa.inspect(engine)
    linha("índices que existem no banco:",
          [i["name"] for i in inspetor.get_indexes("produtos")])
    print("    >>> o índice está no MODELO e não no banco, porque a tabela")
    print("        já existia quando o create_all rodou. Mesma lacuna da")
    print("        cena 5, e mesma resposta: 05.10")
    print()


def main() -> None:
    engine = sa.create_engine(URI_SA)
    try:
        with engine.begin() as conexao:
            conexao.execute(sa.text("DROP TABLE IF EXISTS cotacoes"))
        Base.metadata.create_all(engine)
        cena_1_classe_e_tabela()
        cena_2_anotacao_decide()
        cena_3_ddl(engine)
        cena_4_defaults(engine)
        cena_5_create_all(engine)
        cena_6_conferir_contra_o_banco(engine)
        cena_7_restricoes(engine)
        with engine.begin() as conexao:
            conexao.execute(sa.text("DROP TABLE IF EXISTS cotacoes"))
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
