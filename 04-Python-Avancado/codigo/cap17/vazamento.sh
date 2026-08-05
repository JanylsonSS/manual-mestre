#!/usr/bin/env bash
# ------------------------------------------------------------
# vazamento.sh
# Capítulo 04.17 — Organização de projetos
# O que este arquivo demonstra: por que o layout plano deixa passar
#   um defeito de empacotamento. Monta um projeto que funciona na
#   máquina de quem escreveu e quebra na de quem instala.
# Uso: bash codigo/cap17/vazamento.sh
# Requer: ~40 MB de disco. Não usa rede.
# ------------------------------------------------------------

set -euo pipefail

LAB="${TMPDIR:-/tmp}/lab-04-17"
rm -rf "$LAB"
mkdir -p "$LAB/plano/aurora"

titulo() { echo; echo "=== $1 ==="; }

# --- 1. Um projeto de layout plano, com um vazamento plantado ---
cd "$LAB/plano"

cat > utilitarios.py <<'PY'
def normalizar(texto):
    return " ".join(texto.split()).title()
PY

cat > aurora/__init__.py <<'PY'
from aurora.modelo import Produto
PY

cat > aurora/modelo.py <<'PY'
from dataclasses import dataclass
from utilitarios import normalizar        # <- MÓDULO DE FORA DO PACOTE

@dataclass(frozen=True)
class Produto:
    nome: str
    preco_centavos: int

    def __post_init__(self):
        object.__setattr__(self, "nome", normalizar(self.nome))
PY

cat > pyproject.toml <<'TOML'
[project]
name = "aurora-plano"
version = "0.1.0"
requires-python = ">=3.10"

[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
include = ["aurora*"]
TOML

titulo "[1] ESTRUTURA (layout plano)"
echo "   plano/"
echo "   ├── aurora/            <- o pacote"
echo "   │   ├── __init__.py"
echo "   │   └── modelo.py      <- faz 'from utilitarios import normalizar'"
echo "   ├── utilitarios.py     <- FORA do pacote"
echo "   └── pyproject.toml"

titulo "[2] NA MÁQUINA DE QUEM ESCREVEU"
python3 -c "
import aurora
print('   ', aurora.Produto('  mouse  gamer ', 8990))
print('    passou — a pasta atual está no sys.path (04.17 §6.2)')
"

titulo "[3] NA MÁQUINA DE QUEM INSTALA"
python3 -m venv "$LAB/cliente" >/dev/null
"$LAB/cliente/bin/pip" install --quiet --no-build-isolation . 2>/dev/null \
    || "$LAB/cliente/bin/pip" install --quiet .
cd "$LAB"
set +e
"$LAB/cliente/bin/python" -c "import aurora" 2>&1 | tail -2 | sed 's/^/    /'
set -e
echo "    >>> mesmo pacote, mesma versão, e não funciona"

titulo "[4] O QUE FOI DE FATO EMPACOTADO"
find "$LAB/cliente/lib" -path "*site-packages/aurora*" -name "*.py" \
    | sed "s|.*site-packages/|    |"
echo "    >>> utilitarios.py não está aqui: ele nunca fez parte do pacote"

titulo "[5] O MESMO DEFEITO, COM LAYOUT src/"
mkdir -p "$LAB/src-projeto/src/aurora"
cd "$LAB/src-projeto"
cp "$LAB/plano/utilitarios.py" .
cp "$LAB/plano/aurora/__init__.py" "$LAB/plano/aurora/modelo.py" src/aurora/
sed 's/aurora-plano/aurora-src/; s|include = \["aurora\*"\]|where = ["src"]|' \
    "$LAB/plano/pyproject.toml" > pyproject.toml
echo "   estrutura: src/aurora/ (pacote) e utilitarios.py na raiz"
set +e
python3 -c "import aurora" 2>&1 | tail -1 | sed 's/^/    /'
set -e
echo '    >>> com src/, `import aurora` não funciona ANTES de instalar.'
echo "        Você é obrigado a instalar — e a instalação é o mesmo"
echo "        caminho que o cliente vai usar."

titulo "[6] O LIMITE HONESTO DO LAYOUT src/"
python3 -m venv "$LAB/dev" >/dev/null
"$LAB/dev/bin/pip" install --quiet -e . 2>/dev/null || true
echo "   depois de 'pip install -e .', rodando DA pasta do projeto:"
set +e
MSG="import aurora; print('    passou — a pasta atual ainda está no path')"
"$LAB/dev/bin/python" -c "$MSG" 2>&1 | tail -1 | sed 's/^/    /'
echo "   e rodando de QUALQUER OUTRA pasta:"
cd "$LAB"
"$LAB/dev/bin/python" -c "import aurora" 2>&1 | tail -1 | sed 's/^/    /'
set -e
echo "    >>> src/ garante que o PACOTE venha da instalação."
echo "        A pasta atual continua no sys.path, então um módulo solto"
echo "        na raiz ainda pode vazar. O teste que pega é rodar de fora."

echo
echo "Laboratório em: $LAB"
echo "Para remover:   rm -rf $LAB"
