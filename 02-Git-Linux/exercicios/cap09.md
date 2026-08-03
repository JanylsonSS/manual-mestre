# Exercícios — Capítulo 02.09: Fluxo essencial do Git

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap09.md`](gabaritos/cap09.md).

## Aquecimento

### A1 — O comando certo `[Aquecimento · ~10 min · a intenção]`

**Tarefa.** Qual comando resolve cada intenção?

1. Ver quais arquivos foram alterados desde o último commit.
2. Ver as linhas que mudaram e ainda não foram preparadas.
3. Ver o que exatamente vai entrar no próximo commit.
4. Preparar apenas o `analise.py`.
5. Ver os 5 commits mais recentes, uma linha cada.
6. Procurar no histórico os commits cuja mensagem cita "cidade".
7. Tirar um arquivo da área de preparo, mantendo as alterações.
8. Ver todos os arquivos alterados pelo último commit.

### A2 — Lendo um diff `[Aquecimento · ~10 min · interpretação]`

**Tarefa.** Interprete a saída abaixo, linha a linha, e responda: quantas linhas foram acrescentadas, quantas removidas, e o que a mudança faz?

```diff
--- a/analise.py
+++ b/analise.py
@@ -8,6 +8,8 @@ def calcular_total(vendas):
     total = 0
     for venda in vendas:
-        total += venda["valor"]
+        if venda["valor"] > 0:
+            total += venda["valor"]
+    total = round(total, 2)
     return total
```

### A3 — `.gitignore` `[Aquecimento · ~10 min · entra ou não?]`

**Tarefa.** Para cada arquivo, decida se deve ser versionado e escreva a regra de `.gitignore` quando não:

1. `relatorio_aurora.py`
2. `__pycache__/analise.cpython-312.pyc`
3. `.env` (com a senha do banco)
4. `.env.example` (com as chaves e valores fictícios)
5. `vendas.csv` (dados de exemplo, 4 KB)
6. `base_completa.db` (banco de 800 MB)
7. `saidas/relatorio_2026_07.txt` (gerado pelo script)
8. `README.md`

### A4 — Mensagens de commit `[Aquecimento · ~10 min · reescreva]`

**Tarefa.** Reescreva cada mensagem, explicando em uma linha o que estava errado:

1. `mudanças`
2. `Corrigido o bug do relatório e adicionado o filtro por cidade e atualizado o README`
3. `ajustes finais v3 AGORA VAI`
4. `Adicionando validação`
5. `.`

## Aplicação

### AP1 — Versionando o seu repositório `[Aplicação · ~25 min · o primeiro commit]`

**Tarefa.** Transforme sua pasta de estudo num repositório Git: (1) configure identidade global; (2) crie o `.gitignore` **antes** do `init`; (3) `git init`; (4) confira com `git status` que nada indevido aparece; (5) primeiro commit; (6) comprove com `git ls-files` que só o que deve está rastreado. Registre cada comando e sua saída.

### AP2 — As três comparações `[Aplicação · ~20 min · o diff em ação]`

**Tarefa.** Num arquivo versionado: (1) altere duas linhas; (2) rode e registre `git diff`, `git diff --staged` e `git diff HEAD`; (3) prepare o arquivo; (4) rode os três de novo e registre; (5) explique, em duas linhas, por que as saídas trocaram de lugar.

### AP3 — Investigando o histórico `[Aplicação · ~20 min · o log como ferramenta]`

**Tarefa.** No seu repositório (ou num clone de algum projeto público), responda usando apenas o `git log`: (1) quantos commits existem? (2) qual o commit mais antigo? (3) quais commits citam determinada palavra na mensagem? (4) quais arquivos o último commit tocou? (5) qual foi o histórico de mudanças de um arquivo específico? Registre o comando de cada resposta.

## Desafio

### D1 — O repositório do Manual Mestre `[Desafio · ~50 min · padrão profissional]`

**Tarefa.** Transforme sua pasta de estudo num repositório Git profissional:

- **(a)** `.gitignore` completo (Python, segredos, saídas geradas, sistema), com ao menos uma exceção `!`;
- **(b)** primeiro commit com **apenas** o que deve ser versionado — comprove com `git ls-files`;
- **(c)** construa **5 commits temáticos** a partir do trabalho existente, separando por assunto com `git add` seletivo;
- **(d)** escreva um `README.md` explicando a estrutura e comite-o;
- **(e)** demonstre três consultas úteis (`--grep`, `--stat`, `-p` num arquivo) e explique o que cada uma responde.

**Fecho:** 5 linhas sobre o que você faria diferente se pudesse recomeçar o repositório.

<details><summary>💡 Dica 1 (conceito)</summary>
`git status --short` confere rápido; `git ls-files` lista exatamente o que está rastreado — é a prova do item (b).
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para separar em 5 commits o que já existe: prepare por pasta ou assunto (`git add 00-Introducao/`), conferindo com `--staged` antes de cada commit.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
.gitignore → init → add seletivo ×5 com commits temáticos → README → log --oneline → as três consultas → reflexão.
</details>
