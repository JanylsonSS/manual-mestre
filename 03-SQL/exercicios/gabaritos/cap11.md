# Gabarito — Capítulo 03.11: `INSERT`, `UPDATE`, `DELETE`

Leia depois de tentar. Enunciados em [`../cap11.md`](../cap11.md).

> Todos os números abaixo vieram de execução real contra uma cópia limpa de `aurora.db`.
> Cada bloco parte do rascunho recém-criado — se você encadeou os exercícios sem recriá-lo,
> seus números vão divergir a partir do primeiro `UPDATE`, e isso não é erro seu.

## A1 — Preveja a saída

| # | Linhas afetadas | O detalhe |
|---|---|---|
| 1 | `1` | `INSERT` de uma linha afeta uma linha. Sem surpresa — e é por isso que `INSERT` é o comando que menos assusta. |
| 2 | `2` | **Mesmo que os dois já estejam com `ativo = 1`.** |
| 3 | `2` | há exatamente 2 pedidos pendentes no banco |
| 4 | `0` | nenhum produto passa de R$ 10 000,00; `DELETE` que não acha nada não é erro |
| 5 | `8` | **sem `WHERE`: a tabela inteira.** Oito clientes viraram de campinas |
| 6 | `1` | o pedido 20 (o cancelado) tem um item |

**O item 2 é o que ensina.** `UPDATE produtos SET ativo = 1 WHERE categoria = 'perifericos'`
devolve `Linhas afetadas: 2` mesmo com os dois produtos já ativos. O número conta as linhas que
o `WHERE` **encontrou**, não as que mudaram de valor. Consequência prática: linhas afetadas
serve para conferir se o seu `WHERE` pegou o conjunto certo — não serve para saber se algo de
fato mudou. São perguntas diferentes.

**O item 5 é o capítulo inteiro em uma linha.** Nenhum erro, nenhum aviso, oito linhas
sobrescritas. Se você previu 1 ou 0, releia o comando: não há `WHERE`.

## A2 — Ache o perigo

| # | Classificação | Por quê |
|---|---|---|
| 1 | **seguro** | `SELECT` não altera nada |
| 2 | **seguro** | tem `WHERE` por chave primária; o id 999 nem existe → 0 linhas |
| 3 | **catastrófico** | sem `WHERE`: dobra o preço de **todo** o catálogo |
| 4 | **catastrófico** | esvazia `itens_pedido`; o histórico de vendas do negócio inteiro |
| 5 | **perigoso** | tem `WHERE` e é reversível só se você souber o e-mail antigo — anote antes |
| 6 | **catastrófico** | atribui **todos** os pedidos ao cliente 1 |

**O item 6 merece atenção, porque a chave estrangeira não salva.** `UPDATE pedidos SET
cliente_id = 1` afeta as 20 linhas e **não viola nada**: o cliente 1 existe, então cada
`cliente_id` continua apontando para um cliente válido. A integridade referencial está
perfeita e os dados estão completamente errados. **A restrição garante consistência
estrutural, não correção de negócio** — é a distinção que separa quem confia demais no banco
de quem confia na medida.

**O item 5 é "perigoso" e não "seguro" por um motivo específico:** a reversibilidade depende de
informação que você tem *antes* e perde *depois*. `SELECT email FROM clientes WHERE id = 3`
custa um segundo e transforma o comando em reversível.

## A3 — O ensaio

| # | `SELECT` de ensaio | Linhas | O que aprender |
|---|---|---|---|
| 1 | `WHERE categoria = 'mobiliario'` | **0** | ver abaixo |
| 2 | `WHERE cliente_id = 5` | 2 | |
| 3 | `WHERE id = 3` | 1 | chave primária: sempre 1 ou 0 |
| 4 | `WHERE preco_centavos > 50000` | 1 | só o Monitor 24 polegadas |
| 5 | `WHERE cidade IS NULL` | 1 | `IS NULL`, nunca `= NULL` (03.03) |

**O item 1 era uma armadilha, e ela é o ponto do exercício.** Não existe categoria
`mobiliario` na Aurora — as categorias são `acessorios`, `audio`, `perifericos` e `video`. O
`UPDATE` roda, não dá erro, e devolve `Linhas afetadas: 0`.

Sem o ensaio, você reportaria "desativei os produtos de mobiliário" e ninguém saberia que nada
aconteceu — até alguém perguntar por que os produtos continuam no site. **O ensaio não pega só
o `WHERE` largo demais; pega o `WHERE` que não acha nada**, que é o erro silencioso na direção
oposta. Zero linhas afetadas é um resultado que exige explicação, não um resultado tranquilo.

