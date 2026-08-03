# Questões de revisão — Módulo 02

10 objetivas + 5 discursivas. Usadas nas revisões D+7 (3 por capítulo) e D+30. Gabarito ao final.

## Objetivas

**Q1.** Quem expande o curinga em `rm *.log`?
a) O comando `rm` · b) O shell, antes de executar · c) O sistema de arquivos · d) O terminal

**Q2.** `wc -l vendas.csv` devolve 40001. Quantos registros de dados o arquivo tem?
a) 40001 · b) 40000 · c) 39999 · d) Impossível saber

**Q3.** `comando > saida.txt` e o erro continua aparecendo na tela porque:
a) O comando falhou · b) `>` redireciona apenas stdout; erros vão por stderr · c) O arquivo está cheio · d) Faltou `sudo`

**Q4.** Um diretório com permissão `r` mas sem `x` permite:
a) Entrar e listar · b) Listar os nomes, mas não acessar o conteúdo · c) Nada · d) Tudo, menos apagar

**Q5.** `export PATH="/home/eu/bin"` (sem `$PATH` ao final) causa:
a) Nada · b) Erro de sintaxe · c) Nenhum comando é encontrado até o terminal ser reaberto · d) Perda permanente do PATH

**Q6.** Em `set -euo pipefail`, o `-u` serve para:
a) Encerrar ao primeiro erro · b) Transformar variável não definida em erro · c) Fazer o pipe falhar · d) Ativar modo detalhado

**Q7.** Um commit guarda:
a) Só as linhas alteradas · b) O estado completo do projeto, com autor, data, mensagem e ponteiro para o pai · c) Apenas os arquivos preparados, sem histórico · d) Uma cópia compactada da pasta `.git`

**Q8.** `git diff --staged` compara:
a) Diretório de trabalho × área de preparo · b) Área de preparo × último commit · c) Duas branches · d) Local × remoto

**Q9.** Você está na `main` e quer trazer a branch `funcionalidade`. A sequência correta é:
a) `git switch funcionalidade` + `git merge main` · b) `git merge main funcionalidade` · c) `git switch main` + `git merge funcionalidade` · d) `git push funcionalidade main`

**Q10.** Um commit **já publicado** quebrou o sistema. O comando correto é:
a) `git reset --hard` · b) `git revert` · c) `git restore` · d) `git push --force`

## Discursivas

**D1.** Explique o mecanismo do PATH e use-o para diagnosticar dois problemas distintos: `command not found` num programa que está instalado, e um `python` que responde a versão errada.

**D2.** Descreva as três áreas do Git e justifique a existência da área de preparo com um exemplo concreto de uma manhã de trabalho.

**D3.** Um colega diz que branches são caras e prefere copiar a pasta do projeto para experimentar. Responda tecnicamente — o que é uma branch, quanto custa, e o que a cópia de pasta perde.

**D4.** Explique a diferença entre `git fetch` e `git pull` em termos das três camadas (branch local, rastreamento, remoto), e descreva uma situação em que usar `pull` seria a escolha errada.

**D5.** Você fez `git reset --hard HEAD~3` e perdeu 3 commits e duas horas de alterações não comitadas. Explique o que é recuperável, o que não é, e por que — e derive daí uma prática de trabalho.

---

# Gabarito

**Objetivas:** Q1-b `[02.02]` · Q2-b `[02.03]` · Q3-b `[02.04]` · Q4-b `[02.05]` · Q5-c `[02.06]` · Q6-b `[02.07]` · Q7-b `[02.08]` · Q8-b `[02.09]` · Q9-c `[02.10]` · Q10-b `[02.12]`

**D1 — pontos-chave** `[02.06]`: o PATH é uma lista ordenada de pastas, separadas por `:`, percorrida **na ordem** quando você digita um nome sem barra; a busca usa o **primeiro** arquivo com aquele nome **e** com bit de execução, e para ali. Diagnóstico 1 (`command not found` num programa instalado): a pasta do programa não está no PATH — `which -a`, `ls` na pasta de instalação, e acrescentar ao PATH. Diagnóstico 2 (versão errada): há **duas** instalações, e a antiga vem primeiro na lista — `which -a python` revela a fila, e a correção é colocar a pasta da versão desejada **no início**. *Equívoco típico:* tratar os dois como o mesmo problema ("reinstala"), sem citar a ordem.

**D2 — pontos-chave** `[02.08]`: diretório de trabalho (o que você edita), área de preparo (o que entra no próximo commit) e repositório (`.git/`, o histórico). Exemplo esperado: numa manhã você corrige um bug de cálculo **e**, de passagem, arruma a formatação de outro arquivo; sem a área de preparo, as duas mudanças entrariam no mesmo commit com uma mensagem vaga; com ela, você prepara e comita cada uma separadamente, produzindo dois pontos distintos de retorno e duas mensagens úteis. *Equívoco típico:* descrever as três áreas sem justificar a intermediária — que é exatamente o que a pergunta cobra.

**D3 — pontos-chave** `[02.10]`: uma branch é um arquivo de **41 bytes** em `.git/refs/heads/` contendo o identificador de um commit; criar não copia arquivo nenhum, e o custo é constante independentemente do tamanho do projeto. A cópia de pasta perde três coisas: (1) as correções feitas de um lado não aparecem no outro, e reuni-las depois é trabalho manual; (2) não há registro de **onde** as duas versões divergiram, que é o que permite ao merge saber o que comparar; (3) o histórico não acompanha — a cópia começa do zero. Fecho maduro: em sistemas anteriores ao Git, ramificar de fato copiava o projeto, e é dessa época que vem a intuição do colega.

**D4 — pontos-chave** `[02.11]`: `fetch` baixa os objetos e atualiza **apenas** a branch de rastreamento (`origin/main`) — sua branch e seus arquivos ficam intocados; `pull` é `fetch` + `merge`, e portanto altera sua branch, reescreve arquivos e pode gerar conflito. Situação em que `pull` é a escolha errada: quando você tem trabalho em andamento não comitado, ou está no meio de uma mudança delicada — um merge inesperado no meio disso mistura coisas e pode conflitar em cima de alterações soltas. O caminho seguro: `fetch`, inspecionar com `git log main..origin/main`, comitar ou guardar o que está em andamento, e só então incorporar.

**D5 — pontos-chave** `[02.12]`: **os 3 commits são recuperáveis** — o `reset` moveu um ponteiro, os objetos continuam no banco, e o `reflog` guarda o identificador anterior (`git reflog` + `git switch -c recuperado <id>`, que não fecha portas). **As duas horas não são** — nunca foram comitadas, portanto nunca entraram no banco de objetos, e o reflog rastreia movimentos do HEAD, não o conteúdo do diretório de trabalho. A prática que decorre: **comitar cedo e com frequência**, mesmo que imperfeito — commits podem ser reorganizados depois (`--amend`, `reset --soft`), trabalho não comitado não pode ser recuperado nunca. Complementos: `stash` antes de qualquer operação destrutiva e `git status` como reflexo antes de digitar `--hard`. *Equívoco típico:* responder só "sim, o reflog recupera" — a nota está em identificar as **duas** respostas.
