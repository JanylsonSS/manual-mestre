# Módulo 02 — Git e Linux

> **Fase 1 — Fundamentos** · 12 capítulos · ~30 h · Profundidade: N1 → N2 · _Gerado sob spec 3.0.0_

## Missão do módulo

Você sai deste módulo **vivendo no terminal sem medo** e usando Git como ferramenta diária — inclusive para desfazer erros. Não é um módulo de decorar comandos: é sobre entender **por que** profissionais trabalham assim, e sobre ganhar a rede de segurança que permite mexer em código sem receio de perder trabalho.

O Python do módulo 01 continua sendo o objeto: você versiona os scripts que escreveu, automatiza tarefas do seu próprio fluxo de estudo, e termina com o Atlas publicado no GitHub — o repositório que será seu portfólio pelos próximos onze módulos.

## A dor da Aurora e a entrega Atlas

**Dor:** *"Perdemos uma versão do script ontem."* O relatório funcionava na sexta; alguém editou, salvou por cima, e o comportamento mudou. Não há histórico, não há como voltar, e ninguém sabe o que foi alterado.
**Entrega Atlas:** repositório do Atlas versionado e publicado no GitHub, com histórico legível desde o primeiro commit, `.gitignore` adequado, README de projeto e scripts de automação em shell para o fluxo de estudo.

## Pré-requisitos do módulo

Módulo 01 completo, com CP2 aprovado — os exemplos versionam **código Python real** (o seu). O `git init` do Atlas foi executado no 00.05 como caixa-preta; aqui ela se abre por completo.

## Capítulos

| # | Capítulo | Objetivo central | Nível |
|---|---|---|---|
| 02.01 | Terminal: por que a linha de comando | **Explicar** shell vs. interface gráfica e por que profissionais vivem no terminal | N1 |
| 02.02 | Navegação e manipulação de arquivos | **Executar** `pwd`, `ls`, `cd`, `mkdir`, `cp`, `mv`, `rm` com segurança | N1 |
| 02.03 | Inspecionando arquivos | **Executar** `cat`, `less`, `head`, `tail`, `wc` e edição com `nano` | N1 |
| 02.04 | Pipes, redirecionamento e busca | **Compor** comandos com `\|`, `>`, `>>`, `grep` e `find` para investigar dados | N2 |
| 02.05 | Permissões e processos | **Explicar** usuários e permissões e **executar** `chmod`, `ps` e `kill` | N2 |
| 02.06 | Variáveis de ambiente e PATH | **Explicar** como o sistema encontra programas e **configurar** variáveis | N2 |
| 02.07 | Scripts de shell | **Construir** pequenos scripts de automação para o fluxo de estudo | N2 |
| 02.08 | Git: o modelo mental | **Explicar** snapshots, área de stage e o grafo de commits (com `gitGraph`) | N1 |
| 02.09 | Fluxo essencial do Git | **Executar** `init`, `add`, `commit`, `status`, `log` e `diff` no dia a dia | N1 |
| 02.10 | Branches e merge | **Aplicar** ramificação e **resolver** conflitos simples sem pânico | N2 |
| 02.11 | Remotos e GitHub | **Publicar** o repositório com `clone`, `push`, `pull` e chaves SSH | N1 |
| 02.12 | Desfazendo + mini projeto | **Diferenciar** `restore`, `revert`, `reset` e `stash`; **construir** o fluxo de trabalho padrão do Atlas | N2 |

## Objetivos detalhados por capítulo

**[02.01 — Terminal: por que a linha de comando](01-terminal-por-que-a-linha-de-comando.md)**
- **Explicar** a diferença entre shell, terminal e interface gráfica, e o que cada um oferece.
- **Justificar** por que servidores, containers e automações não têm interface gráfica.
- **Executar** os primeiros comandos com confiança, lendo a saída como informação.
- **Identificar** o shell em uso no seu sistema (bash, zsh, PowerShell, Git Bash) e as implicações.

**[02.02 — Navegação e manipulação de arquivos](02-navegacao-e-manipulacao-de-arquivos.md)**
- **Executar** `pwd`, `ls` (com `-l`, `-a`, `-h`), `cd` (absoluto e relativo, `..`, `~`, `-`).
- **Criar, copiar, mover e remover** com `mkdir -p`, `cp -r`, `mv`, `rm` — e **explicar** por que `rm` não tem lixeira.
- **Aplicar** globs (`*`, `?`, `[]`) para operar em vários arquivos.
- **Depurar** os erros clássicos: caminho errado, espaço no nome, pasta não vazia.

**[02.03 — Inspecionando arquivos](03-inspecionando-arquivos.md)**
- **Executar** `cat`, `less`, `head`, `tail` (incluindo `-f`), `wc` para investigar arquivos sem abrir editor.
- **Decidir** qual ferramenta usar conforme o tamanho e a pergunta.
- **Editar** no terminal com `nano` — o mínimo para consertar um arquivo em servidor.
- **Aplicar** as ferramentas ao CSV de vendas da Aurora (contar linhas, ver cabeçalho, últimos registros).

**[02.04 — Pipes, redirecionamento e busca](04-pipes-redirecionamento-e-busca.md)**
- **Compor** comandos com `|`, encadeando ferramentas pequenas (a filosofia Unix).
- **Redirecionar** saída e erro com `>`, `>>`, `2>`, `&>` — e **explicar** a relação com stdout/stderr (01.07).
- **Buscar** com `grep` (incluindo `-i`, `-n`, `-v`, `-r`) e localizar arquivos com `find`.
- **Investigar** dados reais: quantas vendas de Campinas há no CSV, sem abrir o arquivo.

