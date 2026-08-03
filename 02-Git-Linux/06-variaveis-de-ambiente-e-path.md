# 02.06 — Variáveis de ambiente e PATH

> **Módulo 02 — Git e Linux** · Nível: N2 · Tempo estimado: 2h30 · Código: `codigo/cap06/`

## 1. Objetivo

- **Explicar** o que são variáveis de ambiente e como o shell as usa.
- **Descrever** como o sistema encontra programas via **PATH** — fechando o arco aberto no 00.03.
- **Configurar** variáveis temporárias e persistentes; **ler** valores com `echo` e `env`.
- **Antecipar** o uso profissional: configuração por ambiente e segredos fora do código.

Ao final, `command not found` deixa de ser mistério, seus scripts viram comandos de verdade — e você entende por que senhas nunca devem estar no código.

---

## 2. Pré-requisitos

- [02.05 — Permissões e processos](05-permissoes-e-processos.md) — o `./` que você ainda precisa digitar é o que este capítulo elimina.
- [00.03 — Preparando o ambiente](../00-Introducao/03-preparando-o-ambiente.md) — **a dívida deste capítulo**: lá o PATH foi apresentado como "agenda de endereços"; aqui a agenda se abre.

**Autoteste:** (1) Por que `command not found` quase nunca significa "não instalado"? (2) Por que você precisa do `./` para executar um script na pasta atual? (3) O que você fez, no 00.03, quando o Python não era reconhecido? As três apontam para o mesmo lugar.

---

## 3. Motivação

Duas perguntas ficaram penduradas desde o começo da trilha.

A primeira é do **00.03**: você marcou uma caixinha chamada "Add python.exe to PATH" durante a instalação, e o manual explicou que "PATH é a lista de endereços onde o sistema procura programas". A explicação bastou para resolver o problema — e não explicou o mecanismo. Por que uma **lista de pastas** determina o que você pode digitar no terminal? Por que reabrir o terminal resolve? Por que a mesma máquina responde `python` numa janela e não em outra?

A segunda é do **02.05**: você tornou seus scripts executáveis, e ainda precisa digitar `./backup.sh` em vez de `backup.sh`. O `./` incomoda — e a razão dele existir é a mesma da primeira pergunta.

Mas há um terceiro motivo, e é o mais importante para a sua carreira. Todo sistema profissional precisa de **configuração**: o endereço do banco de dados, a chave da API de pagamento, a senha do e-mail, o modo de operação (desenvolvimento ou produção). Essas informações **não podem estar no código** — porque o código vai para o Git (a partir do 02.09), e o Git vai para o GitHub (02.11), e senha em repositório público é incidente de segurança real, que acontece todos os dias com desenvolvedores experientes.

A solução que a indústria adotou tem nome, tem princípio documentado (os *12 fatores*, que o 09.04 formaliza) e começa exatamente aqui: **configuração vive no ambiente, não no código**. As variáveis de ambiente são o mecanismo.

Este capítulo resolve isso assim: abre o PATH por completo, apresenta variáveis de ambiente como o sistema de configuração do sistema operacional, mostra como torná-las persistentes — e antecipa o padrão `.env` que o Atlas usará quando tiver banco de dados e chaves de API.

---

## 4. Modelo mental

> 🧠 **Modelo mental**
> Variáveis de ambiente são um **quadro de avisos que cada processo herda ao nascer**. Quando o shell executa um comando, ele entrega ao novo processo uma cópia do seu quadro — e o programa lê dali as informações de que precisa (onde procurar coisas, qual idioma usar, onde fica a pasta pessoal). O **PATH** é o aviso mais importante: uma **lista ordenada de pastas** que o shell percorre, **de cima para baixo**, quando você digita um nome de comando. Achou na primeira pasta? Usa e para de procurar — e é por isso que "ordem no PATH" decide qual versão de um programa você executa.

**Exercício de previsão.** O seu PATH é `/usr/local/bin:/usr/bin:/bin`. Existem dois programas chamados `python`: um em `/usr/bin/python` (versão 3.9) e outro em `/usr/local/bin/python` (versão 3.12). Sem rodar, decida: qual roda quando você digita `python`? E se você digitar `./python` estando em `/usr/bin`?

*Resposta comentada:* roda o **3.12**, de `/usr/local/bin` — porque essa pasta vem **primeiro** na lista, e a busca para no primeiro achado. Já `./python` executa **exatamente** o arquivo daquela pasta (o 3.9), porque o `./` é um caminho explícito e não usa o PATH. Se você respondeu "o 3.9, porque `/usr/bin` é o padrão", acabou de entender o erro nº 2 do 00.03 — aquele em que a máquina respondia uma versão antiga do Python que você jurava ter atualizado.

