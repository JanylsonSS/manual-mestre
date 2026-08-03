# Perguntas de entrevista — Módulo 02

Acumulativo: cada capítulo acrescenta seus itens (IDs `P-MM.CC-nn`). Formato do §30 da spec.

### P-02.01-01 `[conceitual · júnior]` — Qual a diferença entre terminal e shell?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Terminal é o programa/janela que fornece a interação (emulador);
2. Shell é o interpretador que lê e executa comandos (bash, zsh, PowerShell);
3. Um pode ser trocado sem o outro;
4. Contexto prático: bash domina servidores Linux; no Windows, Git Bash/WSL como alternativas Unix.
</details>

### P-02.01-02 `[conceitual · júnior]` — Por que profissionais preferem o terminal à interface gráfica?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Ambientes remotos e containers não têm interface;
2. Comandos são automatizáveis (viram scripts e tarefas agendadas);
3. Comandos são comunicáveis, versionáveis e reproduzíveis;
4. Maturidade: para tarefas visuais, a interface gráfica é melhor — não é ideologia.
</details>

### P-02.01-03 `[pegadinha · júnior]` — Você roda `ls` e o arquivo que existe não aparece. O que houve?

<details><summary>Resposta esperada</summary>

Por que derruba: parece problema do sistema, e é do usuário.

Pontos da saída forte, em ordem de probabilidade:
1. Pasta errada — `pwd` primeiro;
2. Arquivo oculto (nome com ponto) — `ls -a`;
3. Diferença de maiúsculas (Linux é sensível a caixa);
4. Está em subpasta — `find`. A ordem de diagnóstico é a resposta.
</details>

### P-02.02-01 `[conceitual · júnior]` — Caminho absoluto × relativo: diferença e quando usar cada um?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Absoluto começa na raiz e funciona de qualquer lugar; relativo parte da pasta atual;
2. Em projetos, relativo (sobrevive à mudança de lugar) ou ancorado no script;
3. Absoluto para alvos externos e fixos (`/var/log`, `/etc`);
4. O problema clássico do "só funciona se eu rodar da pasta certa".
</details>

### P-02.02-02 `[código · júnior]` — Como copiar uma pasta com subpastas? E por que `mv` não precisa de `-r`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `cp -r origem destino`;
2. `mv` no mesmo disco só altera a entrada de nome — instantâneo;
3. Copiar duplica dados de verdade (custo proporcional ao tamanho);
4. Bônus: `rsync` para cópias grandes ou incrementais.
</details>

### P-02.02-03 `[pegadinha · pleno]` — Diferença entre `rm -rf pasta/` e `rm -rf pasta /`?

<details><summary>Resposta esperada</summary>

Por que derruba: um espaço muda tudo — e o erro é real em produção.

Pontos da saída forte:
1. O segundo vira dois argumentos: remove a pasta **e tenta remover a raiz**;
2. Sistemas modernos protegem `/` por padrão (`--preserve-root`), mas o hábito é a defesa;
3. Práticas: conferir com `ls` antes, caminhos relativos curtos, não colar comandos destrutivos;
4. E trabalhar sem privilégios de administrador no dia a dia.
</details>

### P-02.03-01 `[código · júnior]` — Como inspecionar um log de 2 GB?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Nunca com `cat` ou editor;
2. `wc -l` para dimensionar, `head` para formato, `tail -n` para o fim, `less` para navegar;
3. `grep` para filtrar;
4. O porquê: head/tail leem só as pontas; less carrega sob demanda.
</details>

### P-02.03-02 `[conceitual · júnior]` — Para que serve `tail -f`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Acompanha o arquivo em tempo real, exibindo novas linhas conforme são escritas;
2. Uso: monitorar deploy, pipeline, serviço no ar;
3. Encerra com Ctrl+C;
4. Em ambientes maduros, a versão agregada é o log centralizado (09.09) — mas o tail -f segue como primeiro recurso.
</details>

