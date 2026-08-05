# Gabarito — Capítulo 04.16: Ambientes virtuais e pip

Leia depois de tentar. Enunciados em [`../cap16.md`](../cap16.md).

> Toda saída abaixo é execução real, no Python 3.10 em Linux.

## A1 — Qual python roda?

| # | Situação | Interpretador | Procura bibliotecas em |
|---|---|---|---|
| 1 | sem ambiente | o do `PATH` (`/usr/bin/python3`) | `site-packages` do sistema |
| 2 | `.venv` criado, **não** ativado | o do `PATH` | `site-packages` do sistema |
| 3 | `.venv` ativado | `.venv/bin/python` | `site-packages` do `.venv` |
| 4 | `.venv/bin/python` direto | `.venv/bin/python` | `site-packages` do `.venv` |
| 5 | `.venv/bin/python`, com **outro** ativado | `.venv/bin/python` | `site-packages` do `.venv` |
| 6 | `pip install` com `.venv` ativado | `.venv/bin/pip` | instala no `.venv` |
| 7 | `python -m pip install`, ativado | `.venv/bin/python` → seu pip | instala no `.venv` |
| 8 | `bash script.sh` que chama `python` | `.venv/bin/python` | `site-packages` do `.venv` |

**Os três que ensinam.**

O **2** é o erro mais frequente do capítulo: criar o ambiente **não** faz nada acontecer. Ele fica lá, e o `python` continua sendo o de sempre até que alguém ative ou chame o caminho completo.

O **5** é a prova da frase da §4: **quem decide é qual `python` você chamou**, não o que está ativo. O ambiente ativado só afeta o que o `PATH` resolve, e você contornou o `PATH` ao dar o caminho.

O **8** funciona porque variáveis de ambiente são **herdadas** pelos processos filhos (02.06). O script recebe o `PATH` alterado e resolve `python` do mesmo jeito. É também por isso que ativar num terminal não afeta outro.

**A diferença entre 6 e 7** não aparece aqui, e aparece quando o `PATH` está confuso — dois ambientes, uma ativação mal desfeita, um `pip` do sistema à frente. `python -m pip` elimina a dúvida por construção: o `pip` que roda é o do interpretador que você invocou.

## A2 — Preveja o resultado

**1.** Dois pacotes, não zero:

```
Package    Version
---------- -------
pip        22.0.2
setuptools 59.6.0
```

Um ambiente "vazio" traz `pip` e `setuptools` — e são eles que respondem pelos 19 MB da §13.

**2. Cinco linhas.** Você pediu um pacote:

```
annotated-types==0.8.0
pydantic==2.13.4
pydantic_core==2.46.4
typing-inspection==0.4.2
typing_extensions==4.16.0
```

**3. `True`.** O `deactivate` restaurou o `PATH` anterior, e `sys.prefix == sys.base_prefix` volta a valer — o sinal de que não há ambiente.

**4.** `bad interpreter`:

```
bash: ambiente/bin/pip: /tmp/ver16/.v2/bin/python3: bad interpreter: No such file or directory
```

O caminho antigo está gravado na primeira linha do script.

**5. Funciona**, e imprime o caminho **novo**:

```
/tmp/ver16/ambiente
```

**O contraste entre 4 e 5 é o ponto.** O `python` descobre o prefixo a partir do próprio caminho; os scripts têm o caminho **gravado**. Descobrir sobrevive a mudar de lugar; ter escrito, não.

**6. `No broken requirements found`** — num ambiente onde a versão 2 foi rebaixada para a 1 e `pydantic_core` ficou órfão. O `pip check` confere se cada pacote instalado tem as dependências que **declarou**. Nenhum pacote declara nada sobre o que o **seu** código esperava.

## A3 — Ache o erro

**1. Ativou num projeto e instalou em outro — funciona, e é o erro mais comum de todos.**

```bash
cd projeto-a && source .venv/bin/activate
cd ../projeto-b && pip install requests
```

O `cd` não desativa nada. O `requests` foi para o ambiente do **projeto-a**, e o projeto-b continua sem ele. Não há erro, e o sintoma chega depois: `ModuleNotFoundError` num projeto e um pacote inexplicável no outro.

Correção: `deactivate` antes de trocar, ou o hábito de `python -m pip` depois de conferir `sys.prefix`.