---

## 5. Analogia

Variáveis de ambiente são as **instruções afixadas na parede de uma oficina**. Todo funcionário que entra (cada processo) lê a parede e trabalha conforme o que está lá: "as ferramentas ficam nesses três armários, nesta ordem" (PATH), "o idioma dos manuais é português" (LANG), "a sua bancada é esta" (HOME).

Duas propriedades importam. Primeira: quem entra **recebe uma cópia** das instruções — se um funcionário rabisca a própria cópia, a parede da oficina não muda, e o funcionário seguinte lê a original (é por isso que uma variável definida dentro de um script não sobrevive quando ele termina). Segunda: a **ordem dos armários** decide qual ferramenta você pega quando há duas com o mesmo nome — exatamente o comportamento do PATH.

**Onde a analogia quebra:** paredes de oficina são visíveis a todos; variáveis de ambiente são **por processo**, e um programa pode receber um quadro diferente do outro. E há uma consequência prática que a analogia não sugere: como cada processo tem sua cópia, **alterar variáveis é sempre local** — a menos que você altere o arquivo de configuração que o shell lê ao nascer (a seção 6 mostra como).

---

## 6. Teoria

### Lendo e criando variáveis

```bash
echo $HOME                  # imprime o valor (o $ pede o CONTEÚDO)
echo $USER $SHELL $PWD      # várias de uma vez
env                         # lista TODAS as variáveis de ambiente
env | grep PATH             # filtrando (o pipe do 02.04)

NOME="Aurora"               # cria uma variável do SHELL (só aqui)
echo $NOME                  # Aurora
echo "Bem-vindo à $NOME"    # interpolação: aspas duplas expandem o $
echo 'Bem-vindo à $NOME'    # aspas simples NÃO expandem — sai literal
```

A distinção das aspas é a mesma de sempre: **duplas expandam variáveis, simples não**. É a fonte de metade dos bugs em scripts de shell.

### Variável de shell × variável de ambiente

```bash
NOME="Aurora"               # variável do SHELL: só este shell enxerga
export NOME="Aurora"        # variável de AMBIENTE: processos filhos herdam
export NOME                 # exporta uma já existente
```

A diferença aparece quando você executa um programa: ele recebe as **exportadas**, não as locais do shell. É o "quadro de avisos herdado" do modelo mental — e a razão de scripts precisarem de `export` para passar configuração adiante.

### As variáveis que você vai encontrar

| Variável | O que guarda |
|---|---|
| `PATH` | lista de pastas onde procurar programas (a estrela do capítulo) |
| `HOME` | sua pasta pessoal (o `~`) |
| `USER` | seu nome de usuário |
| `SHELL` | o shell padrão |
| `PWD` | a pasta atual (atualizada a cada `cd`) |
| `LANG` | idioma e codificação (`pt_BR.UTF-8`) |
| `EDITOR` | editor preferido (usado por Git e outros) |

### O PATH, aberto

```bash
echo $PATH
```

```text
/usr/local/bin:/usr/bin:/bin:/home/voce/.local/bin
```

É uma única string com pastas separadas por **`:`** (no Windows, `;`). Para ver uma por linha — e treinar o pipe:

```bash
echo $PATH | tr ':' '\n'
```

Quando você digita `git`, o shell percorre essa lista **na ordem** procurando um arquivo executável chamado `git`. Achou na primeira? Executa. Não achou em nenhuma? `command not found`.

Duas ferramentas de diagnóstico fecham o assunto do 00.03:

```bash
which git          # mostra QUAL arquivo será executado
which -a python3   # mostra TODOS os encontrados, na ordem de prioridade
type git           # variante com mais informação (aliases, funções)
```

O `which -a` é o diagnóstico definitivo para "por que está rodando a versão errada?": ele revela a fila inteira, e o primeiro da lista é o que ganha.

E a resposta para a pergunta do `./`: a **pasta atual não está no PATH**, por decisão de segurança. Se estivesse, um arquivo malicioso chamado `ls` numa pasta qualquer seria executado quando você digitasse `ls` ali dentro. O `./` é você dizendo explicitamente "quero este daqui".

### Alterando o PATH

```bash
export PATH="$HOME/meus-scripts:$PATH"      # acrescenta NO INÍCIO (prioridade)
export PATH="$PATH:$HOME/meus-scripts"      # acrescenta NO FIM
```

Repare no padrão: você **reconstrói** o PATH incluindo o valor antigo (`$PATH`). Esquecer isso é o erro nº 1 do capítulo — sem o `$PATH`, você apaga a lista inteira e o terminal para de encontrar qualquer comando.

Colocar no **início** dá prioridade (útil para sobrepor uma versão do sistema); no **fim** é mais conservador.

