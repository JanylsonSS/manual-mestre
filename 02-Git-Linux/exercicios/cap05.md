# Exercícios — Capítulo 02.05: Permissões e processos

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap05.md`](gabaritos/cap05.md).

## Aquecimento

### A1 — Lendo permissões `[Aquecimento · ~10 min · quem pode o quê]`

**Tarefa.** Para cada linha, diga o tipo, e o que o dono, o grupo e outros podem fazer:

1. `-rw-r--r--  1 ana dev  1240 relatorio.py`
2. `-rwxr-xr-x  1 ana dev   890 backup.sh`
3. `drwxr-x---  2 ana dev  4096 privado`
4. `-rw-------  1 ana dev   120 .env`
5. `-rwxrwxrwx  1 ana dev   340 perigoso.sh`
6. `dr-xr-xr-x  2 ana dev  4096 somente_leitura`

### A2 — Traduzindo notações `[Aquecimento · ~10 min · simbólico ↔ numérico]`

**Tarefa.** Complete a tradução:

1. `755` → ?
2. `644` → ?
3. `600` → ?
4. `777` → ?
5. `rwxr-x---` → ?
6. `rw-rw-r--` → ?
7. `r--------` → ?
8. `rwx------` → ?

### A3 — Qual comando? `[Aquecimento · ~5 min · a intenção]`

**Tarefa.** Escreva o `chmod` para cada intenção:

1. Tornar `backup.sh` executável por todos.
2. Tornar `deploy.sh` executável só pelo dono.
3. Proteger `.env` para que só o dono leia e escreva.
4. Remover a permissão de escrita de grupo e outros em `dados.csv`.
5. Definir uma pasta como 755.

### A4 — Diagnóstico `[Aquecimento · ~10 min · falhas de execução]`

**Tarefa.** Causa provável e sequência de investigação:

1. `bash: ./script.sh: Permission denied`
2. `./relatorio.py: line 3: syntax error near unexpected token '('`
3. `bash: ./script.sh: /usr/bin/env bash^M: bad interpreter`
4. `bash: script.sh: command not found` (o arquivo existe e é executável)

## Aplicação

### AP1 — Seu primeiro comando `[Aplicação · ~20 min · shebang + chmod]`

**Tarefa.** Crie dois scripts (um `.sh`, um `.py`), cada um imprimindo uma mensagem. Para cada um: (1) tente executar com `./` antes do chmod e registre o erro; (2) confira com `ls -l`; (3) aplique `chmod +x`; (4) execute e registre a saída; (5) remova o shebang de um deles e execute de novo — registre o que acontece.

### AP2 — O caçador de processos `[Aplicação · ~20 min · ps, grep, kill]`

**Tarefa.** Em dois terminais: inicie três processos `sleep` com durações diferentes; no outro terminal, liste-os com `ps aux | grep sleep | grep -v grep`; encerre um com `kill`, outro com `kill -9`, e deixe o terceiro terminar sozinho. Registre: os PIDs, os comandos usados, e a diferença observada entre os dois `kill`.

### AP3 — Permissões de projeto `[Aplicação · ~15 min · o trio certo]`

**Tarefa.** Num projeto simulado com `deploy.sh`, `config.env`, `dados.csv`, `README.md` e a pasta `scripts/`, aplique a permissão adequada a cada um e justifique em uma linha. Confira com `ls -l` e explique o que aconteceria se o `config.env` estivesse 644 num servidor compartilhado.

## Desafio

### D1 — O auditor de permissões `[Desafio · ~40 min · revisão de segurança]`

**Tarefa.** Audite o repositório do Manual Mestre: (a) quais arquivos são executáveis — algum não deveria ser? (b) há arquivos graváveis por "outros"? (c) que permissão um `.env` com senha deveria ter, e o risco de 644 num servidor compartilhado? (d) seus scripts têm shebang e bit `x`? Corrija o que estiver errado, registrando os comandos. Fecho: 5 linhas sobre o princípio do menor privilégio.

<details><summary>💡 Dica 1 (conceito)</summary>
`find . -type f -perm -u+x` lista executáveis; compare com o que **deveria** ser executável.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
`find . -perm -o+w` acha arquivos graváveis por qualquer um — o achado mais grave de uma auditoria.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Tabela: achado · comando revelador · risco · correção. Fecho com o princípio.
</details>
