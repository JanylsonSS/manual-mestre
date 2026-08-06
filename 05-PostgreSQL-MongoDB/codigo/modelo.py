"""Os modelos ORM da Aurora — usados dos capítulos 05.06 ao 05.11.

Eles descrevem **as mesmas tabelas** que o `laboratorio.py` cria, e que
o módulo 03 usava em SQLite. Nada aqui inventa schema: a ideia é que
você compare o `CREATE TABLE` do laboratório com estas classes e veja a
mesma coisa dita de dois jeitos.

A tipagem é o assunto do 05.06: `Mapped[int]` vira `NOT NULL` e
`Mapped[str | None]` vira coluna que aceita nulo — a anotação do 04.14
passa a ter efeito no banco.
"""

from __future__ import annotations

import datetime as dt
from decimal import Decimal

from sqlalchemy import (CheckConstraint, Column, Date, DateTime, ForeignKey,
                        Index, Integer, Numeric, Table, Text, func)

from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column,
                            relationship)

# `Mapped[datetime]` sozinho produz TIMESTAMP **WITHOUT TIME ZONE** — o
# tipo que o 05.03/§6.8 recomenda evitar para eventos. O SQLAlchemy não
# tem como adivinhar, e o padrão dele é o do SQL. Declarar é obrigatório.
INSTANTE = DateTime(timezone=True)


class Base(DeclarativeBase):
    """A raiz de todos os modelos. Ela guarda o MetaData do projeto."""


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(Text)
    email: Mapped[str | None] = mapped_column(Text, unique=True)
    cidade: Mapped[str | None] = mapped_column(Text)
    criado_em: Mapped[dt.datetime] = mapped_column(
        INSTANTE, server_default=func.now())

    pedidos: Mapped[list[Pedido]] = relationship(
        back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return "Cliente(id=%r, nome=%r)" % (self.id, self.nome)


# Tabela de associação pura: ela só liga duas chaves e não tem atributo
# nenhum. Quando o vínculo TEM atributo — como quantidade e preço em
# `itens_pedido` —, ele merece uma classe, e não uma Table. É a decisão
# que a §6.5 do 05.08 discute.
produto_etiqueta = Table(
    "produto_etiqueta",
    Base.metadata,
    Column("produto_id", Integer, ForeignKey("produtos.id",
                                             ondelete="CASCADE"),
           primary_key=True),
    Column("etiqueta_id", Integer, ForeignKey("etiquetas.id",
                                              ondelete="CASCADE"),
           primary_key=True),
)


class Etiqueta(Base):
    __tablename__ = "etiquetas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(Text, unique=True)

    produtos: Mapped[list[Produto]] = relationship(
        secondary=produto_etiqueta, back_populates="etiquetas")

    def __repr__(self) -> str:
        return "Etiqueta(%r)" % self.nome


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(Text)
    categoria: Mapped[str] = mapped_column(Text)
    preco_centavos: Mapped[int]
    ativo: Mapped[bool] = mapped_column(default=True, server_default="true")

    itens: Mapped[list[ItemPedido]] = relationship(back_populates="produto")
    etiquetas: Mapped[list[Etiqueta]] = relationship(
        secondary=produto_etiqueta, back_populates="produtos")

    __table_args__ = (
        CheckConstraint("preco_centavos >= 0",
                        name="produtos_preco_centavos_check"),
        Index("produtos_categoria_idx", "categoria"),
    )

    @property
    def preco(self) -> Decimal:
        return Decimal(self.preco_centavos) / 100

    def __repr__(self) -> str:
        return "Produto(id=%r, nome=%r, preco=%s)" % (
            self.id, self.nome, self.preco)


class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"))
    data: Mapped[dt.date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(Text)

    cliente: Mapped[Cliente] = relationship(back_populates="pedidos")
    itens: Mapped[list[ItemPedido]] = relationship(
        back_populates="pedido", cascade="all, delete-orphan",
        order_by="ItemPedido.id")

    __table_args__ = (
        CheckConstraint("status IN ('pago', 'pendente', 'cancelado')",
                        name="pedidos_status_check"),
    )

    @property
    def total_centavos(self) -> int:
        return sum(item.subtotal_centavos for item in self.itens)

    def __repr__(self) -> str:
        return "Pedido(id=%r, data=%r, status=%r)" % (
            self.id, self.data, self.status)


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id: Mapped[int] = mapped_column(primary_key=True)
    pedido_id: Mapped[int] = mapped_column(
        ForeignKey("pedidos.id", ondelete="CASCADE"))
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"))
    quantidade: Mapped[int]
    preco_unitario_centavos: Mapped[int]

    pedido: Mapped[Pedido] = relationship(back_populates="itens")
    produto: Mapped[Produto] = relationship(back_populates="itens")

    __table_args__ = (
        CheckConstraint("quantidade > 0", name="itens_pedido_quantidade_check"),
    )

    @property
    def subtotal_centavos(self) -> int:
        return self.quantidade * self.preco_unitario_centavos

    def __repr__(self) -> str:
        return "ItemPedido(id=%r, produto_id=%r, quantidade=%r)" % (
            self.id, self.produto_id, self.quantidade)


class Cotacao(Base):
    """Existe só para o 05.06: uma tabela nova, criada pelo create_all."""

    __tablename__ = "cotacoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    moeda: Mapped[str] = mapped_column(Text)
    valor: Mapped[Decimal] = mapped_column(Numeric(12, 4))
    observacao: Mapped[str | None] = mapped_column(Text)
    registrada_em: Mapped[dt.datetime] = mapped_column(
        INSTANTE, server_default=func.now())