### Tornando permanente

Variáveis definidas no terminal **morrem** quando ele fecha. Para persistir, elas vão para o arquivo de configuração que o shell lê ao iniciar:

| Shell | Arquivo |
|---|---|
| bash | `~/.bashrc` (Linux) ou `~/.bash_profile` (macOS) |
| zsh | `~/.zshrc` (padrão no macOS moderno) |
| Git Bash (Windows) | `~/.bashrc` |

```bash
echo 'export PATH="$HOME/meus-scripts:$PATH"' >> ~/.bashrc   # acrescenta (>> !)
source ~/.bashrc                                              # recarrega sem reabrir
```

O `source` (ou `.`) executa o arquivo **no shell atual** — é o que faz a mudança valer sem fechar o terminal. E agora você entende por que o 00.03 mandava "feche e reabra o terminal": porque o PATH é lido **ao nascer** do shell.

> ⚠️ **Atenção**
> Use sempre `>>` ao editar arquivos de configuração — um `>` distraído **apaga** todo o seu `.bashrc`, e com ele configurações que você levou meses acumulando. E antes de qualquer edição, um backup custa nada: `cp ~/.bashrc ~/.bashrc.backup`.

### Configuração e segredos: o padrão profissional

Aqui está o motivo mais importante do capítulo. Aplicações precisam de configuração — e ela **não pode estar no código**:

```bash
export DATABASE_URL="postgresql://usuario:senha@localhost/aurora"
export API_KEY="chave-secreta-do-gateway"
export AMBIENTE="producao"
```

O programa lê essas variáveis em vez de carregar valores fixos. Em Python (o que o Atlas fará no módulo 06):

```python
import os
banco = os.environ.get("DATABASE_URL", "sqlite:///local.db")   # com padrão!
```

Repare no `.get` com padrão — é o mesmo idioma do 01.15, agora para configuração: se a variável não existir, usa um valor de desenvolvimento.

Na prática, ninguém digita `export` a cada vez: usa-se um arquivo **`.env`** na raiz do projeto (`chave=valor`, uma por linha), lido por uma biblioteca. E a regra inegociável que acompanha: **o `.env` nunca vai para o Git** — ele entra no `.gitignore` (02.09), e o repositório guarda apenas um `.env.example` com as chaves **sem** os valores. O 06.12 formaliza isso; a permissão 600 do 02.05 completa a defesa.

---

## 7. Funcionamento interno

Por dentro, na medida N2: cada processo tem um **bloco de ambiente** — uma lista de pares `NOME=valor` entregue pelo sistema no momento da criação. Quando o shell executa um comando, ele duplica-se e passa **uma cópia** desse bloco ao filho (a mecânica do 02.05/seção 7). Daí decorrem os três comportamentos que confundem: (1) alterar uma variável dentro de um script **não afeta** o shell que o chamou (o filho mexeu na própria cópia) — e é por isso que scripts que "configuram o ambiente" precisam ser executados com `source`, não com `./`; (2) o PATH é lido pelo shell **a cada busca de comando**, mas o shell só recebe o valor inicial ao nascer — daí a necessidade de reabrir o terminal ou usar `source`; (3) o shell mantém um **cache** de onde encontrou cada comando (por isso `hash -r` às vezes é necessário depois de instalar algo novo no mesmo terminal). E a busca no PATH percorre as pastas em ordem, testando se existe um arquivo com aquele nome **e com bit de execução** (02.05) — permissão e PATH trabalham juntos.

---

## 8. Visualização do fluxo

A busca de um comando — o mecanismo completo do `command not found`:

```mermaid
flowchart TD
    A["Você digita: git status"] --> B{"Tem barra no nome?<br/>(./git, /usr/bin/git)"}
    B -- "Sim" --> C["Usa o caminho DIRETO<br/>(ignora o PATH)"]
    B -- "Não" --> D["Percorre o PATH<br/>pasta por pasta, EM ORDEM"]
    D --> E{"Existe arquivo 'git'<br/>com bit de execução?"}
    E -- "Sim" --> F["EXECUTA o primeiro encontrado<br/>e para de procurar"]
    E -- "Não, próxima pasta" --> D
    D -- "acabaram as pastas" --> G["command not found"]
    C --> H{"O arquivo existe<br/>e é executável?"}
    H -- "Sim" --> F
    H -- "Não" --> I["No such file / Permission denied"]
```

**Como ler:** o primeiro losango explica o `./` — qualquer nome com barra é tratado como caminho, e o PATH nem é consultado. O laço do meio é a busca ordenada: **para no primeiro achado**, o que explica versões antigas ganhando de novas. E repare que o teste inclui o **bit de execução** (02.05): um arquivo com o nome certo, na pasta certa, sem `x`, é ignorado — e a busca continua, podendo terminar em `command not found` mesmo com o arquivo ali.

