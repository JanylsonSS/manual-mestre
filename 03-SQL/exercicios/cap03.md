# Exercícios — Capítulo 03.03: `SELECT` e `WHERE`

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap03.md`](gabaritos/cap03.md).

## Aquecimento

### A1 — Preveja a saída `[Aquecimento · ~10 min · quantas linhas?]`

**Tarefa.** **Escreva a previsão antes de executar.** Quantas linhas cada consulta devolve?

1. `SELECT * FROM clientes;`
2. `SELECT * FROM clientes WHERE cidade = 'santos';`
3. `SELECT * FROM clientes WHERE cidade IS NULL;`
4. `SELECT * FROM clientes WHERE cidade <> 'santos';`
5. `SELECT * FROM produtos WHERE preco_centavos BETWEEN 8990 AND 15990;`
6. `SELECT * FROM produtos WHERE categoria IN ('audio');`
7. `SELECT * FROM pedidos WHERE status <> 'concluido';`
8. `SELECT * FROM clientes WHERE email = NULL;`

### A2 — Traduza a pergunta `[Aquecimento · ~10 min · escreva o WHERE]`

**Tarefa.** Escreva a consulta para cada pergunta de negócio:

1. Clientes cadastrados em 2026.
2. Produtos de áudio acima de R$ 400,00.
3. Pedidos que **não** foram cancelados (incluindo os de status desconhecido, se houvesse).
4. Clientes cujo nome começa com "A".
5. Produtos cujo nome contém "USB".
6. Clientes sem e-mail cadastrado.
7. Produtos inativos **ou** com preço abaixo de R$ 50,00.
8. Pedidos de 2026 dos clientes 1, 2 e 4.

### A3 — Lógica de três valores `[Aquecimento · ~10 min · V, F ou desconhecido?]`

**Tarefa.** Para cada expressão, diga se o resultado é verdadeiro, falso ou desconhecido — e se o `WHERE` deixaria a linha passar:

1. `10 = 10`
2. `10 <> 10`
3. `NULL = 10`
4. `NULL <> 10`
5. `NULL = NULL`
6. `NULL IS NULL`
7. `NULL IS NOT NULL`
8. `5 > 3 AND NULL = 1`

### A4 — Ache o erro `[Aquecimento · ~10 min · o que está errado?]`

**Tarefa.** Cada consulta tem um defeito. Identifique e corrija:

1. `SELECT nome FROM clientes WHERE email = NULL;`
2. `SELECT nome FROM clientes WHERE cidade = "campinas";`
3. `SELECT nome FROM clientes WHERE cidade = 'campinas' OR cidade = 'santos' AND data_cadastro >= '2026-01-01';`
4. `SELECT nome FROM produtos WHERE preco_centavos / 100 > 300;`
5. `SELECT nome FROM produtos WHERE nome LIKE 'Mouse';`
6. `SELECT * FROM pedidos WHERE status != 'cancelado';` *(num sistema em que `status` aceita `NULL`)*

## Aplicação

### AP1 — O caçador de `NULL` `[Aplicação · ~25 min · auditoria]`

**Tarefa.** (1) Para **cada** coluna de **cada** tabela do laboratório, descubra quantos `NULL` existem — use `SELECT COUNT(*) - COUNT(coluna) FROM tabela`; (2) monte uma tabela com os achados; (3) para cada coluna com `NULL`, escreva uma consulta de negação que **perderia** linhas por causa dele, e a versão corrigida; (4) explique em duas linhas por que essa auditoria deveria ser o primeiro passo ao receber um banco desconhecido.

### AP2 — Precedência `[Aplicação · ~20 min · a mesma pergunta, três formas]`

**Tarefa.** A pergunta é: *"clientes de Campinas ou Santos, cadastrados em 2026"*. (1) Escreva-a **sem** parênteses e registre o resultado; (2) escreva **com** parênteses e registre; (3) escreva uma terceira versão usando `IN` e registre; (4) explique por que (1) difere das outras duas e qual seria a leitura literal de cada uma; (5) diga qual das três você deixaria no código e por quê.

### AP3 — Busca textual `[Aplicação · ~20 min · explorando o LIKE]`

**Tarefa.** Sobre a tabela `produtos`: (1) prefixo — nomes que começam com "M"; (2) sufixo — nomes que terminam com um dígito; (3) contém — nomes com "USB"; (4) use `_` para achar nomes cujo segundo caractere seja "o"; (5) teste maiúsculas e acentuação: `'%mecanico%'` e `'%mecânico%'` — registre a diferença e explique; (6) reescreva a consulta (3) de forma portável, que funcionaria também em PostgreSQL.

## Desafio

### D1 — O relatório que não fecha `[Desafio · ~45 min · bug silencioso]`

**Tarefa.** Um relatório traz três números que não batem: *"clientes de Campinas: 3"*, *"clientes de fora de Campinas: 4"*, *"total de clientes: 8"*.

- **(a)** Reproduza as três consultas e confirme a divergência;
- **(b)** explique **exatamente** por que a soma não fecha, usando a lógica de três valores;
- **(c)** corrija as consultas de **duas** formas diferentes e compare;
- **(d)** proponha a correção **estrutural** (na tabela, não na consulta) e diga o que ela impediria;
- **(e)** escreva uma consulta de **auditoria** que liste, para cada coluna de cada tabela, quantos `NULL` existem — e interprete o resultado.

**Fecho:** 5 linhas sobre por que este bug é mais perigoso que um erro de sintaxe.

<details><summary>💡 Dica 1 (conceito)</summary>
Para o item (e), você precisa de uma consulta por coluna. Não há como percorrer colunas em SQL puro — escreva-as à mão, ou gere-as com Python a partir de `pragma_table_info`.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
`SELECT COUNT(*) - COUNT(coluna) FROM tabela` conta os nulos numa tacada: `COUNT(*)` conta linhas, `COUNT(coluna)` ignora nulos. O 03.05 explica por quê.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Reprodução → explicação com a tabela de três valores → duas correções (`OR IS NULL` / `COALESCE`) → a correção estrutural (`NOT NULL` + `DEFAULT`) → a auditoria → reflexão.
</details>
