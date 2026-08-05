#!/usr/bin/env bash
# ------------------------------------------------------------
# conflito.sh
# Capítulo 04.16 — Ambientes virtuais e pip
# O que este arquivo demonstra: por que dois projetos não cabem
#   num interpretador só. Cria dois ambientes com versões
#   diferentes do Pydantic e roda O MESMO arquivo nos dois.
# Uso: bash codigo/cap16/conflito.sh
# Requer: internet (baixa dois pacotes) e ~60 MB de disco.
# ------------------------------------------------------------

set -euo pipefail

AQUI="$(cd "$(dirname "$0")" && pwd)"
LAB="${TMPDIR:-/tmp}/lab-04-16"
MODELO="$AQUI/modelo.py"

titulo() {
    echo
    echo "=== $1 ==="
}

# --- 1. Ambiente limpo, para o script poder rodar duas vezes ---
rm -rf "$LAB"
mkdir -p "$LAB"

titulo "[1] ONDE O PYTHON PROCURA PACOTES, SEM AMBIENTE"
python3 -c "
import sys
print('   prefix:      ', sys.prefix)
print('   base_prefix: ', sys.base_prefix)
print('   iguais? ', sys.prefix == sys.base_prefix, ' <- fora de um ambiente, sim')
"

# --- 2. Dois ambientes, duas versões ---
titulo "[2] CRIANDO DOIS AMBIENTES"
python3 -m venv "$LAB/projeto-novo"
python3 -m venv "$LAB/projeto-antigo"
echo "   criados. tamanho de um ambiente vazio: $(du -sh "$LAB/projeto-novo" | cut -f1)"

"$LAB/projeto-novo/bin/python" -c "
import sys
print('   dentro -> prefix:', sys.prefix)
print('   dentro -> iguais?', sys.prefix == sys.base_prefix, ' <- agora não')
"

titulo "[3] INSTALANDO VERSÕES INCOMPATÍVEIS"
"$LAB/projeto-novo/bin/pip"   install --quiet "pydantic==2.13.4"
"$LAB/projeto-antigo/bin/pip" install --quiet "pydantic==1.10.13"
echo "   projeto-novo:"
"$LAB/projeto-novo/bin/pip" freeze | sed 's/^/     /'
echo "   projeto-antigo:"
"$LAB/projeto-antigo/bin/pip" freeze | sed 's/^/     /'
echo "   >>> pediu 1 pacote e vieram 5: as dependências das dependências"

titulo "[4] O MESMO ARQUIVO, NOS DOIS AMBIENTES"
echo "   projeto-novo:"
"$LAB/projeto-novo/bin/python" "$MODELO" 2>&1 | tail -3 | sed 's/^/     /'
echo "   projeto-antigo:"
set +e
"$LAB/projeto-antigo/bin/python" "$MODELO" 2>&1 | tail -2 | sed 's/^/     /'
set -e
echo "   >>> mesmo código, mesmo computador, resultados diferentes"

# --- 5. E se os dois estivessem no MESMO ambiente? ---
titulo "[5] OS DOIS NO MESMO AMBIENTE"
python3 -m venv "$LAB/projeto-conflito"
"$LAB/projeto-conflito/bin/pip" install --quiet "pydantic==2.13.4"
echo "   instalando a versão 1 por cima da 2..."
"$LAB/projeto-conflito/bin/pip" install --quiet "pydantic==1.10.13"
"$LAB/projeto-conflito/bin/pip" freeze | sed 's/^/     /'
echo "   >>> pydantic caiu para 1.10.13 SEM erro — e pydantic_core 2.x"
echo "       ficou órfão, sem nada que o use"
echo "   pip check diz:"
"$LAB/projeto-conflito/bin/pip" check | sed 's/^/     /'
echo "   >>> 'nenhum problema' — o pip confere declarações, não uso"

titulo "[6] O AMBIENTE NÃO É PORTÁTIL"
echo "   a primeira linha do executável do pip:"
head -1 "$LAB/projeto-novo/bin/pip" | sed 's/^/     /'
mv "$LAB/projeto-novo" "$LAB/renomeado"
echo "   depois de renomear a pasta:"
set +e
"$LAB/renomeado/bin/pip" --version 2>&1 | tail -1 | sed 's/^/     /'
set -e
echo "   mas o interpretador continua achando os pacotes:"
"$LAB/renomeado/bin/python" -c "
import pydantic
print('     import ok:', pydantic.VERSION)
"
echo "   >>> o python descobre o prefixo pelo próprio caminho;"
echo "       os scripts têm o caminho gravado na primeira linha"

echo
echo "Laboratório em: $LAB"
echo "Para remover:   rm -rf $LAB"
