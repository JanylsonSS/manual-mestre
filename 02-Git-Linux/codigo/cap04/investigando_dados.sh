#!/usr/bin/env bash
# ------------------------------------------------------------
# investigando_dados.sh
# Capítulo 02.04 — Pipes, redirecionamento e busca
# O que este arquivo demonstra: pipes, redirecionamento, grep e
#   find respondendo perguntas reais sobre um CSV
# Como executar: bash investigando_dados.sh
# ------------------------------------------------------------

set -e

PASTA="investigacao_temporaria"
CSV="$PASTA/vendas.csv"
LOG="$PASTA/app.log"

echo "--- 1. Criando o cenário ---"
mkdir -p "$PASTA"
{
  echo "codigo;produto;valor_centavos;cidade"
  echo "PED-001;Fone Bluetooth;46990;Campinas"
  echo "PED-002;Mouse Sem Fio;8990; santos"
  echo "PED-003;Teclado Mecanico;34900;CAMPINAS"
  echo "PED-004;Cabo HDMI;9890;Sorocaba"
  echo "PED-005;Webcam HD;47890;campinas"
  echo "PED-006;Headset Gamer;34900;Santos"
  echo "PED-007;Monitor 24;129900;Santos"
  echo "PED-008;Mousepad;4990;Campinas"
} > "$CSV"

{
  echo "2026-07-31 03:00:01 INFO iniciando importacao"
  echo "2026-07-31 03:00:02 INFO 8 linhas lidas"
  echo "2026-07-31 03:00:03 ERROR linha 4: valor invalido"
  echo "2026-07-31 03:00:03 WARN cidade vazia na linha 7"
  echo "2026-07-31 03:00:04 ERROR linha 6: cidade nao atendida"
  echo "2026-07-31 03:00:05 INFO importacao concluida"
} > "$LOG"

echo
echo "--- 2. GREP: buscar dentro (com -i, -n, -c, -v) ---"
echo "Vendas de Campinas (ignorando maiusculas):"
grep -ic "campinas" "$CSV"

echo "Com numero de linha:"
grep -in "campinas" "$CSV"

echo "Linhas que NAO sao de Campinas (-v), sem o cabecalho:"
tail -n +2 "$CSV" | grep -vi "campinas" | wc -l

echo
echo "--- 3. PIPES: a esteira de estacoes ---"
echo "Quantas vendas por cidade (o 'group by' do terminal):"
# pula cabeçalho -> recorta col 4 -> remove espaços -> minúsculas -> ordena -> conta -> ordena por número
tail -n +2 "$CSV" | cut -d';' -f4 | tr -d ' ' | tr 'A-Z' 'a-z' | sort | uniq -c | sort -rn

echo
echo "--- 4. REDIRECIONAMENTO: > (sobrescreve) e >> (acrescenta) ---"
grep -i "campinas" "$CSV" > "$PASTA/campinas.csv"
echo "Linhas gravadas em campinas.csv: $(wc -l < "$PASTA/campinas.csv")"

echo "-- acrescentando ao mesmo arquivo com >> --"
grep -i "santos" "$CSV" >> "$PASTA/campinas.csv"
echo "Agora com Santos junto: $(wc -l < "$PASTA/campinas.csv")"

echo
echo "--- 5. STDOUT x STDERR: os dois canais ---"
# O erro aparece na TELA mesmo com > desviando o stdout:
ls arquivo_que_nao_existe > "$PASTA/saida.txt" 2> "$PASTA/erros.txt" || true
echo "Conteudo de saida.txt (stdout): $(wc -c < "$PASTA/saida.txt") bytes (vazio!)"
echo "Conteudo de erros.txt (stderr):"
cat "$PASTA/erros.txt"

echo
echo "--- 6. Analisando o log (o caso real de producao) ---"
echo "Quantos ERROR:"
grep -c "ERROR" "$LOG"
echo "Quais foram:"
grep "ERROR" "$LOG"
echo "Resumo por nivel:"
cut -d' ' -f3 "$LOG" | sort | uniq -c | sort -rn

echo
echo "--- 7. FIND: localizar arquivos ---"
echo "Arquivos .csv a partir daqui:"
find "$PASTA" -name "*.csv"
echo "Arquivos modificados (todos, com tipo arquivo):"
find "$PASTA" -type f | sort

echo
echo "--- 8. Limpeza ---"
rm -r "$PASTA"
echo "Cenario removido."
