# DECISOES.md — Registro de decisões de geração

Decisões tomadas durante a geração que a especificação não cobria (§34.3). Nunca apagar entradas; superar com nova entrada que referencia a anterior. Toda sessão de geração lê este arquivo antes de gerar.

## D-001 — 2026-07-30 — Nome do arquivo da especificação
**Contexto:** a árvore do §5 prevê `manualMestre.md` na raiz, mas o arquivo existente chama-se `manualMestre_v3.0.md`.
**Decisão:** manter o nome `manualMestre_v3.0.md` e referenciá-lo assim em todos os links. Renomear exigiria tocar um arquivo que só muda via §35.
**Consequência:** links internos ao repositório apontam para `manualMestre_v3.0.md`.

## D-002 — 2026-07-30 — Seção 10 em capítulos sem código executável
**Contexto:** os capítulos 00.01 e 00.02 são conceituais e antecedem a montagem do ambiente (00.03). O template exige a seção "10. Código comentado", e o §15 manda que seção não aplicável exista e explique como se aplica.
**Decisão:** nesses capítulos, a seção 10 existe, declara explicitamente que o capítulo não produz código executável (o ambiente ainda não existe) e aponta onde o primeiro código aparece (00.03). A pasta `codigo/capNN/` correspondente não é criada.
**Consequência:** vale para qualquer capítulo futuro comprovadamente sem código; a linha de metadados usa `Código: —`.

## D-003 — 2026-07-30 — Seção 11 (Erros comuns) em capítulos sem código
**Contexto:** o §15 exige mensagens de erro reais do interpretador na seção 11, impossíveis em capítulo sem código.
**Decisão:** em capítulos conceituais, a seção 11 cataloga **erros de método** (formato Sintoma → Causa → Correção mantido), sem bloco de mensagem de interpretador.
**Consequência:** o formato tríplice é preservado; a exigência de mensagem real fica restrita a capítulos com código.

## D-004 — 2026-07-30 — Volumes mínimos de entrevista no módulo 00
**Contexto:** o §30 exige por módulo 10 conceituais + 5 de código + 5 pegadinhas + 3 de decisão, mas o módulo 00 não ensina código.
**Decisão:** o módulo 00 fica dispensado dos volumes mínimos e dos desafios de código (`entrevistas/desafios.md` explica e aponta os treinos equivalentes); os volumes valem integralmente a partir do módulo 01.
**Consequência:** `00-Introducao/entrevistas/` contém 13 perguntas (conceituais, decisão e pegadinhas) e nenhum desafio de código.

## D-005 — 2026-07-30 — Simulado do módulo 00 e nomenclatura da variante B
**Contexto:** a árvore do §5 lista `Simulados/modulo-01.md ... modulo-13.md` (sem o 00), mas o §8 e o §27 exigem CP2 para todo módulo; o §28 exige variante B sem definir o nome do arquivo.
**Decisão:** existe `Simulados/modulo-00.md`; variantes B seguem o padrão `modulo-NN-b.md`.
**Consequência:** todos os módulos, inclusive o 00, fecham com simulado CP2 em variantes A e B.

## D-006 — 2026-07-30 — Escala reduzida do fechamento do módulo 00
**Contexto:** o §15 prevê mini projeto de módulo de 3–6 h e o §36 prevê cheatsheet "por tecnologia", mas o módulo 00 tem ~6 h totais e não ensina tecnologia.
**Decisão:** o mini projeto do módulo 00 tem ~1h30 (consolidação da calibração); a cheatsheet do módulo é `Recursos/cheatsheets/metodo.md` (método de estudo, com referências `MM.CC`).
**Consequência:** exceção única do módulo 00; do módulo 01 em diante valem as escalas e o padrão "1 cheatsheet por tecnologia" da spec.

## D-007 — 2026-07-31 — Comprimento máximo de linha no código
**Contexto:** a PEP 8 recomenda 79 caracteres; o §18 da spec não fixa um limite, e os exemplos do manual usam blocos de código que precisam caber na leitura em tela dividida.
**Decisão:** adotar **até 100 caracteres** por linha nos arquivos de `codigo/`, com quebra dentro de parênteses quando necessário. O capítulo 01.25 documenta a escolha ao aluno.
**Consequência:** vale para todos os módulos; quando o `ruff` for configurado (módulo 12), a regra de comprimento usará 100.

## D-009 — 2026-07-31 — Shell de referência do módulo 02 no Windows
**Contexto:** o módulo 02 ensina comandos Unix, mas o aluno pode estar no Windows, onde o shell padrão (PowerShell/cmd) tem outra sintaxe. A spec não define o ambiente de referência.
**Decisão:** o ambiente de referência é **bash** (Linux/macOS nativo; no Windows, o **Git Bash** instalado no 00.03 — alternativa mencionada: WSL). Todos os comandos e saídas dos capítulos assumem bash; diferenças relevantes do PowerShell aparecem em callout 📌 quando puderem confundir.
**Consequência:** vale para todo o módulo 02 e para os capítulos de terminal dos módulos 08 e 09; a `Recursos/ambiente/windows.md` já orienta a instalação do Git Bash.