O reflexo certo diante de `Linhas afetadas: 0`: rodar `SELECT DISTINCT categoria FROM produtos`
e descobrir que o nome estava errado.

## A4 — Apagar ou desativar?

| # | Decisão | A pergunta que você faz |
|---|---|---|
| 1 | **desativar** | "Ele já foi vendido alguma vez?" (Se sim, apagar destrói o histórico — e a FK recusa) |
| 2 | **caso especial** | ver abaixo |
| 3 | **apagar** | "Esse cadastro duplicado chegou a ser vendido?" Se nunca foi usado, não há histórico a preservar |
| 4 | **desativar/anular** | "Esse pedido entrou em algum relatório já fechado?" Pedido de teste em base real vira `status = 'cancelado'` |
| 5 | **apagar** | "Existe retenção legal ou de auditoria para esses logs?" Logs têm prazo e são apagados por rotina |
| 6 | **desativar** | "As compras passadas desse fornecedor precisam continuar rastreáveis?" Quase sempre sim |

**O item 2 é o único em que "apagar" quer mesmo dizer apagar** — e é onde a regra do capítulo
encontra seu limite. Um pedido de exclusão sob a LGPD é uma obrigação legal, e um `ativo = 0`
não a cumpre: o dado continua lá. Mas apagar a linha do cliente esbarra na chave estrangeira,
porque os pedidos dele precisam continuar existindo para a contabilidade.

A solução usual não é nenhuma das duas: é **anonimizar** — substituir nome, e-mail e demais
dados pessoais por marcadores, preservando a linha e as relações. `UPDATE clientes SET nome =
'Cliente removido', email = NULL, cidade = NULL WHERE id = ...`. O histórico financeiro
sobrevive; o dado pessoal, não.

Se você respondeu "apagar" no item 2, você acertou a leitura do pedido. Se respondeu
"desativar", acertou a restrição técnica. A resposta completa reconhece que **as duas estão
certas e incompatíveis**, e que por isso existe uma terceira — que é como a maioria dos
problemas difíceis desta profissão se resolve.

## AP1 — O cadastro

A ordem correta é **pai antes de filho**: cliente → pedido → itens. E produtos antes dos itens
que os referenciam.

```sql
INSERT INTO clientes (nome, email, cidade, data_cadastro)
VALUES ('Otavio Ramos', 'otavio@exemplo.com', 'jundiai', '2026-08-04');

INSERT INTO produtos (nome, categoria, preco_centavos) VALUES
    ('Webcam HD',          'video',       24900),
    ('Suporte de Monitor', 'acessorios',  18900);

INSERT INTO pedidos (cliente_id, data, status)
VALUES (9, '2026-08-04', 'pendente');

INSERT INTO itens_pedido
    (pedido_id, produto_id, quantidade, preco_unitario_centavos) VALUES
    (21, 13, 1, 24900),
    (21, 14, 2, 18900),
    (21,  5, 1, 89900);
```

**A parte que ensina — inserir o item primeiro:**

```
Erro de SQL: FOREIGN KEY constraint failed
```

A `FOREIGN KEY (pedido_id) REFERENCES pedidos(id)` exige que o pedido **já exista** no momento
do `INSERT`. Não é burocracia: é a garantia de que nunca existirá um item órfão, apontando
para um pedido que não existe. A ordem de inserção não é convenção — é imposta pela estrutura
que você desenhou no 03.02.

**Sobre os ids.** Se você escreveu `21` no `pedido_id` sem verificar, teve sorte. O jeito
correto é ler o id gerado: `SELECT MAX(id) FROM pedidos` logo após o `INSERT`, ou usar
`RETURNING id` nos bancos que suportam. Em código de aplicação, o driver devolve o id gerado
(`cursor.lastrowid` no Python) — nunca se chuta um id.

**Sobre `preco_unitario_centavos`.** Ele repete o preço do produto de propósito. Se o preço do
produto mudar amanhã, o pedido de hoje precisa continuar valendo o que valeu hoje — a coluna
guarda o preço **no momento da venda**. É a decisão de modelagem do 03.02 aparecendo na prática.

## AP2 — O reajuste

**Reajuste 1 — +8% em periféricos ativos.**

```
ensaio:            2 linhas (Mouse Sem Fio, Teclado Mecanico K2)
total antes:  318020 centavos
comando:           2 linhas afetadas
total depois: 321371 centavos
diferença:      3351 centavos
```

**A conferência que fecha:** a soma dos preços dos dois periféricos antes era 41 890; 8% disso
é 3 351,2. A diferença observada foi 3 351 — o `.2` perdido é o `CAST(... AS INTEGER)`
truncando. Bate. **Se a diferença fosse muito maior, o `WHERE` teria pegado produtos demais**,
e essa conta de dois segundos revelaria isso antes de qualquer relatório.