**[02.05 — Permissões e processos](05-permissoes-e-processos.md)**
- **Explicar** o modelo usuário/grupo/outros e a notação `rwx` (e a numérica).
- **Aplicar** `chmod` para tornar um script executável e **explicar** o `#!` (shebang).
- **Listar e encerrar** processos com `ps`, `top`/`htop`, `kill` — e o Ctrl+C do 01.10 em contexto.
- **Reconhecer** quando `sudo` é necessário — e por que raramente deveria ser.

**[02.06 — Variáveis de ambiente e PATH](06-variaveis-de-ambiente-e-path.md)**
- **Explicar** o que são variáveis de ambiente e como o shell as usa.
- **Descrever** como o sistema encontra programas via PATH — fechando o arco aberto no 00.03.
- **Configurar** variáveis temporárias e persistentes; **ler** valores com `echo` e `env`.
- **Antecipar** o uso profissional: configuração por ambiente e segredos fora do código (06.12).

**[02.07 — Scripts de shell](07-scripts-de-shell.md)**
- **Construir** scripts com shebang, permissão de execução e argumentos posicionais.
- **Aplicar** variáveis, condicionais e laços de shell no essencial.
- **Automatizar** tarefas reais do fluxo de estudo (backup do dia, checagem do ambiente, execução do relatório).
- **Decidir** quando usar shell e quando usar Python — o critério que evita scripts monstruosos.

**[02.08 — Git: o modelo mental](08-git-o-modelo-mental.md)**
- **Explicar** o que é controle de versão e o problema que ele resolve.
- **Descrever** os três estados (working directory, staging, repositório) e o fluxo entre eles.
- **Explicar** commit como **snapshot** (não como diff) e o grafo de commits.
- **Ler** um `gitGraph` e reconhecer HEAD, branch e histórico linear.

**[02.09 — Fluxo essencial do Git](09-fluxo-essencial-do-git.md)**
- **Executar** o ciclo diário: `status` → `add` → `commit` → `log`.
- **Escrever** mensagens de commit que servem ao futuro (o que e por quê).
- **Ler** `diff` (working vs. stage vs. último commit) e `log` com formatos úteis.
- **Configurar** `.gitignore` — aposentando o `__pycache__` prometido desde o 01.02.

**[02.10 — Branches e merge](10-branches-e-merge.md)**
- **Explicar** branch como ponteiro móvel e por que criar uma é barato.
- **Aplicar** `branch`, `switch`/`checkout`, `merge` no fluxo de uma funcionalidade.
- **Resolver** conflitos simples: entender os marcadores, decidir, concluir o merge.
- **Reconhecer** os fluxos de trabalho do mercado (main + feature branches) e o papel do PR (módulo 09).

**[02.11 — Remotos e GitHub](11-remotos-e-github.md)**
- **Explicar** a relação entre repositório local e remoto.
- **Configurar** autenticação com chaves SSH e **publicar** com `remote add` + `push`.
- **Executar** `clone`, `pull`, `fetch` e entender a diferença.
- **Publicar** o Atlas com README decente — o repositório que vira portfólio.

**[02.12 — Desfazendo + mini projeto](12-desfazendo-e-mini-projeto.md)**
- **Diferenciar** `restore`, `revert`, `reset` (soft/mixed/hard) e `stash` pelo que cada um desfaz.
- **Aplicar** a árvore de decisão: "o que eu quero desfazer, e o commit já foi publicado?"
- **Recuperar** trabalho aparentemente perdido (`reflog`) — a rede de segurança que tira o medo.
- **Construir** o fluxo de trabalho padrão do Atlas e publicá-lo com histórico legível.

## Critério de conclusão (CP2)

`Simulados/modulo-02.md`: 10 objetivas + 3 discursivas + 1 prático de ~45 min (um exercício de recuperação: dado um repositório em estado problemático, restaurar sem perder trabalho, documentando cada comando). Aprovação: ≥ 8/10 e prático ≥ 3. A entrega Atlas (repositório publicado com histórico) é pré-requisito para o CP3 da Fase 1.

## Tempo estimado

~30 h: capítulos de 2–3 h, com prática intensiva no terminal (a fluência vem de repetição deliberada, não de leitura). No ritmo de 32 h/semana, ~1 semana.

> 📌 **Observação sobre sistemas**
> Os comandos deste módulo são de ambiente Unix (Linux/macOS). No Windows, use o **Git Bash** (instalado no 00.03) ou o WSL — ambos oferecem o mesmo shell. Cada capítulo indica as diferenças relevantes quando existirem; a decisão está registrada em `DECISOES.md` (D-009).

## Pacote de fechamento

Concluídos os 12 capítulos, o módulo entrega:

| Item | Onde |
|---|---|
| Resumo de uma página | [`revisao/resumo.md`](revisao/resumo.md) |
| Mapa mental (Mermaid) | [`revisao/mapa-mental.md`](revisao/mapa-mental.md) |
| 60 flashcards | [`revisao/flashcards.md`](revisao/flashcards.md) |
| 15 questões de revisão | [`revisao/questoes.md`](revisao/questoes.md) |
| 45 perguntas de entrevista | [`entrevistas/perguntas.md`](entrevistas/perguntas.md) |
| 4 desafios de entrevista | [`entrevistas/desafios.md`](entrevistas/desafios.md) |
| Simulado CP2 — variantes A e B | [`Simulados/modulo-02.md`](../Simulados/modulo-02.md) · [B](../Simulados/modulo-02-b.md) |
| Cheatsheet da tecnologia | [`Recursos/cheatsheets/git-linux.md`](../Recursos/cheatsheets/git-linux.md) |
