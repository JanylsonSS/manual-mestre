# Exercícios — Capítulo 03.11: `INSERT`, `UPDATE`, `DELETE`

> **Antes de tudo:** `python codigo/cap11/preparar_rascunho.py`. Todo exercício deste capítulo
> roda com `AURORA_BANCO=dados/rascunho.db`. Bagunçou? Rode o script de novo.

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap11.md`](gabaritos/cap11.md).

## Aquecimento

### A1 — Preveja a saída `[Aquecimento · ~10 min · quantas linhas?]`

**Tarefa.** Antes de executar, escreva quantas linhas cada comando afeta. Depois execute e compare:

1. `INSERT INTO produtos (nome, categoria, preco_centavos) VALUES ('Webcam HD', 'perifericos', 24900);`
2. `UPDATE produtos SET ativo = 1 WHERE categoria = 'perifericos';`
3. `UPDATE pedidos SET status = 'concluido' WHERE status = 'pendente';`
4. `DELETE FROM produtos WHERE preco_centavos > 1000000;`
5. `UPDATE clientes SET cidade = 'campinas';`
6. `DELETE FROM itens_pedido WHERE pedido_id = 20;`

### A2 — Ache o perigo `[Aquecimento · ~10 min · qual é destrutivo?]`

**Tarefa.** Classifique cada comando em **seguro**, **perigoso** ou **catastrófico**, e justifique:

1. `SELECT * FROM clientes;`
2. `DELETE FROM clientes WHERE id = 999;`
3. `UPDATE produtos SET preco_centavos = preco_centavos * 2;`
4. `DELETE FROM itens_pedido;`
5. `UPDATE clientes SET email = NULL WHERE id = 3;`
6. `UPDATE pedidos SET cliente_id = 1;`

### A3 — O ensaio `[Aquecimento · ~10 min · escreva o SELECT antes]`

**Tarefa.** Para cada `UPDATE`, escreva o `SELECT` de ensaio correspondente, execute-o e anote o número de linhas. Só então execute o `UPDATE` e confira:

1. Desativar todos os produtos de `mobiliario`. **(Leia o que acontece com atenção.)**
2. Cancelar os pedidos do cliente 5.
3. Corrigir o e-mail do cliente 3 para `beatriz@exemplo.com`.
4. Dar 5% de desconto nos produtos acima de R$ 500,00.
5. Preencher a cidade dos clientes que estão com cidade nula, usando `'nao informada'`.

### A4 — Apagar ou desativar? `[Aquecimento · ~10 min · o julgamento]`

**Tarefa.** Para cada situação, decida entre `DELETE` e `UPDATE ... SET ativo = 0` (ou equivalente) — e diga que pergunta você faria ao solicitante:

1. "Tira esse produto do site, saiu de linha."
2. "Esse cliente pediu para excluir a conta dele (LGPD)."
3. "Cadastrei o produto duas vezes por engano, agora há pouco."
4. "Esse pedido foi um teste do time, apaga."
5. "Limpa a tabela de logs de acesso de mais de 2 anos."
6. "Esse fornecedor não trabalha mais com a gente."

## Aplicação

### AP1 — O cadastro `[Aplicação · ~20 min · um pedido inteiro]`

**Tarefa.** Cadastre, na ordem correta: (1) um cliente novo; (2) dois produtos novos; (3) um pedido para esse cliente com status `'pendente'`; (4) três itens desse pedido, sendo dois dos produtos novos. Depois, escreva a consulta que exibe o pedido completo com nome do cliente, produtos e valor total — reaproveitando o que você fez no 03.07.

**A parte que ensina:** tente inserir os itens **antes** do pedido e registre o erro que aparece. Explique por que a ordem importa.

### AP2 — O reajuste `[Aplicação · ~25 min · ensaio e conferência documentados]`

**Tarefa.** Execute três reajustes, cada um com o ciclo completo documentado (ensaio → número esperado → comando → linhas afetadas → conferência):

1. +8% em `perifericos` ativos;
2. −15% nos produtos que nunca venderam (use `NOT EXISTS`);
3. arredondar todos os preços para a dezena de centavos mais próxima.

Para cada um, registre o total do catálogo **antes e depois** e explique se a variação faz sentido.

### AP3 — A rede `[Aplicação · ~20 min · erre de propósito]`

**Tarefa.** Provoque os três erros abaixo, registre a mensagem exata e desfaça cada um:

1. Um `UPDATE` sem `WHERE` — dentro de `BEGIN`, desfeito com `ROLLBACK`. Prove com um `SELECT` antes e depois.
2. Um `DELETE` que a chave estrangeira recusa. Explique qual regra da tabela o impediu.
3. Um `INSERT` que viola `NOT NULL`. Explique qual coluna e por quê.

**Extra:** rode o erro 1 **sem** o `BEGIN`, no rascunho, e responda: como você recuperaria o banco agora?

## Desafio

### D1 — A correção de produção `[Desafio · ~50 min · um roteiro que outra pessoa executa]`

**Cenário.** Um relatório apontou pedidos com `status = 'pendente'` e data anterior a `2026-07-20`. O comercial confirmou por escrito que devem virar `'cancelado'`. Você não vai executar — vai escrever o roteiro que um colega executa em produção, sozinho, às 22h.

Descubra **quantos são** com o `SELECT` de investigação; o número entra no roteiro como valor esperado.

Entregue um arquivo `roteiro-correcao.sql` contendo, em ordem e comentado:

- **(a)** o `SELECT` de **investigação** — quais são esses pedidos, de quem, de quando, com que valor;
- **(b)** o `SELECT` de **ensaio** com o `WHERE` exato do comando, e o número esperado escrito no comentário;
- **(c)** `BEGIN`, o `UPDATE`, e a linha de conferência;
- **(d)** o critério explícito: **se o número não bater, `ROLLBACK`** — escrito de forma que não dependa de julgamento no momento;
- **(e)** a consulta de **verificação final** que prova que só os pedidos certos mudaram e nenhum outro;
- **(f)** um parágrafo de abertura no topo do arquivo: o que fazer se algo der errado e quem avisar.

**Fecho:** 5 linhas sobre por que o roteiro é entregue **antes** da execução, e não escrito durante.

**Pergunta obrigatória (é onde mora a nota).** O critério "antigo" poderia ser escrito como `julianday('now') - julianday(data) > 90` ou como `data < '2026-07-20'`. As duas rodam no SQLite. **Qual delas você coloca num roteiro que outra pessoa executa amanhã, e por quê?** Responda em três linhas antes de escrever o arquivo.

<details><summary>💡 Dica 1 (conceito)</summary>
Datas no SQLite são texto `YYYY-MM-DD`, e esse formato compara corretamente com `<` (03.04). `julianday('now')` também funciona — mas repare no que a palavra `now` significa para quem executa o roteiro num dia diferente do seu.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para (e): guarde os ids do ensaio e verifique que os pedidos **fora** dessa lista continuam com o status original. Uma contagem por status antes e depois também serve.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Cabeçalho com o plano de contingência → `SELECT` de investigação → `SELECT` de ensaio (`-- esperado: N`) → `BEGIN` → `UPDATE` → `-- se != N, ROLLBACK` → `SELECT` de verificação → `COMMIT`.
</details>