---

## 9. Aplicação prática

Fechando a dívida do 00.03 e eliminando o `./`.

**Passo 1 — Veja o seu PATH, pasta por pasta:**

```bash
echo $PATH | tr ':' '\n'
```

```text
/usr/local/bin
/usr/bin
/bin
/home/voce/.local/bin
```

**Passo 2 — Descubra qual programa está sendo executado:**

```bash
which python3
which -a python3      # TODOS os encontrados, na ordem de prioridade
which git
```

Se o `which -a` mostrar mais de um `python3`, você acabou de ver o mecanismo do erro do 00.03: o primeiro da lista é o que responde.

**Passo 3 — Variáveis: leia, crie, exporte:**

```bash
echo "Usuário: $USER | Casa: $HOME | Shell: $SHELL"

EMPRESA="Aurora"                    # variável do shell
echo "Trabalho na $EMPRESA"

bash -c 'echo "Do processo filho: $EMPRESA"'     # vazio! não foi exportada
export EMPRESA
bash -c 'echo "Do processo filho: $EMPRESA"'     # agora aparece
```

Três linhas provam o modelo mental: sem `export`, o filho não herda.

**Passo 4 — Seus scripts viram comandos (o fim do `./`):**

```bash
mkdir -p ~/meus-scripts
cp meus-testes/terminal/ola.sh ~/meus-scripts/     # o script do 02.05
chmod +x ~/meus-scripts/ola.sh

ola.sh                                              # ainda não funciona
export PATH="$HOME/meus-scripts:$PATH"              # acrescenta ao PATH
ola.sh                                              # agora sim!
which ola.sh                                        # confirma de onde veio
```

Você acabou de instalar um comando próprio no sistema. É exatamente assim que ferramentas se tornam disponíveis — e por que o instalador do Python pedia para "adicionar ao PATH".

**Passo 5 — Torne permanente:**

```bash
cp ~/.bashrc ~/.bashrc.backup                                  # backup primeiro!
echo 'export PATH="$HOME/meus-scripts:$PATH"' >> ~/.bashrc     # >> e não >
source ~/.bashrc                                                # recarrega agora
```

Abra um terminal novo e teste `ola.sh` — ele funciona sem nenhum `export`. A configuração passou a fazer parte do seu ambiente.

**Passo 6 — O padrão de configuração (antecipando o módulo 06):**

```bash
export AURORA_AMBIENTE="desenvolvimento"
export AURORA_CIDADE_SEDE="campinas"

python3 -c "import os; print('Ambiente:', os.environ.get('AURORA_AMBIENTE', 'não definido'))"
python3 -c "import os; print('Banco:', os.environ.get('DATABASE_URL', 'sqlite local (padrão)'))"
```

O segundo comando mostra o idioma completo: variável ausente → valor padrão de desenvolvimento. É assim que a mesma aplicação roda na sua máquina e em produção, **sem uma linha diferente de código**.

> 🎯 **Checkpoint rápido**
> De cabeça: o que acontece se você rodar `export PATH="/home/voce/scripts"` (sem o `$PATH` no fim)? E como você se recupera disso sem fechar o terminal?

---

## 10. Código comentado

Arquivo completo em [`codigo/cap06/ambiente_e_path.sh`](codigo/cap06/ambiente_e_path.sh).

