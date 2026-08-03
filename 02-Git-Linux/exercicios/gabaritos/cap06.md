# Gabaritos — Capítulo 02.06

Abra somente após tentativa honesta.

## A1 — Lendo variáveis

1. O caminho da sua pasta pessoal (`/home/voce`) — o `$` pede o **conteúdo**.
2. A palavra literal `HOME` — sem `$`, é apenas texto.
3. `Bem-vindo à Aurora` — aspas duplas **expandem** variáveis.
4. `Bem-vindo à $NOME` — aspas simples **não** expandem; sai literal.
5. Uma linha em branco — variável inexistente vira string vazia, **sem erro**.
6. `[]` — os colchetes revelam a string vazia. É o truque de diagnóstico: sempre delimite quando estiver investigando.

**Critério:** 6/6; o par 3–4 é a fonte de metade dos bugs em scripts.

## A2 — PATH e busca

1. **3.12** (`/usr/local/bin` vem primeiro; a busca para no primeiro achado).
2. **3.7** — o `./` é caminho direto, o PATH não é consultado.
3. **3.9** — caminho absoluto, idem.
4. Passaria a rodar o **3.9**: a ordem do PATH é que decide, não a "novidade" da versão.
5. Rodaria o **3.9**: a busca exige nome **e bit de execução** (02.05); sem `x`, a pasta é ignorada e a busca continua.

**Critério:** 5/5. O item 5 é o que separa quem entendeu o mecanismo de quem decorou "o primeiro ganha".

## A3 — Shell × ambiente

1. **Vazio** — sem `export`, o filho não herda.
2. **`a`** — exportada, é herdada.
3. **`a`** — o filho alterou a **própria cópia**; o pai não muda.
4. **Vazio** — o script rodou num processo filho; o `export` morreu com ele. Para persistir: `source configura.sh`.

**Critério:** 4/4, com a palavra "cópia" aparecendo na explicação dos itens 3 e 4.

## A4 — Diagnóstico

1. Instalado, mas fora do PATH (ou com outro nome — `python3` em vez de `python`). Investigação: `which -a python python3`, `ls /usr/bin/python*`. Correção: acrescentar a pasta ao PATH.
2. Duas versões instaladas; a antiga vem primeiro na lista. Investigação: `which -a python`. Correção: pôr a pasta da nova **no início** do PATH.
3. O `.bashrc` é lido ao **nascer** do shell. Correção: `source ~/.bashrc` (ou abrir um terminal novo).
4. O PATH foi substituído em vez de acrescentado. Correção: `export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"` — ou fechar e abrir outro terminal.

**Critério:** 4/4; nos itens 1 e 2, o `which -a` deve aparecer como primeira ferramenta.

## AP1 — Abrindo o seu PATH

**Comandos de referência:** `echo $PATH | tr ':' '\n'` · `echo $PATH | tr ':' '\n' | wc -l` · `which bash python3 git ls grep` · `which -a python3` · `echo $SHELL`.

**Observação esperada:** entre 4 e 15 pastas é o comum; muito mais que isso costuma indicar gerenciadores de versão acumulados (pyenv, nvm, conda), e é justamente a situação em que `which -a` vira indispensável. Se você usa Windows com Git Bash, verá caminhos do Windows traduzidos (`/c/Program Files/...`) — a tradução é do próprio Git Bash.

**Critério:** os 5 itens registrados no caderno, com o arquivo de configuração identificado corretamente pelo shell em uso.

## AP2 — Seu comando no PATH

**Sequência de referência:**

```bash
mkdir -p ~/meus-scripts
printf '#!/usr/bin/env bash\necho "Meu comando funciona!"\n' > ~/meus-scripts/aurora
chmod +x ~/meus-scripts/aurora
aurora                                                   # command not found
export PATH="$HOME/meus-scripts:$PATH"
aurora                                                   # funciona
which aurora                                             # confirma a origem
cp ~/.bashrc ~/.bashrc.backup
echo 'export PATH="$HOME/meus-scripts:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Erro esperado:** usar `>` em vez de `>>` no penúltimo comando — e apagar o `.bashrc` inteiro. É por isso que o backup é o passo 4 e não o último.

**Critério:** o comando funcionando em terminal **novo** (a prova da persistência) e o arquivo de backup existindo.

## AP3 — Configuração externa

**Referência de adaptação:**

```python
import os

ARQUIVO = os.environ.get("VENDAS_ARQUIVO", "vendas.csv")
SEPARADOR = os.environ.get("VENDAS_SEPARADOR", ";")
LIMITE = int(os.environ.get("VENDAS_TOP", "5"))     # ambiente é sempre texto!
```

**Ponto de atenção:** variáveis de ambiente são **sempre strings** — números precisam de `int()`/`float()` (o mesmo cuidado do 01.04), e "booleanos" viram comparação de texto (`os.environ.get("DEBUG", "0") == "1"`). Esquecer isso produz o erro de comparar `"5"` com `5`.

**Critério:** as duas execuções registradas, mostrando comportamento diferente com o **mesmo** arquivo de código.

## D1 — O Atlas configurável

**Cadeia de precedência (referência):**

```python
def carregar_config():
    """Ambiente > config.json > padrões embutidos."""
    padroes = {"arquivo": "vendas.csv", "separador": ";", "top": 5}
    try:
        with open("config.json", encoding="utf-8") as f:
            do_arquivo = json.load(f)
    except FileNotFoundError:
        do_arquivo = {}

    config = {**padroes, **do_arquivo}          # arquivo sobrepõe padrão
    # ambiente sobrepõe tudo:
    if os.environ.get("AURORA_ARQUIVO_VENDAS"):
        config["arquivo"] = os.environ["AURORA_ARQUIVO_VENDAS"]
    if os.environ.get("AURORA_SEPARADOR"):
        config["separador"] = os.environ["AURORA_SEPARADOR"]
    if os.environ.get("AURORA_TOP_PRODUTOS"):
        config["top"] = int(os.environ["AURORA_TOP_PRODUTOS"])
    return config
```

**`.env.example` (versionável):**

```text
AURORA_ARQUIVO_VENDAS=vendas.csv
AURORA_SEPARADOR=;
AURORA_TOP_PRODUTOS=5
```

**`rodar.sh`:**

```bash
#!/usr/bin/env bash
set -a          # tudo que for definido a partir daqui é exportado
source .env
set +a
python3 relatorio_aurora.py
```

**Demonstração esperada (item d):**

```bash
python3 relatorio_aurora.py                          # top 5, padrão
AURORA_TOP_PRODUTOS=2 python3 relatorio_aurora.py    # top 2, sem editar nada
```

**Reflexão esperada:** a precedência ambiente > arquivo > padrão existe porque cada camada serve a um público. O **padrão embutido** garante que o programa rode recém-clonado, sem configuração alguma — a barreira de entrada de quem chega no projeto. O **arquivo** serve à equipe: valores compartilhados, versionáveis (quando não são segredos), revisáveis em código. O **ambiente** serve à operação: o servidor, o container e o pipeline injetam valores no momento da execução, sem tocar em arquivo nenhum — e é a única camada que funciona quando o código está empacotado numa imagem imutável (módulo 08). Inverter a ordem quebraria a operação: um arquivo do repositório sobrepondo a configuração de produção é como a máquina do desenvolvedor mandando no servidor.

**Critério de "está bom":** as três camadas funcionando e demonstráveis; `.env` com 600 e **fora** do Git; `.env.example` versionado sem valores reais; a conversão `int()` presente (ambiente é texto); a reflexão citando a imutabilidade da imagem ou a injeção pelo orquestrador.