**2. `pydantic>=2.0` e `mypy` sem versão — funciona hoje e quebra depois.** O primeiro aceita a versão 3.0.0, que por convenção é a que quebra compatibilidade; o segundo aceita qualquer coisa. Correção: `pydantic==2.13.4` e `mypy==2.3.0` — ou, no mínimo, `>=2.0,<3.0`.

**3. `git add .` sem `.gitignore` — funciona, e o estrago é grande.** Entram no repositório os 3.524 arquivos do `.venv`, o `__pycache__`, e — o pior — qualquer `.env` com senha. Os arquivos do ambiente não servem em outra máquina (A2.4), e uma senha versionada continua no histórico depois de removida.

**4. Criou o ambiente e não ativou — falha na hora, ou pior.**

```bash
python -m venv .venv
pip install pydantic        # foi para fora do ambiente
python -c "import pydantic" # e o import funciona, do lugar errado
```

O ambiente ficou vazio e a biblioteca foi para o Python do sistema — exatamente o que o capítulo veio evitar. E note que **pode não haver erro nenhum**: se a instalação der certo fora, o `import` funciona, e você segue meses achando que tem um ambiente.

**5. "Copie a pasta `.venv`" — falha na hora, e por dois motivos independentes.** Os scripts têm caminho absoluto (A2.4), e pacotes compilados são específicos de sistema operacional e arquitetura — um `.venv` de Linux não funciona em Windows nem com os caminhos corrigidos. Correção: versione o `requirements.txt`.

**6. `pip freeze` num ambiente sujo — funciona, e produz um arquivo enganoso.** Entram no `requirements.txt` as bibliotecas que você instalou para testar uma ideia e esqueceu. Quem instalar a partir dele recebe tudo, sem saber o que é necessário. Correção: escrever à mão o que você escolheu (§6.6), e usar um ambiente novo quando quiser conferir a lista.

**A leitura do lote:** **quatro dos seis funcionam** (1, 2, 3, 6). São os que produzem o problema longe da causa — o padrão do módulo inteiro.

## A4 — Qual especificador?

| # | Situação | Escrever |
|---|---|---|
| 1 | exatamente 2.13.4 | `==2.13.4` |
| 2 | só correções de defeito | `~=2.13.4` (equivale a `>=2.13.4,<2.14`) |
| 3 | funcionalidades novas, sem quebra | `~=2.13` (equivale a `>=2.13,<3.0`) |
| 4 | qualquer 2.x menos a 2.13.2 | `>=2.0,<3.0,!=2.13.2` |
| 5 | projeto começando hoje | `==` na versão que você instalou |
| 6 | vai para produção | `==` em tudo, inclusive nas transitivas |

**As duas respostas que costumam sair erradas.**

No **5**, a tentação é não fixar nada — "ainda estou explorando". Mas fixar hoje custa nada e economiza a semana em que o projeto para de funcionar sem que você tenha mudado uma linha. Atualizar é uma decisão; receber uma versão nova por omissão não é.

No **6**, a resposta completa vai além do `==` nas suas dependências: em produção convém fixar também as **transitivas**, com `pip-tools`, `uv` ou o `pip freeze` de um ambiente limpo. É o nível 3 da §6.6, com o custo declarado — o arquivo deixa de documentar suas escolhas, e por isso se mantêm dois arquivos.

E o contraste entre **2 e 3** merece o teste que o capítulo fez: `~=2.13.4` aceita só a série 2.13, e `~=2.13` aceita 2.14. Um til, um dígito, e a diferença entre receber correções e receber funcionalidades.

## AP1 — O ambiente do zero

```bash
mkdir projeto && cd projeto
python -m venv .venv
source .venv/bin/activate
python -m pip install pydantic==2.13.4 pydantic-settings==2.7.0
python -m pip install mypy==2.3.0 pytest==8.3.4
```

```
# requirements.txt              # requirements-dev.txt
pydantic==2.13.4                -r requirements.txt
pydantic-settings==2.7.0        mypy==2.3.0
                                pytest==8.3.4
```

```
# .gitignore
.venv/
__pycache__/
.mypy_cache/
.env
```

**A contagem:** você escreveu **quatro** pacotes; o `freeze` lista **dez ou mais**. A diferença são as **dependências transitivas** — as dependências das suas dependências.