```bash
#!/usr/bin/env bash
# ------------------------------------------------------------
# ambiente_e_path.sh
# Capítulo 02.06 — Variáveis de ambiente e PATH
# O que este arquivo demonstra: leitura e criação de variáveis,
#   export e herança, o PATH aberto e o padrão de configuração
# Como executar: bash ambiente_e_path.sh
# ------------------------------------------------------------

set -e

PASTA="ambiente_temporario"

echo "--- 1. Lendo variáveis do ambiente ---"
echo "  Usuário: $USER"
echo "  Casa (HOME): $HOME"
echo "  Pasta atual (PWD): $PWD"
echo "  Shell: $SHELL"

echo
echo "--- 2. O PATH, uma pasta por linha ---"
echo "$PATH" | tr ':' '\n' | head -6
echo "  (total de pastas no PATH: $(echo "$PATH" | tr ':' '\n' | wc -l))"

echo
echo "--- 3. Onde estão os programas que eu uso? ---"
echo "  bash:    $(which bash)"
echo "  python3: $(which python3 2>/dev/null || echo 'não encontrado')"
echo "  ls:      $(which ls)"

echo
echo "--- 4. Variável de SHELL x variável de AMBIENTE ---"
EMPRESA="Aurora"                 # variável do shell: só este processo vê
echo "  No shell atual: $EMPRESA"
# O processo filho NÃO herda (a variável não foi exportada):
bash -c 'echo "  No processo filho (sem export): [$EMPRESA]"'

export EMPRESA                   # agora vai para o "quadro de avisos" herdado
bash -c 'echo "  No processo filho (com export): [$EMPRESA]"'

echo
echo "--- 5. Aspas: duplas expandem, simples não ---"
echo "  Duplas: Trabalho na $EMPRESA"
echo '  Simples: Trabalho na $EMPRESA'

echo
echo "--- 6. Instalando um comando próprio no PATH ---"
mkdir -p "$PASTA/bin"
cat > "$PASTA/bin/ola-aurora" << 'FIM'
#!/usr/bin/env bash
echo "  Olá! Sou um comando de verdade, encontrado pelo PATH."
FIM
chmod +x "$PASTA/bin/ola-aurora"

echo "  Antes de alterar o PATH:"
ola-aurora 2>/dev/null || echo "    command not found (esperado)"

# Acrescenta a pasta ao PATH — repare no \$PATH ao final (NUNCA esqueça!)
export PATH="$PWD/$PASTA/bin:$PATH"
echo "  Depois de acrescentar ao PATH:"
ola-aurora
echo "  Encontrado em: $(which ola-aurora)"

echo
echo "--- 7. O padrão de configuração (antecipando o módulo 06) ---"
export AURORA_AMBIENTE="desenvolvimento"
export AURORA_CIDADE_SEDE="campinas"

# O programa lê a configuração do AMBIENTE, com valor padrão se faltar:
python3 - << 'FIM'
import os
ambiente = os.environ.get("AURORA_AMBIENTE", "não definido")
sede = os.environ.get("AURORA_CIDADE_SEDE", "não definida")
banco = os.environ.get("DATABASE_URL", "sqlite local (padrão de desenvolvimento)")
print(f"  Ambiente: {ambiente}")
print(f"  Cidade sede: {sede}")
print(f"  Banco: {banco}")
print("  (o banco não foi definido — o programa usou o padrão, sem quebrar)")
FIM

echo
echo "--- 8. Limpeza ---"
rm -r "$PASTA"
echo "Cenário removido. (O PATH volta ao normal quando este shell terminar.)"
```

---

## 11. Erros comuns

### Erro 1 — Sobrescrever o PATH (o desastre reversível)

**Sintoma:** de repente, **nada** funciona:

```text
$ export PATH="/home/voce/scripts"
$ ls
bash: ls: command not found
```

**Causa:** você substituiu a lista inteira em vez de acrescentar — as pastas do sistema sumiram, e nenhum comando é encontrado.
**Correção:** no mesmo terminal, use caminhos absolutos para se recuperar: `export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"` — ou **feche e abra outro terminal** (o PATH original é lido de novo ao nascer). Prevenção: **sempre** inclua `$PATH` ao redefinir: `export PATH="nova_pasta:$PATH"`.

### Erro 2 — Esperar que a variável sobreviva ao script

**Sintoma:** sem erro — o script define a variável, e ela some quando ele termina:

```bash
./configurar.sh          # define DATABASE_URL lá dentro
echo $DATABASE_URL       # vazio!
```

**Causa:** o script roda num **processo filho** com sua própria cópia do ambiente; alterações morrem com ele (o modelo mental da seção 4).
**Correção:** execute com `source configurar.sh` (ou `. configurar.sh`) — assim os comandos rodam **no shell atual**, e as variáveis permanecem. É por isso que instruções de instalação frequentemente dizem "rode `source` no arquivo", e não `./`.

### Erro 3 — Segredo no código (o erro caro)

**Sintoma:** nenhum erro técnico — e um incidente de segurança: a senha do banco vai para o Git, o repositório vai para o GitHub (02.11), e a chave fica pública para sempre no histórico (mesmo que você a apague depois — o histórico guarda).
**Causa:** valores de configuração escritos direto no código.
**Correção:** leia do ambiente com padrão (`os.environ.get("CHAVE", padrao)`); mantenha valores num `.env` **fora do Git** (`.gitignore` — 02.09), com permissão 600 (02.05); versione um `.env.example` com as chaves e valores fictícios. E se já vazou: **considere a chave comprometida e a revogue** — apagar do repositório não resolve, porque o histórico e os clones já a têm.

> ⚠️ **Atenção**
> Vazamento de credenciais em repositório é uma das falhas de segurança mais comuns da indústria — bots varrem o GitHub continuamente procurando chaves publicadas, e uma chave de nuvem exposta pode virar prejuízo financeiro em minutos. A defesa é procedimental, não técnica: **nunca digite um segredo dentro de um arquivo que será versionado**.

