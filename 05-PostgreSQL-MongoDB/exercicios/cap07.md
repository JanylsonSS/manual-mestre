# Exercícios — Capítulo 05.07: ORM, sessões e ciclo de vida

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap07.md`](gabaritos/cap07.md).

## Aquecimento

### A1 — Quantas consultas? `[Aquecimento · ~12 min]`

```python
# 1
p = sessao.get(Produto, 1); q = sessao.get(Produto, 1)

# 2
p = sessao.get(Produto, 1); sessao.commit(); print(p.nome)

# 3
p = sessao.get(Produto, 1); sessao.commit(); print(p.nome, p.categoria)

# 4
sessao.add(Cliente(id=99, nome="X"))
n = sessao.scalar(select(func.count()).select_from(Cliente))

# 5
sessao.add(Cliente(id=99, nome="X"))
n = sessao.scalar(select(func.count()).select_from(Cliente.__table__))

# 6
for p in sessao.scalars(select(Produto)):
    pass
sessao.commit()
for p in sessao.scalars(select(Produto)):
    print(p.nome)
```

### A2 — Em que estado ele está? `[Aquecimento · ~10 min]`

```python
p = Produto(nome="X", categoria="y", preco_centavos=1)   # 1
sessao.add(p)                                            # 2
sessao.flush()                                           # 3
sessao.commit()                                          # 4
sessao.expunge(p)                                        # 5
sessao.add(p)                                            # 6
sessao.rollback()                                        # 7
sessao.close()                                           # 8
```

### A3 — Ache o erro `[Aquecimento · ~15 min]`

```python
# 1
sessao = Session(engine)   # no topo do módulo

# 2
def buscar_produto(id):
    with Session(engine) as s:
        p = s.get(Produto, id)
        s.commit()
    return p

# 3
def criar_pedido(cliente_id):
    with Session(engine) as s:
        pedido = Pedido(cliente_id=cliente_id, data=date.today(),
                        status="pendente")
        s.add(pedido)
        s.commit()
    return pedido.id

# 4
def transferir(de, para, valor):
    with Session(engine) as s:
        debitar(s, de, valor)
        s.commit()
        creditar(s, para, valor)
        s.commit()

# 5
try:
    s.add(Cliente(id=1, nome="duplicado"))
    s.commit()
except IntegrityError:
    pass
s.add(Cliente(id=200, nome="outro"))
s.commit()

# 6
with Session(engine) as s:
    for produto in s.scalars(select(Produto)):
        threading.Thread(target=processar, args=(s, produto)).start()
```

### A4 — Onde fica o `commit`? `[Aquecimento · ~8 min]`

1. Dentro de `criar_pedido`.
2. Dentro do endpoint que chama `criar_pedido`.
3. Num decorador de transação.
4. Num teste que precisa desfazer tudo ao final.
5. Numa tarefa em lote que processa 100 mil linhas.
6. Numa função chamada por outras duas funções de domínio.

---

## Aplicação

### AP1 — Instrumente e meça `[Aplicação · ~25 min]`

Escreva um contador de SQL reutilizável, com `event.listen`, e meça três operações suas.

**Requisitos:** contar por tipo (`SELECT`, `INSERT`, `UPDATE`, `DELETE`); poder zerar; e um gerenciador de contexto que reporte ao sair.

**A pergunta que fecha:** por que contar é mais útil do que cronometrar, para um teste automatizado?

### AP2 — Conserte a camada que vaza `[Aplicação · ~25 min]`

Dada uma camada de dados cujas funções devolvem objetos do ORM e cujos chamadores dão `DetachedInstanceError`, aplique as **três** correções da §6.7 em três versões diferentes.

**Compare por escrito:** qual delas você levaria para produção, e o que cada uma custa.

### AP3 — `criar_pedido` com transação na borda `[Aplicação · ~30 min]`

Implemente `criar_pedido(sessao, cliente_id, linhas)` que não comita, e um endpoint que agrupa `criar_pedido` e `baixar_estoque`.

**Requisitos:** conversão para dataclass dentro da sessão; erro de domínio quando o produto não existe; e um teste que prove que estoque e pedido são atômicos.

---

## Desafio

### D1 — Unidade de trabalho explícita `[Desafio · ~55 min]`

Uma classe `UnidadeDeTrabalho` que encapsula a sessão e expõe repositórios.

**Requisitos:**

- `with UnidadeDeTrabalho() as uow:` abre e fecha.
- `uow.produtos`, `uow.pedidos` como repositórios.
- `uow.commit()` explícito; sair sem comitar desfaz.
- Testes com uma implementação falsa em memória.

**As três perguntas que valem a nota:**

1. Escreva um teste que passe contra a falsa e **falhe** contra o Postgres. (Ele existe.)
2. O que a falsa não consegue simular? Liste ao menos quatro comportamentos deste capítulo.
3. Qual o valor da falsa, então? Argumente pelos dois lados.

---

## Mini projeto

### MP — O serviço de pedidos `[Mini projeto · ~45 min]`

Sessão por operação, com `sessionmaker`.

**Requisitos:** `criar_pedido`, `cancelar_pedido`, `listar_pedidos_do_cliente`; saída em dataclasses; e o contador do AP1 reportando as consultas de cada operação.

**E a pergunta que fecha:** quantas consultas `listar_pedidos_do_cliente` emitiu, com os itens de cada pedido? Se foi uma por pedido, você acabou de reproduzir o problema do 05.09 — descreva o que observou antes de ler aquele capítulo.