**Reajuste 2 — −15% nos que nunca venderam.** `NOT EXISTS` acha **1** produto (o Mousepad
Grande). Com `NOT IN` você correria o risco do 03.09; aqui `itens_pedido.produto_id` é
`NOT NULL`, então funcionaria — **e é exatamente por isso que o hábito é perigoso**: funciona
até o dia em que a coluna aceita nulo.

**Reajuste 3 — arredondar para a dezena de centavos.**

```sql
UPDATE produtos
SET preco_centavos = CAST(ROUND(preco_centavos / 10.0) * 10 AS INTEGER);
```

Este é o único `UPDATE` legítimo sem `WHERE` do capítulo — a intenção **é** a tabela inteira.
Duas observações: rode-o dentro de `BEGIN` mesmo assim, porque um `UPDATE` sem `WHERE` merece
rede até quando está certo; e note que `ROUND` arredonda, enquanto `CAST` sozinho truncaria —
`CAST(12.9 AS INTEGER)` dá 12, não 13. A diferença entre truncar e arredondar, aplicada a
milhares de produtos, é dinheiro.

## AP3 — A rede

**1. `UPDATE` sem `WHERE`, desfeito.**

```sql
SELECT COUNT(*) FROM produtos WHERE preco_centavos = 1;   -- 0
BEGIN;
UPDATE produtos SET preco_centavos = 1;                   -- 13 linhas
SELECT COUNT(*) FROM produtos WHERE preco_centavos = 1;   -- 13
ROLLBACK;
SELECT COUNT(*) FROM produtos WHERE preco_centavos = 1;   -- 0
```

O `13` no meio é o estrago real, visível, dentro da transação. O `0` no fim é a rede
funcionando. Note que `BEGIN` e `ROLLBACK` devolvem `Linhas afetadas: -1` — o `-1` significa
"não se aplica", não erro.

**2. `DELETE` recusado pela chave estrangeira.**

```
Erro de SQL: FOREIGN KEY constraint failed
```

A regra que impediu: `pedidos.FOREIGN KEY (cliente_id) REFERENCES clientes(id)`. O cliente 1
tem pedidos; removê-lo criaria órfãos. Nada a desfazer — o comando não chegou a acontecer, e
essa é a natureza de uma restrição: ela previne em vez de reverter.

**3. `INSERT` violando `NOT NULL`.**

```
Erro de SQL: NOT NULL constraint failed: clientes.data_cadastro
```

A coluna `data_cadastro` é `NOT NULL` e não tem `DEFAULT`. Compare com `produtos.ativo`, que é
`NOT NULL DEFAULT 1` e pode ser omitida sem problema — **`NOT NULL` sozinho obriga você a
passar o valor; com `DEFAULT`, o banco passa por você.** A mensagem do SQLite nomeia a tabela e
a coluna exatas, o que a torna uma das mais úteis que ele produz.

**O extra — sem `BEGIN`.** Você rodou `UPDATE produtos SET preco_centavos = 1` no rascunho, em
autocommit. Não há `ROLLBACK` possível: a transação implícita foi confirmada no instante em que
o comando terminou. A recuperação é `python codigo/cap11/preparar_rascunho.py` — recriar do
original.

**E é aqui que o exercício fecha:** você tem esse comando porque o rascunho é uma cópia de algo
íntegro. Em produção, o equivalente é o backup — e a pergunta "de quando é o último backup, e
quanto tempo leva para restaurá-lo?" tem que ter resposta **antes** de você precisar dela. Se a
resposta é "não sei", o `BEGIN` deixa de ser boa prática e vira a única defesa que existe.

## D1 — A correção de produção

**A pergunta obrigatória, primeiro.** Entre `julianday('now') - julianday(data) > 90` e
`data < '2026-07-20'`, o roteiro leva a **segunda**. `'now'` significa o momento da execução:
se o colega rodar o roteiro amanhã, ou reexecutar semana que vem para conferir, o conjunto de
linhas muda. Um roteiro cujo alvo muda conforme o relógio não pode ser revisado antes, nem
auditado depois — a verificação final não teria como provar que só as linhas previstas
mudaram. **Data absoluta em roteiro, data relativa em rotina automática.**

O `SELECT` de investigação encontra **2** pedidos: o 15 (2026-06-15, cliente 5) e o 18
(2026-07-12, cliente 3).