### P-02.03-03 `[pegadinha · júnior]` — `cat arquivo.bin` embaralhou o terminal. E agora?

<details><summary>Resposta esperada</summary>

Por que derruba: parece travamento, e é estado corrompido do terminal.

Pontos da saída forte:
1. Bytes de controle alteraram o estado do terminal;
2. Solução: `reset` (ou `stty sane`) — mesmo sem ver o que digita;
3. Prevenção: `file arquivo` antes, e preferir `less`, que trata binários com aviso;
4. Fechar/reabrir também resolve, mas perde histórico e sessões.
</details>

### P-02.04-01 `[conceitual · pleno]` — O que faz o `|` e por que ele é central no Unix?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Conecta stdout de um comando ao stdin do próximo;
2. Processos rodam em paralelo, com memória constante (os dados escoam);
3. Materializa "faça uma coisa e faça bem" — composição sobre monólito;
4. Encerramento antecipado: `comando_pesado | head` para o comando pesado.
</details>

### P-02.04-02 `[código · júnior]` — Diferença entre `>`, `>>` e `2>`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `>` grava stdout truncando; `>>` acrescenta; `2>` grava stderr;
2. `2>&1` junta os canais; `> /dev/null` descarta;
3. O truncamento acontece na abertura — antes de o comando rodar;
4. Em automações, separar stdout de stderr (o arquivo de erros é o que dispara alerta).
</details>

### P-02.04-03 `[código · pleno]` — Como contar quantas vezes cada valor aparece numa coluna de CSV?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `cut -d';' -f4 arquivo | sort | uniq -c | sort -rn`;
2. `tail -n +2` para pular o cabeçalho;
3. Normalização (caixa, espaços) com `tr` quando os dados são sujos;
4. Reconhecer que é o mesmo `GROUP BY` do SQL e o `value_counts()` do Pandas.
</details>

### P-02.04-04 `[pegadinha · pleno]` — Por que `uniq` sozinho não remove todas as duplicatas?

<details><summary>Resposta esperada</summary>

Por que derruba: quem decorou o comando sem entender o mecanismo.

Pontos da saída forte:
1. `uniq` compara cada linha com a **anterior** (duplicatas adjacentes), num passe só;
2. Por isso o idioma `sort | uniq` (ou `sort -u`);
3. É eficiente em memória justamente por não guardar o que já viu;
4. Quando a ordem original importa, a solução é outra (padrão "já vistos" — 01.16).
</details>

### P-02.05-01 `[conceitual · júnior]` — Explique `-rwxr-xr-x` e o significado de 755, 644 e 600.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Tipo (`-` arquivo, `d` diretório) + três trios: dono, grupo, outros;
2. r=4, w=2, x=1, somados por trio — `rwxr-xr-x` = 755;
3. O trio de uso diário: 755 (scripts/pastas), 644 (arquivos comuns), 600 (segredos);
4. Bônus: em diretório, o `x` significa **atravessar**, não executar.
</details>

### P-02.05-02 `[código · júnior]` — Como transformar um script num comando executável?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Shebang na primeira linha (`#!/usr/bin/env bash` ou `python3`);
2. `chmod +x script.sh`;
3. Executar com `./script.sh` (a pasta atual não está no PATH);
4. Para virar comando sem `./`, colocar numa pasta do PATH (02.06).
</details>

### P-02.05-03 `[conceitual · pleno]` — Diferença entre `kill` e `kill -9`. Qual usar primeiro?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `kill` envia TERM — o programa pode capturar, fechar arquivos e sair limpo;
2. `kill -9` envia KILL — o núcleo encerra sem aviso, sem chance de limpeza;
3. Sempre TERM primeiro; KILL só quando o processo não responde;
4. Risco do -9: arquivo pela metade, transação aberta, lock não liberado.
</details>

### P-02.05-04 `[pegadinha · pleno]` — Um script tem `chmod +x`, o caminho está certo, e ainda assim dá erro estranho. O que investigar?

