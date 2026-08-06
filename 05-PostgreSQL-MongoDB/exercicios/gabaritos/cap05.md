# Gabarito — Capítulo 05.05: SQLAlchemy, visão geral e Core

Leia depois de tentar. Enunciados em [`../cap05.md`](../cap05.md).

> Execução real: SQLAlchemy 2.0.51, psycopg 3.3.4, PostgreSQL 16.2.

## A1 — Grava ou não grava?

| # | Trecho | Grava? |
|---|---|---|
| 1 | `connect()` sem `commit` | **não** |
| 2 | `begin()` | **sim** |
| 3 | `connect()` + `commit()` | **sim** |
| 4 | `begin()` com exceção | **não** |
| 5 | `connect()` sem `with`, `close()` | **não** |
| 6 | `with psycopg.connect(...)` | **sim** |

O 5, medido — o preço continuou o original:

```
preco 11: 27900
```

**O par 1/6 é o exercício inteiro.** O mesmo desenho de código, contra o mesmo banco, com resultados opostos: o `with` do `psycopg` comita, o `connect()` do SQLAlchemy descarta.

**E o 5 mostra que não é o `with` que decide.** Fechar a conexão sem `commit` descarta do mesmo jeito — o `with` só garante que o fechamento aconteça.

## A2 — Preveja o estado do pool

Com `pool_size=3, max_overflow=2, pool_timeout=5`, medido:

```
status inicial:   Pool size: 3  Connections in pool: 0  Checked out: 0
com 3 abertas:    Pool size: 3  Connections in pool: 0  Checked out: 3
com 5 abertas:    Pool size: 3  Overflow: 2             Checked out: 5
a 6a:             5.0s -> QueuePool limit of size 3 overflow 2 reached
apos devolver:    Pool size: 3  Connections in pool: 3  Checked out: 0
```

| # | Pergunta | Resposta |
|---|---|---|
| 1 | Depois de `create_engine` | **zero** — nada foi aberto |
| 2 | Três simultâneas | 3, o pool cheio |
| 3 | Cinco | 5 — três do pool, duas de estouro |
| 4 | A sexta | espera 5 s e levanta `TimeoutError` |
| 5 | Ao devolver as cinco | **três** ficam guardadas |
| 6 | Quatro instâncias | **20** conexões possíveis |

**A resposta 5 é a que quase todo mundo erra.** As duas conexões de estouro **não** são guardadas: elas foram abertas sob demanda e são fechadas na devolução. O pool volta ao tamanho declarado, e a linha `Connections in pool: 3` confirma.

**E a 6 é a que decide arquitetura:** `(3 + 2) × 4 = 20`. Com `max_connections = 100` no servidor, sobram 80 para tudo o mais — e é exatamente essa conta que o AP2 pede.

## A3 — Ache o erro

**1. `create_engine` dentro da função.** Cada chamada cria um pool novo, abre conexões novas e nenhuma é reaproveitada. O pool antigo só é descartado pelo coletor de lixo, deixando conexões abertas até lá. Correção: engine no módulo.

**2. String pura.** `Not an executable object: 'SELECT 1'`. Correção: `text("SELECT 1")`.

**3. Consumir o resultado duas vezes.** Medido:

```
len 1a: 12   2a chamada: []
```

**Sem erro, sem aviso, lista vazia.** O `r.all()[0]` levanta `IndexError` — e o rastro aponta para uma linha que parece correta. Correção: `linhas = r.all()` e usar a variável.

**4. `pool_size=100, max_overflow=100`.** Duzentas conexões por instância. Com duas instâncias o `max_connections` padrão de 100 já estourou, e o erro que aparece é `FATAL: sorry, too many clients already` — do lado do banco, afetando **todo mundo**, inclusive quem só queria administrar.

**5. URL sem driver.** `postgresql://` deixa o SQLAlchemy escolher, e a escolha pode não ser o que está instalado. Correção: `postgresql+psycopg://`.

