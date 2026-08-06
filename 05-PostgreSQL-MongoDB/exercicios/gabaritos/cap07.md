# Gabarito — Capítulo 05.07: ORM, sessões e ciclo de vida

Leia depois de tentar. Enunciados em [`../cap07.md`](../cap07.md).

> Execução real: SQLAlchemy 2.0.51 contra PostgreSQL 16.2.

## A1 — Quantas consultas?

Medido:

```
A1.1 get + get                       1  ['SELECT']
A1.2 get, commit, ler 1 atributo     2  ['SELECT', 'SELECT']
A1.3 get, commit, ler 2 atributos    2  ['SELECT', 'SELECT']
A1.6 laço, commit, laço de novo      2  ['SELECT', 'SELECT']
```

| # | Trecho | Consultas |
|---|---|---|
| 1 | dois `get` do mesmo id | **1** |
| 2 | `get`, `commit`, um atributo | **2** |
| 3 | `get`, `commit`, dois atributos | **2** |
| 4 | pendente + `COUNT` na classe | **2** (`INSERT` + `SELECT`) |
| 5 | pendente + `COUNT` na `__table__` | **1** |
| 6 | laço, `commit`, laço | **2** |

**O par 2/3 corrige um exagero comum.** A recarga depois do vencimento traz **a linha inteira**, não uma coluna: ler dois atributos custa o mesmo que ler um. O custo é por **objeto**, não por atributo — e é isso que torna o laço da §13 caro, e não a quantidade de campos.

**O 6 mostra que o vencimento não multiplica consultas quando você reconsulta.** O segundo `select` traz as linhas e repopula os objetos vencidos no caminho.

**E o par 4/5 é a pegadinha do capítulo:** a mesma pergunta, respostas 9 e 8.

## A2 — Em que estado ele está?

```
1 criado     : transient
2 add        : pending
3 flush      : persistent
4 commit     : persistent
5 expunge    : detached
6 add again  : persistent
7 rollback   : persistent
8 close      : detached
```

**Os passos 6 e 7 contrariam o esperado, e pelo mesmo motivo.**

No 6, `add()` de um objeto destacado devolve `persistent` e não `pending` — porque ele **já tem chave de identidade**: a sessão sabe que a linha existe e o readota, em vez de tratá-lo como novo.

No 7, o `rollback` deixa `persistent`, e não `transient`. **Compare com a cena 4 do capítulo**, onde o mesmo `rollback` produziu `transient`:

```
depois do rollback, o id:   21
e o estado:                 transient
```

A diferença é que lá o objeto tinha sido apenas **inserido e nunca comitado** — desfazer a transação apagou a linha, e o objeto voltou a não existir. Aqui a linha foi comitada antes; o `rollback` só desfez o que veio depois.

**A regra que sai disso:** `rollback` devolve o objeto ao estado que ele tinha no último `commit` — que pode ser "nunca existiu" ou "existe e está vencido".

## A3 — Ache o erro

**1. Sessão global no topo do módulo.** O mapa de identidade nunca esvazia (memória crescendo), o trabalho de contextos diferentes se mistura, e ela não é segura entre threads. Correção: `sessionmaker` e uma sessão por unidade de trabalho.

**2. Devolver objeto depois de `commit` e `close`.** É a §6.7: o `commit` venceu o objeto e a sessão fechou. `DetachedInstanceError` no primeiro acesso. Correção: converter para dataclass dentro do `with`, ou `expire_on_commit=False`.

**3. `return pedido.id` depois do `with`.** O mesmo defeito do 2, com um agravante: ele **funciona às vezes**. Se o objeto já tiver sido carregado e a sessão fechada sem `commit`, o `id` está lá. Com `commit`, quebra. Correção: `identificador = pedido.id` **dentro** do bloco.

**4. Dois `commit` numa transferência.** O primeiro grava o débito. Se `creditar` falhar, o dinheiro sumiu — o `rollback` do segundo não desfaz o primeiro. Correção: um `commit` só, no fim, ou `with sessao.begin():`.

**5. `except IntegrityError: pass` sem `rollback`.** Medido:

```
1o erro:     IntegrityError
2o insert:   PendingRollbackError - This Session's transaction has been
             rolled back due to a previous exception during flush
```

