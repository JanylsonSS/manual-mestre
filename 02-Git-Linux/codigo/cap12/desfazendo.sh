#!/usr/bin/env bash
# ------------------------------------------------------------
# desfazendo.sh
# Capítulo 02.12 — Desfazendo
# O que este arquivo demonstra: restore, stash, amend, os três
#   modos de reset, revert e a recuperação pelo reflog
# Como executar: bash desfazendo.sh
# ------------------------------------------------------------

set -euo pipefail

PASTA="desfazendo_temporario"
rm -rf "$PASTA"; mkdir "$PASTA"; cd "$PASTA"

git init -q -b main
git config user.name "Estudante Aurora"
git config user.email "estudante@exemplo.local"

echo "VERSAO = '1.0'" > config.py
echo "def total(v): return sum(v)" > analise.py
git add . && git commit -q -m "Inicia projeto Aurora"

echo "--- 1. restore: descartando alteracao nao preparada ---"
echo "VERSAO = 'ERRADO'" > config.py
echo "  Antes:  $(cat config.py)"
git restore config.py                    # descarta (irreversivel!)
echo "  Depois: $(cat config.py)"

echo
echo "--- 2. restore --staged: tirando da area de preparo ---"
echo "SENHA=123" > .env
git add .env
echo "  Preparados: $(git diff --staged --name-only | tr '\n' ' ')"
git restore --staged .env                # sai da mesa, fica no disco
echo "  Depois do restore --staged: $(git status --short | tr '\n' ' ')"
echo ".env" > .gitignore                 # e resolve de vez
git add .gitignore && git commit -q -m "Ignora arquivo de segredos"

echo
echo "--- 3. commit --amend: corrigindo a ultima mensagem ---"
echo "# nota" >> analise.py
git add . && git commit -q -m "correcoes"
echo "  Mensagem ruim: $(git log -1 --format=%s)"
git commit -q --amend -m "Documenta a funcao de total"
echo "  Corrigida:     $(git log -1 --format=%s)"

echo
echo "--- 4. stash: pausando o trabalho para uma urgencia ---"
echo "def por_cidade(v): pass  # incompleto" >> analise.py
git stash push -q -m "meio da refatoracao"
echo "  Diretorio limpo? [$(git status --short)]"
echo "  Guardado: $(git stash list | head -1)"
echo "URGENTE = True" >> config.py
git add . && git commit -q -m "Corrige urgencia em producao"
git stash pop -q
echo "  Trabalho de volta: $(git status --short | tr '\n' ' ')"
git add . && git commit -q -m "Esboca agrupamento por cidade"

echo
echo "--- 5. reset --soft: refazendo o ultimo commit (nao publicado) ---"
git log --oneline | head -3 | sed 's/^/    /'
echo "  reset --soft HEAD~1 (desfaz o commit, mantem preparado):"
git reset -q --soft HEAD~1
git status --short | sed 's/^/    /'
git commit -q -m "Esboca agrupamento por cidade (refeito)"

echo
echo "--- 6. revert: desfazendo um commit JA publicado ---"
ALVO=$(git log --oneline --format="%h %s" | grep "urgencia" | cut -d' ' -f1)
echo "  Anulando o commit: $ALVO"
git revert --no-edit "$ALVO" > /dev/null
echo "  Os DOIS commits aparecem na historia:"
git log --oneline -2 | sed 's/^/    /'
echo "  URGENTE ainda existe no arquivo? \
$(grep -c URGENTE config.py || true) ocorrencia(s)"

echo
echo "--- 7. reflog: recuperando o que 'sumiu' ---"
ANTES=$(git rev-parse --short HEAD)
git reset -q --hard HEAD~3                # apaga 3 commits da historia
echo "  Depois do reset --hard, commits: $(git rev-list --count HEAD)"
echo "  O reflog guarda o rastro:"
git reflog -3 | sed 's/^/    /'
git reset -q --hard "$ANTES"              # de volta ao ponto anterior
echo "  Recuperado. Commits: $(git rev-list --count HEAD)"

echo
echo "--- 8. Limpeza ---"
cd ..; rm -rf "$PASTA"
echo "Laboratorio removido."
