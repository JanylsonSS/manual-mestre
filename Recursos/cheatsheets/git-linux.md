# Cheatsheet — Git e Linux (Módulo 02)

Gerada no fechamento do módulo 02. Índice de memória, não substituto de estudo — cada linha referencia o capítulo de origem.

## Navegação e arquivos

| Operação | Comando | Ref. |
|---|---|---|
| Onde estou | `pwd` | 02.01 |
| Listar (com ocultos e detalhes) | `ls -la` | 02.01 |
| Entrar / voltar / casa / anterior | `cd pasta` · `cd ..` · `cd ~` · `cd -` | 02.02 |
| Criar pasta (com intermediárias) | `mkdir -p a/b/c` | 02.02 |
| Copiar / mover / renomear | `cp -r origem destino` · `mv antigo novo` | 02.02 |
| Apagar com segurança | `ls padrao` → conferir → ↑ → trocar `ls` por `rm` | 02.02 |
| Curingas | `*` (qualquer) · `?` (um) · `[abc]` — expandidos pelo **shell** | 02.02 |

## Inspeção

| Operação | Comando | Ref. |
|---|---|---|
| Contar linhas | `wc -l arquivo` (cuidado com o cabeçalho) | 02.03 |
| Início / fim | `head -20` · `tail -20` | 02.03 |
| Acompanhar ao vivo | `tail -f app.log` (Ctrl+C sai) | 02.03 |
| Navegar e buscar | `less arquivo` — `/` busca, **`q` sai** | 02.03 |
| Tipo do arquivo | `file arquivo` (antes de `cat`) | 02.03 |
| Terminal embaralhado | `reset` (ou `stty sane`) | 02.03 |

## Composição

| Operação | Comando | Ref. |
|---|---|---|
| Gravar / acrescentar | `> arquivo` (trunca!) · `>> arquivo` | 02.04 |
| Erros / juntar / descartar | `2> erros.txt` · `2>&1` · `> /dev/null` | 02.04 |
| Conectar comandos | `comando1 \| comando2` | 02.04 |
| Contar por categoria | `cut -d';' -f4 \| sort \| uniq -c \| sort -rn` | 02.04 |
| Buscar em conteúdo | `grep -i -n -r "texto" .` · `-c` conta · `-v` inverte | 02.04 |
| Buscar arquivos | `find . -name "*.py" -type f` | 02.04 |
| Pular cabeçalho | `tail -n +2 arquivo.csv` | 02.04 |

## Permissões e processos

| Operação | Comando | Ref. |
|---|---|---|
| Ver permissões | `ls -l` — `-rwxr-xr-x` = tipo + dono/grupo/outros | 02.05 |
| Somar | r=4 · w=2 · x=1 | 02.05 |
| O trio essencial | **755** scripts/pastas · **644** arquivos · **600** segredos | 02.05 |
| Tornar executável | `chmod +x script.sh` | 02.05 |
| Shebang | `#!/usr/bin/env bash` · `#!/usr/bin/env python3` | 02.05 |
| Listar processos | `ps aux \| grep nome \| grep -v grep` | 02.05 |
| Encerrar | `kill PID` (TERM, limpa) → `kill -9 PID` (KILL, imediato) | 02.05 |

## Ambiente e PATH

| Operação | Comando | Ref. |
|---|---|---|
| Ler / listar | `echo $HOME` · `env` | 02.06 |
| Shell × ambiente | `VAR=x` (local) · `export VAR=x` (herdável) | 02.06 |
| PATH por linha | `echo $PATH \| tr ':' '\n'` | 02.06 |
| Qual programa roda | `which -a python3` (a fila completa) | 02.06 |
| Acrescentar ao PATH | `export PATH="$HOME/bin:$PATH"` — **nunca esqueça o `$PATH`** | 02.06 |
| Tornar permanente | `echo '...' >> ~/.bashrc` (backup antes!) · `source ~/.bashrc` | 02.06 |
| Ler config em Python | `os.environ.get("CHAVE", padrao)` | 02.06 |

## Scripts de shell

