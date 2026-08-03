# Exercícios — Capítulo 02.06: Variáveis de ambiente e PATH

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap06.md`](gabaritos/cap06.md).

## Aquecimento

### A1 — Lendo variáveis `[Aquecimento · ~10 min · o que sai?]`

**Tarefa.** Para cada comando, diga o que é impresso e por quê:

1. `echo $HOME`
2. `echo HOME`
3. `NOME="Aurora"; echo "Bem-vindo à $NOME"`
4. `NOME="Aurora"; echo 'Bem-vindo à $NOME'`
5. `echo $NAO_EXISTE`
6. `echo "[$NAO_EXISTE]"`

### A2 — PATH e busca `[Aquecimento · ~10 min · quem é executado?]`

**Tarefa.** O PATH é `/usr/local/bin:/usr/bin:/bin`. Existem: `/usr/bin/python3` (3.9), `/usr/local/bin/python3` (3.12) e `./python3` na pasta atual (3.7). Para cada comando, diga qual é executado:

1. `python3`
2. `./python3`
3. `/usr/bin/python3`
4. E se o PATH virasse `/usr/bin:/usr/local/bin:/bin`, o que muda no item 1?
5. E se `/usr/local/bin/python3` existisse **sem** o bit `x`?

### A3 — Shell × ambiente `[Aquecimento · ~5 min · herda ou não?]`

**Tarefa.** Em cada situação, a segunda linha imprime o valor ou vazio?

1. `X="a"` → `bash -c 'echo $X'`
2. `export X="a"` → `bash -c 'echo $X'`
3. `export X="a"` → `bash -c 'X="b"'` → `echo $X` (no shell original)
4. `./configura.sh` (que faz `export Y="z"` lá dentro) → `echo $Y`

### A4 — Diagnóstico `[Aquecimento · ~10 min · causa e correção]`

**Tarefa.** Causa provável e correção:

1. `bash: python: command not found` (mas o Python está instalado)
2. `python --version` responde 3.9, e você instalou o 3.12 ontem
3. Você acrescentou o `export` ao `.bashrc` e nada mudou no terminal aberto
4. Depois de um `export PATH=...`, nem o `ls` funciona mais

## Aplicação

### AP1 — Abrindo o seu PATH `[Aplicação · ~20 min · exploração real]`

**Tarefa.** Na sua máquina: (1) liste o PATH uma pasta por linha; (2) conte quantas pastas ele tem; (3) descubra a origem de 5 comandos que você usa (`which`); (4) rode `which -a python3` (ou `python`) e verifique se há mais de um; (5) registre no caderno de bordo qual arquivo de configuração o seu shell lê ao iniciar (`echo $SHELL` ajuda a decidir).

### AP2 — Seu comando no PATH `[Aplicação · ~20 min · instalação permanente]`

**Tarefa.** (1) Crie `~/meus-scripts` e ponha lá um script com shebang e `chmod +x`; (2) tente chamá-lo pelo nome e registre o erro; (3) acrescente a pasta ao PATH na sessão atual e chame de novo; (4) faça **backup** do arquivo de configuração e torne a mudança permanente com `>>`; (5) prove abrindo um terminal novo. Registre todos os comandos.

### AP3 — Configuração externa `[Aplicação · ~20 min · o padrão profissional]`

**Tarefa.** Pegue um script Python seu que tenha valores fixos (nome de arquivo, separador, limite). Adapte-o para ler cada um do ambiente com `os.environ.get("CHAVE", padrao)`. Depois execute-o (a) sem definir nada — deve funcionar com os padrões; (b) com `CHAVE=valor python3 script.py` — deve mudar o comportamento sem editar o código. Registre as duas saídas lado a lado.

## Desafio

### D1 — O Atlas configurável `[Desafio · ~45 min · cadeia de precedência]`

**Tarefa.** Evolua o `relatorio_aurora.py` (01.25) para o padrão profissional de configuração:

- **(a)** `AURORA_ARQUIVO_VENDAS`, `AURORA_SEPARADOR` e `AURORA_TOP_PRODUTOS` lidas do **ambiente**, com o `config.json` como segunda opção e valores embutidos como último recurso (ambiente → arquivo → padrão).
- **(b)** Crie `.env.example` documentando as três variáveis com valores fictícios.
- **(c)** Crie um `.env` real (permissão **600** — 02.05) e um `rodar.sh` que carrega o `.env` e executa o relatório.
- **(d)** Demonstre duas execuções com configurações diferentes **sem alterar nenhum arquivo** — só variáveis na linha de comando.

**Fecho:** 5 linhas sobre por que a precedência ambiente > arquivo > padrão é o padrão da indústria.

<details><summary>💡 Dica 1 (conceito)</summary>
Em Python: `os.environ.get("CHAVE") or config.get("chave") or PADRAO` — ou com ifs explícitos, se quiser tratar string vazia.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Variável pontual, só para uma execução: `AURORA_TOP_PRODUTOS=3 python3 relatorio_aurora.py`. Nada é exportado.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
`carregar_config()` com a cadeia → `.env.example` versionável → `.env` com 600 → `rodar.sh` com `set -a; source .env; set +a` → duas execuções com valores diferentes.
</details>
