# ------------------------------------------------------------
# valida_ambiente.py
# Capítulo 00.03 — Preparando o ambiente
# O que este arquivo demonstra: checagem automatizada da instalação
#   (versão do Python, PATH, Git e sistema operacional)
# Como executar: python valida_ambiente.py
# ------------------------------------------------------------

# Módulos da biblioteca padrão — vêm junto com o Python (01.20 explica imports)
import sys
import platform
import shutil
import subprocess

MINIMO = (3, 12)  # versão mínima exigida pela trilha (spec §18.1)


def checar_versao_python():
    # sys.version_info traz a versão do interpretador que está executando este arquivo
    atual = sys.version_info[:2]
    versao = platform.python_version()
    if atual >= MINIMO:
        return True, f"Python {versao} (>= {MINIMO[0]}.{MINIMO[1]} exigido)"
    return False, f"Python {versao} — a trilha exige {MINIMO[0]}.{MINIMO[1]}+ (reinstale pelo guia)"


def checar_python_no_path():
    # shutil.which faz a mesma busca que o terminal faz: procura o nome no PATH
    caminho = shutil.which("python") or shutil.which("python3")
    if caminho:
        return True, "Interpretador encontrado no PATH"
    return False, "Interpretador fora do PATH — veja Erros comuns, Erro 1"


def checar_git():
    if shutil.which("git") is None:
        return False, "Git não encontrado — instale pelo guia do seu sistema"
    # Pergunta a versão ao próprio Git, como você fez manualmente no Passo 3
    resultado = subprocess.run(["git", "--version"], capture_output=True, text=True)
    return True, f"Git encontrado: {resultado.stdout.strip()}"


def checar_sistema():
    # Apenas informativo: registra onde a trilha está sendo cursada
    bits = "64 bits" if sys.maxsize > 2**32 else "32 bits"
    return True, f"Sistema: {platform.system()} {platform.release()} ({bits})"


def main():
    print("=" * 44)
    print(" Manual Mestre — Validação de ambiente")
    print("=" * 44)

    checagens = [
        checar_versao_python(),
        checar_python_no_path(),
        checar_git(),
        checar_sistema(),
    ]

    aprovadas = 0
    for passou, mensagem in checagens:
        etiqueta = "[OK]   " if passou else "[FALHOU]"
        print(f"{etiqueta} {mensagem}")
        if passou:
            aprovadas = aprovadas + 1

    print("-" * 44)
    total = len(checagens)
    if aprovadas == total:
        print(f"Veredito: AMBIENTE APROVADO — {aprovadas}/{total} checagens.")
        print("Bem-vindo(a) à trilha. Registre no PROGRESSO.md!")
    else:
        print(f"Veredito: PENDENTE — {aprovadas}/{total} checagens.")
        print("Corrija os itens [FALHOU] (seção 11 do capítulo) e rode de novo.")
    print("=" * 44)


main()
# Saída: (o relatório completo mostrado na seção 9 do capítulo)
