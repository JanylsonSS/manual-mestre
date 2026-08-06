# Exercícios — Capítulo 05.08: ORM, relacionamentos

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap08.md`](gabaritos/cap08.md).

## Aquecimento

### A1 — Quantas consultas? `[Aquecimento · ~12 min]`

Sessão nova em cada item, com o pedido 20 (três itens):

```python
# 1
p = sessao.get(Pedido, 20)

# 2
p = sessao.get(Pedido, 20); p.cliente

# 3
p = sessao.get(Pedido, 20); len(p.itens)

# 4
p = sessao.get(Pedido, 20)
for i in p.itens: i.produto.nome

# 5
p = sessao.get(Pedido, 20); p.cliente.pedidos

# 6
p = sessao.get(Pedido, 20); p.itens; p.itens; p.itens
```

### A2 — Onde fica a chave estrangeira? `[Aquecimento · ~10 min]`

1. Cliente e pedidos.
2. Pedido e itens.
3. Produto e etiquetas.
4. Usuário e perfil (um para um).
5. Funcionário e gerente (o gerente também é funcionário).
6. Post e comentários, onde um comentário responde a outro comentário.

### A3 — Ache o erro `[Aquecimento · ~15 min]`

```python
# 1
class Pedido(Base):
    itens: Mapped[list[ItemPedido]] = relationship()
class ItemPedido(Base):
    pedido: Mapped[Pedido] = relationship()

# 2
class Pedido(Base):
    itens: Mapped[list[ItemPedido]] = relationship(
        back_populates="pedido", cascade="all, delete-orphan")
class ItemPedido(Base):
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"))

# 3
for item in pedido.itens:
    print(item.produto.preco_centavos)   # para saber quanto o cliente pagou

# 4
class Pedido(Base):
    produtos: Mapped[list[Produto]] = relationship(secondary=itens_pedido)
    # (itens_pedido tem quantidade e preco_unitario_centavos)

# 5
for pedido in cliente.pedidos:
    print(pedido.itens[0].produto.nome)

# 6
class Pedido(Base):
    endereco_entrega_id: Mapped[int] = mapped_column(ForeignKey("enderecos.id"))
    endereco_cobranca_id: Mapped[int] = mapped_column(ForeignKey("enderecos.id"))
    entrega: Mapped[Endereco] = relationship()
    cobranca: Mapped[Endereco] = relationship()
```

### A4 — `secondary` ou classe? `[Aquecimento · ~8 min]`

1. Produto e etiquetas.
2. Aluno e disciplina, com nota e frequência.
3. Post e categorias.
4. Usuário e grupo, com data de entrada.
5. Filme e gênero.
6. Playlist e música, com a ordem das faixas.

---

## Aplicação

### AP1 — Catálogo com etiquetas `[Aplicação · ~30 min]`

Modele `Produto` ↔ `Etiqueta` com `secondary`, carregue dados e escreva três consultas: produtos de uma etiqueta, etiquetas de um produto, e produtos que têm **todas** as etiquetas de uma lista.

**A pergunta que separa:** a terceira consulta não sai de um `JOIN` simples. Como você a escreve, e por quê?

### AP2 — Prove as duas cascatas `[Aplicação · ~25 min]`

Monte um cenário e prove, com contagens antes e depois:

1. `pedido.itens.pop()` apaga a linha (ORM).
2. `sessao.delete(pedido)` apaga os itens (ORM).
3. `DELETE FROM pedidos` no `psql` apaga os itens (banco).
4. O que acontece em (3) **sem** `ON DELETE CASCADE`.

### AP3 — Instrumente a tela `[Aplicação · ~25 min]`

Implemente a tela da §9 e conte as consultas com quatro pedidos, depois com vinte.

**As duas perguntas:** a contagem cresceu como você previu? E qual é a fórmula, em função do número de pedidos e de itens?

---

## Desafio

### D1 — O total sem carregar os itens `[Desafio · ~50 min]`

Três formas de obter o total de cada pedido sem carregar as coleções.

**Requisitos:**

- Uma consulta agregada separada, devolvendo `pedido_id → total`.
- Uma `column_property` com subconsulta correlacionada.
- Uma coluna denormalizada, com o gatilho que a mantém.
- Medição das três, em consultas e em tempo.

**As três perguntas que valem a nota:**

1. Qual você usaria numa tela que lista mil pedidos? E num relatório mensal?
2. O que a `column_property` custa nas consultas que **não** precisam do total?
3. A coluna denormalizada pode divergir. Descreva um cenário concreto e a defesa.

---

## Mini projeto

### MP — O painel do cliente `[Mini projeto · ~45 min]`

Pedidos, itens, produtos e totais numa tela.

**Requisitos:** a versão ingênua medida; a versão declarada medida; e um teste que **afirme** um limite de consultas.

**E a pergunta que fecha:** qual número você escolheu como limite, e por quê? "O que mede hoje" é resposta ruim — qualquer mudança legítima o quebra. Descreva o critério que você usou.