**6. f-string dentro de `text()`.** É o 05.04 de novo, com uma camada a mais de disfarce — e o `text()` dá a impressão de que algo está sendo tratado. Correção: `text("... = :nome")` com parâmetro.

## A4 — `text()` ou expressão?

| # | Caso | Escolha |
|---|---|---|
| 1 | Três `JOIN` e uma janela | **`text()`** — mais legível |
| 2 | Filtro opcional | **expressão** — ela se monta em pedaços |
| 3 | `INSERT ... ON CONFLICT` | **expressão** — existe `insert().on_conflict_do_update()` |
| 4 | Contagem com `WHERE` fixo | **qualquer uma** |
| 5 | Rodar em dois bancos | **expressão** — ela reescreve o SQL |
| 6 | `CREATE INDEX CONCURRENTLY` | **`text()`** — e fora de transação (05.02/AP3) |

**O 2 é o critério que mais aparece na prática.** Uma consulta que muda conforme os parâmetros é montada em pedaços, e concatenar pedaços de texto é o defeito do 05.04. A expressão do Core é um objeto: `consulta = consulta.where(...)` acrescenta sem risco.

**E o 1 admite discordância legítima.** Uma função de janela em expressão é possível e costuma ficar menos legível que o SQL. Projetos maduros misturam as duas coisas de propósito.

## AP1 — Meça o pool

A referência, 30 ciclos:

```
abrindo de verdade a cada vez:   110.9 ms (3.70 ms cada)
pegando do pool a cada vez:       24.2 ms (0.81 ms cada)
a MESMA conexão, sem soltar:       7.2 ms (0.24 ms cada)
ganho do pool:                   4.6x
quanto falta para o teto:        3.4x
```

**A proporção que precisa se repetir** é a ordem: abrir ≫ pool > mesma conexão. Os fatores variam.

**A segunda pergunta é a mais importante do exercício.** Num Postgres em outra máquina, o custo de abrir inclui o handshake TCP, a negociação de TLS e a autenticação — dezenas de milissegundos. O custo do pool continua sendo o `ROLLBACK` de devolução, que é **uma** ida e volta. **A razão salta de 4,6× para algo entre 20× e 100×**, e é por isso que o laboratório subestima: soquete Unix na mesma máquina é o melhor caso possível para o lado errado da comparação.

## AP2 — Dimensione o pool

Uma resposta defensável, com a conta explícita:

```
4 instâncias × 8 processos = 32 processos
32 × (pool_size + max_overflow) ≤ 100 − reserva

reserva:  5 (migrações)  +  5 (administração)  +  3 (monitoramento) = 13
32 × (p + o) ≤ 87   →   p + o ≤ 2
```

**A conta não fecha, e reconhecer isso é metade da resposta.** Com 32 processos e 100 conexões, cada processo pode ter **duas**. As saídas reais:

1. **`pool_size=2, max_overflow=0`** — cabe, e derruba a vazão se a requisição gastar 20 ms de banco.
2. **Aumentar `max_connections`** para 300 — funciona até certo ponto; cada conexão é um processo com alguns MB.
3. **Pôr um PgBouncer na frente** — a resposta usada em produção. Ele multiplexa milhares de conexões de aplicação sobre dezenas de conexões reais.

**`pool_timeout`: 5 segundos.** A requisição dura 30 ms; esperar 30 s por uma conexão é servir um erro tarde demais.

**Os dois erros têm sintomas opostos, e é isso que o exercício quer.** Errar **para mais** derruba o banco inteiro com `too many clients` — inclusive as conexões de administração, o que impede diagnosticar. Errar **para menos** deixa o banco ocioso e a aplicação em fila: o painel mostra CPU baixa no banco e latência alta na API, e a conclusão apressada é que o banco está lento.

## AP3 — Do SQL para o Core

A receita por categoria, e o SQL que sai:

```sql
SELECT produtos.categoria,
       sum(itens_pedido.quantidade * itens_pedido.preco_unitario_centavos)
       AS receita
FROM itens_pedido JOIN produtos ON itens_pedido.produto_id = produtos.id
WHERE produtos.ativo IS true
GROUP BY produtos.categoria ORDER BY receita DESC
```

