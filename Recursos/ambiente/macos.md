# Guia de ambiente — macOS

Guia da Fase 1: Python, VS Code e Git. Siga na ordem. Referenciado pelo capítulo 00.03.

## 1. Python 3.12+

**Opção A — instalador oficial (recomendada para quem não usa Homebrew):**

1. Baixe em <https://www.python.org/downloads/macos/> e instale (padrões servem).
2. Verificação, num terminal novo (`Cmd+Espaço` → "Terminal"):

```bash
python3 --version
```

**Opção B — Homebrew (se você já o usa):**

```bash
brew install python@3.12
```

**Nota sobre o nome:** no macOS, use `python3` onde a trilha escrever `python`.

## 2. VS Code

1. Baixe em <https://code.visualstudio.com/>, arraste para *Applications*.
2. Para o comando `code` funcionar no terminal: abra o VS Code → `Cmd+Shift+P` → digite "shell command" → **Install 'code' command in PATH**.
3. `Cmd+Shift+X` → instale **Python** (Microsoft) e **Markdown Preview Mermaid Support**.

## 3. Git

O caminho mais direto é via Command Line Tools da Apple. No terminal:

```bash
git --version
```

Se não estiver instalado, o próprio sistema oferece a instalação — aceite e aguarde. Verifique de novo ao final.

## 4. Validação final

Na raiz do repositório do Manual Mestre:

```bash
python3 00-Introducao/codigo/cap03/valida_ambiente.py
```

Veredito esperado: **AMBIENTE APROVADO — 4/4**. Se algo falhou, a seção "Erros comuns" do capítulo 00.03 cobre os casos clássicos.
