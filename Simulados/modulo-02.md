# Simulado CP2 — Módulo 02 (variante A)

**Tempo:** 60–90 min · **Composição:** 10 objetivas + 3 discursivas + 1 prático (~45 min)
**Aprovação:** ≥ 8/10 objetivas **e** prático ≥ 3 na rubrica. 6–7/10 ou prático = 2 → revisão dirigida + [variante B](modulo-02-b.md). ≤ 5/10 → refazer o módulo em ritmo de revisão.
**Regra de honestidade:** sem consultar durante as objetivas e discursivas; o prático é de consulta livre. Gabarito no fim — depois de terminar tudo.

## Objetivas

**Q1.** `ls relatorio *.txt` (com espaço antes do `*`) faz o quê?
a) Lista os `.txt` que começam com "relatorio" · b) Lista o arquivo `relatorio` **e** todos os `.txt` · c) Erro de sintaxe · d) Lista apenas o arquivo `relatorio`

**Q2.** `grep -c "campinas" vendas.csv` devolve 2, mas há 5 vendas na cidade. A causa mais provável é:
a) O arquivo está corrompido · b) Busca sensível a maiúsculas · c) `grep` conta arquivos, não linhas · d) Faltou o pipe

**Q3.** `sort | uniq -c` é o idioma correto porque `uniq` sozinho:
a) Não conta · b) Compara cada linha apenas com a **anterior** · c) Exige arquivo, não aceita pipe · d) Ignora linhas vazias

**Q4.** Um script tem `chmod +x`, o caminho está certo, e `./script.py` produz `syntax error near unexpected token`. O suspeito nº 1 é:
a) Permissão insuficiente · b) Shebang ausente ou errado · c) Python não instalado · d) Arquivo vazio

**Q5.** Sem `export`, uma variável definida no shell:
a) Não existe · b) Existe no shell atual, mas não é herdada por processos filhos · c) É herdada por todos os processos · d) Vira variável de sistema

**Q6.** Num script com `set -e`, `grep xyz arquivo.txt` sem resultado:
a) Não afeta nada · b) Encerra o script, porque `grep` devolve código ≠ 0 · c) Gera aviso e continua · d) Devolve string vazia

**Q7.** Apagar a pasta `.git` de um projeto:
a) Apaga os arquivos do projeto · b) Apaga o histórico; os arquivos atuais permanecem · c) Não faz nada, o Git recria · d) Apaga apenas o último commit

**Q8.** Você faz `git add arquivo.py`, edita o arquivo de novo e comita. O commit grava:
a) A versão mais recente · b) A versão do momento do `add` · c) As duas, em commits separados · d) Erro: o arquivo está em dois estados

**Q9.** A `main` tem 10 commits. Você cria uma branch, muda para ela e faz 3 commits. A `main` agora tem:
a) 13 · b) 10 · c) 3 · d) Depende do merge

**Q10.** `git fetch origin` altera:
a) Sua branch e seus arquivos · b) Apenas a branch de rastreamento `origin/main` · c) O repositório remoto · d) Nada, é somente leitura sem efeito

## Discursivas

**D1.** Explique por que um script de backup sem `set -euo pipefail` pode apagar o arquivo original sem ter feito a cópia — e descreva o que cada uma das três opções teria evitado.

**D2.** Um colega afirma: "vou colocar a senha do banco no `config.py` por enquanto, e removo antes de publicar no GitHub". Explique tecnicamente por que o plano falha, e apresente a alternativa correta, com o procedimento caso a senha já tenha sido publicada.

**D3.** Descreva a diferença entre `reset` e `revert` e explique por que a pergunta "já foi publicado?" é a única que precisa ser respondida para escolher entre eles.

## Prático (~45 min, consulta livre)

**O auditor do repositório.** Escreva `auditar.sh <pasta-do-repositorio>` que produz um relatório de saúde de um repositório Git:

1. **Valide** a entrada: sem argumento → mensagem de uso em stderr e `exit 2`; pasta inexistente ou sem `.git` → erro e `exit 1`.
2. **Colete e imprima**: número de commits, número de branches locais, número de arquivos rastreados, e a data do último commit.
3. **Verifique** (cada achado impresso em **stderr**, com o motivo):
   - existe `.gitignore`?
   - algum arquivo rastreado parece ser segredo (`.env`, `*.key`, nomes com "senha"/"token")?
   - algum arquivo rastreado é um artefato gerado (`__pycache__`, `*.pyc`, `*.log`)?
   - há commits com mensagem de menos de 15 caracteres? (liste-os)
