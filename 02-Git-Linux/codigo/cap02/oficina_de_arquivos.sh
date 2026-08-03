#!/usr/bin/env bash
# ------------------------------------------------------------
# oficina_de_arquivos.sh
# Capítulo 02.02 — Navegação e manipulação de arquivos
# O que este arquivo demonstra: criar, copiar, mover, remover e
#   curingas — num cenário isolado que se limpa ao final
# Como executar: bash oficina_de_arquivos.sh
# ------------------------------------------------------------

set -e   # para na primeira falha (boa prática — o 02.07 explica)

PASTA_TESTE="oficina_temporaria"

echo "--- 1. Criando o cenário ---"
# -p cria a hierarquia inteira e não reclama se já existir (idempotente)
mkdir -p "$PASTA_TESTE/saidas/arquivo"
cd "$PASTA_TESTE"

# touch cria arquivos vazios (ou atualiza a data dos existentes)
touch relatorio_2026-07-28.txt relatorio_2026-07-29.txt relatorio_2026-07-30.txt
touch quarentena_2026-07-28.csv quarentena_2026-07-29.csv
touch rascunho.tmp cache.tmp observacoes.md
ls

echo
echo "--- 2. Investigando ANTES de agir (o hábito que salva) ---"
echo "Relatórios encontrados:"
ls relatorio_*.txt
echo "Tudo do dia 28:"
ls ./*2026-07-28*
echo "Arquivos temporários (candidatos a apagar):"
ls ./*.tmp

echo
echo "--- 3. Organizando com curingas ---"
mv relatorio_*.txt saidas/       # move os 3 de uma vez
mv quarentena_*.csv saidas/
echo "Conteúdo de saidas/:"
ls saidas/

echo
echo "--- 4. Arquivando e limpando ---"
# cp mantém o original; mv o levaria embora
cp saidas/relatorio_2026-07-28.txt saidas/arquivo/
echo "Arquivo histórico:"
ls saidas/arquivo/

# O par LISTAR -> APAGAR (nunca apague sem conferir a lista antes)
echo "Vou apagar estes arquivos:"
ls ./*.tmp
rm ./*.tmp
echo "Após a limpeza:"
ls

echo
echo "--- 5. Estrutura final ---"
ls -R

echo
echo "--- 6. Limpeza do cenário de teste ---"
cd ..
# -r porque é pasta com conteúdo; sem -f para que erros apareçam
rm -r "$PASTA_TESTE"
echo "Pasta temporária removida. Nada ficou para trás."