**A sessão fica inutilizável**, e o segundo `INSERT` — que não tinha nada de errado — falha com um erro que fala de "exceção anterior". Correção: `sessao.rollback()` no `except`.

**6. Threads compartilhando a sessão.** O mapa de identidade e o rastro de mudanças são estruturas mutáveis sem trava. O resultado é a classe de defeito do 04.21 — aquela que não reproduz em teste. Correção: uma sessão por thread, com `scoped_session`.

## A4 — Onde fica o `commit`?

| # | Lugar | Veredito |
|---|---|---|
| 1 | Dentro de `criar_pedido` | **não** — impede agrupar |
| 2 | No endpoint | **sim** — é a borda |
| 3 | Num decorador | **sim** — é a borda, declarada |
| 4 | No teste que desfaz | **não** — `rollback` no final |
| 5 | Lote de 100 mil | **sim, por lote** |
| 6 | Função chamada por outras duas | **não, nunca** |

**O 5 é o único que pede nuance.** Um `commit` só, no fim de 100 mil linhas, mantém uma transação aberta por minutos — o que segura o `autovacuum` (05.01/§6.3) e cresce o rastro de mudanças na memória. Um `commit` por linha paga um `fsync` por linha (05.04/AP3). **A resposta é lotes de alguns milhares**, e o número certo se mede.

**E o 6 é a regra em forma pura:** uma função que pode ser chamada de dentro de outra transação não pode decidir encerrá-la. Ela não sabe se é a borda.

## AP1 — Instrumente e meça

```python
class ContadorSQL:
    def __init__(self, engine: sa.Engine) -> None:
        self.por_tipo: Counter[str] = Counter()
        event.listen(engine, "before_cursor_execute", self._anotar)

    def _anotar(self, conn, cursor, comando, param, ctx, muitos) -> None:
        self.por_tipo[comando.split(None, 1)[0].upper()] += 1

    @property
    def total(self) -> int:
        return sum(self.por_tipo.values())

    def zerar(self) -> None:
        self.por_tipo.clear()

    @contextmanager
    def medindo(self, rotulo: str) -> Iterator[None]:
        self.zerar()
        yield
        print("%s: %d (%s)" % (rotulo, self.total, dict(self.por_tipo)))
```

**A pergunta que fecha: por que contar é melhor que cronometrar num teste?**

Porque a contagem é **determinística** e o tempo não. Os 660 ms do N+1 do 05.09 viram 200 ms numa máquina rápida e 2 s numa carregada; as 301 consultas são 301 em qualquer lugar.

**Um teste de tempo fica intermitente** — falha na integração contínua sobrecarregada, passa na máquina do desenvolvedor — e um teste intermitente é desligado em duas semanas. Um teste de contagem falha exatamente quando alguém acrescentou uma consulta, que é o evento que se quer detectar.

## AP2 — Conserte a camada que vaza

**Versão 1 — `expire_on_commit=False`:**

```python
Sessao = sessionmaker(engine, expire_on_commit=False)
```

Custa uma linha. **O preço é trabalhar com dados de um instante atrás** — o objeto sai da sessão com os valores do `commit`, e se outra transação alterou a linha, você não fica sabendo.

**Versão 2 — converter dentro da sessão:**

```python
def buscar_produto(id_produto: int) -> ProdutoSaida | None:
    with Sessao() as sessao:
        produto = sessao.get(Produto, id_produto)
        if produto is None:
            return None
        return ProdutoSaida(id=produto.id, nome=produto.nome,
                            preco_centavos=produto.preco_centavos)
```

Custa uma classe e uma conversão por função. **Ganha uma fronteira explícita**: nada do ORM sai da camada de dados, e o tipo de retorno documenta o contrato.

**Versão 3 — manter a sessão aberta:**

```python
def buscar_produto(sessao: Session, id_produto: int) -> Produto | None:
    return sessao.get(Produto, id_produto)
```

Custa passar a sessão adiante. **Ganha o poder todo do ORM** para quem chama — inclusive carregar relacionamentos sob demanda.

**Qual levar para produção?** A **2**, com a **3** por baixo. As funções recebem a sessão (3), e a conversão para dataclass acontece na borda do serviço, uma vez. A 1 é conveniente e resolve o sintoma sem resolver o vazamento: objetos do ORM continuam circulando pelo sistema, carregando uma referência à sessão de origem, e o próximo problema é um objeto guardado em cache entre requisições.