O nome importa porque a distinção é a base da §6.6: as quatro são **decisões suas**, e as outras seis são **consequências**. Um `requirements.txt` gerado por `freeze` perde essa distinção, e com ela a possibilidade de responder "por que este pacote está aqui?".

## AP2 — Reproduzir

```bash
rm -rf .venv
python -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

```
diff antes.txt depois.txt  ->  IDÊNTICOS (hoje)
```

**E a palavra "hoje" é a resposta do exercício.** Reconstruído no mesmo dia, o ambiente saiu igual. Não há garantia de que sairia igual em novembro, e dá para mostrar exatamente onde está a folga:

```
pydantic 2.13.4 declara:
   annotated-types>=0.6.0
   pydantic-core==2.46.4
   typing-extensions>=4.14.1
   typing-inspection>=0.4.2
```

**`pydantic-core` está fixo — o próprio Pydantic o fixou.** Os outros três estão abertos. Uma versão nova de `typing-extensions` publicada amanhã entra na próxima instalação, com o seu `requirements.txt` idêntico, sem que ninguém tenha decidido nada.

Isso quase sempre não dá problema, e quando dá é do pior tipo: o mesmo arquivo, o mesmo comando, resultados diferentes em máquinas diferentes. É o motivo de existirem arquivos de trava (§6.6 e §14), e é a diferença entre "reproduzível" e "reproduzível de verdade".

## AP3 — O conflito na sua máquina

As seis cenas, na ordem, com o que cada uma prova:

1. **`sys.prefix == sys.base_prefix`** fora de qualquer ambiente. É o sinal, e é o que o mini projeto vai usar.
2. **Dois ambientes criados**, e o `prefix` de dentro apontando para a pasta do projeto. 19 MB cada, vazios.
3. **Cinco pacotes para um pedido.** As transitivas.
4. **O mesmo arquivo, dois resultados.** É a §3 do capítulo, executada.
5. **O rebaixamento silencioso.** Ver abaixo.
6. **O ambiente renomeado.** Ver abaixo.

**Por que o `pip check` diz que está tudo bem (cena 5).** Porque ele responde a uma pergunta diferente da que você fez. A pergunta dele é: *cada pacote instalado tem as dependências que declarou, nas versões que pediu?* Depois do rebaixamento, `pydantic==1.10.13` declara precisar de `typing_extensions>=4.2.0`, e ele está lá. Nada mais é conferido.

O `pydantic_core` órfão não incomoda ninguém: nenhum pacote instalado depende dele, então não há dependência quebrada — há um pacote a mais, que é uma situação **válida** para o `pip`.

E o que quebrou — o seu código chamando `model_dump_json()` — está fora do alcance da ferramenta por completo. **Nenhum pacote declara qual versão o seu código esperava.** Só o `requirements.txt` sabe disso, e o `pip check` não o lê.

É a mesma forma do "Success" enganoso do 04.14: a ferramenta responde bem à pergunta dela, e o erro é achar que a pergunta era a sua.

**Por que o `pip` quebrou e o `python` não (cena 6).** Os dois estão na mesma pasta renomeada, e a diferença é **como cada um sabe onde está**.

O `pip` é um script de texto cuja primeira linha é `#!/caminho/antigo/.venv/bin/python3`. O sistema lê essa linha para saber com que interpretador executar o arquivo, e o caminho não existe mais. O erro vem do sistema operacional, antes de o `pip` rodar uma linha sequer.

O `python` é o interpretador. Ao iniciar, ele olha o **próprio caminho de execução** e procura um `pyvenv.cfg` ali ao lado. Encontra, na pasta nova, e define `sys.prefix` como a pasta nova.

**Descobrir sobrevive a mudar de lugar; ter escrito, não.** É a mesma distinção que separa um caminho relativo de um absoluto, e é a razão de o ambiente não ser portátil.

## D1 — O projeto reproduzível

**(1) Como detectar o ambiente — e por que `$VIRTUAL_ENV` não serve.**

```bash
python -c "import sys; sys.exit(0 if sys.prefix != sys.base_prefix else 1)"
```

O teste correto compara `sys.prefix` com `sys.base_prefix`. Diferentes, há ambiente.

`$VIRTUAL_ENV` **só existe quando alguém rodou `activate`**:

```
.venv/bin/python direto   -> VIRTUAL_ENV definido? False · sinal confiável: True
com activate              -> VIRTUAL_ENV definido? True  · sinal confiável: True
```