---

## 12. Boas práticas

✅ **Sempre `$PATH` ao redefinir: `export PATH="nova:$PATH"`** — a única linha que evita o desastre reversível do Erro 1.

✅ **`which -a comando` como primeiro diagnóstico de "versão errada"** — mostra a fila completa e revela quem está ganhando.

✅ **Backup antes de editar `~/.bashrc`, e sempre `>>`** — `cp ~/.bashrc ~/.bashrc.backup` custa um segundo.

✅ **Configuração pelo ambiente, com valor padrão de desenvolvimento** — `os.environ.get("CHAVE", padrao)` faz o mesmo código rodar na sua máquina e em produção.

❌ **Evite segredos no código — sempre** — `.env` fora do Git, permissão 600, `.env.example` versionado sem valores.

❌ **Evite acrescentar tudo ao PATH "por precaução"** — um PATH gigante torna a busca imprevisível e cria conflitos de versão difíceis de diagnosticar.

---

## 13. Performance

Nesta escala, irrelevante — a busca no PATH percorre poucas pastas e o shell mantém um cache do que já encontrou. Duas notas úteis: um PATH **muito longo** (dezenas de pastas, comum em máquinas com muitos gerenciadores de versão instalados) torna a primeira execução de cada comando levemente mais lenta e, o que é pior, torna **imprevisível** qual versão responde; e o arquivo `~/.bashrc` é executado a **cada** terminal aberto — encher de comandos pesados (verificações, chamadas de rede) deixa o terminal lento para abrir, incômodo diário clássico. A lição transferível: configuração de inicialização deve ser leve, e a ordem do PATH é decisão de engenharia, não acaso.

---

## 14. Mercado

> 🏢 **Mercado**
> Variáveis de ambiente são o padrão universal de configuração da indústria — é assim que containers (módulo 08) recebem parâmetros, que serviços em nuvem injetam credenciais, que pipelines de CI (módulo 09) passam segredos para os jobs. O princípio tem nome: a metodologia dos **12 fatores**, cujo terceiro fator é literalmente "armazene a configuração no ambiente" (09.04). Na prática do dia a dia: o mesmo código roda em desenvolvimento, homologação e produção, mudando apenas as variáveis — e nenhuma senha aparece no repositório. Em entrevistas, "como você gerencia configuração e segredos?" é pergunta padrão para pleno, e a resposta esperada tem três camadas: ambiente para valores, `.env` local fora do Git, e um gerenciador de segredos (Vault, AWS Secrets Manager) em produção madura.
>
> **Mini-cenário:** quando o Atlas ganhar banco de dados (módulo 05) e for para o servidor (módulo 09), a string de conexão com a senha do PostgreSQL virá de `DATABASE_URL`. Na sua máquina, ela aponta para um banco local; no servidor, para o de produção. **O código é idêntico** — e é isso que permite que o mesmo commit rode nos dois lugares com segurança.

---

## 15. Entrevistas

**P1. "O que é o PATH e como o shell encontra um comando?"**
*Resposta esperada:* lista ordenada de pastas (separadas por `:`) que o shell percorre ao receber um nome sem barra; usa o **primeiro** executável encontrado e para. Nomes com barra (`./script`, `/usr/bin/git`) são caminhos diretos e ignoram o PATH. Diagnóstico: `which -a` mostra a fila; a ordem explica versões "erradas" respondendo.

**P2. "Qual a diferença entre `VAR=valor` e `export VAR=valor`?"**
*Resposta esperada:* o primeiro cria variável só do shell atual; o segundo a coloca no ambiente, e **processos filhos a herdam**. Consequência prática: script executado com `./` não altera o ambiente de quem chamou (cópia própria) — para isso, `source`. Explicar a herança por cópia demonstra o modelo, não a decoreba.

**P3. "Como você gerencia configuração e segredos numa aplicação?"**
*Resposta esperada:* configuração no ambiente (12 fatores), lida com valor padrão de desenvolvimento; `.env` local **fora do Git** (`.gitignore`), com `.env.example` versionado sem valores; em produção, injeção pelo orquestrador ou gerenciador de segredos. E a regra de ouro: se um segredo vazou para o repositório, **revogue** — apagar não resolve, porque histórico e clones o preservam.

