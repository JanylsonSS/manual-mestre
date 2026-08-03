# Resumo — Módulo 02: Git e Linux

Uma página. Usado nas revisões D+30/D+90 dos capítulos deste módulo.

## Terminal (02.01–02.04)

**Terminal** é a janela, **shell** é o interpretador (bash/zsh), **prompt** é o convite. O terminal domina porque servidores e containers não têm interface gráfica, e porque comandos são automatizáveis, comunicáveis e versionáveis. Anatomia: `comando -opções argumentos` — identifique o **verbo** primeiro. **Tab** é o atalho de maior retorno.

Navegação: `pwd` (onde estou), `ls -la`, `cd` com `.` `..` `~` `-`. Caminho **absoluto** parte da raiz, **relativo** da pasta atual. Manipulação: `mkdir -p`, `cp -r`, `mv` (renomeia e move), `rm` — e o par de segurança **listar→apagar** com o mesmo curinga. Curingas são expandidos pelo **shell**, não pelo comando.

Inspeção sem abrir: `wc -l` dimensiona (lembre do cabeçalho), `head`/`tail` leem só as pontas (instantâneo em 10 GB), `tail -f` acompanha ao vivo, `less` navega (`/` busca, **`q` sai**). `cat` só em arquivo pequeno; se embaralhar, `reset`.

Composição: `>` trunca, `>>` acrescenta, `2>` grava erros (que **não** vão no `>`), `|` conecta stdout ao stdin com memória constante. O idioma que responde "quanto por categoria": `cut | sort | uniq -c | sort -rn`. `uniq` só remove duplicatas **adjacentes** — daí o `sort` antes. `grep -i` para caixa, `find` para localizar.

## Sistema (02.05–02.07)

**Permissões**: trio dono/grupo/outros com `rwx` (4/2/1). O trio que resolve quase tudo: **755** (scripts e pastas), **644** (arquivos), **600** (segredos). Em diretório, `x` significa **atravessar**. Executar exige `chmod +x` **e** shebang (`#!/usr/bin/env bash`) — e `./` porque a pasta atual não está no PATH. **Processos**: `ps aux`, `kill` (TERM, permite limpeza) antes de `kill -9` (KILL, imediato).

**Variáveis de ambiente** são um quadro de avisos herdado **por cópia**: `VAR=x` é local, `export VAR=x` é herdável — e por isso alteração dentro de script não sobe (use `source`). **PATH**: lista ordenada separada por `:`; a busca **para no primeiro achado** com bit de execução — `which -a` revela a fila. Persistência em `~/.bashrc` (sempre `>>`, backup antes). Configuração vive **no ambiente**: `os.environ.get("CHAVE", padrao)`, `.env` fora do Git com 600, `.env.example` versionado.

**Scripts**: cabeçalho `set -euo pipefail` (encerra ao erro · variável indefinida é erro · o pipe inteiro conta). Argumentos `$1 $# $@`, padrão com `${2:-valor}`, **sempre entre aspas**. Testes `[ -f ]` `[ -d ]` `[ -z ]`, `=` para texto e `-eq` para número. Estrutura: **valide primeiro, processe depois**; erros em `>&2`; código de saída 0/≠0. Shell orquestra, Python calcula.

## Git — modelo e fluxo (02.08–02.09)

Git é **distribuído**: cada cópia tem o histórico inteiro e funciona offline. **Git ≠ GitHub**. Três áreas: diretório de trabalho → (`add`) → área de preparo → (`commit`) → repositório. Quatro estados: não rastreado, modificado, preparado, versionado — o `git status` sempre diz qual. Um **commit** é a **fotografia completa** do projeto + autor + data + mensagem + ponteiro para o pai, identificado por um resumo do conteúdo; o histórico é um **grafo**.

Ciclo diário: `status` → `diff` → `add` seletivo → `diff --staged` → `commit -m` → `log`. Três comparações: `diff` (trabalho×preparo), `--staged` (preparo×commit), `HEAD` (trabalho×commit). Mensagens no **imperativo**, ~50 caracteres, respondendo *por quê* — se precisa de "e", são dois commits. `.gitignore` **antes** do primeiro commit (não afeta o que já está rastreado).

## Git — colaboração e recuperação (02.10–02.12)

**Branch** é uma etiqueta de **41 bytes** que anda com os commits; trocar de branch reescreve os arquivos do disco. Merge: **vá para quem recebe, traga quem chega** — fast-forward (etiqueta desliza) ou merge commit (dois pais). **Conflito** = as duas linhas mudaram as mesmas linhas; resolver é editar, **apagar os três marcadores**, `add`, `commit`. Branches **curtas** conflitam menos.

**Remotos**: três camadas — sua branch, o rastreamento (`origin/main`, sua anotação) e o remoto real. `fetch` baixa **sem** incorporar; `pull` = `fetch` + `merge`. Push recusado significa que o remoto avançou — **nunca** `--force` em branch compartilhada. SSH com chave privada em **600**, nunca publicada.

**Desfazendo**, com duas perguntas: *o que* e *já foi publicado?* `restore` (arquivos) · `restore --staged` (tira do preparo) · `stash push -m` (pausa) · `reset` soft/mixed/hard (só antes de publicar) · `revert` (obrigatório depois) · `commit --amend` (último commit local). O **`reflog`** recupera commits órfãos por ~90 dias. Assimetria central: **o que foi comitado é quase indestrutível; o que não foi não tem proteção**.

## Números do módulo

12 capítulos · ~34 h · N1→N2 · entrega Atlas: **repositório publicado no GitHub, com fluxo de branches e histórico legível** · fechamento: [questões](questoes.md) + [mapa mental](mapa-mental.md) + [simulado CP2](../../Simulados/modulo-02.md).