<details><summary>Resposta esperada</summary>

Por que derruba: a permissão está certa, e o candidato fica sem hipóteses.

Pontos da saída forte, em ordem de investigação:
1. **Shebang** ausente ou errado (`head -1`) — o shell tenta interpretar Python como shell;
2. **Quebras de linha CRLF** (`bad interpreter: ...^M`) — arquivo salvo no Windows;
3. Interpretador não instalado ou fora do PATH;
4. Permissão `x` faltando em alguma **pasta** do caminho (o `x` de travessia).
</details>

### P-02.06-01 `[conceitual · júnior]` — O que é o PATH e como o shell encontra um comando?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Lista ordenada de pastas separadas por `:`, percorrida na ordem;
2. Usa o **primeiro** executável encontrado e para a busca;
3. Nomes com barra (`./script`, `/usr/bin/git`) ignoram o PATH;
4. Diagnóstico: `which -a` revela a fila e explica versões "erradas" respondendo.
</details>

### P-02.06-02 `[código · júnior]` — Diferença entre `VAR=valor` e `export VAR=valor`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Sem `export`: variável só do shell atual; com `export`: processos filhos herdam;
2. A herança é por **cópia** — o filho não altera o pai;
3. Consequência: script com `./` não configura o ambiente de quem chamou; use `source`;
4. Persistência: `~/.bashrc`/`~/.zshrc`, lido ao nascer do shell.
</details>

### P-02.06-03 `[decisão · pleno]` — Como você gerencia configuração e segredos numa aplicação?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Configuração no **ambiente** (12 fatores), lida com valor padrão de desenvolvimento;
2. `.env` local fora do Git (`.gitignore`), com permissão 600; `.env.example` versionado sem valores;
3. Em produção: injeção pelo orquestrador ou gerenciador de segredos (Vault, Secrets Manager);
4. Se vazou: **revogar** a credencial — apagar do repositório não resolve (histórico e clones).
</details>

### P-02.06-04 `[pegadinha · pleno]` — Você rodou `export PATH=/home/voce/bin` e nenhum comando funciona. Como sai dessa?

<details><summary>Resposta esperada</summary>

Por que derruba: pânico — parece que a máquina quebrou, e nada foi perdido.

Pontos da saída forte:
1. A lista foi **substituída**, não acrescentada — o shell não encontra mais nada;
2. Recuperação no mesmo shell: `export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"` (funciona porque `export` é built-in);
3. Alternativas: usar caminhos completos (`/bin/ls`) ou abrir outro terminal (o PATH é lido de novo);
4. Prevenção: sempre incluir `$PATH`; e o alerta — escrita no `.bashrc`, a falha seria permanente.
</details>

### P-02.07-01 `[conceitual · pleno]` — O que faz `set -euo pipefail` e por que usar?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `-e` encerra ao primeiro comando que falha (o padrão do shell é continuar);
2. `-u` transforma variável não definida em erro — pega erro de digitação que viraria string vazia;
3. `-o pipefail` faz o pipe falhar se qualquer parte falhar (sem ele, só o último comando conta);
4. O risco concreto: sem `-e`, um script de backup apaga o original depois de uma cópia que falhou.
</details>

### P-02.07-02 `[código · júnior]` — Por que sempre usar aspas em variáveis de shell?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Sem aspas, o shell divide o valor em palavras e expande curingas;
2. Exemplo concreto: `rm $ARQUIVO` com `ARQUIVO="Relatório de vendas.csv"` tenta apagar três arquivos;
3. `"$@"` preserva os argumentos; `$*` não;
4. Prevenção estrutural: `shellcheck` aponta cada ocorrência.
</details>

### P-02.07-03 `[decisão · pleno]` — Quando usar shell e quando usar Python?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Shell para **orquestrar**: encadear ferramentas, mover arquivos, preparar ambiente, colar comandos;
2. Python quando aparecem estruturas de dados, lógica aninhada, parsing de formato, ou testes;
3. Sinal de alerta concreto: script passando de ~100 linhas ou precisando de arrays;
4. O critério importa mais que a preferência — demonstrar o raciocínio é o que se avalia.
</details>

