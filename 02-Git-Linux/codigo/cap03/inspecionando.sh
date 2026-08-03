#!/usr/bin/env bash
# ------------------------------------------------------------
# inspecionando.sh
# Capítulo 02.03 — Inspecionando arquivos
# O que este arquivo demonstra: wc, head, tail e cat aplicados a
#   um CSV de vendas — o instrumental de diagnóstico
# Como executar: bash inspecionando.sh
# ------------------------------------------------------------

set -e

PASTA="inspecao_temporaria"
ARQUIVO="$PASTA/vendas.csv"

echo "--- 1. Criando um CSV de teste (cabeçalho + 12 registros) ---"
mkdir -p "$PASTA"
{
  echo "codigo;produto;valor_centavos;cidade"
  echo "PED-001;Fone Bluetooth;46990;Campinas"
  echo "PED-002;Mouse Sem Fio;8990; santos"
  echo "PED-003;Teclado Mecanico;34900;CAMPINAS"
  echo "PED-004;Cabo HDMI;9890;Sorocaba"
  echo "PED-005;Webcam HD;47890;campinas"
  echo "PED-006;Headset Gamer;34900;Sao Paulo"
  echo "PED-007;Monitor 24;129900;Santos"
  echo "PED-008;Suporte de Mesa;12990;Santos"
  echo "PED-009;Hub USB-C;15990;sao paulo"
  echo "PED-010;Mousepad Grande;4990;Campinas"
  echo "PED-011;Luminaria LED;23900;Santos"
  echo "PED-012;Filtro de Linha;3990;Campinas"
} > "$ARQUIVO"          # o > redireciona a saída para o arquivo (02.04)

echo
echo "--- 2. MEDIR: quantas linhas? (wc) ---"
wc -l "$ARQUIVO"
# Atenção: conta o CABEÇALHO também — registros = linhas - 1

echo
echo "--- 3. ESPIAR O COMEÇO: qual o formato? (head) ---"
head -3 "$ARQUIVO"
# Em 3 linhas: separador, colunas e um exemplo de registro
# (repare o espaço antes de 'santos' — sujeira detectada sem abrir editor)

echo
echo "--- 4. ESPIAR O FIM: o arquivo está completo? (tail) ---"
tail -2 "$ARQUIVO"
# Última linha completa = arquivo não truncado

echo
echo "--- 5. PULAR O CABEÇALHO: só os dados (tail -n +2) ---"
tail -n +2 "$ARQUIVO" | head -3
# Da linha 2 em diante, mostrando só as 3 primeiras (o | é do 02.04)

echo
echo "--- 6. DESPEJAR: arquivo pequeno cabe no cat ---"
cat "$ARQUIVO"

echo
echo "--- 7. Contagens úteis para um relatório ---"
echo "Linhas físicas: $(wc -l < "$ARQUIVO")"
echo "Registros de dados: $(( $(wc -l < "$ARQUIVO") - 1 ))"
echo "Palavras: $(wc -w < "$ARQUIVO")"
echo "Bytes: $(wc -c < "$ARQUIVO")"

echo
echo "--- 8. Limpeza ---"
rm -r "$PASTA"
echo "Cenário removido."
