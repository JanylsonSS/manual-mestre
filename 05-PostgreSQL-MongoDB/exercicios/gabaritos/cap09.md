# Gabarito — Capítulo 05.09: ORM, consultas e carregamento

Leia depois de tentar. Enunciados em [`../cap09.md`](../cap09.md).

> Execução real: SQLAlchemy 2.0.51, PostgreSQL 16.2, base semeada com 2020 pedidos e 10031 itens.

## A1 — Quantas consultas?

Com 100 pedidos e cinco itens cada:

```
A1.1 preguiçoso                        101
A1.2 selectinload                        2
A1.3 joinedload                          1
A1.4 selectinload só nos itens          14
A1.5 selectinload em dois níveis         3
A1.6 sum() agregado                      1
```

**O 4 é o exercício, e o número surpreende: 14, não 501.**

O `selectinload` resolveu os itens (2 consultas). Faltava o produto de cada um dos 500 itens — e deveriam ser 500 consultas. Foram **12**.

**A explicação é o mapa de identidade** (05.07/§6.1): o catálogo tem doze produtos, e cada um é buscado **uma vez**. Do décimo terceiro item em diante, todos os produtos já estão na sessão.

**A conclusão que vale guardar é desconfortável:** a gravidade de um N+1 depende da **cardinalidade** do que está sendo repetido. Com doze produtos, é irrelevante; com um catálogo de cem mil, seria devastador. **E os dois casos têm o mesmo código.**

**O 5 é a correção certa:** 3 consultas, independentemente do catálogo.

**E o 1 é a linha de base:** 101 = 1 + 100.

## A2 — Qual estratégia?

| # | Caso | Escolha |
|---|---|---|
| 1 | `item.produto` para mil itens | **`joinedload`** — muitos-para-um |
| 2 | `pedido.itens` para mil pedidos | **`selectinload`** |
| 3 | `pedido.cliente` para mil pedidos | **`joinedload`** |
| 4 | `itens` e `pagamentos` juntos | **`selectinload` nos dois** |
| 5 | `cliente.pedidos` para **um** cliente | **qualquer uma** |
| 6 | Só data e status de cem pedidos | **nenhuma** — nem carregue |

**O 4 é o que produz desastre com a escolha errada.** Dois `joinedload` de coleção na mesma consulta multiplicam: um pedido com 5 itens e 3 pagamentos vira **15 linhas**, e o SQLAlchemy precisa deduplicar as duas coleções. Com 50 e 20, são mil linhas por pedido.

**O 5 admite qualquer uma porque N é um.** Não há N+1 com um único pai — e otimizar aí é esforço no lugar errado, que é o erro comum número 9 do capítulo.

**E o 6 é a resposta que o capítulo mais quer:** se a tela mostra data e status, `select(Pedido.data, Pedido.status)` não constrói objeto nenhum e não toca em relacionamento.

## A3 — Ache o N+1

**1. `total_por_cliente` — N+1 em dois níveis.** Uma consulta para os clientes, uma para os pedidos de cada, e uma para os itens de cada pedido (porque `total_centavos` percorre `self.itens`). Correção:

```python
select(Cliente).options(selectinload(Cliente.pedidos)
                        .selectinload(Pedido.itens))
```

Melhor ainda: uma agregação, já que a resposta é um número por cliente.

**2. `exportar_csv` — N+1 clássico.** `p.cliente` para cada pedido. Correção: `joinedload(Pedido.cliente)`, que é muitos-para-um.

**3. `validar` com `sessao.get` num laço — N+1 disfarçado de validação.** Correção: uma consulta só.

```python
existentes = set(sessao.scalars(
    select(Produto.id).where(Produto.id.in_(ids))))
return [i for i in ids if i in existentes]
```

**4. `relatorio` com `selectinload` e ainda com N+1 — é o item do AP2.** Ver abaixo.

**5. `nomes` — não tem N+1**, e está no exercício para você não sair vendo N+1 em tudo. Uma consulta, sem relacionamento nenhum. **Ainda dá para melhorar:** `select(Produto.nome)` evita construir doze objetos.

