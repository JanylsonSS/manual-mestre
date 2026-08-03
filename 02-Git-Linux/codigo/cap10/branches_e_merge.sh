#!/usr/bin/env bash
# ------------------------------------------------------------
# branches_e_merge.sh
# Capítulo 02.10 — Branches e merge
# O que este arquivo demonstra: branch como ponteiro, merge por
#   fast-forward, merge com dois pais, e um conflito resolvido
# Como executar: bash branches_e_merge.sh
# ------------------------------------------------------------

set -euo pipefail

PASTA="branches_temporario"
rm -rf "$PASTA"; mkdir "$PASTA"; cd "$PASTA"

git init -q -b main
git config user.name "Estudante Aurora"
git config user.email "estudante@exemplo.local"

echo "--- 1. Dois commits na main ---"
echo "VERSAO = '1.0'" > versao.py
git add . && git commit -q -m "Inicia projeto Aurora"
echo "def total(v): return sum(v)" > analise.py
git add . && git commit -q -m "Cria funcao de total"
git log --oneline

echo
echo "--- 2. Nasce a branch (uma etiqueta, 41 bytes) ---"
git switch -q -c funcionalidade/por-cidade
echo "  Branches existentes:"
git branch | sed 's/^/  /'
echo "  Tamanho do arquivo da branch: \
$(wc -c < .git/refs/heads/funcionalidade/por-cidade) bytes"

echo
echo "--- 3. Dois commits na branch ---"
echo "def por_cidade(v): pass" >> analise.py
git add . && git commit -q -m "Agrupa vendas por cidade"
echo "# ordena por valor" >> analise.py
git add . && git commit -q -m "Ordena relatorio por valor"

echo
echo "--- 4. A main NAO andou (a etiqueta ficou parada) ---"
echo "  Commits na branch: $(git rev-list --count HEAD)"
echo "  Commits na main:   $(git rev-list --count main)"

echo
echo "--- 5. Trocar de branch reescreve os arquivos do disco ---"
git switch -q main
echo "  Conteudo de analise.py na main:"
sed 's/^/    /' analise.py
git switch -q -
echo "  Conteudo de analise.py na branch:"
sed 's/^/    /' analise.py

echo
echo "--- 6. Merge por fast-forward (a main nao andou) ---"
git switch -q main
git merge -q funcionalidade/por-cidade
git branch -d funcionalidade/por-cidade      # a etiqueta some, o historico fica
git log --oneline --graph

echo
echo "--- 7. Provocando um conflito de proposito ---"
git switch -q -c ajuste-versao
echo "VERSAO = '1.1-beta'" > versao.py
git add . && git commit -q -m "Marca versao como beta"

git switch -q main
echo "VERSAO = '2.0'" > versao.py
git add . && git commit -q -m "Promove para versao 2.0"

# O "|| true" é necessário: o merge com conflito devolve código != 0,
# e com "set -e" o script encerraria justamente no ponto de interesse.
git merge ajuste-versao || true

echo
echo "--- 8. O arquivo em conflito, com os marcadores ---"
sed 's/^/    /' versao.py

echo
echo "--- 9. Resolvendo: a decisao combina os dois lados ---"
echo "VERSAO = '2.0-beta'" > versao.py       # apaga os marcadores!
git add versao.py
git commit -q -m "Reune versao 2.0 com a marcacao beta"

echo "  Resultado final:"
sed 's/^/    /' versao.py
echo "  O merge criou um commit com DOIS pais:"
git log -1 --format="    %h  pais: %p"

echo
echo "--- 10. O grafo completo ---"
git log --oneline --graph --all | sed 's/^/  /'

echo
echo "--- 11. Limpeza ---"
cd ..; rm -rf "$PASTA"
echo "Laboratorio removido."