**Pegadinha clássica: "Você rodou `export PATH=/home/voce/bin` e agora nenhum comando funciona — nem `ls`. Como sai dessa?"**
Ela testa presença de espírito e entendimento do mecanismo. Três saídas, em ordem de elegância: (1) **restaurar no mesmo shell** usando caminho absoluto, que não depende do PATH — `export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"` (e note que até o `export` funciona porque é um built-in do shell, não um programa externo); (2) usar comandos com caminho completo enquanto isso (`/bin/ls`); (3) **fechar e abrir outro terminal** — o PATH original é lido de novo do `.bashrc`, e nada foi perdido, porque a alteração era só daquela sessão. Fechar com a prevenção (`sempre "$PATH"` ao redefinir) e com o alerta que separa: se você tivesse escrito essa linha **no `.bashrc`**, o problema seria permanente — e a recuperação exigiria editar o arquivo com caminho completo (`/usr/bin/nano ~/.bashrc`) ou usar o backup.

---

## 16. Exercícios guiados

Enunciados completos em [`exercicios/cap06.md`](exercicios/cap06.md); gabaritos em [`exercicios/gabaritos/cap06.md`](exercicios/gabaritos/cap06.md).

### Aquecimento

- **A1** `[~10 min · leitura de variáveis]` — 6 comandos: o que cada um imprime e por quê?
- **A2** `[~10 min · PATH e busca]` — 5 cenários: qual programa é executado?
- **A3** `[~5 min · shell × ambiente]` — 4 situações: a variável é herdada?
- **A4** `[~10 min · diagnóstico]` — 4 falhas relacionadas a PATH/ambiente: causa e correção.

### Aplicação

- **AP1** `[~20 min · abrindo o PATH]` — Explore o seu PATH real, descubra a origem de 5 comandos e identifique conflitos de versão.
- **AP2** `[~20 min · seu comando no PATH]` — Instale um script próprio numa pasta do PATH e torne a configuração permanente.
- **AP3** `[~20 min · configuração externa]` — Adapte um script Python seu para ler configuração do ambiente, com padrões de desenvolvimento.

---

## 17. Desafios

- **D1** `[~45 min · o Atlas configurável]` — **Configuração por ambiente, de ponta a ponta.** Pegue o `relatorio_aurora.py` (01.25), que hoje lê configuração de um `config.json`, e evolua-o para o padrão profissional: (a) as variáveis `AURORA_ARQUIVO_VENDAS`, `AURORA_SEPARADOR` e `AURORA_TOP_PRODUTOS` são lidas do **ambiente**, com o `config.json` como segunda opção e valores embutidos como último recurso (a cadeia ambiente → arquivo → padrão); (b) crie um `.env.example` documentando as três variáveis com valores fictícios; (c) crie um `.env` real (com permissão 600 — 02.05) e um script `rodar.sh` que carrega o `.env` e executa o relatório; (d) demonstre a mesma execução com configurações diferentes **sem alterar nenhum arquivo** — só variáveis de ambiente na linha de comando. Fecho: 5 linhas sobre por que essa cadeia de precedência (ambiente > arquivo > padrão) é o padrão da indústria.

<details><summary>💡 Dica 1 (conceito)</summary>
A cadeia em Python: `os.environ.get("CHAVE") or config_json.get("chave") or PADRAO` — ou, mais explícito, com ifs. O importante é a ordem de precedência.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Para rodar com variáveis pontuais sem exportar: `AURORA_TOP_PRODUTOS=3 python3 relatorio_aurora.py` — a variável vale só para aquela execução.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
carregar_config() com a cadeia → .env.example versionável → .env com 600 → rodar.sh com `set -a; source .env; set +a` → duas execuções com valores diferentes.
</details>

---

## 18. Mini projeto

**Seu ambiente de trabalho, documentado e permanente** `[~50 min]` — a configuração que vai te acompanhar pelos próximos dez módulos.

Requisitos numerados:

1. Crie a pasta `~/meus-scripts` e mova para lá os comandos que você criou no 02.05 (com shebang e `chmod +x`).
2. Acrescente essa pasta ao PATH **permanentemente**, com backup do arquivo de configuração antes da edição. Prove que funciona abrindo um terminal novo.
3. Documente no caderno de bordo: o conteúdo do seu PATH (uma pasta por linha), a origem de 5 comandos que você usa (`which`), e qual arquivo de configuração o seu shell lê.
4. Crie um `ambiente-aurora.sh` que exporta as variáveis do projeto (`AURORA_AMBIENTE`, `AURORA_CIDADE_SEDE`, e outras que fizerem sentido) — e documente que ele deve ser executado com `source`, explicando por quê.
5. Escreva a seção "segredos" no caderno: as três regras (ambiente, `.env` fora do Git com 600, `.env.example` versionado), e o que fazer se uma chave vazar.

**Critério de "está bom":** o comando próprio funcionando em terminal novo (a prova de que a persistência deu certo); o backup do `.bashrc` existindo; a documentação suficiente para reconstruir o ambiente numa máquina nova. Este último ponto é o teste real: **você conseguiria montar sua estação de trabalho de novo lendo apenas o seu caderno?**