## D-008 — 2026-07-31 — Ordenação por campo antes do 04.02
**Contexto:** vários capítulos do módulo 01 precisam de "top N por valor", mas `sorted(..., key=...)` com função só é ensinado em 04.02 (funções como valores).
**Decisão:** até o 04.02, ordenações por campo usam o padrão **acumulador de máximo repetido** (com cópia do dicionário), sempre com comentário citando a alternativa idiomática futura. Formas prontas sem função (`key=str.lower`) são permitidas quando apresentadas.
**Consequência:** o mini projeto do 01.25 e os gabaritos correspondentes trazem a solução artesanal comentada; a refatoração é sugerida como exercício no módulo 04.

## D-010 — 2026-07-31 — Git ensinado por modelo antes dos comandos
**Contexto:** o §15 exige que todo capítulo tenha seção de código comentado, e o mapa do módulo 02 reserva quatro capítulos para Git (02.08–02.11). A prática comum de ensinar Git é começar pelos comandos (`init`, `add`, `commit`), o que produz decoreba e paralisia quando algo sai do roteiro.
**Decisão:** o capítulo **02.08 é exclusivamente conceitual** — três áreas, quatro estados, grafo de commits e conteúdo do `.git` —, e os comandos aparecem apenas como demonstração observável (o script `ciclo_do_git.sh` imprime o `git status` em cada estado). A operação do dia a dia fica no 02.09.
**Consequência:** o 02.08 não tem exercícios de "decorar comando"; seus exercícios cobram leitura de estado e qualidade de mensagem. O mesmo padrão (modelo antes da sintaxe) vale para o módulo 05 (bancos) e o 08 (containers).

## D-011 — 2026-07-31 — Remotos demonstrados sem depender de internet
**Contexto:** o §32 exige que todo código do manual seja executável e verificado, mas o capítulo 02.11 (remotos e GitHub) depende de rede e de uma conta em serviço externo — impossível de validar no ambiente de geração e frágil na máquina do aluno.
**Decisão:** o script do capítulo (`codigo/cap11/remoto_local.sh`) usa um repositório **bare** local como servidor, demonstrando `clone`, `push`, `fetch`, `pull` e a recusa `non-fast-forward` **sem rede**. As instruções de GitHub (chave SSH, criação do repositório, PR) ficam na seção 9 (aplicação prática), como passo a passo conferível pelo aluno.
**Consequência:** vale como padrão para todo capítulo que dependa de serviço externo — a mecânica é demonstrada localmente e o serviço aparece na aplicação prática. Aplica-se ao módulo 05 (bancos), 08 (registries) e 09 (deploy).

## D-012 — 2026-07-31 — Nome da linha principal: `main`
**Contexto:** versões antigas do Git criam a linha principal como `master`; versões recentes e todos os serviços de hospedagem usam `main`. O aluno pode ter qualquer uma das duas.
**Decisão:** o manual adota **`main`** em todo o texto e nos scripts (`git init -b main`, `git config --global init.defaultBranch main`), com nota no 02.08 informando que versões antigas mostram `master` e que os dois são apenas nomes de branch.
**Consequência:** vale para todos os módulos seguintes; os scripts que criam repositórios de laboratório passam `-b main` explicitamente para produzir a mesma saída em qualquer versão.

## D-013 — 2026-08-03 — Executor Python em vez da CLI do SQLite
**Contexto:** o §32 exige que todo código do manual seja executável e verificado. A CLI `sqlite3` é um download extra no Windows, e ferramentas gráficas (DB Browser, extensões do VS Code) não produzem saída copiável para o texto do capítulo.
**Decisão:** o laboratório do módulo 03 é operado por **`codigo/sql.py`**, um executor em Python (biblioteca padrão, ~130 linhas) que roda um arquivo `.sql`, uma consulta passada como argumento, ou abre modo interativo — e formata o resultado em tabela, exibindo `NULL` explicitamente. Os arquivos `.sql` permanecem SQL puro e portável.
**Consequência:** zero instalação além do Python do 00.03; toda saída dos capítulos é verificável; ferramentas gráficas são mencionadas como conforto opcional, nunca como pré-requisito. O caminho do banco respeita `AURORA_BANCO` (02.06).

## D-014 — 2026-08-03 — Banco de laboratório pré-construído
**Contexto:** o mapa da spec põe a modelagem no 03.16, mas os capítulos 03.03 a 03.10 precisam de dados para consultar desde o início.
**Decisão:** o 03.01 entrega o schema da Aurora **pronto e populado** (clientes, produtos, pedidos, itens_pedido — 71 linhas), com casos de ensino embutidos de propósito: um cliente sem compras (anti-join, 03.08), um e-mail `NULL` (03.03), uma cidade `NULL` (03.05), um produto nunca vendido (03.08) e pedidos cancelado/pendente (filtros, 03.03). O aluno **consulta** um schema existente antes de **projetar** o próprio.
**Consequência:** o 03.16 reconstrói o mesmo schema do zero, agora justificando cada decisão — o aluno compara a própria modelagem com a que usou por quinze capítulos. O arquivo `.db` é gerado, nunca versionado (`*.db` já está no `.gitignore`).
