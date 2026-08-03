#!/usr/bin/env bash
# ------------------------------------------------------------
# verificar_manual.sh
# Capítulo 02.07 — Scripts de shell
# O que este arquivo demonstra: validação de argumentos, funções,
#   laços, condicionais e código de saída num script útil de verdade
# Uso: ./verificar_manual.sh <pasta-do-modulo>
# ------------------------------------------------------------

set -euo pipefail

# --- 1. Validação de argumentos (antes de qualquer processamento) ---
if [ "$#" -lt 1 ]; then
    echo "Uso: $0 <pasta-do-modulo>" >&2
    echo "Exemplo: $0 02-Git-Linux" >&2
    exit 2
fi

PASTA="$1"

if [ ! -d "$PASTA" ]; then
    echo "Erro: '$PASTA' não é uma pasta existente." >&2
    exit 1
fi

# --- 2. Funções auxiliares ---
registrar() {
    echo "[$(date '+%H:%M:%S')] $1"
}

# Conta capítulos (arquivos NN-nome.md, exceto o 00-visao)
contar_capitulos() {
    find "$1" -maxdepth 1 -name "[0-9][0-9]-*.md" \
        -not -name "00-visao*" | wc -l
}

# --- 3. Coleta de dados ---
registrar "Auditando: $PASTA"
echo

CAPITULOS=$(contar_capitulos "$PASTA")
EXERCICIOS=$(find "$PASTA/exercicios" -maxdepth 1 -name "cap*.md" 2>/dev/null | wc -l)
GABARITOS=$(find "$PASTA/exercicios/gabaritos" -name "cap*.md" 2>/dev/null | wc -l)
SCRIPTS=$(find "$PASTA/codigo" -name "*.sh" 2>/dev/null | wc -l)

echo "  Capítulos:  $CAPITULOS"
echo "  Exercícios: $EXERCICIOS"
echo "  Gabaritos:  $GABARITOS"
echo "  Scripts:    $SCRIPTS"
echo

# --- 4. Verificações (cada uma pode registrar um problema) ---
PROBLEMAS=0

registrar "Verificando pares capítulo/exercício..."
if [ "$CAPITULOS" -ne "$EXERCICIOS" ]; then
    echo "  ! $CAPITULOS capítulos para $EXERCICIOS exercícios" >&2
    PROBLEMAS=$((PROBLEMAS + 1))
else
    echo "  OK: todo capítulo tem exercício"
fi

if [ "$EXERCICIOS" -ne "$GABARITOS" ]; then
    echo "  ! $EXERCICIOS exercícios para $GABARITOS gabaritos" >&2
    PROBLEMAS=$((PROBLEMAS + 1))
else
    echo "  OK: todo exercício tem gabarito"
fi

registrar "Verificando shebang e permissão dos scripts..."
for script in $(find "$PASTA/codigo" -name "*.sh" 2>/dev/null); do
    if ! head -1 "$script" | grep -q "^#!"; then
        echo "  ! sem shebang: $script" >&2
        PROBLEMAS=$((PROBLEMAS + 1))
    fi
done
echo "  OK: shebangs conferidos"

registrar "Procurando pendências deixadas no texto..."
# O ":" evita casar com a palavra portuguesa TODO/TODOS.
# O "|| true" é obrigatório: grep sem resultado devolve 1 e, com
# "set -e" + pipefail, encerraria o script justamente quando está tudo certo.
PENDENCIAS=$(grep -rEo "(TODO|FIXME|XXX):" "$PASTA"/*.md 2>/dev/null | wc -l || true)
if [ "$PENDENCIAS" -gt 0 ]; then
    echo "  ! $PENDENCIAS marcação(ões) de pendência esquecida(s)" >&2
    PROBLEMAS=$((PROBLEMAS + 1))
else
    echo "  OK: nenhuma pendência esquecida"
fi

# --- 5. Conclusão e código de saída ---
echo
if [ "$PROBLEMAS" -eq 0 ]; then
    registrar "Auditoria concluída: nenhum problema."
    exit 0
else
    registrar "Auditoria concluída: $PROBLEMAS problema(s)."
    exit 1        # código != 0 permite usar em automação (módulo 09)
fi
