#!/usr/bin/env bash
# ------------------------------------------------------------
# primeiros_comandos.sh
# Capítulo 02.01 — Terminal: por que a linha de comando
# O que este arquivo demonstra: o repertório mínimo de orientação
#   no terminal, com a saída esperada comentada
# Como executar: bash primeiros_comandos.sh
#   (ou copie cada linha para o terminal, uma a uma — recomendado)
# ------------------------------------------------------------

# 1. ONDE ESTOU? (print working directory)
pwd
# Saída: o caminho completo da pasta atual

# 2. O QUE TEM AQUI? (list)
ls
# Saída: nomes de arquivos e pastas, em colunas

# 3. COM DETALHES: -l (longo), -h (tamanhos legíveis), -a (ocultos)
ls -lha
# Saída: uma linha por item — permissões, dono, tamanho, data, nome
# O 'd' inicial marca diretórios; nomes com ponto são ocultos (.git!)

# 4. QUEM SOU EU E ONDE ESTOU RODANDO?
whoami
# Saída: seu nome de usuário no sistema

echo "Shell em uso: $SHELL"
# Saída: o caminho do shell (ex.: /bin/bash) — a variável do 02.06

# 5. QUE DIA É HOJE? (útil em scripts de automação — 02.07)
date
# Saída: data e hora do sistema

# 6. O MANUAL ESTÁ NO PRÓPRIO TERMINAL
# ls --help | head -5    # descomente para ver as primeiras linhas da ajuda
# man ls                 # manual completo (Linux/macOS) — saia com 'q'

# 7. HISTÓRICO: o que já digitei?
history | tail -5
# Saída: os 5 comandos mais recentes (o | e o tail chegam no 02.03/02.04)

echo "--- Caderno concluído. Agora repita cada comando à mão, usando Tab. ---"
