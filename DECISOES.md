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

## D-015 — 2026-08-04 — Banco de rascunho para os capítulos de escrita
**Contexto:** a partir do 03.11 os comandos alteram dados. Os gabaritos de 03.01 a 03.10 comparam com os números exatos de `aurora.db`, e um único `UPDATE` do aluno invalidaria todos eles.
**Decisão:** `codigo/cap11/preparar_rascunho.py` copia `aurora.db` para `dados/rascunho.db`, e todo exercício de escrita roda com `AURORA_BANCO=dados/rascunho.db`. O script é idempotente: rodá-lo de novo recomeça limpo.
**Consequência:** o aluno pode destruir o banco de propósito — e é instruído a fazê-lo, no AP3 do 03.11. A separação também ensina, por analogia direta, a distinção entre ambiente de teste e produção, que volta no módulo 09. Ambos os `.db` são gerados, nunca versionados.

## D-016 — 2026-08-04 — Executor em autocommit explícito
**Contexto:** o `codigo/sql.py` chamava `conexao.commit()` após cada comando de escrita, e o driver `sqlite3` do Python abria transações por conta própria. Consequência: um `ROLLBACK` escrito pelo aluno não desfazia nada — a demonstração central do 03.11 falhava em silêncio.
**Decisão:** `conexao.isolation_level = None` (autocommit), e remoção do `commit()` automático. Cada comando vale sozinho; `BEGIN`/`COMMIT`/`ROLLBACK` escritos pelo aluno funcionam como funcionariam num cliente real.
**Consequência:** o comportamento do laboratório passa a corresponder ao que o capítulo ensina. A própria correção virou conteúdo: o 03.11 §6.7 explica que toda ferramenta tem uma política de transação e que descobri-la é pré-requisito para confiar num `ROLLBACK`. Regressão dos capítulos 03.01–03.10 executada — nenhuma mudança de saída.

## D-017 — 2026-08-04 — Terceiro banco: `ddl.db` para os capítulos de estrutura
**Contexto:** o 03.12 cria, altera e destrói tabelas. Fazer isso no `aurora.db` invalidaria os gabaritos de 03.01–03.11; fazer no `rascunho.db` do 03.11 misturaria "alterar dados" com "alterar estrutura", que são assuntos e riscos diferentes.
**Decisão:** `codigo/cap12/preparar_ddl.py` cria `dados/ddl.db` **vazio**, apagando o anterior a cada execução. O script imprime a versão do SQLite e avisa se for anterior à 3.37, porque `STRICT` não existe antes disso.
**Consequência:** o módulo passa a ter três bancos com papéis distintos — `aurora.db` (leitura, imutável), `rascunho.db` (escrita de dados), `ddl.db` (estrutura). A separação é ela mesma conteúdo: prefigura ambientes separados, do módulo 09. O aviso de versão evita que um leitor com SQLite antigo aprenda a lição errada ao ver `STRICT` falhar — o mesmo cuidado com mensagens de erro do 02.07.

## D-018 — 2026-08-04 — Quarto banco: `indices.db` com 500.000 linhas, e o método de medição
**Contexto:** o efeito de um índice não aparece em 71 linhas. Sem uma tabela grande, o 03.14 seria um capítulo de afirmações — exatamente o que a spec proíbe.
**Decisão:** `codigo/cap14/preparar_indices.py` gera 500.000 eventos com `random.seed(42)` (números reproduzíveis) e quatro colunas de cardinalidade escolhida: `cliente_id` ~50.000 distintos, `valor` ~90.000, `data` 224, `tipo` 5. O `medir.py` acompanha, com três exigências de método: **conexão nova a cada medição**, **mediana** de 7 repetições, e medição **antes e depois**.
**Consequência:** o capítulo demonstra em vez de afirmar, e o próprio método virou conteúdo. A exigência da conexão nova nasceu de um erro real: na primeira medição, o plano em cache fez parecer que o índice tornava a consulta mais lenta; com conexão nova, o resultado honesto é que ele não ajuda nem atrapalha naquele caso. O §6.8 registra o episódio — medição errada é pior que nenhuma, porque produz um número, e números convencem. Os quatro bancos do módulo (`aurora`, `rascunho`, `ddl`, `indices`) permanecem gerados e fora do Git.