### P-02.07-04 `[pegadinha · pleno]` — Encontre os problemas: `DESTINO=$1; rm -rf $DESTINO/*; cp -r /origem/* $DESTINO/`

<details><summary>Resposta esperada</summary>

Por que derruba: o candidato encontra um problema e para; a nota está na **ordem** dos quatro.

Pontos da saída forte:
1. **Sem validação** — sem argumento, `$DESTINO` fica vazio e `rm -rf /*` tenta apagar o sistema (o catastrófico vem primeiro);
2. **Sem aspas** — destino com espaço quebra de forma imprevisível;
3. **Sem `set -euo pipefail`** — variável vazia não gera erro; a cópia roda mesmo se a limpeza falhar;
4. **Ordem perigosa** — apaga antes de verificar a origem; correção: validar → verificar origem → copiar → remover.
</details>

### P-02.08-01 `[conceitual · júnior]` — Qual a diferença entre Git e GitHub?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Git é o sistema de controle de versão distribuído, que roda na sua máquina;
2. GitHub é um serviço que hospeda repositórios Git, com colaboração por cima;
3. Git funciona offline e sem GitHub; alternativas: GitLab, Bitbucket, servidor próprio;
4. É pergunta de triagem — errar encerra a conversa técnica.
</details>

### P-02.08-02 `[conceitual · júnior]` — Explique as três áreas do Git.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Diretório de trabalho (arquivos que você edita), área de preparo (o que entra no próximo commit), repositório (`.git/`);
2. O caminho: editar → `add` → `commit`;
3. O **porquê** da área intermediária: separar mudanças em commits coerentes mesmo tendo editado várias coisas;
4. Os quatro estados (não rastreado, modificado, preparado, versionado) e o `git status` como ferramenta de leitura.
</details>

### P-02.08-03 `[conceitual · pleno]` — O que é um commit e o que ele guarda?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Fotografia completa do projeto num instante, com autor, data, mensagem e ponteiro para o pai;
2. Identificado por um resumo criptográfico do próprio conteúdo;
3. O histórico é um **grafo**, não uma lista — daí ramificações e reuniões;
4. Alterar o passado muda todos os identificadores posteriores (histórico verificável).
</details>

### P-02.08-04 `[pegadinha · pleno]` — Se cada commit é uma fotografia do projeto inteiro, mil commits ocupam mil vezes o projeto?

<details><summary>Resposta esperada</summary>

Por que derruba: quem decorou a metáfora sem saber o que há embaixo.

Pontos da saída forte:
1. **Conceitualmente sim** — é o que torna qualquer ponto do histórico recuperável por inteiro;
2. **Na prática não** — o Git endereça o conteúdo pelo resumo dele; arquivo não alterado é referenciado pelo mesmo objeto;
3. Um commit de uma linha acrescenta ~3 objetos: o blob novo, as trees afetadas e o commit;
4. A exceção honesta: **binários grandes** mudam por inteiro a cada versão — a solução é não versioná-los.
</details>

### P-02.09-01 `[conceitual · júnior]` — Descreva o seu fluxo de trabalho diário com Git.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `status` → `diff` → `add` seletivo → `diff --staged` → `commit` com o porquê → `log`;
2. Commits pequenos e temáticos, um assunto por commit;
3. `.gitignore` criado no primeiro dia do projeto;
4. Ler a saída do `git status`, que sugere o comando seguinte.
</details>

### P-02.09-02 `[código · júnior]` — Qual a diferença entre `git diff` e `git diff --staged`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `git diff`: diretório de trabalho × área de preparo — o que **ainda não** foi preparado;
2. `git diff --staged`: área de preparo × último commit — o que **vai** no próximo commit;
3. `git diff HEAD`: diretório × último commit — tudo o que mudou;
4. Ancorar nas três áreas (02.08) em vez de decorar as opções.
</details>

