# Gabarito — Capítulo 05.08: ORM, relacionamentos

Leia depois de tentar. Enunciados em [`../cap08.md`](../cap08.md).

> Execução real: SQLAlchemy 2.0.51 contra PostgreSQL 16.2, pedido 20 com três itens.

## A1 — Quantas consultas?

```
A1.1 get                          1
A1.2 + .cliente                   2
A1.3 + len(.itens)                2
A1.4 + produto de cada item       5
A1.5 + cliente.pedidos            3
A1.6 .itens três vezes            2
```

**O 6 é a resposta que corrige a intuição pessimista.** Ler `.itens` três vezes custa **uma** consulta: depois de carregada, a coleção fica no objeto. O carregamento é preguiçoso, não repetido.

**O 4 é a soma que interessa:** 1 (pedido) + 1 (itens) + 3 (um produto por item) = 5. Com dez itens seriam doze, e é essa progressão que o 05.09 mede.

**E o 5 mostra a navegação em profundidade:** 1 (pedido) + 1 (cliente) + 1 (pedidos do cliente) = 3. O último traz quatro pedidos numa consulta só, porque é uma coleção — e não quatro consultas.

## A2 — Onde fica a chave estrangeira?

| # | Relação | Onde fica |
|---|---|---|
| 1 | Cliente / pedidos | `pedidos.cliente_id` |
| 2 | Pedido / itens | `itens_pedido.pedido_id` |
| 3 | Produto / etiquetas | numa **terceira tabela** |
| 4 | Usuário / perfil (1-1) | em **qualquer um** — escolha |
| 5 | Funcionário / gerente | `funcionarios.gerente_id`, para a própria tabela |
| 6 | Post / comentários encadeados | **duas**: `post_id` e `resposta_a_id` |

**O 4 é decisão, e o critério é a obrigatoriedade.** Se todo usuário tem perfil e nem todo perfil tem usuário, a chave vai em `perfis.usuario_id` com `UNIQUE`. Se for o contrário, inverte. **A restrição `UNIQUE` é o que faz um 1-N virar 1-1** — sem ela, nada impede dois perfis para o mesmo usuário.

**O 5 é auto-relacionamento**, e exige `remote_side` no `relationship` para o SQLAlchemy saber qual lado é qual.

**E o 6 é o caso que produz o erro do A3.6:** duas chaves estrangeiras, e o SQLAlchemy não adivinha qual usar.

## A3 — Ache o erro

**1. `relationship()` sem `back_populates`.** O SQLAlchemy monta dois relacionamentos **independentes** que não se conhecem. `pedido.itens.append(item)` não preenche `item.pedido`, e os dois lados discordam até recarregar. Correção: `back_populates` nos dois.

**2. Falta `ondelete="CASCADE"` na chave estrangeira.** O `delete-orphan` do ORM cobre quem passa pelo Python. Um `DELETE` externo é **recusado**:

```
ForeignKeyViolation - DETAIL:  Key (id)=(1) is still referenced from
table "it_sem".
```

**A recusa é o melhor resultado possível** — melhor do que apagar e deixar órfãos —, e mesmo assim é um defeito: a operação legítima falha. Correção: declarar as duas cascatas.

**3. `item.produto.preco_centavos` para saber quanto o cliente pagou.** Devolve o preço **de hoje**, não o da compra. Correção: `item.preco_unitario_centavos`, que existe exatamente para isso.

**4. `secondary` numa ligação com atributos.** Não há onde pôr `quantidade` nem `preco_unitario_centavos`. Correção: classe de associação (`ItemPedido`).

**5. N+1 em profundidade.** Uma consulta para os pedidos, uma para os itens de cada, uma para o produto de cada primeiro item. Medido para o cliente 1, com quatro pedidos: **12 consultas**. Correção: 05.09.

**6. Duas chaves estrangeiras para a mesma tabela.** `AmbiguousForeignKeysError`: o SQLAlchemy não sabe qual usar em cada `relationship`. Correção: `foreign_keys=[endereco_entrega_id]` em cada um.

