#!/usr/bin/env bash
# ------------------------------------------------------------
# ambiente_e_path.sh
# Capítulo 02.06 — Variáveis de ambiente e PATH
# O que este arquivo demonstra: leitura e criação de variáveis,
#   export e herança, o PATH aberto e o padrão de configuração
# Como executar: bash ambiente_e_path.sh
# ------------------------------------------------------------

set -e

PASTA="ambiente_temporario"

echo "--- 1. Lendo variáveis do ambiente ---"
echo "  Usuário: $USER"
echo "  Casa (HOME): $HOME"
echo "  Pasta atual (PWD): $PWD"
echo "  Shell: $SHELL"

echo
echo "--- 2. O PATH, uma pasta por linha ---"
echo "$PATH" | tr ':' '\n' | head -6
echo "  (total de pastas no PATH: $(echo "$PATH" | tr ':' '\n' | wc -l))"

echo
echo "--- 3. Onde estão os programas que eu uso? ---"
echo "  bash:    $(which bash)"
echo "  python3: $(which python3 2>/dev/null || echo 'não encontrado')"
echo "  ls:      $(which ls)"

echo
echo "--- 4. Variável de SHELL x variável de AMBIENTE ---"
EMPRESA="Aurora"                 # variável do shell: só este processo vê
echo "  No shell atual: $EMPRESA"
# O processo filho NÃO herda (a variável não foi exportada):
bash -c 'echo "  No processo filho (sem export): [$EMPRESA]"'

export EMPRESA                   # agora vai para o "quadro de avisos" herdado
bash -c 'echo "  No processo filho (com export): [$EMPRESA]"'

echo
echo "--- 5. Aspas: duplas expandem, simples não ---"
echo "  Duplas: Trabalho na $EMPRESA"
echo '  Simples: Trabalho na $EMPRESA'

echo
echo "--- 6. Instalando um comando próprio no PATH ---"
mkdir -p "$PASTA/bin"
cat > "$PASTA/bin/ola-aurora" << 'FIM'
#!/usr/bin/env bash
echo "  Olá! Sou um comando de verdade, encontrado pelo PATH."
FIM
chmod +x "$PASTA/bin/ola-aurora"

echo "  Antes de alterar o PATH:"
ola-aurora 2>/dev/null || echo "    command not found (esperado)"

# Acrescenta a pasta ao PATH — repare no $PATH ao final (NUNCA esqueça!)
export PATH="$PWD/$PASTA/bin:$PATH"
echo "  Depois de acrescentar ao PATH:"
ola-aurora
echo "  Encontrado em: $(which ola-aurora)"

echo
echo "--- 7. O padrão de configuração (antecipando o módulo 06) ---"
export AURORA_AMBIENTE="desenvolvimento"
export AURORA_CIDADE_SEDE="campinas"

# O programa lê a configuração do AMBIENTE, com valor padrão se faltar:
python3 - << 'FIM'
import os
ambiente = os.environ.get("AURORA_AMBIENTE", "não definido")
sede = os.environ.get("AURORA_CIDADE_SEDE", "não definida")
banco = os.environ.get("DATABASE_URL", "sqlite local (padrão de desenvolvimento)")
print(f"  Ambiente: {ambiente}")
print(f"  Cidade sede: {sede}")
print(f"  Banco: {banco}")
print("  (o banco não foi definido — o programa usou o padrão, sem quebrar)")
FIM

echo
echo "--- 8. Limpeza ---"
rm -r "$PASTA"
echo "Cenário removido. (O PATH volta ao normal quando este shell terminar.)"
