# Guia de ambiente — Windows 10/11

Guia da Fase 1: Python, VS Code e Git. Siga na ordem, do início ao fim. Referenciado pelo capítulo 00.03.

## 1. Python 3.12+

1. Baixe o instalador em <https://www.python.org/downloads/> (botão amarelo — versão estável mais recente).
2. Execute o instalador. **Antes de clicar em Install Now, marque a caixa "Add python.exe to PATH"** — a etapa mais importante do guia inteiro.
3. Conclua e feche.
4. Verificação: abra um terminal **novo** (tecla Windows → digite `cmd` ou `powershell` → Enter) e rode:

```bash
python --version
```

Deve responder `Python 3.12.x` (ou superior).

**Se abrir a Microsoft Store em vez de responder:** Configurações → Aplicativos → Configurações avançadas de aplicativos → *Aliases de execução de aplicativo* → desative os dois itens `python.exe` e `python3.exe`. Abra um terminal novo e teste de novo.

## 2. VS Code

1. Baixe em <https://code.visualstudio.com/> e instale (as opções padrão servem; marcar "Adicionar ao PATH" se oferecido).
2. Abra o VS Code → ícone de blocos na barra lateral (`Ctrl+Shift+X`) → instale:
   - **Python** (Microsoft)
   - **Markdown Preview Mermaid Support**
3. Verificação: `code --version` num terminal novo deve responder com a versão.

## 3. Git

1. Baixe em <https://git-scm.com/download/win> e execute.
2. O instalador faz muitas perguntas — **as opções padrão servem para a trilha inteira.** (De brinde, você ganha o *Git Bash*, um terminal no estilo Linux.)
3. Verificação: `git --version` num terminal novo.

## 4. Validação final

Na raiz do repositório do Manual Mestre:

```bash
python 00-Introducao/codigo/cap03/valida_ambiente.py
```

Veredito esperado: **AMBIENTE APROVADO — 4/4**. Se algo falhou, a seção "Erros comuns" do capítulo 00.03 cobre os casos clássicos.