**6. `cancelar_antigos` — não tem N+1 de leitura**, mas emite **um `UPDATE` por pedido**. Com dez mil pedidos antigos, são dez mil comandos. Correção: `sessao.execute(update(Pedido).where(...).values(status="cancelado"))`, que é um comando só — com a ressalva de que ele **não passa pelos objetos em memória**, e a sessão fica com dados vencidos.

## A4 — O que este `options()` gera?

| # | Opção | SQL |
|---|---|---|
| 1 | `joinedload(Pedido.cliente)` | um `SELECT` com `LEFT OUTER JOIN clientes` |
| 2 | `selectinload(Pedido.itens)` | dois: o original, e `... WHERE pedido_id IN (...)` |
| 3 | `joinedload` × `joinedload` | um `SELECT` com **dois** `LEFT OUTER JOIN` |
| 4 | `selectinload` × `selectinload` | **três** consultas |
| 5 | `raiseload(Pedido.itens)` | o `SELECT` normal; ler a coleção levanta erro |
| 6 | `load_only(Pedido.status)` | menos colunas |

O 6, medido:

```
load_only(Pedido.status)   SELECT pedidos.id, pedidos.status FROM pedidos LIMIT ...
```

**A chave primária vem sempre**, mesmo sem ser pedida — o ORM precisa dela para o mapa de identidade.

**O 3 merece cuidado:** dois `joinedload` **encadeados** (pedido → itens → produto) não multiplicam entre si, porque o segundo é muitos-para-um. Dois `joinedload` **irmãos** (itens e pagamentos) multiplicam. A diferença é encadeamento contra paralelismo, e é a origem do erro do A2.4.

## AP1 — Meça na sua máquina

A referência:

| Operação | Consultas | Tempo |
|---|---|---|
| Laço ingênuo, 300 pedidos | 301 | 660,0 ms |
| `joinedload` | 1 | 33,8 ms |
| `subqueryload` | 2 | 38,6 ms |
| `selectinload` | 2 | 60,1 ms |
| Somar em Python | 2 | 31,1 ms |
| Somar no banco | 1 | 5,5 ms |
| 5000 linhas como objetos | 1 | 60,0 ms |
| 5000 linhas como tuplas | 1 | 8,2 ms |

**As contagens têm que bater exatamente.** Se as suas forem diferentes, há diferença de código, não de máquina.

**Os tempos, não.** A razão de ~20× entre ingênuo e `joinedload` deve se manter em ordem de grandeza, e ela **aumenta** se o banco estiver em outra máquina — porque cada uma das 301 consultas paga a latência de rede.

**A ordem entre as três estratégias pode inverter**, e inverter é o resultado interessante. Nesta medição `selectinload` ficou atrás de `joinedload`; com coleções maiores, a repetição de colunas do `joinedload` inverte a conta. **Se a sua ordem for diferente, isso não é erro: é a demonstração de que a escolha depende da forma dos dados.**

## AP2 — Corrija três funções

**O item 4 é a pergunta que separa.** Ele tem `selectinload(Pedido.itens)` e ainda emite N+1:

```python
return sum(i.produto.preco_centavos for p in pedidos for i in p.itens)
```

**A frase para quem não leu o capítulo: o `selectinload` trouxe os itens, e o código lê o produto de cada item — que é outro relacionamento, e esse ninguém declarou.**

A correção encadeia:

```python
.options(selectinload(Pedido.itens).selectinload(ItemPedido.produto))
```

Medido, com 100 pedidos: **14 consultas viram 3**.

**E o item 4 tem um segundo defeito, mais grave que o desempenho.** Ele soma `produto.preco_centavos` — o preço de **hoje** — quando deveria somar `item.preco_unitario_centavos`, o preço da compra. O relatório está errado, e otimizá-lo o deixaria rapidamente errado.

**É a lição de ordem:** conferir a correção antes de otimizar. Um relatório rápido e errado é pior que um lento e certo.

## AP3 — O relatório em Core

O Core evita a construção de objetos, e o número da §6.8 quantifica: **7,3×** para cinco mil linhas.

**A pergunta que fecha: qual número você precisa estimar?**

**Quantas linhas o relatório processa.** A conta é direta:

- Até alguns milhares de linhas, a diferença é de dezenas de milissegundos. Ninguém percebe, e a legibilidade ganha.
- A partir de centenas de milhares, a diferença é de segundos, e o relatório sai da faixa de "espera aceitável".

