#!/usr/bin/env bash
# ------------------------------------------------------------
# remoto_local.sh
# Capítulo 02.11 — Remotos e GitHub
# O que este arquivo demonstra: clone, push, fetch, pull e a
#   recusa de push, usando um repositório "bare" como servidor
# Como executar: bash remoto_local.sh
# ------------------------------------------------------------

set -euo pipefail

BASE="remoto_temporario"
rm -rf "$BASE"; mkdir "$BASE"; cd "$BASE"
RAIZ="$PWD"

identificar() {                      # a identidade em cada cópia
    git config user.name "Estudante Aurora"
    git config user.email "estudante@exemplo.local"
}

echo "--- 1. O 'servidor': um repositório bare (sem pasta de trabalho) ---"
git init -q --bare -b main servidor.git       # -b main: mesma linha principal
echo "  Criado: servidor.git (é o que o GitHub hospeda por baixo)"

echo
echo "--- 2. Máquina A: repositório local e primeiro push ---"
mkdir maquina-a && cd maquina-a
git init -q -b main; identificar
echo "# Aurora" > README.md
git add . && git commit -q -m "Cria README do projeto"
git remote add origin "$RAIZ/servidor.git"
git push -q -u origin main
echo "  Enviado. Remotos configurados:"
git remote -v | sed 's/^/    /'

echo
echo "--- 3. Máquina B: clone (o histórico completo vem junto) ---"
cd "$RAIZ"
git clone -q servidor.git maquina-b
cd maquina-b; identificar
echo "  Commits recebidos: $(git rev-list --count HEAD)"
echo "  Remoto já configurado: $(git remote get-url origin | xargs basename)"

echo
echo "--- 4. Máquina B trabalha e envia ---"
echo "vendas = []" > analise.py
git add . && git commit -q -m "Cria estrutura de analise"
git push -q origin main
echo "  Máquina B enviou 1 commit."

echo
echo "--- 5. Máquina A tenta enviar SEM sincronizar → recusado ---"
cd "$RAIZ/maquina-a"
echo "config = {}" > config.py
git add . && git commit -q -m "Cria arquivo de configuracao"
# O "|| true" mantém o script vivo: o push recusado devolve código != 0
git push origin main 2>&1 | grep -E "rejected|fetch first" | sed 's/^/    /' || true
echo "    (o Git protegeu o commit da outra máquina)"

echo
echo "--- 6. O caminho correto: fetch, olhar, merge ---"
git fetch -q origin
echo "  O que existe no remoto e não aqui:"
git log --oneline main..origin/main | sed 's/^/    /'
git merge -q origin/main -m "Reune trabalho da maquina B"
echo "  Depois do merge, commits locais: $(git rev-list --count HEAD)"

echo
echo "--- 7. Agora o push é aceito ---"
git push -q origin main
echo "  Enviado com sucesso."

echo
echo "--- 8. Máquina B se atualiza com pull (fetch + merge) ---"
cd "$RAIZ/maquina-b"
git pull -q origin main
echo "  Arquivos na máquina B agora:"
ls | sed 's/^/    /'
echo "  Histórico conciliado:"
git log --oneline --graph | sed 's/^/    /'

echo
echo "--- 9. Limpeza ---"
cd "$RAIZ/.."; rm -rf "$BASE"
echo "Laboratório removido."