4. **Conclua** com um resumo e `exit 0` se não houver achados, `exit 1` se houver.
5. Use `set -euo pipefail`, ao menos duas funções, aspas em todas as variáveis, e trate o caso "grep sem resultado" corretamente.

Teste em dois repositórios: um saudável (o do Manual Mestre) e um que você estrague de propósito (comite um `.env` e um commit com mensagem `wip`).

**Rubrica reduzida (0–4 cada):** Funcionalidade (5 requisitos) · Robustez (nenhum erro não tratado; os três cenários de entrada testados) · Qualidade (funções coesas, stderr/exit corretos, aspas).
**Aprovação: ≥ 3 de média, nenhum < 2.**

---

# Gabarito

**Objetivas:** Q1-b `[02.02]` · Q2-b `[02.04]` · Q3-b `[02.04]` · Q4-b `[02.05]` · Q5-b `[02.06]` · Q6-b `[02.07]` · Q7-b `[02.08]` · Q8-b `[02.09]` · Q9-b `[02.10]` · Q10-b `[02.11]`

**D1 — pontos-chave** `[02.07]`: por padrão, o shell **ignora falhas** e segue para o comando seguinte — o `cp` falha (destino inexistente, disco cheio, permissão), o `rm` executa mesmo assim, e o `echo "Backup concluído"` mente com código de saída 0. `set -e` teria encerrado o script na linha do `cp`, antes do `rm`. `set -u` teria pego o caso vizinho: uma variável de caminho digitada errado vira string vazia, e `rm -r "$PAST/"` apaga o lugar errado. `pipefail` cobre a variante com pipe (`tar ... | gzip > backup.gz`): sem ele, se o `tar` falhar e o `gzip` funcionar, o pipe reporta sucesso sobre um arquivo vazio. *Equívoco típico:* explicar só o `-e`.

**D2 — pontos-chave** `[02.06, 02.09, 02.11]`: o plano falha porque o Git guarda **todas as versões**, não só a atual — remover o arquivo antes de publicar não remove os commits anteriores que o continham, e qualquer pessoa que clone recebe o histórico completo. Alternativa correta: valor no **ambiente** (`os.environ.get("DATABASE_URL", padrao)`), `.env` local com permissão 600 e no `.gitignore` desde o primeiro commit, `.env.example` versionado com as chaves e valores fictícios. Se já foi publicado, a ordem importa: **(1) revogar a credencial** — considere-a comprometida, porque repositórios públicos são varridos continuamente; (2) gerar nova e movê-la para o ambiente; (3) só então limpar o histórico, sabendo que isso reescreve commits e não alcança clones existentes. *Equívoco típico:* propor `git rm` como se resolvesse — o arquivo sai, a credencial continua comprometida.

**D3 — pontos-chave** `[02.12]`: `reset` **move o ponteiro** da branch, fazendo commits deixarem de pertencer à história — reescreve o passado; `revert` calcula o inverso das mudanças e grava como um **commit novo** — acrescenta ao passado. A pergunta "já foi publicado?" é suficiente porque ela determina se o passado é **só seu** ou compartilhado: enquanto for local, reescrever é barato e invisível; depois de publicado, outras máquinas já têm aqueles commits com aqueles identificadores, e reescrever produz históricos incompatíveis, push recusado e, se forçado, perda do trabalho alheio. Complemento maduro: a mesma lógica se aplica a `commit --amend` e à exceção controlada (branch pessoal publicada, `--force-with-lease`).

**Prático — referência de correção:** a validação dos três cenários de entrada (sem argumento → 2, pasta sem `.git` → 1, correta → 0/1 conforme achados) é o item que mais separa; os achados **precisam** ir para stderr, verificável com `./auditar.sh repo > /dev/null` (os problemas continuam aparecendo); `grep` sem resultado devolve 1 e, com `set -e` + `pipefail`, encerraria o script — o `|| true` é obrigatório e sua ausência é o defeito mais comum; `git ls-files` é o caminho para listar rastreados; `git log --format="%h %s" | awk 'length($0) < 15'` (ou equivalente) para as mensagens curtas. Um script que funciona no repositório saudável mas quebra no estragado não passa.