## D-019 — 2026-08-04 — Concorrência demonstrada com duas conexões, não com threads
**Contexto:** o 03.15 precisa mostrar *lost update*, bloqueio e isolamento — fenômenos que exigem dois clientes simultâneos e não cabem num arquivo `.sql`, que tem um só.
**Decisão:** `codigo/cap15/transacoes.py` abre duas conexões (`a` e `b`) e as intercala em **ordem explícita**, em vez de usar threads. Também usa `timeout=1.0` (o padrão de 5 s faria o leitor esperar cinco segundos para ver o `database is locked`) e repõe o saldo antes de cada cena.
**Consequência:** o exemplo falha **toda vez**, e não às vezes. Com threads, o resultado dependeria do escalonador e a cena central do capítulo seria intermitente — um exemplo de concorrência que só falha de vez em quando ensina menos que um que falha sempre. O gabarito do D1 usa o mesmo princípio para argumentar por que um teste de concorrência que passa "quase sempre" é pior que nenhum: ele vira teste instável, é desabilitado, e o defeito segue em produção com a bênção da automação.

## D-020 — 2026-08-05 — Anotações entram em 04.13 como "lista de campos", não como tipos
**Contexto:** a §21.1 da spec proíbe type hints até 04.13 e os introduz em 04.14. Mas `@dataclass` **não funciona** sem anotação: é ela que declara o campo. O capítulo 04.13 precisa de uma construção que a spec ainda não liberou.
**Decisão:** apresentar `nome: str` no 04.13 exclusivamente como **a forma de declarar um campo**, sem ensinar notação de tipos, e registrar em Caixa-preta 1 que ela é uma anotação de tipo, que o Python não a usa para nada em execução, e que o assunto é o 04.14. O capítulo transforma a restrição em conteúdo: a §6.2 demonstra que a anotação **não verifica nada** (`Produto(123, "abc")` passa) e que **sem ela o campo desaparece** do `__init__`, do `repr` e do `__eq__`.
**Consequência:** a proibição foi respeitada no espírito — nenhuma carga cognitiva de sistema de tipos — e o capítulo ganhou seu achado mais forte. O 04.14 herda uma pergunta já formulada pelo leitor ("então quem lê isso?") em vez de precisar motivá-la do zero, e o 04.15 herda a segunda ("e quem valida?"), preparada pela Caixa-preta 2 e pela contagem de linhas que o mini projeto pede.

## D-021 — 2026-08-05 — Arquivos de exemplo nunca levam nome de módulo da biblioteca padrão
**Contexto:** o arquivo natural para o 04.13 se chamaria `dataclasses.py`. Com esse nome, `import dataclasses` encontraria o arquivo do próprio leitor, e o erro seria `ImportError: cannot import name 'dataclass' from partially initialized module` — uma mensagem que não aponta para a causa.
**Decisão:** o arquivo é `codigo/cap13/dados.py`, com o motivo escrito no docstring e repetido na §10 do capítulo, estendido a `random.py`, `json.py` e `sqlite3.py`. Regra geral para o restante do manual: nenhum arquivo de exemplo recebe nome de módulo da biblioteca padrão.
**Consequência:** um erro clássico de iniciante vira conteúdo explícito em vez de armadilha herdada. E a regra fica valendo para os módulos seguintes, onde os nomes tentadores são mais numerosos — `logging.py` no 04.19, `datetime.py` no 04.18, `typing.py` no 04.14.

