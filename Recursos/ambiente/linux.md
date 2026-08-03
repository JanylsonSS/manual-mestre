# Guia de ambiente — Linux (Ubuntu/Debian)

Guia da Fase 1: Python, VS Code e Git. Siga na ordem. Referenciado pelo capítulo 00.03. (Para outras distribuições, adapte o gerenciador de pacotes: `dnf`, `pacman`, etc.)

## 1. Python 3.12+

Ubuntu 24.04+ já traz Python 3.12 como `python3`. Verifique primeiro:

```bash
python3 --version
```

Se responder `3.12` ou superior, siga ao passo 2. Se for anterior:

```bash
sudo apt update
sudo apt install python3.12
```

**Nota sobre o nome:** no Linux, o interpretador atende por `python3` (e às vezes só por `python3.12`). Nos comandos da trilha, onde se lê `python`, use `python3`.

## 2. VS Code

1. Baixe o `.deb` em <https://code.visualstudio.com/> e instale:

```bash
sudo apt install ./code_*.deb
```

2. Abra o VS Code → `Ctrl+Shift+X` → instale **Python** (Microsoft) e **Markdown Preview Mermaid Support**.
3. Verificação: `code --version`.

## 3. Git

```bash
sudo apt update
sudo apt install git
git --version
```

## 4. Validação final

Na raiz do repositório do Manual Mestre:

```bash
python3 00-Introducao/codigo/cap03/valida_ambiente.py
```

Veredito esperado: **AMBIENTE APROVADO — 4/4**. Se algo falhou, a seção "Erros comuns" do capítulo 00.03 cobre os casos clássicos.
