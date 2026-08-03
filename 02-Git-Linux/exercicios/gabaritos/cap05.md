# Gabaritos — Capítulo 02.05

Abra somente após tentativa honesta.

## A1 — Lendo permissões

1. Arquivo; dono lê/escreve; grupo e outros só leem; **ninguém executa** (644).
2. Arquivo; dono tudo; grupo e outros leem e executam (755) — script pronto para uso.
3. **Diretório**; dono tudo; grupo entra e lista; outros **sem acesso nenhum** (750).
4. Arquivo; só o dono lê e escreve (600) — o correto para segredos.
5. Arquivo; **todos podem tudo** (777) — inseguro: qualquer usuário do sistema pode alterar o script que você executa.
6. Diretório somente-leitura (555): todos entram e listam, **ninguém cria ou remove** dentro.

**Critério:** 6/6, com o item 5 identificado como risco e o 3 com o `d` reconhecido.

## A2 — Traduzindo notações

1. `rwxr-xr-x` · 2. `rw-r--r--` · 3. `rw-------` · 4. `rwxrwxrwx` · 5. `750` · 6. `664` · 7. `400` · 8. `700`.

**Critério:** 8/8 (r=4, w=2, x=1, somados por trio).

## A3 — Qual comando?

1. `chmod +x backup.sh` (ou `chmod 755 backup.sh`)
2. `chmod u+x deploy.sh` (ou `chmod 700`, se quiser restringir tudo ao dono)
3. `chmod 600 .env`
4. `chmod go-w dados.csv`
5. `chmod 755 pasta/`

**Critério:** 5/5.

## A4 — Diagnóstico

1. Falta o bit `x`. Investigação: `ls -l script.sh` → `chmod +x`.
2. Falta o shebang (ou está errado): o shell tentou interpretar Python. Investigação: `head -1 relatorio.py` → acrescentar `#!/usr/bin/env python3`.
3. Quebras de linha CRLF (arquivo salvo no Windows) — o `^M` no fim do shebang. Correção: converter para LF (no VS Code, canto inferior direito) ou `dos2unix`.
4. O arquivo existe, mas o shell não procura na pasta atual (ela não está no PATH). Correção: `./script.sh` — ou colocar o script num diretório do PATH (02.06).

**Critério:** 4/4; o item 3 é o que mais consome tempo na vida real.

## AP1 — Seu primeiro comando

**Resultados esperados:** (1) `Permission denied` nos dois; (2) `-rw-r--r--`; (3) sem saída (chmod é silencioso); (4) as mensagens; (5) sem shebang, o `.sh` ainda funciona (o shell é o padrão), mas o `.py` produz erro de sintaxe — o shell tentou interpretar Python.

**Critério:** 5 etapas registradas nos dois arquivos; a diferença do item 5 observada e explicada.

## AP2 — O caçador de processos

**Observação esperada:** com `kill` (TERM), o processo termina e o shell costuma informar (`Terminated`); com `kill -9` (KILL), termina igualmente, mas sem qualquer chance de limpeza — a diferença não aparece com `sleep` (que nada tem a limpar), e é justamente essa a lição: **em programas que escrevem arquivos, o -9 corrompe**; com `sleep`, não há diferença visível.

**Erro esperado:** esquecer o `grep -v grep` e encontrar o próprio comando de busca na lista de PIDs (e tentar matá-lo).
**Critério:** 3 PIDs registrados, os dois comandos usados, e a observação honesta de que a diferença **não** é visível com `sleep`.

## AP3 — Permissões de projeto

Referências: `deploy.sh` → 755 (precisa executar) · `config.env` → **600** (contém segredos) · `dados.csv` → 644 (leitura geral) · `README.md` → 644 · `scripts/` → 755 (precisa de `x` para atravessar).

**Sobre o 644 no `.env`:** qualquer usuário com acesso ao servidor poderia **ler as senhas** — é achado grave em auditoria de segurança, e o motivo de o 600 ser padrão documentado em guias de deploy.

**Critério:** 5 permissões corretas com justificativa; a explicação do risco do `.env`.

## D1 — O auditor de permissões

**Achados típicos no repositório:** os `.sh` do módulo 02 devem ter `x`; arquivos `.md`, `.csv` e `.py` (exceto os que viraram comando) **não** precisam. Se muitos arquivos aparecem executáveis, o suspeito é cópia de sistema de arquivos do Windows (que não guarda permissões Unix e marca tudo como 777) — achado clássico e digno de menção.

**Referências de comando:** (a) `find . -type f -perm -u+x -not -name "*.sh" | head` · (b) `find . -perm -o+w -type f` · (c) 600, e com 644 qualquer usuário do servidor lê a senha · (d) `head -1 02-Git-Linux/codigo/*/*.sh` para conferir shebangs.

**Reflexão esperada:** o princípio do menor privilégio diz que cada usuário/processo deve ter **exatamente** as permissões necessárias e nada além — porque o dano de um erro (ou de uma invasão) fica limitado ao que aquele privilégio permitia. Aparece em auditorias porque é a defesa mais barata e mais violada: 777 e execução de aplicações como root são os dois achados mais comuns.

**Critério de "está bom":** tabela com achados reais do **seu** repositório; correções aplicadas com comando registrado; a reflexão conectando ao módulo 08 (containers não devem rodar como root).