## D-022 — 2026-08-05 — Capítulo de ferramenta ganha um arquivo espelho que quebra de propósito
**Contexto:** o 04.14 precisa demonstrar a diferença entre o que o verificador encontra e o que a execução encontra. Um arquivo só não serve: se ele tem os defeitos, não roda; se roda, não tem os defeitos.
**Decisão:** dois arquivos por capítulo de ferramenta. `codigo/cap14/tipos.py` roda e passa limpo no `mypy`; `codigo/cap14/defeitos.py` reúne os defeitos, é apontado seis vezes pelo verificador e explode na primeira execução. O docstring de cada um declara seu papel, e a §10 pede as quatro execuções lado a lado.
**Consequência:** a comparação vira experimento em vez de afirmação — seis apontamentos contra um traceback, com dois defeitos que execução nenhuma mostraria. O padrão vale para os capítulos de ferramenta seguintes (04.19 logging, módulo 12 testes). E obrigou uma segunda regra: quando o próprio arquivo que roda contém um erro proposital, ele leva `# type: ignore[codigo]` com o motivo escrito — o que transformou a supressão em conteúdo (§6.8) em vez de deixá-la como ruído.

## D-023 — 2026-08-05 — Política de tipagem a partir daqui
**Contexto:** a §18.2 da spec introduz type hints em 04.14 e os torna obrigatórios do módulo 05 em diante. Falta dizer o que acontece nos capítulos 04.15–04.23, e o que fazer com os treze capítulos já escritos sem tipos.
**Decisão:** todo código novo a partir do 04.15 é tipado e deve passar em `mypy --strict`. O código de 04.01–04.13 **fica como está**, sem retrofit. Os apontamentos que o verificador faz nele são material do próprio 04.14 (§9 e D1): quatro apontamentos, todos corretos, todos propositais.
**Consequência:** o manual ganha um exemplo real de "projeto meio tipado", que é a situação em que quase todo profissional encontra um código pela primeira vez — e o D1 pede exatamente a habilidade que ela exige: classificar cada apontamento em defeito real, código proposital e limitação da ferramenta. Retrofitar os capítulos anteriores destruiria esse exemplo e contradiria a §18.2, que proíbe tipos até o 04.13 por carga cognitiva.

## D-024 — 2026-08-05 — A fronteira do manual: Pydantic na borda, dataclass no núcleo
**Contexto:** o 04.13 e o 04.15 oferecem duas formas de declarar campos com anotação, e nada na spec diz qual usar. Sem uma regra, os capítulos seguintes (módulos 05, 06 e 10) alternariam sem critério, e o leitor herdaria a dúvida.
**Decisão:** `BaseModel` apenas onde o dado **vem de fora do programa** — HTTP, formulário, CSV, fila, variável de ambiente. `@dataclass` no domínio, onde o dado já foi conferido. Todo modelo de borda leva `ConfigDict(extra="forbid")`. Validar o mesmo dado duas vezes é proibido, com uma exceção declarada: invariante de domínio que também protege caminhos internos (carga de banco, teste, migração).
**Consequência:** a regra deixou de ser estética e passou a ser medida — o D1 do 04.15 pede a justificativa pelos números da §13 (criar modelo custa 2,5× a dataclass; entrar e sair de JSON é 1,9× e 3,7× mais rápido; ler atributo é 48% mais caro), e a assimetria entre "validar uma vez" e "ler milhões de vezes" é o argumento inteiro. A separação também prepara o módulo 11: é a mesma fronteira entre domínio e infraestrutura, apresentada aqui como decisão concreta em vez de princípio abstrato.