## AP3 — `criar_pedido` com transação na borda

```python
def criar_pedido(sessao: Session, cliente_id: int,
                 linhas: list[tuple[int, int]]) -> Pedido:
    pedido = Pedido(cliente_id=cliente_id, data=dt.date.today(),
                    status="pendente")
    for produto_id, quantidade in linhas:
        produto = sessao.get(Produto, produto_id)
        if produto is None:
            raise ProdutoInexistente(produto_id)
        pedido.itens.append(ItemPedido(
            produto_id=produto_id, quantidade=quantidade,
            preco_unitario_centavos=produto.preco_centavos))
    sessao.add(pedido)
    return pedido
```

O teste de atomicidade:

```python
def test_pedido_e_estoque_sao_atomicos(engine):
    antes = contar_pedidos(engine)
    with pytest.raises(EstoqueInsuficiente):
        with Session(engine) as sessao, sessao.begin():
            criar_pedido(sessao, 1, [(1, 1)])
            baixar_estoque(sessao, [(1, 10**9)])
    assert contar_pedidos(engine) == antes
```

**A função não comita, e é isso que torna o teste possível.** Se `criar_pedido` comitasse, o pedido ficaria gravado com o estoque intacto — e o teste falharia por um motivo que não é o que ele quer verificar.

**Detalhe que merece atenção:** `preco_unitario_centavos` é copiado do produto **agora**, e não é redundância — é o preço no momento da compra (05.08/§6.6).

## D1 — Unidade de trabalho explícita

**1. O teste que passa contra a falsa e falha contra o Postgres.**

```python
def test_pedido_com_status_invalido(uow):
    with uow:
        uow.pedidos.adicionar(Pedido(cliente_id=1, data=hoje,
                                     status="INVENTADO"))
        uow.commit()
```

Contra uma falsa que guarda em listas, isso **passa**: nada valida o status. Contra o Postgres, o `CHECK` da tabela levanta `CheckViolation` — medido no capítulo:

```
status fora do CHECK:   CheckViolation
```

Qualquer teste que dependa de restrição do banco serve. É o exercício.

**2. O que a falsa não simula.** Ao menos seis comportamentos deste capítulo:

- **Autoflush** — a falsa enxerga o pendente sempre, sem a distinção classe/`__table__`.
- **Vencimento no `commit`** — a falsa não tem o conceito.
- **Ordenação de `INSERT`** por dependência de chave estrangeira.
- **Restrições do banco** — `CHECK`, `UNIQUE`, `FOREIGN KEY`.
- **Geração de `id`** no `flush`.
- **`PendingRollbackError`** depois de uma exceção não tratada.

**3. Qual o valor da falsa, então?**

**A favor:** ela torna os testes de **lógica de domínio** rápidos e independentes de infraestrutura. Um teste de "carrinho com três itens calcula o total certo" não precisa de banco, e rodá-lo em milissegundos permite tê-lo aos milhares.

**Contra:** ela cria confiança falsa exatamente onde o sistema quebra. A lista do item 2 é grande, e todos os itens dela são coisas que **só** falham em produção.

**A síntese que a resposta madura traz:** a falsa serve para testar **o seu código**; ela não serve para testar **a sua integração com o banco**. As duas coisas precisam de teste, e a segunda exige um Postgres de verdade — que é o que o `laboratorio.py` deste módulo torna barato.

## MP — O serviço de pedidos

**A pergunta que fecha, respondida antes do 05.09.**

`listar_pedidos_do_cliente` com os itens emite **1 + N** consultas: uma para os pedidos, uma para os itens de cada um. Com quatro pedidos, cinco consultas; com duzentos, duzentas e uma.

**O que se observa antes de conhecer a solução** é o mais instrutivo: o tempo da operação cresce **linearmente com o número de pedidos**, enquanto o tempo de cada consulta individual permanece na casa do milissegundo. Nenhuma consulta é lenta. A operação é lenta.

É esse descompasso — nenhuma parte lenta, o todo lento — que caracteriza o N+1, e é por isso que ele resiste a quem procura a "consulta pesada" no monitoramento.