```
audio:         R$ 2914.70
video:         R$ 2753.80
perifericos:   R$ 2503.30
acessorios:    R$ 1422.20
```

Clientes sem pedido usa `outerjoin` com `is_(None)`; o produto mais vendido por mês precisa de função de janela, com `sa.func.row_number().over(partition_by=..., order_by=...)`.

**A pergunta que separa: qual deixar em `text()`?**

A terceira. A expressão com `over()` e uma subconsulta filtrando `posicao = 1` fica com quatro níveis de aninhamento em Python para produzir um SQL de doze linhas que qualquer pessoa lê. **O critério defensável é a razão entre o esforço de escrever e o de ler** — e ele muda quando a consulta precisa ser montada dinamicamente, porque aí o texto volta a ser o problema.

## D1 — O pool sob pressão

**1. A espera deixa de ser zero exatamente em `pool_size + max_overflow + 1`.** A thread de número `p + o + 1` é a primeira que encontra tudo emprestado. Com `pool_size=3, max_overflow=2`, é a sexta — e o `TimeoutError` de 5,0 s medido no A2 é o caso extremo dessa espera.

**2. A consulta lenta contamina as rápidas, e este é o achado do exercício.** Uma thread com `pg_sleep(2)` segura a conexão por dois segundos. As threads rápidas que chegarem depois do esgotamento esperam **até que ela devolva**. O p95 das rápidas passa a ser função da lenta, e não do próprio trabalho.

**A conclusão que vale escrever:** num serviço com pool esgotado, a latência de todos é ditada pela consulta mais lenta. É o argumento contra deixar relatórios pesados no mesmo pool das requisições interativas — e a solução usual são **dois pools**, ou uma réplica de leitura.

**3. Dobrar `pool_size` e dobrar `max_overflow` não são equivalentes.** `pool_size` aumenta as conexões **guardadas**: elas ficam prontas, e o ganho aparece imediatamente. `max_overflow` aumenta o teto, mas cada conexão de estouro é **aberta na hora** (3,70 ms medidos) e **fechada na devolução** — ela ajuda a absorver pico e não ajuda em carga sustentada, porque paga abertura toda vez.

## MP — A camada de acesso em Core

O esqueleto:

```python
_engine = sa.create_engine(os.environ["DATABASE_URL"],
                           pool_size=10, max_overflow=5,
                           pool_timeout=10, pool_pre_ping=True)

def criar_pedido(conexao: Connection, cliente_id: int,
                 linhas: list[tuple[int, int]]) -> int:
    resultado = conexao.execute(
        sa.insert(pedidos).values(cliente_id=cliente_id,
                                  data=date.today(), status="pendente")
        .returning(pedidos.c.id))
    return resultado.scalar_one()

def fechar() -> None:
    _engine.dispose()
```

E o teste de atomicidade:

```python
def test_pedido_e_estoque_sao_atomicos():
    antes = contar_pedidos()
    with pytest.raises(EstoqueInsuficiente):
        with _engine.begin() as conexao:
            criar_pedido(conexao, 1, [(1, 1)])
            baixar_estoque(conexao, [(1, 999999)])
    assert contar_pedidos() == antes
```

**A pergunta que fecha: por que `Connection` e não `Engine`?**

Porque a transação é de quem sabe qual é o trabalho. Se `criar_pedido` recebesse a engine, ela abriria a própria conexão e a própria transação — e `baixar_estoque` abriria outra. **As duas gravariam de forma independente**, e o teste acima seria impossível de escrever: o pedido ficaria criado com o estoque intacto.

**O que ficaria impossível, em uma frase:** agrupar duas operações numa transação só. E como toda operação de negócio interessante é composta, essa impossibilidade aparece na primeira semana.

É a mesma conclusão do 05.04/D1, e o 05.07 vai lhe dar um nome próprio — a sessão como unidade de trabalho.
