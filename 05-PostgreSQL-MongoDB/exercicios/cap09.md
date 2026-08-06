# Exercícios — Capítulo 05.09: ORM, consultas e carregamento

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap09.md`](gabaritos/cap09.md).

> Rode `python codigo/cap09/carregamento.py` antes: ele semeia o volume das medições.

## Aquecimento

### A1 — Quantas consultas? `[Aquecimento · ~12 min]`

Com 100 pedidos, cada um com 5 itens:

```python
# 1
for p in sessao.scalars(select(Pedido).limit(100)):
    for i in p.itens: pass

# 2
for p in sessao.scalars(select(Pedido).limit(100)
        .options(selectinload(Pedido.itens))):
    for i in p.itens: pass

# 3
for p in sessao.scalars(select(Pedido).limit(100)
        .options(joinedload(Pedido.itens))).unique():
    for i in p.itens: pass

# 4
for p in sessao.scalars(select(Pedido).limit(100)
        .options(selectinload(Pedido.itens))):
    for i in p.itens: i.produto.nome

# 5
for p in sessao.scalars(select(Pedido).limit(100)
        .options(selectinload(Pedido.itens).selectinload(ItemPedido.produto))):
    for i in p.itens: i.produto.nome

# 6
sessao.scalar(select(func.sum(ItemPedido.quantidade)))
```

### A2 — Qual estratégia? `[Aquecimento · ~10 min]`

1. `item.produto` para mil itens.
2. `pedido.itens` para mil pedidos.
3. `pedido.cliente` para mil pedidos.
4. `pedido.itens` e `pedido.pagamentos`, na mesma consulta.
5. `cliente.pedidos` para **um** cliente.
6. Uma tela que mostra só a data e o status de cem pedidos.

### A3 — Ache o N+1 `[Aquecimento · ~15 min]`

```python
# 1
def total_por_cliente(sessao):
    return {c.nome: sum(p.total_centavos for p in c.pedidos)
            for c in sessao.scalars(select(Cliente))}

# 2
def exportar_csv(sessao, arquivo):
    for p in sessao.scalars(select(Pedido)):
        arquivo.write("%s,%s,%s\n" % (p.id, p.cliente.nome, p.status))

# 3
def validar(sessao, ids):
    return [i for i in ids if sessao.get(Produto, i) is not None]

# 4
def relatorio(sessao):
    pedidos = sessao.scalars(
        select(Pedido).options(selectinload(Pedido.itens))).all()
    return sum(i.produto.preco_centavos for p in pedidos for i in p.itens)

# 5
def nomes(sessao):
    return [p.nome for p in sessao.scalars(select(Produto))]

# 6
def cancelar_antigos(sessao, limite):
    for p in sessao.scalars(select(Pedido).where(Pedido.data < limite)):
        p.status = "cancelado"
    sessao.commit()
```

### A4 — O que este `options()` gera? `[Aquecimento · ~10 min]`

Descreva o SQL de cada um:

1. `joinedload(Pedido.cliente)`
2. `selectinload(Pedido.itens)`
3. `joinedload(Pedido.itens).joinedload(ItemPedido.produto)`
4. `selectinload(Pedido.itens).selectinload(ItemPedido.produto)`
5. `raiseload(Pedido.itens)`
6. `load_only(Pedido.status)`

---

## Aplicação

### AP1 — Meça na sua máquina `[Aplicação · ~30 min]`

Reproduza a tabela da §13 completa.

**As três perguntas:** a razão entre o ingênuo e o `joinedload` foi parecida com 20×? A ordem entre as três estratégias se manteve? E a razão entre objetos e tuplas ficou perto de 7×?

### AP2 — Corrija três funções `[Aplicação · ~30 min]`

Pegue os itens 1, 2 e 4 do A3 e corrija cada um, medindo antes e depois.

**A pergunta que separa:** o item 4 tem `selectinload` e continua com N+1. Explique por que, em uma frase, para alguém que não leu o capítulo.

### AP3 — O relatório em Core `[Aplicação · ~25 min]`

Reescreva a receita por categoria e por mês em Core puro, e compare com a versão ORM em consultas, tempo e linhas de código.

**A pergunta que fecha:** a diferença de tempo justifica a diferença de legibilidade? A resposta depende de um número que você precisa estimar — qual?

---

## Desafio

### D1 — Detector de N+1 `[Desafio · ~55 min]`

Um utilitário de teste que falhe quando uma função emitir mais consultas do que o declarado.

**Requisitos:**

- Um decorador ou gerenciador de contexto: `com_orcamento(5)`.
- Mensagem de falha listando as consultas emitidas, agrupadas por forma.
- Detecção de repetição: a mesma consulta com parâmetros diferentes N vezes.
- Rodar contra o código dos capítulos 05.07 e 05.08.

**As três perguntas que valem a nota:**

1. Como você lida com funções cujo número de consultas depende do volume?
2. Agrupar "a mesma consulta com parâmetros diferentes" exige normalizar o SQL. Como?
3. Rode contra o 05.07 e o 05.08 e reporte o que encontrou. Há N+1 lá, de propósito.

---

## Mini projeto

### MP — Relatório mensal com orçamento `[Mini projeto · ~50 min]`

Receita por mês e categoria, cinco produtos mais vendidos, ticket médio, e clientes sem pedido no período.

**Requisito central:** no máximo **cinco consultas**, declarado como teste com o detector do D1.

**E a pergunta que fecha:** qual das quatro perguntas justifica carregar objetos, e por quê? A resposta tem a ver com o que precisa ser exibido item a item, e não com o que precisa ser somado.