## D-025 — 2026-08-05 — O laboratório do 04.16 usa Pydantic 1 × 2, e não um exemplo inventado
**Contexto:** o capítulo precisa demonstrar um conflito de versões. A saída cômoda seria descrever o problema em prosa, ou inventar um pacote de exemplo. As duas produzem um capítulo que afirma em vez de mostrar, o que a spec proíbe.
**Decisão:** `codigo/cap16/conflito.sh` cria dois ambientes de verdade e instala `pydantic==2.13.4` e `pydantic==1.10.13`, as mesmas versões que o leitor acabou de usar no 04.15. O `modelo.py` é escrito para funcionar numa e quebrar na outra por uma diferença real de API (`model_dump_json`, que só existe na 2). O script baixa ~60 MB, apaga e recria o laboratório a cada execução, e informa onde a pasta ficou.
**Consequência:** o conflito deixa de ser hipótese. E a escolha rendeu três achados que um exemplo inventado não teria: o rebaixamento silencioso com `pydantic_core` órfão, o `pip check` aprovando um ambiente quebrado, e a assimetria entre o `pip` (que quebra ao renomear a pasta) e o `python` (que não). O custo é a dependência de rede e de disco, declarada no cabeçalho do script e na §10.

## D-026 — 2026-08-05 — Ambiente virtual passa a ser obrigatório a partir do 04.16
**Contexto:** a §18.2 da spec proíbe venvs até o 04.15 e os introduz no 04.16, sem dizer o que fazer com os capítulos anteriores nem com os seguintes.
**Decisão:** todo projeto a partir do 04.17 começa criando `.venv` na pasta do projeto, com `requirements.txt` e `requirements-dev.txt` **escritos à mão** (nunca gerados por `pip freeze`) e `.venv/` no `.gitignore`. Os capítulos 04.01–04.15 continuam rodando no interpretador padrão, como a spec manda, e o 04.16 é o único lugar em que os dois modos coexistem — por necessidade da demonstração.
**Consequência:** a política de `requirements.txt` escrito à mão é uma escolha pedagógica com custo declarado no próprio capítulo (§6.6): ela reproduz pior que um arquivo de trava e documenta melhor, e o D1 pede a justificativa nos dois sentidos em vez de tratar uma das opções como certa. Arquivos de trava e `uv` ficam registrados na §14 como o que a indústria usa, sem virar requisito de um manual cujo objetivo aqui é entender o mecanismo.

## D-027 — 2026-08-05 — O capítulo de layout mede o limite do `src/` em vez de recomendá-lo sem ressalva
**Contexto:** a literatura sobre layout `src/` costuma afirmar que ele "garante que você testa o que distribui". A afirmação é atraente e é forte demais, e a spec proíbe conteúdo que afirme sem demonstrar (§19.4 item 6).
**Decisão:** o `vazamento.sh` tem seis cenas, e a sexta existe para medir o limite. Ela mostra que, depois de `pip install -e .`, um módulo solto na raiz **continua sendo encontrado** quando se roda da pasta do projeto — porque a pasta atual permanece no `sys.path` em `-c`, `-m` e sob o `pytest`. O capítulo formula então a garantia real: `src/` assegura que **o pacote** venha da instalação, e nada além disso.
**Consequência:** a recomendação fica mais fraca e verdadeira, e o capítulo ganha uma prática concreta em lugar da falsa segurança — o teste de um `cd` ("saia da pasta e rode de novo") e o teste completo (`pip install .` sem `-e`, em ambiente novo). O achado veio de uma verificação que contrariou o texto já escrito: o `pytest` na raiz passa nos **dois** layouts com o defeito presente, o que teria transformado a versão anterior do capítulo numa afirmação falsa.

## D-028 — 2026-08-05 — Todo projeto do manual passa a usar layout `src/` e `pyproject.toml`
**Contexto:** a §18.2 da spec adota layout `src/` a partir do módulo 06 e o ensina no 04.17. Faltava decidir o que fazer nos capítulos 04.18–04.23 e nos projetos do módulo 05.
**Decisão:** a partir do 04.18, qualquer projeto com mais de um módulo usa `src/` e `pyproject.toml`, com `tests/` fora de `src/`, `__init__.py` declarando `__all__`, imports absolutos e instalação com `pip install -e ".[dev]"`. Os arquivos soltos por capítulo continuam permitidos para demonstrações de um arquivo só — que é o que a maioria dos capítulos do módulo 04 usa. `codigo/cap17/projeto-aurora/` é o modelo de referência.
**Consequência:** o manual passa a ter um exemplo canônico que os módulos seguintes copiam em vez de reinventar, e a fronteira do D-024 fica visível no layout (`modelo.py` para o domínio, `esquemas.py` para a borda). O custo é que capítulos com projeto exigem `pip install -e .` antes de rodar, o que está registrado no `LEIAME.md` de cada projeto.