### P-02.09-03 `[decisão · pleno]` — O que deve e o que não deve ir para o repositório?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Vai: código-fonte, configuração de projeto, documentação, `.env.example`;
2. Não vai: segredos, arquivos gerados (cache, saídas, dependências), binários grandes;
3. Mecanismo: `.gitignore` **antes** do primeiro commit;
4. A ressalva de quem já se queimou: `.gitignore` não afeta o que já está rastreado, e segredo comitado exige **revogar** a credencial.
</details>

### P-02.09-04 `[pegadinha · pleno]` — Você comitou e publicou um arquivo com a senha do banco. O que faz?

<details><summary>Resposta esperada</summary>

Por que derruba: a resposta intuitiva ("removo o arquivo e comito") trata como problema de Git o que é problema de segurança.

Pontos da saída forte, **nesta ordem**:
1. **Revogar a credencial imediatamente** — bots varrem repositórios públicos continuamente;
2. Gerar nova credencial e movê-la para variável de ambiente, com `.env` no `.gitignore`;
3. Só então limpar o histórico — sabendo que reescreve commits e não alcança clones já feitos;
4. Prevenir: verificação automática de segredos antes do commit (módulo 09).
</details>

### P-02.10-01 `[conceitual · júnior]` — O que é uma branch e por que criá-las é barato?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Uma referência (ponteiro) para um commit, num arquivo de 41 bytes em `.git/refs/heads/`;
2. Criar não copia arquivos — custo constante, independente do tamanho do projeto;
3. HEAD indica a branch ativa; comitar avança o ponteiro;
4. Comparação com sistemas anteriores, em que ramificar copiava o projeto.
</details>

### P-02.10-02 `[conceitual · pleno]` — Explique o fluxo main + feature branches.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `main` sempre funcional e publicável; ninguém escreve nela diretamente;
2. Cada mudança nasce numa branch curta com nome descritivo;
3. PR para revisão + testes automatizados; aprovado, merge e branch apagada;
4. O motivo das branches curtas: menos divergência desde o ancestral comum, menos conflito.
</details>

### P-02.10-03 `[código · pleno]` — O que é um conflito e como você resolve?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Ocorre quando as duas linhas alteraram **as mesmas linhas**; o resto o Git resolve sozinho;
2. Marcadores: `<<<<<<< HEAD` (versão local) · `=======` · `>>>>>>>` (a que chegou);
3. Resolver: editar decidindo o resultado (que pode **combinar** os dois), apagar os marcadores, `add`, `commit`;
4. `git merge --abort` como saída; verificar marcadores esquecidos antes de comitar.
</details>

### P-02.10-04 `[pegadinha · júnior]` — Você troca da sua branch para a `main` e seus arquivos "sumiram". Perdeu o trabalho?

<details><summary>Resposta esperada</summary>

Por que derruba: provoca pânico e revela se a pessoa separa "disco" de "banco de objetos".

Pontos da saída forte:
1. **Não** — os arquivos refletem o commit onde o HEAD está; os commits seguem guardados sob a etiqueta da branch;
2. `git switch minha-branch` traz tudo de volta; `git log --oneline --all` prova que nada saiu;
3. O perigo real é outro: **trabalho não comitado** não tem proteção nenhuma;
4. Branch apagada não reunida: o Git avisa e exige `-D`; ainda assim o `reflog` recupera.
</details>

### P-02.11-01 `[conceitual · pleno]` — Qual a diferença entre `fetch` e `pull`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `fetch` baixa objetos e atualiza só as branches de rastreamento (`origin/main`) — não toca no seu trabalho;
2. `pull` = `fetch` + `merge`: altera sua branch e seus arquivos, e pode conflitar;
3. Prática: `fetch` + inspecionar (`git log main..origin/main`) quando há trabalho em andamento;
4. Ancorar nas três camadas: branch local, rastreamento, remoto real.
</details>

