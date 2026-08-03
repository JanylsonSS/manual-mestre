#!/usr/bin/env bash
# ------------------------------------------------------------
# permissoes_e_processos.sh
# Capítulo 02.05 — Permissões e processos
# O que este arquivo demonstra: leitura de permissões, chmod,
#   shebang, e o ciclo listar/encerrar processos
# Como executar: bash permissoes_e_processos.sh
# ------------------------------------------------------------

set -e

PASTA="permissoes_temporaria"

echo "--- 1. Criando o cenário ---"
mkdir -p "$PASTA"
cd "$PASTA"

# Um script COM shebang, mas sem permissão de execução ainda
cat > ola.sh << 'FIM'
#!/usr/bin/env bash
echo "  (saída do script) Olá do meu comando!"
FIM

echo "Permissões recém-criadas:"
ls -l ola.sh
# Repare: -rw-r--r-- (644) — nenhum 'x' em lugar nenhum

echo
echo "--- 2. Tentando executar SEM permissão ---"
# O || true evita que o 'set -e' interrompa o script na falha esperada
./ola.sh 2>/dev/null || echo "  -> Permission denied (esperado!)"

echo
echo "--- 3. Dando a permissão (chmod) e executando ---"
chmod +x ola.sh
echo "Depois do chmod +x:"
ls -l ola.sh          # agora -rwxr-xr-x (755)
./ola.sh              # e agora executa

echo
echo "--- 4. As duas notações do chmod ---"
touch arquivo_comum.txt segredo.env
chmod 644 arquivo_comum.txt     # dono rw- · grupo r-- · outros r--
chmod 600 segredo.env           # dono rw- · mais ninguém (segredos!)
ls -l arquivo_comum.txt segredo.env
echo "  644 = arquivo comum · 755 = script/pasta · 600 = segredo"

echo
echo "--- 5. Um script Python vira comando ---"
cat > saudacao.py << 'FIM'
#!/usr/bin/env python3
print("  (saída do Python) Rodei sem digitar 'python' na frente!")
FIM
chmod +x saudacao.py
./saudacao.py

echo
echo "--- 6. Processos: quem está rodando ---"
echo "  PID deste script: $$"
echo "Total de processos no sistema:"
ps aux | tail -n +2 | wc -l      # tail -n +2 pula o cabeçalho (02.03!)

echo
echo "--- 7. Ciclo completo: criar, achar e encerrar um processo ---"
sleep 60 &                       # o & roda em segundo plano
PID_SLEEP=$!                     # $! guarda o PID do último comando em background
echo "  Iniciei um 'sleep 60' com PID $PID_SLEEP"
ps -p "$PID_SLEEP" -o pid,comm   # confirma que existe
kill "$PID_SLEEP"                # pede para terminar (sinal TERM)
sleep 0.2
echo "  Após o kill, o processo ainda existe?"
ps -p "$PID_SLEEP" > /dev/null 2>&1 && echo "  sim" || echo "  não — encerrado ✓"

echo
echo "--- 8. Limpeza ---"
cd ..
rm -r "$PASTA"
echo "Cenário removido."