## A4 — `secondary` ou classe?

| # | Ligação | Escolha |
|---|---|---|
| 1 | Produto / etiquetas | **`secondary`** |
| 2 | Aluno / disciplina, com nota | **classe** |
| 3 | Post / categorias | **`secondary`** |
| 4 | Usuário / grupo, com data de entrada | **classe** |
| 5 | Filme / gênero | **`secondary`** |
| 6 | Playlist / música, com ordem | **classe** |

**O critério é uma pergunta só: a ligação tem atributo?** Nota, data de entrada e ordem são atributos da **ligação**, não de nenhum dos lados — a nota não pertence a quem cursa nem à disciplina: ela é da matrícula.

**O 6 merece nota porque o atributo é discreto.** "A ordem das faixas" parece detalhe de apresentação e é dado: a mesma música em duas playlists tem posições diferentes. Um `secondary` obrigaria a inventar um lugar para isso.

**E o 1 e o 3 têm um risco de futuro:** etiquetas e categorias frequentemente ganham "quem etiquetou" e "quando" alguns meses depois. Migrar de `secondary` para classe é uma refatoração pequena, e reconhecer o risco na modelagem é o que separa uma escolha de um chute.

## AP1 — Catálogo com etiquetas

As duas primeiras consultas saem de um `JOIN`:

```python
sa.select(Produto).join(Produto.etiquetas).where(Etiqueta.nome == "sem-fio")
```

**A terceira — produtos que têm todas as etiquetas de uma lista — não sai de um `JOIN` simples**, e essa é a pergunta que separa.

Um `JOIN` com `IN (['a','b'])` devolve produtos que têm **alguma** das etiquetas. Para exigir todas, é preciso contar:

```python
sa.select(Produto)
  .join(Produto.etiquetas)
  .where(Etiqueta.nome.in_(exigidas))
  .group_by(Produto.id)
  .having(sa.func.count(sa.distinct(Etiqueta.id)) == len(exigidas))
```

**O `HAVING` é o instrumento**, e o `DISTINCT` dentro dele não é decoração: sem ele, uma etiqueta duplicada na tabela de ligação inflaria a contagem e aprovaria um produto que não deveria passar.

É o padrão chamado *divisão relacional*, e ele aparece sempre que a pergunta é "todos os X que têm todos os Y".

## AP2 — Prove as duas cascatas

As três primeiras, medidas no capítulo:

```
itens criados:                 2
depois de pop() na lista:      1
depois de delete(pedido):      0
DELETE cru, sem ORM nenhum:    sobraram 0 itens
```

**A quarta é a que ensina.** Sem `ON DELETE CASCADE`, o `DELETE` é recusado:

```
ForeignKeyViolation - DETAIL:  Key (id)=(1) is still referenced from
table "it_sem".
```

**Três comportamentos possíveis, e vale saber que a escolha é sua:**

| `ondelete` | O que acontece |
|---|---|
| ausente (`NO ACTION`) | o `DELETE` é **recusado** |
| `CASCADE` | os filhos são apagados |
| `SET NULL` | a chave dos filhos vira nula |

O padrão é a recusa, e ela é o comportamento seguro: nada some por acidente. `CASCADE` é uma decisão de que o filho **não existe sem o pai** — verdadeira para item de pedido, falsa para pedido de cliente (você quer manter o histórico).

## AP3 — Instrumente a tela

Medido para o cliente 1, com quatro pedidos:

```
cliente 1, todos os pedidos: 12
```

**A fórmula**, com P pedidos e I itens por pedido:

```
1  (o cliente)
+ 1  (os pedidos dele)
+ P  (os itens de cada pedido)
+ D  (os produtos DISTINTOS entre todos os itens)
```

