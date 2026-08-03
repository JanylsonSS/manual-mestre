# Gabaritos — Capítulo 02.08

Abra somente após tentativa honesta.

## A1 — Em qual área está?

1. Diretório de trabalho — **não rastreado** (`??`). O Git vê o arquivo, mas não o acompanha.
2. Área de preparo — **preparado** (`A`). Continua também no diretório de trabalho: as áreas não são exclusivas.
3. Repositório — **versionado**; o diretório está limpo (`git status` sem nada a reportar).
4. Diretório de trabalho — **modificado** (` M`): existe a versão no histórico e a versão editada, e elas divergem.
5. **Preparado** de novo (`M `) — a nova versão está na mesa, esperando a foto.
6. Diretório de trabalho — **ignorado**: o Git enxerga o arquivo e o omite deliberadamente do `status`.

**Critério:** 6/6, com o item 2 reconhecendo que o arquivo está nas duas áreas.

## A2 — Lendo o status

1. Um arquivo novo foi criado e o Git nunca o viu — nenhum `add` foi feito.
2. O arquivo novo foi preparado com `git add` — ainda não houve commit.
3. Um arquivo **já versionado** foi editado e ainda não foi preparado. (Note a posição da letra: a segunda coluna é o diretório de trabalho.)
4. Um arquivo versionado foi editado **e preparado** (primeira coluna), e outro arquivo novo foi criado sem `add`. É exatamente o cenário do passo 6 do capítulo.

**Critério:** 4/4; identificar que a **coluna** da letra distingue "preparado" de "modificado" vale ponto extra.

## A3 — Verdadeiro ou falso

1. **F** — Git é local; só `push`, `pull` e `clone` usam rede.
2. **F** — o commit é a fotografia do estado completo; a economia acontece por dentro, reutilizando objetos.
3. **F** — os arquivos permanecem; o que some é o **histórico**.
4. **F** — GitHub é um serviço de hospedagem, de empresa diferente; Git é um programa livre e gratuito.
5. **F** — é um resumo criptográfico calculado a partir do **conteúdo** (e do pai).
6. **V**.
7. **F** — mudam todos os posteriores, porque cada identificador depende do pai.
8. **V** — é o significado de "distribuído".

**Critério:** 8/8 com as falsas corrigidas. A 2 e a 7 são as que mais aparecem em entrevista.

## A4 — Mensagens de commit

| # | Avaliação | Reescrita |
|---|---|---|
| 1 | Ruim — não informa nada | `Atualiza limites de validação do CSV de vendas` |
| 2 | **Boa** — imperativo, específica, explica o caso | — |
| 3 | Ruim — descreve arquivos, não a mudança; e são **três** commits disfarçados de um | separar: um commit por mudança lógica |
| 4 | Ruim — "work in progress" não sobrevive a seis meses | descrever o estado real: `Esboça leitura do CSV (incompleto)` |
| 5 | **Boa** | — |
| 6 | Ruim — corrige o quê? | `Corrige acentuação ao ler CSV em Windows` |

**Critério:** as 4 ruins identificadas e reescritas com verbo no imperativo e objeto específico. O item 3 merece a observação de que o problema não é só a mensagem — é o commit ter escopo demais.

## AP1 — O laboratório

**Saídas esperadas de `git status --short`:** `?? arquivo` → `A  arquivo` → (vazio) → ` M arquivo`.

**Colunas de `git log --oneline`:** os 7 primeiros caracteres do identificador do commit + a primeira linha da mensagem. A ordem é do **mais recente para o mais antigo** — percorrendo a corrente de trás para frente, que é como o grafo se lê.

**Erro esperado:** esquecer de configurar `user.name`/`user.email` e receber um aviso do Git antes do primeiro commit. A configuração local (`git config user.name "..."`) resolve para aquele repositório; o `--global` vale para a máquina inteira (02.09).

**Critério:** os quatro estados registrados com a saída literal, e a explicação das colunas do log.

## AP2 — A área de preparo trabalhando

**Sequência de referência:** edite os três arquivos; depois `git add a.py b.py` → `git commit -m "..."` (a mudança lógica dupla) → `git add c.md` → `git commit -m "..."`.

**Observação esperada:** entre os dois commits, o `git status --short` mostra o terceiro arquivo ainda pendente — a prova visual de que a área de preparo **seleciona** em vez de arrastar tudo. Quem tenta obter o mesmo resultado com `git add .` acaba com um único commit e descobre, na prática, por que a área intermediária existe.

**Critério:** dois commits temáticos no `git log --oneline`, com mensagens que fazem sentido isoladas.

## AP3 — Autópsia do `.git`

**Respostas de referência:**

1. `objects/`, `refs/`, `HEAD`, `config`, `index`, `hooks/`, `logs/`.
2. `HEAD` contém `ref: refs/heads/main` (ou `master`, conforme a versão do Git) — um ponteiro para o ponteiro da linha de trabalho atual, e não o identificador diretamente.
3. `git count-objects` mostra a contagem de objetos soltos.
4. Um commit que altera **um** arquivo acrescenta tipicamente **três** objetos: o blob (novo conteúdo), a tree (o diretório que mudou) e o commit.
5. Porque o Git só guarda o que mudou de fato: os demais arquivos continuam apontando para os blobs antigos, que já existiam no banco. É a resposta à pegadinha da seção 15 — o modelo é de fotografia, o armazenamento é de reaproveitamento.

**Critério:** o item 5 explicado com as palavras "blob", "tree" e "reaproveitamento" (ou equivalentes próprios).

## D1 — O histórico que conta uma história

**Roteiro de referência (as 6 mensagens):**

```text
1. Cria script de análise de vendas
2. Extrai cálculo do total para uma função
3. Trata CSV inexistente com mensagem clara
4. Corrige total ignorando linhas vazias do CSV
5. Ajusta formatação conforme PEP 8
6. Documenta uso do script no README
```

**O commit de dois arquivos (item c):** o de nº 6 é o candidato natural (README + docstring no script) ou o nº 3 (o tratamento de erro no script + a nota no README sobre o comportamento). O critério é conceitual: **os dois arquivos mudaram pela mesma razão**.

**Tabela final esperada (item d):** para cada commit, "o que uma pessoa de fora entenderia" deve ser respondível **sem abrir o código** — se você precisa olhar o conteúdo para explicar, a mensagem falhou.

**Reflexão esperada:** a estratégia `_v2_final` guarda **estados**, o Git guarda **decisões**. A diferença aparece nas três perguntas do início do capítulo: com arquivos numerados, "o que mudou entre a v2 e a v3?" exige comparar manualmente, "por que mudou?" não tem resposta em lugar nenhum, e "como duas pessoas trabalham juntas?" não tem solução. Some-se que o Git guarda tudo num único lugar (a pasta `.git`), com autoria e data automáticas, e que qualquer ponto do passado é recuperável por inteiro — não só um arquivo, o projeto todo. O custo é aprender um modelo; o retorno é permanente, e vale para todo projeto que você tocar pelo resto da carreira.

**Critério de "está bom":** 6 commits, cada um com uma mudança coerente; mensagens no imperativo, específicas e curtas; ao menos um commit com dois arquivos justificado; a tabela do item (d) completa; a reflexão citando "estados × decisões" ou equivalente próprio.