| Operação | Comando | Ref. |
|---|---|---|
| Cabeçalho de segurança | `set -euo pipefail` | 02.07 |
| Argumentos | `$0` nome · `$1 $2` · `$#` quantos · `"$@"` todos | 02.07 |
| Padrão | `SEP="${2:-;}"` | 02.07 |
| Testes de arquivo | `[ -f arq ]` · `[ -d pasta ]` · `[ -x arq ]` | 02.07 |
| Testes de texto/número | `[ -z "$V" ]` · `[ "$A" = "$B" ]` · `[ "$A" -eq "$B" ]` | 02.07 |
| Laços | `for a in *.csv; do ... done` · `while read -r l; do ... done < arq` | 02.07 |
| Capturar saída | `TOTAL=$(wc -l < arquivo)` | 02.07 |
| Erro e saída | `echo "msg" >&2` · `exit 0/1/2` · `$?` | 02.07 |
| Grep que pode não achar | `RES=$(grep ... \|\| true)` — senão o `set -e` encerra | 02.07 |

## Git — ciclo diário

| Operação | Comando | Ref. |
|---|---|---|
| Configurar (uma vez) | `git config --global user.name/user.email` | 02.09 |
| Iniciar | `git init` (com `.gitignore` **antes** do primeiro add) | 02.09 |
| Estado | `git status` · `git status --short` | 02.08 |
| Preparar | `git add arquivo` · `git add -p` (pedaço por pedaço) | 02.09 |
| Comitar | `git commit -m "Verbo no imperativo, ~50 chars"` | 02.09 |
| Três comparações | `git diff` · `git diff --staged` · `git diff HEAD` | 02.09 |
| Histórico | `git log --oneline --graph --all` · `--stat` · `--grep="x"` | 02.09 |
| Ver um commit | `git show a3f7c9e` | 02.09 |
| O que está rastreado | `git ls-files` | 02.09 |

## Git — branches e remotos

| Operação | Comando | Ref. |
|---|---|---|
| Listar / criar e trocar | `git branch` · `git switch -c nome` · `git switch -` | 02.10 |
| Reunir | `git switch main` **e depois** `git merge nome` | 02.10 |
| Apagar etiqueta | `git branch -d nome` (`-D` força) | 02.10 |
| Conflito | editar → **apagar os 3 marcadores** → `add` → `commit` | 02.10 |
| Abortar merge | `git merge --abort` | 02.10 |
| Conectar remoto | `git remote add origin git@github.com:u/p.git` · `git remote -v` | 02.11 |
| Publicar | `git push -u origin main` (depois só `git push`) | 02.11 |
| Baixar sem incorporar | `git fetch origin` · `git log main..origin/main` | 02.11 |
| Baixar e incorporar | `git pull` (= fetch + merge) | 02.11 |
| Chave SSH | `ssh-keygen -t ed25519` · privada em **600** · `ssh -T git@github.com` | 02.11 |

## Git — desfazendo

| Situação | Comando | Ref. |
|---|---|---|
| Descartar alteração não preparada | `git restore arquivo` (**irreversível**) | 02.12 |
| Tirar da área de preparo | `git restore --staged arquivo` | 02.12 |
| Pausar o trabalho | `git stash push -m "desc"` · `git stash pop` | 02.12 |
| Corrigir o último commit local | `git commit --amend -m "..."` · `--amend --no-edit` | 02.12 |
| Desfazer commit **não** publicado | `git reset --soft/--mixed/--hard HEAD~1` | 02.12 |
| Desfazer commit **já** publicado | `git revert <id>` | 02.12 |
| Recuperar o que sumiu | `git reflog` → `git switch -c recuperado <id>` | 02.12 |
| Parar de rastrear (sem apagar) | `git rm --cached arquivo` | 02.12 |

## `.gitignore` de referência

```gitignore
__pycache__/
*.pyc
.venv/
.env
*.key
saidas/
*.log
.DS_Store
Thumbs.db
!.env.example
```

## As três perguntas que resolvem quase tudo

1. **"Onde eu estou?"** → `pwd` · `git status` · `git branch`
2. **"O que exatamente mudou?"** → `git diff` (as três comparações) · `ls -l`
3. **"Já foi publicado?"** → decide entre `reset` (não) e `revert` (sim)