Um `verificar.sh` baseado em `$VIRTUAL_ENV` **recusa um uso perfeitamente correto** — chamar o interpretador do ambiente pelo caminho completo, que é o que fazem editores, agendadores e servidores de integração contínua. Ele testa se você digitou um comando, e não se o ambiente está em uso.

`$VIRTUAL_ENV` continua útil para **mostrar** qual ambiente foi ativado. Como condição, não.

**(2) Fixar as transitivas?** As duas respostas são defensáveis, e a nota é pela justificativa:

**Sim, se o projeto vai para produção.** Uma versão nova de uma transitiva pode mudar o comportamento, e você quer que o servidor rode o que você testou. O custo é manter dois arquivos (o das escolhas e o gerado) e uma rotina de atualização.

**Não, se o projeto é de estudo ou biblioteca.** Fixar tudo transforma o arquivo num inventário ilegível, e numa **biblioteca** é ativamente ruim: você força as suas transitivas em quem a instalar, criando o conflito da §3 no projeto dos outros.

A resposta que não vale é "fixei tudo porque é mais seguro", sem mencionar o custo.

**(3) O que muda em um ano, e o que protege.**

Muda a **versão do Python** disponível na máquina — e o `requirements.txt` não diz de qual você precisa. Protege declarar isso no `LEIAME.md` (e, a partir do 04.17, no `pyproject.toml`).

Mudam as **transitivas não fixadas** (AP2). Protege fixá-las, com o custo do item 2.

Podem **sair do ar** versões antigas de pacotes, embora seja raro no PyPI.

E muda o **sistema operacional** — pacotes compilados podem não ter versão pronta para a plataforma nova, e a instalação passa a exigir compilador. Protege registrar no `LEIAME.md` em que sistema e versão de Python o projeto foi testado. É a lacuna que o módulo 08 fecha de vez, com o container carregando o sistema junto.

## MP — O diagnóstico de ambiente

O núcleo, sem nenhuma dependência externa:

```python
import sys
import importlib.metadata as metadados

def dentro_de_ambiente() -> bool:
    return sys.prefix != sys.base_prefix

def relatorio() -> None:
    print("interpretador:", sys.executable)
    print("versão:       ", sys.version.split()[0])
    print("ambiente:     ", sys.prefix if dentro_de_ambiente() else "NENHUM")
    print("base:         ", sys.base_prefix)
    instalados = {d.metadata["Name"].lower(): d.version
                  for d in metadados.distributions()}
    print("pacotes:      ", len(instalados))
```

E a conferência contra o arquivo, sem depender de nada instalado:

```python
for linha in open("requirements.txt", encoding="utf-8"):
    linha = linha.split("#")[0].strip()
    if not linha or linha.startswith("-r"):
        continue
    nome, _, pedida = linha.partition("==")
    atual = instalados.get(nome.strip().lower().replace("_", "-"))
    if atual is None:
        print("  FALTA   ", nome)
    elif pedida and atual != pedida.strip():
        print("  DIVERGE ", nome, "pedido", pedida.strip(), "· instalado", atual)
    else:
        print("  ok      ", nome, atual)
```

**Três detalhes que decidem.** `importlib.metadata` é da biblioteca padrão — usar `pkg_resources` ou pedir `pip` importado quebraria a restrição do exercício. O `.replace("_", "-")` existe porque os nomes de pacote são comparados sem distinguir `-` de `_` (`typing_extensions` e `typing-extensions` são o mesmo pacote), e ignorar isso produz "FALTA" para coisas instaladas. E `sys.executable` é o que responde de verdade "qual python está rodando" — mais útil que `which python`, que responde o que o `PATH` acha e não o que está executando.

**A pergunta que fecha: `sys.prefix != sys.base_prefix`.**

Ele funciona nas **duas** formas de usar o ambiente. `$VIRTUAL_ENV` não:

```
.venv/bin/python direto   -> VIRTUAL_ENV: False · prefix != base_prefix: True
com activate              -> VIRTUAL_ENV: True  · prefix != base_prefix: True
```

Um diagnóstico baseado em `$VIRTUAL_ENV` diria "você não está num ambiente" para alguém que está — e essa é a pior resposta possível numa ferramenta cuja razão de existir é ser confiável quando tudo o mais está confuso.
