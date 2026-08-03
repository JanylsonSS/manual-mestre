#!/usr/bin/env bash
# ------------------------------------------------------------
# fluxo_diario.sh
# Capítulo 02.09 — Fluxo essencial do Git
# O que este arquivo demonstra: .gitignore, o ciclo status/diff/
#   add/commit/log e as três comparações possíveis do diff
# Como executar: bash fluxo_diario.sh
# ------------------------------------------------------------

set -euo pipefail

PASTA="fluxo_temporario"
rm -rf "$PASTA"; mkdir "$PASTA"; cd "$PASTA"

echo "--- 1. .gitignore ANTES de tudo ---"
cat > .gitignore << 'FIM'
__pycache__/
*.log
.env
!.env.example
FIM
echo "  .gitignore criado com 4 regras"

git init -q
git config user.name "Estudante Aurora"
git config user.email "estudante@exemplo.local"

echo
echo "--- 2. Criando arquivos: dois versionáveis, dois que devem sumir ---"
echo "total = 0" > analise.py
echo "AURORA_TOP=5" > .env.example         # versionável (a exceção com !)
echo "SENHA=secreta123" > .env             # NUNCA versionar
mkdir -p __pycache__ && touch __pycache__/analise.cpython-312.pyc
echo "erro na linha 3" > sistema.log
git status --short                          # .env e .log NÃO aparecem

echo
echo "--- 3. Primeiro commit ---"
git add .
git commit -q -m "Inicia projeto de análise da Aurora"
git log --oneline

echo
echo "--- 4. As três comparações do diff ---"
echo "total = sum(valores)" > analise.py    # altera o arquivo versionado

echo "  (a) git diff — trabalho x preparo (o que ainda NAO preparei):"
git diff --stat

git add analise.py
echo "  (b) git diff — depois do add (vazio: nada fora da mesa):"
git diff --stat
echo "      [vazio, como esperado]"

echo "  (c) git diff --staged — o que VAI no commit:"
git diff --staged --stat

echo
echo "--- 5. Fotografando com uma mensagem que serve ao futuro ---"
git commit -q -m "Calcula total somando a lista de valores"

echo
echo "--- 6. O histórico como documento consultável ---"
echo "  Últimos commits:"
git log --oneline
echo "  Buscando pela mensagem (--grep 'total'):"
git log --oneline --grep="total"
echo "  Arquivos tocados pelo último commit:"
git log -1 --stat --format="  %h %s"

echo
echo "--- 7. A prova de que o .gitignore funcionou ---"
echo "  Arquivos rastreados pelo Git:"
git ls-files | sed 's/^/    /'
echo "  (.env, .log e __pycache__ ficaram de fora — como planejado)"

echo
echo "--- 8. Limpeza ---"
cd ..; rm -rf "$PASTA"
echo "Laboratório removido."