```sql
-- ============================================================
-- roteiro-correcao.sql
-- Objetivo: cancelar pedidos pendentes anteriores a 2026-07-20
-- Autorização: e-mail do comercial de 2026-08-04
-- Esperado: 2 linhas afetadas.
--
-- SE ALGO DER ERRADO: execute ROLLBACK; e NÃO tente corrigir.
-- Avise <responsável> antes de rodar qualquer outro comando.
-- Nenhum comando abaixo deve ser executado por seleção parcial:
-- rode o arquivo inteiro ou uma linha completa por vez.
-- ============================================================

-- (a) INVESTIGAÇÃO: quem são, de quem, de quando, quanto valem.
SELECT p.id, p.data, c.nome AS cliente,
       SUM(i.quantidade * i.preco_unitario_centavos) / 100.0 AS valor
FROM pedidos p
JOIN clientes c     ON c.id = p.cliente_id
JOIN itens_pedido i ON i.pedido_id = p.id
WHERE p.status = 'pendente' AND p.data < '2026-07-20'
GROUP BY p.id, p.data, c.nome;

-- (b) ENSAIO: o WHERE exato do UPDATE. ESPERADO: 2 linhas.
SELECT id, data, status
FROM pedidos
WHERE status = 'pendente' AND p.data < '2026-07-20';

-- (c) EXECUÇÃO
BEGIN;

UPDATE pedidos
SET status = 'cancelado'
WHERE status = 'pendente' AND data < '2026-07-20';
-- (d) CRITÉRIO: a saída acima DEVE ser "Linhas afetadas: 2".
--     Qualquer outro número: execute ROLLBACK; e pare aqui.
--     Não é julgamento — é comparação com o número desta linha.

-- (e) VERIFICAÇÃO FINAL, ainda dentro da transação:
SELECT status, COUNT(*) AS quantos FROM pedidos GROUP BY status;
-- ESPERADO: cancelado 3 (era 1) e concluido 17 — DUAS linhas.
--     A linha 'pendente' NAO aparece com 0: ela desaparece.
--     GROUP BY so mostra grupos que existem (03.06).

SELECT COUNT(*) AS nao_deveriam_ter_mudado
FROM pedidos
WHERE status = 'cancelado' AND id NOT IN (15, 18) AND id <> 20;
-- ESPERADO: 0.

COMMIT;
```

**O erro plantado no ensaio.** A consulta (b) acima tem `p.data` sem que `p` exista — a tabela
não recebeu apelido ali. Ela dá `no such column: p.data`. Foi deixada de propósito: se você
copiou o roteiro sem executar o ensaio, o erro passou. É a razão de o ensaio existir. Corrija
para `data < '2026-07-20'` — e note que **este erro é o inofensivo**, porque falha alto. O
perigoso é o que roda.

**Os números finais, verificados:** antes, `cancelado 1 / concluido 17 / pendente 2` em três
linhas; depois, `cancelado 3 / concluido 17` em **duas**. A linha `pendente` não vira zero —
ela some, porque `GROUP BY` só produz grupos que existem (03.06). Quem escreveu o valor
esperado como "pendente 0" vai ver duas linhas onde esperava três e achar que deu errado. É a
mesma lição do 03.08: **ausência não é zero**, e um valor esperado mal escrito provoca o
`ROLLBACK` de uma operação correta.

**Por que a verificação fica dentro da transação.** Se ela viesse depois do `COMMIT`, descobrir
um problema já não adiantaria. Dentro, o `ROLLBACK` ainda está disponível. A ordem correta é
sempre: alterar → verificar → confirmar. Nunca alterar → confirmar → verificar.

**O fecho.** O roteiro é entregue antes porque a revisão precisa acontecer quando ainda é
barata. Escrito durante a execução, ele não é roteiro — é improviso com registro. Entregue
antes, ele pode ser lido por outra pessoa, questionado, corrigido, e o número esperado pode ser
conferido contra o pedido original do comercial. Às 22h, sozinho, o executor não deveria estar
decidindo nada: deveria estar comparando dois números e seguindo uma instrução que já foi
pensada por alguém descansado. **Todo procedimento de produção existe para transformar
julgamento sob pressão em comparação.**

---

## Erros mais comuns

1. **Prever que `UPDATE ... SET ativo = 1` em linhas já ativas afeta 0.** Afeta as que o
   `WHERE` encontrou.
2. **Tratar `Linhas afetadas: 0` como sucesso.** É um resultado que pede explicação.
3. **Confiar na chave estrangeira para além do que ela garante** (A2.6).
4. **Inserir filho antes do pai** no `INSERT`.
5. **Chutar ids** em vez de lê-los.
6. **Truncar quando queria arredondar** — `CAST` corta, `ROUND` arredonda.
7. **Usar `'now'` num roteiro** que outra pessoa executa outro dia.
8. **Verificar depois do `COMMIT`.**
9. **Achar que a LGPD se resolve com `ativo = 0`.**