---

## 19. Revisão

**Resumo do capítulo:**

- Variáveis de ambiente = quadro de avisos **herdado por cópia** pelos processos filhos; `VAR=x` é local do shell, `export VAR=x` é herdável.
- **PATH**: lista ordenada de pastas separadas por `:`; a busca **para no primeiro achado** (com bit de execução) — daí versões antigas ganhando de novas.
- Nomes com barra (`./script`) são caminhos diretos e **ignoram o PATH**; a pasta atual não está no PATH por segurança.
- Diagnóstico: `which -a` mostra a fila completa; `echo $PATH | tr ':' '\n'` lista as pastas; o arco do 00.03 fechado.
- Persistência: `~/.bashrc` (ou `.zshrc`) lido ao nascer do shell; `source` recarrega sem reabrir; **sempre `>>`, nunca `>`**, e backup antes.
- Configuração profissional: valores no ambiente com padrão de desenvolvimento; `.env` fora do Git com permissão 600; `.env.example` versionado — e segredo vazado se **revoga**, não se apaga.

**Flashcards novos** (adicionados a [`revisao/flashcards.md`](revisao/flashcards.md)):

| ID | Frente | Verso |
|---|---|---|
| 02.06-F1 | O que é o PATH e como o shell escolhe qual programa executar? | Lista ordenada de pastas (separadas por `:`); percorre na ordem e usa o **primeiro** executável com aquele nome. Diagnóstico: `which -a`. |
| 02.06-F2 | Explique com suas palavras: por que uma variável definida num script não sobrevive a ele? | (Elaboração) O script roda num processo filho com **cópia** do ambiente; alterações morrem com ele. Para persistir no shell atual: `source script.sh`. |
| 02.06-F3 | Preveja: `export PATH="/home/eu/bin"` (sem `$PATH`). O que acontece e como recuperar? | (Previsão) Nenhum comando é encontrado (a lista foi substituída). Recuperação: redefinir com caminhos absolutos, ou abrir outro terminal. Prevenção: sempre incluir `$PATH`. |
| 02.06-F4 | Onde deve ficar a senha do banco de dados de uma aplicação — e por quê? | (Decisão) No **ambiente** (variável), com `.env` local fora do Git (permissão 600) e `.env.example` versionado sem valores. Segredo no código vai para o histórico e vaza para sempre. |
| 02.06-F5 | Por que é preciso `./` para executar um script na pasta atual? | A pasta atual **não está no PATH**, por segurança (um arquivo malicioso chamado `ls` seria executado). O `./` é um caminho explícito e dispensa a busca. |

**Agendamento:** registre no `PROGRESSO.md` e marque D+1, D+7, D+30, D+90 na [`Revisoes/agenda.md`](../Revisoes/agenda.md).

---

## 20. Checklist

Perguntas de domínio — teste do sim:

- [ ] Sei explicar *o PATH e prever qual programa executa quando há dois com o mesmo nome*?
- [ ] Sei diferenciar *variável de shell e de ambiente, e explicar a herança por cópia*?
- [ ] Sei tornar *uma configuração permanente com segurança (backup + `>>`)*?
- [ ] Sei aplicar *o padrão de configuração por ambiente com valores padrão*?
- [ ] Sei responder *à pegadinha do PATH sobrescrito, com as três saídas*?

Itens práticos:

- [ ] Rodei `ambiente_e_path.sh` e vi a diferença entre com e sem `export`.
- [ ] Instalei um comando próprio no PATH e ele funciona em terminal novo.
- [ ] Fiz backup do `.bashrc` antes de editá-lo.
- [ ] Completei "Seu ambiente de trabalho, documentado e permanente" (5 requisitos).
- [ ] Registrei a sessão e agendei as 4 revisões.

---

## 21. Próximo capítulo

Você tem comandos próprios, ambiente configurado e um repertório de umas trinta ferramentas de terminal. E ainda executa tudo **manualmente**, um comando por vez — inclusive as sequências que repete toda semana: organizar as saídas, conferir o ambiente, rodar o relatório e arquivar o resultado. Ficou deliberadamente em aberto o passo que transforma repertório em **automação**: escrever scripts de verdade, com argumentos, condicionais, laços e tratamento de erro. É a mesma lógica do módulo 01, em outra linguagem — e o capítulo que fecha a parte Linux do módulo, entregando as ferramentas que vão automatizar seu fluxo de estudo (e, no módulo 09, o deploy do Atlas).

→ [02.07 — Scripts de shell](07-scripts-de-shell.md)

---

*Gerado sob spec 3.0.0*
