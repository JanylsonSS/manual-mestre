#!/usr/bin/env bash
# ------------------------------------------------------------
# ciclo_do_git.sh
# Capítulo 02.08 — Git: o modelo mental
# O que este arquivo demonstra: os quatro estados de um arquivo e
#   o caminho entre as três áreas, com git status em cada etapa
# Como executar: bash ciclo_do_git.sh
# ------------------------------------------------------------

set -euo pipefail

PASTA="laboratorio_git_temporario"
rm -rf "$PASTA"
mkdir "$PASTA"
cd "$PASTA"

echo "--- 1. Criando o repositório ---"
git init -q
# Identidade local, só para este repositório (o -q silencia a saída):
git config user.name "Estudante Aurora"
git config user.email "estudante@exemplo.local"
echo "  Pasta .git criada. Conteúdo:"
ls .git | head -5

echo
echo "--- 2. Estado: NÃO RASTREADO ---"
echo "cidade;valor" > vendas.csv
echo "campinas;100.00" >> vendas.csv
git status --short          # o --short resume: ?? = não rastreado

echo
echo "--- 3. Estado: PREPARADO (depois do add) ---"
git add vendas.csv
git status --short          # A = acrescentado à área de preparo

echo
echo "--- 4. Estado: VERSIONADO (depois do commit) ---"
git commit -q -m "Cria base de vendas com a primeira cidade"
git status --short          # nada: o diretório está limpo
echo "  (saída vazia acima = tudo versionado)"

echo
echo "--- 5. Estado: MODIFICADO (editei um arquivo versionado) ---"
echo "sorocaba;200.00" >> vendas.csv
git status --short          # M = modificado, mas ainda não preparado

echo
echo "--- 6. A área de preparo escolhendo o que entra na foto ---"
echo "# Laboratório Aurora" > README.md    # segundo arquivo, novo
git add vendas.csv                          # preparo SÓ o primeiro
git status --short                          # M preparado + ?? não rastreado
git commit -q -m "Registra a venda de sorocaba"

echo
echo "--- 7. O histórico: o grafo de commits ---"
git log --oneline
echo
echo "  Detalhe do commit mais recente:"
git log -1 --format="  id:    %h%n  autor: %an%n  data:  %ad%n  msg:   %s" --date=short

echo
echo "--- 8. O que o Git guardou por dentro ---"
echo "  Objetos no banco: $(git count-objects | cut -d' ' -f1)"
echo "  Onde o HEAD aponta: $(cat .git/HEAD)"

echo
echo "--- 9. Limpeza ---"
cd ..
rm -rf "$PASTA"
echo "Laboratório removido."
