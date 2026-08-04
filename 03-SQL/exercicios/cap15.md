# Exercícios — Capítulo 03.15: Transações e ACID

> **Antes de tudo:** `python codigo/cap15/transacoes.py`. Os exercícios usam `dados/tx.db`,
> recriado a cada execução do script. Concorrência exige **duas conexões** — todos os
> exercícios de aplicação são em Python, não em `.sql`.

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap15.md`](gabaritos/cap15.md).

## Aquecimento

### A1 — Qual letra? `[Aquecimento · ~10 min · A, C, I ou D?]`

**Tarefa.** Para cada situação, diga qual garantia de ACID está em jogo — e se ela foi **cumprida** ou **violada**:

1. A energia cai logo após um `COMMIT`; ao religar, o dado está lá.
2. Um `UPDATE` de débito roda e o de crédito falha; o `ROLLBACK` desfaz os dois.
3. B consulta o saldo enquanto A tem uma transação aberta, e vê o valor antigo.
4. Um `INSERT` é recusado por `CHECK (saldo >= 0)`.
5. Dois clientes leem o mesmo estoque e ambos vendem a última unidade.
6. A energia cai **no meio** de uma transação; ao religar, nada dela foi aplicado.
7. Uma transação vê linhas novas aparecerem entre duas consultas idênticas.
8. `DROP TABLE` e `RENAME` do 03.12 dentro de `BEGIN`/`COMMIT`.

### A2 — Preveja `[Aquecimento · ~10 min · duas conexões]`

**Tarefa.** Saldo inicial R$ 1.000,00 (100000 centavos). Preveja o resultado final de cada sequência e confirme executando:

1. `A: BEGIN` · `A: saldo = 90000` · `B: SELECT saldo` · `A: ROLLBACK` · `B: SELECT saldo`
2. `A: BEGIN` · `A: saldo = 90000` · `B: UPDATE saldo = 80000`
3. `A: BEGIN` · `A: saldo = 90000` · `A: COMMIT` · `B: UPDATE saldo = 80000`
4. `A: lê` · `B: lê` · `A: grava lido−100` · `B: grava lido−200`
5. `A: UPDATE saldo = saldo − 10000` · `B: UPDATE saldo = saldo − 20000`
6. `A: BEGIN` · `A: UPDATE ... erro de CHECK` · `A: COMMIT`

### A3 — Achou o *lost update*? `[Aquecimento · ~10 min · o padrão perigoso]`

**Tarefa.** Quais destes trechos têm o padrão ler-modificar-escrever vulnerável? Para cada um que tiver, escreva a correção:

1. `UPDATE contas SET saldo = saldo - 100 WHERE id = 1;`
2. `s = SELECT saldo...` → `UPDATE contas SET saldo = s - 100 WHERE id = 1;`
3. `UPDATE produtos SET estoque = estoque - 1 WHERE id = ? AND estoque > 0;`
4. `n = SELECT COUNT(*)...` → `INSERT INTO pedidos (numero) VALUES (n + 1);`
5. `UPDATE pedidos SET status = 'enviado' WHERE id = 42;`
6. `v = SELECT visitas...` → `UPDATE paginas SET visitas = v + 1 WHERE id = ?;`

### A4 — `BEGIN` ou `BEGIN IMMEDIATE`? `[Aquecimento · ~10 min · a leitura decide?]`

**Tarefa.** Para cada operação, diga qual usar e por quê:

1. Um relatório que só lê.
2. Marcar um pedido como cancelado, sem condição.
3. Sacar de uma conta, se houver saldo.
4. Inserir três linhas relacionadas.
5. Atribuir o próximo número de nota fiscal.
6. A migração de quatro passos do 03.12.

## Aplicação

### AP1 — Reproduza e corrija `[Aplicação · ~25 min · as três formas]`

**Tarefa.** Escreva um script que reproduza o *lost update* e o corrija de três maneiras diferentes, mostrando o resultado de cada uma:

1. reproduza o erro (esperado R$ 700,00, obtido R$ 800,00);
2. corrija com `SET saldo = saldo - valor`;
3. corrija com `BEGIN IMMEDIATE`;
4. corrija com **bloqueio otimista**: grave com `WHERE saldo = <valor lido>`, verifique as linhas afetadas e, se for 0, releia e tente de novo.

Para cada correção, responda: em que situação ela é a **melhor** das três?

### AP2 — O estoque da Black Friday `[Aplicação · ~20 min · não vender o que não existe]`

**Tarefa.** Uma tabela `produtos` com `estoque = 3` e `CHECK (estoque >= 0)`. Simule **cinco** clientes comprando ao mesmo tempo.

1. Implemente a versão ingênua (ler, decidir, escrever) e conte quantas vendas passam.
2. Implemente a versão correta com a condição embutida no `UPDATE` e as linhas afetadas decidindo.
3. Mostre que exatamente 3 vendem e 2 recebem "sem estoque".
4. Explique por que o `CHECK (estoque >= 0)` **não** teria salvado a versão ingênua.
5. Escreva a mensagem que o quarto cliente vê — e por que ela é diferente de um erro.

### AP3 — A transação longa `[Aplicação · ~20 min · medir os dois extremos]`

**Tarefa.** Insira 3 000 linhas de três formas e cronometre: uma por vez em autocommit; em lotes de 100; tudo numa transação só.

1. Registre os três tempos e a razão entre eles.
2. Explique o que cada `COMMIT` faz para custar tanto.
3. Agora o outro lado: com a transação única aberta, tente escrever de outra conexão e registre o que acontece.
4. **A conclusão que o exercício pede:** se agrupar é tão mais rápido, por que não agrupar tudo sempre? Dê dois motivos.

## Desafio

### D1 — A transferência bancária `[Desafio · ~50 min · o código que você defenderia numa auditoria]`

**Tarefa.** Implemente `transferir(origem, destino, centavos)` correta sob concorrência:

- **(a)** atômica: nunca debita sem creditar;
- **(b)** recusa saldo insuficiente com mensagem clara, **antes** de debitar;
- **(c)** correta com duas chamadas simultâneas na mesma conta;
- **(d)** `ROLLBACK` explícito em **todo** caminho de erro, inclusive exceção inesperada;
- **(e)** não segura o bloqueio de escrita mais que o necessário;
- **(f)** devolve um resultado que o chamador consegue distinguir: sucesso, saldo insuficiente, conta inexistente.

**O teste que prova.** Escreva um teste que dispare duas transferências simultâneas de contas com saldo justo e verifique **duas invariantes**: a soma de todos os saldos permanece constante, e nenhuma conta ficou negativa.

**Fecho:** 5 linhas sobre por que testar concorrência exige provocá-la de propósito — e por que um teste que passa "quase sempre" é pior que nenhum.

<details><summary>💡 Dica 1 (conceito)</summary>
O item (b) exige ler o saldo para decidir — é exatamente o caso do `BEGIN IMMEDIATE`. Ou embuta a condição: `UPDATE ... SET saldo = saldo - ? WHERE id = ? AND saldo >= ?` e deixe as linhas afetadas decidirem.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para (e): a transação começa no `BEGIN IMMEDIATE` e termina no `COMMIT`. Validação de argumentos, busca de nomes e formatação de mensagem ficam **fora** dela. Nada que espere por rede ou por disco lento entra.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`validar argumentos` → `BEGIN IMMEDIATE` → `UPDATE` do débito com a condição → conferir linhas afetadas → se 0, `ROLLBACK` e devolver "saldo insuficiente" → `UPDATE` do crédito → conferir → `COMMIT`. Tudo dentro de `try/except` com `ROLLBACK` no `except`.
</details>