O último termo é o detalhe que quase ninguém prevê: **não é P × I**. O mapa de identidade (05.07/§6.1) garante um objeto por chave, então um produto que aparece em três itens é buscado **uma vez**. Com quatro pedidos e dez itens no total, mas apenas seis produtos distintos, deram 1 + 1 + 4 + 6 = **12**.

**A consequência prática é desconfortável:** a contagem depende dos **dados**, não só da estrutura. Um cliente que compra sempre os mesmos produtos gera menos consultas que um que varia — o que torna a medição em desenvolvimento ainda menos representativa.

## D1 — O total sem carregar os itens

**Forma 1 — consulta agregada separada:**

```python
totais = dict(sessao.execute(
    sa.select(ItemPedido.pedido_id,
              sa.func.sum(ItemPedido.quantidade
                          * ItemPedido.preco_unitario_centavos))
    .where(ItemPedido.pedido_id.in_(ids))
    .group_by(ItemPedido.pedido_id)).all())
```

Uma consulta a mais, sempre. Simples de entender e de otimizar.

**Forma 2 — `column_property` correlacionada:**

```python
total_centavos = column_property(
    sa.select(sa.func.coalesce(
        sa.func.sum(itens.c.quantidade * itens.c.preco_unitario_centavos), 0))
    .where(itens.c.pedido_id == pedidos.c.id).scalar_subquery())
```

Nenhuma consulta a mais, e o total vem junto do pedido.

**Forma 3 — coluna denormalizada com gatilho.** Leitura mais rápida possível; a manutenção passa a ser do banco.

**1. Mil pedidos numa tela, ou relatório mensal?**

Na **tela**, a forma 1 ou a 3. A tela pagina — mostra vinte de mil —, e a forma 2 pagaria a subconsulta em cada uma das vinte, o que é aceitável, mas ela também a paga em toda **outra** consulta de pedido do sistema.

No **relatório mensal**, a forma 1 sem hesitar: ele quer agregado, não objetos, e a §6.7 do 05.09 mede isso.

**2. O que a `column_property` custa nas consultas que não precisam do total.**

Ela é acrescentada ao `SELECT` de **toda** carga de `Pedido`. Buscar um pedido para mudar o status passa a executar a subconsulta de soma. Em volume, isso é um `JOIN` implícito em toda consulta da tabela mais movimentada do sistema.

`deferred=True` resolve — o total só é buscado quando alguém o lê —, e aí você recriou o carregamento preguiçoso, com o N+1 junto.

**3. O cenário de divergência da coluna denormalizada.**

Alguém corrige um preço unitário com um `UPDATE` direto no `psql`, durante um incidente. O gatilho está em `INSERT`, `UPDATE` e `DELETE` de `itens_pedido`? Se o gatilho existir e cobrir os três, o total acompanha. **Se ele cobrir só `INSERT` e `DELETE` — que é o esquecimento comum —, o total fica errado para sempre**, e nada acusa.

**A defesa em duas partes:** o gatilho cobre os três eventos, e uma tarefa periódica reconcilia comparando a coluna com a soma real, reportando divergências. **Denormalização sem conferência é uma dívida que só aparece na auditoria.**

## MP — O painel do cliente

**A pergunta que fecha: qual limite, e por quê?**

O critério defensável não é o número medido, e sim a **ordem de grandeza esperada**:

```python
LIMITE = 5   # 1 cliente + 1 pedidos + 1 itens + 1 produtos + 1 folga
assert contador.total <= LIMITE
```

**O raciocínio: a consulta deve ser O(1) em relação ao número de pedidos.** O limite não descreve o que o código faz hoje — ele descreve a **propriedade** que se quer preservar: nenhuma consulta por pedido.

Com uma folga de uma consulta, uma mudança legítima que acrescente um `SELECT` não quebra o teste. Uma regressão para o carregamento preguiçoso quebra, sempre, porque ela leva o número para a casa das dezenas.

**E o valor do teste está no que ele afirma, não no que ele mede.** Um `assert total == 4` documenta uma implementação; um `assert total <= 5` documenta um requisito.