## D-029 — 2026-08-05 — Política de tempo do manual: uma função `agora()`, UTC em tudo
**Contexto:** o 04.18 mostra que cinco das oito formas comuns de obter um `datetime` produzem valores ingênuos, e que nenhum dos erros da categoria levanta exceção. Sem uma política escrita, os módulos 05 a 13 espalhariam `datetime.now()` por dezenas de arquivos.
**Decisão:** todo projeto do manual, a partir daqui, tem um módulo `tempo.py` com três funções — `agora()` (única forma de obter o instante atual, sempre em UTC), `para_exibir(momento, fuso)` e `de_texto_brasileiro(texto, fuso)`. `datetime.now()` sem argumento fica proibido em código novo; fusos são sempre `ZoneInfo("Regiao/Cidade")`, nunca offset fixo, exceto UTC; persistência sempre em ISO 8601 e UTC; e modelos de borda usam `AwareDatetime`.
**Consequência:** a política é auditável por busca de texto — `grep "datetime.now("` deve devolver uma ocorrência por projeto —, e, mais importante, torna os testes possíveis: uma função que chama `datetime.now()` diretamente não pode ser testada em 04/11/2018 sem mexer no relógio da máquina. Os testes das datas de transição que o D1 pede dependem inteiramente dessa costura, e essa é a razão principal da decisão, não a estética.

## D-030 — 2026-08-05 — `print` proibido em projeto a partir do 04.19, com uma exceção declarada
**Contexto:** a §18.2 da spec aceita `print` até o 04.18 e torna `logging` obrigatório a partir do 04.19. Aplicada ao pé da letra, a regra levaria a substituir **todo** `print`, inclusive o que é a saída legítima do programa.
**Decisão:** `print` fica proibido para mensagens de diagnóstico, progresso e erro. Continua obrigatório para a **saída do programa** — o relatório, o CSV, o resultado que alguém redireciona. A regra escrita é: `stdout` é o resultado, `stderr` é o diário. Todo projeto ganha um `registro.py` com `configurar(nivel, formato)`, chamado uma vez no ponto de entrada; nenhum outro módulo configura nada, e todos usam `logging.getLogger(__name__)`.
**Consequência:** a exceção é conteúdo, não concessão — o AP1 pede justamente para identificar quais `print` **não** deviam virar log, e a resposta ("todo programa de linha de comando tem pelo menos um") corrige o erro de fazer relatórios saírem com `INFO:` no meio. Os arquivos de demonstração dos capítulos continuam usando `print`, porque a saída deles **é** o conteúdo didático; a proibição vale para projetos.

## D-031 — 2026-08-05 — Demonstrações de estado global rodam em subprocessos
**Contexto:** o 04.19 precisa mostrar cinco configurações de log diferentes. A configuração é global ao processo, e `basicConfig` só tem efeito na primeira chamada (§6.3b) — um arquivo único mostraria a primeira cena e mentiria nas outras quatro.
**Decisão:** `codigo/cap19/demonstracao.py` roda cada cena num subprocesso, com o programa embutido como texto. O docstring declara o motivo, e a §10 do capítulo o repete: a necessidade do isolamento **é** parte do conteúdo.
**Consequência:** o padrão se estende a qualquer demonstração de estado global do manual — configuração de log, `sys.path` (já usado no 04.17), variáveis de ambiente, semente de geradores aleatórios. E ele evita a classe de erro em que um exemplo "funciona" porque herdou o estado do exemplo anterior, que é o mesmo problema do layout plano no 04.17: funcionar por acidente de contexto.