### P-02.11-02 `[conceitual · júnior]` — O que é o `origin`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Um **apelido** para a URL de um remoto — convenção, não obrigação;
2. Um repositório pode ter vários remotos (`origin`, `upstream`); `git remote -v` os lista;
3. Não há hierarquia técnica: local e remoto são repositórios completos;
4. `git remote add`, `set-url`, `remove` para gerenciá-los.
</details>

### P-02.11-03 `[código · júnior]` — Como você configura autenticação com o GitHub?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `ssh-keygen -t ed25519`, pública cadastrada no serviço, privada na máquina;
2. Privada com permissão **600** e frase-senha; teste com `ssh -T git@github.com`;
3. Alternativa: HTTPS com token de acesso pessoal — nunca senha de conta;
4. Chave privada não é versionada nem compartilhada; se vazar, revogar e gerar outra.
</details>

### P-02.11-04 `[pegadinha · sênior]` — Um colega fez `git push --force` e o seu trabalho sumiu do repositório. Recuperável?

<details><summary>Resposta esperada</summary>

Por que derruba: testa se a pessoa entende o modelo **distribuído** na prática, não só na definição.

Pontos da saída forte:
1. No remoto, os commits ficaram órfãos mas existem por um tempo — recuperáveis pelo identificador;
2. **O ponto principal**: sendo distribuído, quem tinha o trabalho localmente **ainda tem** — republicar resolve;
3. Prevenção organizacional: proteção de branch, `--force-with-lease`, não reescrever história compartilhada;
4. O limite honesto: se o trabalho **só** existia no remoto e os objetos expiraram, aí sim está perdido.
</details>

### P-02.12-01 `[conceitual · pleno]` — Qual a diferença entre `reset` e `revert`?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. `reset` move o ponteiro da branch, **reescrevendo a história** — só para commits não publicados;
2. `revert` cria um commit novo que anula outro, preservando a história e a sincronia;
3. O critério é uma pergunta só: **já foi publicado?**;
4. Na prática: proteção de branch e `revert` como procedimento de emergência em produção.
</details>

### P-02.12-02 `[código · pleno]` — Explique os três modos do `reset`.

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Todos movem a branch; a diferença está nas outras duas áreas;
2. `--soft` preserva preparo e diretório (refazer o último commit);
3. `--mixed` (padrão) limpa o preparo e preserva o diretório;
4. `--hard` limpa tudo e **destrói** alterações não comitadas — o único que perde trabalho.
</details>

### P-02.12-03 `[conceitual · pleno]` — O que é o `reflog` e quando você o usa?

<details><summary>Resposta esperada</summary>

Pontos que uma boa resposta cobre:
1. Registro local de todos os movimentos do HEAD (~90 dias), inclusive fora da história atual;
2. Uso: recuperar de `reset` equivocado, branch apagada, merge desastroso;
3. Procedimento: achar o identificador anterior ao erro e voltar a ele (de preferência com `switch -c`, que não fecha portas);
4. O limite honesto: não recupera o que nunca foi comitado.
</details>

### P-02.12-04 `[pegadinha · pleno]` — `git reset --hard` apagou 3 commits e 2 horas de alterações não comitadas. O que dá para recuperar?

<details><summary>Resposta esperada</summary>

Por que derruba: tem **duas respostas diferentes** na mesma pergunta, e quem dá só uma não entendeu o modelo.

Pontos da saída forte:
1. **Os 3 commits: sim** — `git reflog` + `reset --hard <id>` (ou `switch -c recuperado <id>`);
2. **As 2 horas: não** — nunca foram gravadas; o reflog rastreia o HEAD, não o diretório de trabalho;
3. A conclusão: **comitar é o que protege** — a assimetria entre o comitado e o não comitado;
4. As práticas que decorrem: commits frequentes, `stash` antes de operações destrutivas, `status` antes de `--hard`.
</details>