**E há um segundo número, que quase ninguém considera: a frequência.** Um relatório que roda uma vez por mês pode levar dois minutos. O mesmo cálculo numa tela consultada mil vezes por dia não pode levar dois segundos.

**A regra que sai daí:** `linhas × frequência` decide, e não `linhas` sozinho.

## D1 — Detector de N+1

**1. Funções cujo número depende do volume.**

Um limite fixo fica intermitente conforme os dados de teste crescem. Duas saídas:

**Declarar o limite como função da entrada:**

```python
with orcamento(lambda n: 3):          # constante em n — é o que se quer
    listar_pedidos(cliente_id)
```

**Ou medir a inclinação**, rodando com dois volumes e exigindo que a contagem não cresça:

```python
com_10 = contar(lambda: listar_pedidos(cliente_com_10))
com_100 = contar(lambda: listar_pedidos(cliente_com_100))
assert com_100 <= com_10 + 1
```

**A segunda é mais forte**, e é o que o exercício quer: ela testa a **propriedade** (O(1) em relação ao volume) em vez de um número.

**2. Normalizar o SQL para agrupar.**

Substituir os literais e os parâmetros por um marcador, e colapsar espaços:

```python
def forma(comando: str) -> str:
    sem_parametros = re.sub(r"%\(\w+\)s|\$\d+|'[^']*'|\b\d+\b", "?", comando)
    return " ".join(sem_parametros.split())
```

Duas consultas com a mesma forma e parâmetros diferentes viram a mesma chave. **O detector reporta "esta forma apareceu 300 vezes"**, que é a mensagem que identifica um N+1 sem ambiguidade — muito melhor do que "301 consultas".

**A ressalva honesta:** essa normalização é aproximada. Um `IN (1,2,3)` e um `IN (1,2,3,4)` viram formas diferentes se você não tratar a lista, e um literal dentro de uma string vira `?` indevidamente. Para o propósito — agrupar repetição — a aproximação serve.

**3. Rodando contra o 05.07 e o 05.08.**

Há N+1 de propósito nos dois:

- **05.08, cena 2** (`cena_2_cada_ponto_custa`): 6 consultas para um pedido, sendo 3 delas uma por item. É o N+1 em miniatura, e a cena existe para exibi-lo.
- **05.08, cena 1** (`cena_1_navegar`): navega quatro tabelas com pontos, cada um custando uma consulta.
- **05.07, cena 6**: o `SELECT` de recarga depois do `commit` — um por objeto, e num laço vira N.

**Nenhum deles é defeito.** São demonstrações, e o detector rodando contra código didático encontrando exatamente o que o código quer demonstrar é a confirmação de que ele funciona.

## MP — Relatório mensal com orçamento

As quatro perguntas e o que cada uma exige:

| Pergunta | Como |
|---|---|
| Receita por mês e categoria | `GROUP BY date_trunc, categoria` — 1 consulta, sem objetos |
| Cinco produtos mais vendidos | `GROUP BY produto ORDER BY sum DESC LIMIT 5` — 1 consulta |
| Ticket médio | `AVG` sobre a soma por pedido — 1 consulta |
| Clientes sem pedido no período | `LEFT JOIN ... WHERE id IS NULL` — 1 consulta |

Quatro consultas, e nenhuma delas carrega objetos.

**A pergunta que fecha: qual justifica carregar objetos?**

**A quarta, e apenas se o relatório exibir os clientes item a item.** As três primeiras devolvem números agregados — não há nada para percorrer. A quarta devolve uma **lista de entidades**, e se a saída mostra nome, e-mail e cidade de cada cliente, você precisa dos campos.

**Mesmo assim, `select(Cliente.nome, Cliente.email, Cliente.cidade)` resolve** sem construir objetos — o que reforça o critério do capítulo: **carregou para modificar, use o ORM; carregou para ler, considere o Core.**

**A única justificativa real para o objeto** seria precisar de um método da classe — um `cliente.rotulo_de_endereco()`, por exemplo. E aí a pergunta seguinte é se essa função precisa mesmo ser um método, ou se ela é uma função de formatação que recebe três campos.
