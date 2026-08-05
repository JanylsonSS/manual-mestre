# Gabarito — Capítulo 04.17: Organização de projetos

Leia depois de tentar. Enunciados em [`../cap17.md`](../cap17.md).

> Toda saída abaixo é execução real, no Python 3.10.

## A1 — O import funciona?

| # | Comando | Resultado |
|---|---|---|
| 1 | `python -m loja.relatorio` (na raiz) | **`ok 0.15`** |
| 2 | `python loja/relatorio.py` (na raiz) | `ModuleNotFoundError: No module named 'loja'` |
| 3 | `python -c "import loja"` (na raiz) | **funciona** |
| 4 | `python /caminho/projeto/loja/relatorio.py` (de `/`) | `ModuleNotFoundError: No module named 'loja'` |
| 5 | `python relatorio.py` (de dentro de `loja/`) | `ModuleNotFoundError: No module named 'loja'` |
| 6 | `python -c "import util"` (na raiz) | **funciona** |
| 7 | `python -c "import util"` (de `/`) | `ModuleNotFoundError: No module named 'util'` |
| 8 | `python -m loja` (sem `__main__.py`) | `No module named loja.__main__; 'loja' is a package and cannot be directly executed` |

**O padrão dos itens 2, 4 e 5 é o mesmo, e é o do capítulo.** Rodar o **arquivo** põe `loja/` no `sys.path[0]`, e de lá o pacote `loja` não é encontrável — precisaria estar um nível acima. Note que o **4 e o 5 falham pelo mesmo motivo do 2**, embora pareçam situações diferentes: em nenhum deles a pasta que **contém** `loja/` entrou na lista.

**O 3 contra o 7** é o outro lado: com `-c`, o `sys.path[0]` é a pasta atual, então o que funciona depende de **onde você está** — não de onde está o arquivo.

O **8** tem uma mensagem que ensina algo útil: um pacote pode ser executado com `-m` **se** tiver um `__main__.py`. É assim que `python -m http.server` e `python -m venv` funcionam.

## A2 — Preveja a saída

| # | Resultado |
|---|---|
| 1 | `ImportError: attempted relative import with no known parent package` |
| 2 | **funciona** — `TAXA = 0.15` |
| 3 | `.../aurora/__init__.py` e `['.../aurora']` |
| 4 | **`None`** |
| 5 | `''` — a pasta atual |
| 6 | `ImportError: cannot import name 'alfa' from partially initialized module 'ciclo.a'` |

**O par 1/2 é o mais útil de decorar.** O ponto em `from .precos import TAXA` significa "o pacote **deste** módulo". Rodando o arquivo direto não há pacote nenhum, e a mensagem diz exatamente isso — ela costuma ser lida como misteriosa por causa da palavra "parent", que aqui significa "o pacote a que este módulo pertence".

**O 4 é o teste de bolso para pacote de espaço de nomes:**

```
com __init__.py    -> __file__: /tmp/prova17/src/aurora/__init__.py
sem __init__.py    -> __file__: None
```

`__file__` valendo `None` é o sinal de que a pasta não tem `__init__.py` — e, portanto, de que ela pode estar fundida com outra de mesmo nome em algum lugar do `sys.path` (§6.1). Quando um import traz o módulo errado, `__file__` costuma resolver o mistério em uma linha.

## A3 — Ache o erro

**1. Módulo fora do pacote — funciona, e é o defeito da §3.** `helpers.py` está na raiz do projeto, e `aurora/modelo.py` o importa. Funciona na sua máquina porque a raiz está no `sys.path`; some no pacote instalado. Correção: `helpers.py` vai para dentro de `aurora/`.

**2. Testes dentro do pacote — funciona, e envia os testes ao cliente.** `src/aurora/tests/` é empacotado junto e instalado na máquina de quem usa a biblioteca. Além disso, os imports de lá deixam de reproduzir o uso real. Correção: `tests/` irmão de `src/`.

**3. `sys.path.append` — funciona, e esconde o problema.** O projeto passa a depender de outro projeto estar num caminho relativo específico. Quebra ao mover a pasta, ao instalar, ao rodar de outro diretório. Correção: se `outro` é uma dependência, declare-a no `pyproject.toml` e instale-a; se é código seu, é um pacote a mais no mesmo projeto.

**4. `pyproject.toml` sem `[build-system]` — falha ou se comporta de forma imprevisível.** Sem essa seção, o pip usa um comportamento antigo de compatibilidade, que pode não achar os pacotes e não respeita `[tool.setuptools.packages.find]`. Falta também `requires-python`, a lacuna que o D1 do 04.16 apontou. Correção:

```toml
[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"
```

**5. `import *` no `__init__.py` — funciona, e desfaz o propósito do arquivo.** A API pública deixa de ser declarada: qualquer nome de qualquer módulo vira público, inclusive os auxiliares, e um nome definido em dois módulos é sobrescrito **em silêncio** pelo `import` de baixo. Além disso viola a §18.3 da spec. Correção: importar os nomes explicitamente e declarar `__all__`.

**6. `from src.aurora.modelo import Produto` — funciona por acidente e testa a coisa errada.** Ele importa **pelo caminho de arquivo**, não pelo pacote instalado. Um erro no `pyproject.toml` que impeça o empacotamento passa despercebido, porque o teste nunca usa a instalação. Correção: `from aurora.modelo import Produto`, com o pacote instalado com `-e`.

**A leitura do lote:** **cinco dos seis funcionam**. Só o 4 tende a falhar de imediato, e mesmo ele pode passar num caso simples — que é o pior dos mundos, porque o defeito aparece quando o projeto cresce.

## A4 — Onde mora?

| # | Arquivo | Lugar |
|---|---|---|
| 1 | dataclasses de domínio | `src/aurora/modelo.py` |
| 2 | modelos Pydantic da API | `src/aurora/esquemas.py` |
| 3 | formatação usada por todos | `src/aurora/formato.py` |
| 4 | testes | `tests/`, **fora** de `src/` |
| 5 | configuração do mypy | `pyproject.toml`, em `[tool.mypy]` |
| 6 | script de carga de exemplo | `scripts/`, fora de `src/` |

**Os itens 1 e 2 são a decisão que importa.** Separá-los em dois arquivos torna visível no layout a fronteira do D-024 — Pydantic na borda, dataclass no núcleo. Quem abre a pasta pela primeira vez descobre a arquitetura sem ler código.

**O 3 tem uma regra embutida:** `formato.py` não importa nada do projeto, e é isso que permite que todo mundo o importe sem criar ciclo. Um módulo folha é um bom lugar para o que é usado por todos.

**O 6 costuma sair errado.** Um script de carga não é parte da biblioteca: ele não deve ser instalado na máquina de quem usa o pacote. Se o script for útil ao usuário final, aí sim ele vira um `[project.scripts]` — e o código dele mora em `src/aurora/cli.py`, não solto.

## AP1 — De plano para `src/`

A conversão é mecânica:

```bash
mkdir src && git mv aurora src/aurora
```

```toml
[tool.setuptools.packages.find]
where = ["src"]
```

```bash
pip install -e .
```

**E a parte que ensina.** O defeito do módulo solto continua lá, e dá para encontrá-lo sem ambiente novo:

```
rodando DA pasta do projeto:
    passou — a pasta atual ainda está no path
rodando de QUALQUER OUTRA pasta:
    ModuleNotFoundError: No module named 'utilitarios'
```

**Funciona porque `sys.path[0]` é a pasta atual em `-c` e em `-m`** (§6.2). Rodando da raiz do projeto, `utilitarios.py` está bem ali e é encontrado; rodando de qualquer outro lugar, ele não está — e o pacote, que foi instalado, continua sendo achado normalmente.

É o teste mais barato que existe para essa classe de defeito: **saia da pasta e rode de novo.** Ele não substitui a instalação num ambiente limpo (que também pega arquivos de dados faltando e configuração de empacotamento errada), mas custa um `cd`.

## AP2 — O `pyproject.toml`

O arquivo do projeto de referência, e o que cada seção decide:

```toml
[project]
name = "aurora"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["pydantic==2.13.4"]

[project.optional-dependencies]
dev = ["mypy==2.3.0", "pytest==8.3.4"]

[project.scripts]
aurora = "aurora.cli:main"

[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.mypy]
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
```

Depois de `pip install -e ".[dev]"`, o comando existe:

```
$ aurora
Mouse Sem Fio            R$ 89.90
Teclado Mecanico K2      R$ 329.00
Fone Bluetooth XZ-9      R$ 469.90
TOTAL                    R$ 888.80
```

`aurora = "aurora.cli:main"` significa: crie um executável chamado `aurora` que importe `aurora.cli` e chame `main()`. O pip gera um script no `bin/` do ambiente — o mesmo tipo de arquivo com caminho absoluto na primeira linha que o 04.16/§6.7 mostrou.

**E o teste da dependência acrescentada sem reinstalar:** ela **não** é instalada. Módulo novo dentro do pacote funciona na hora, porque a instalação editável aponta para a sua pasta; dependência é lida do `pyproject.toml` **no momento da instalação**, e acrescentá-la ao arquivo não faz nada até você rodar `pip install -e .` de novo.

É uma distinção que custa tempo quando não se conhece: o sintoma é um `ModuleNotFoundError` para algo que está, visivelmente, declarado no arquivo.

## AP3 — O vazamento

**(a) Por que a cena 2 passa.** Você está na raiz do projeto, e com `python -c` o `sys.path[0]` é a pasta atual. `utilitarios.py` está lá. O import funciona — e funciona por causa de **onde você está**, não por causa de como o pacote foi montado.

**(b) Por que a cena 3 falha, com o mesmo código.** Porque na máquina de quem instala não existe "a pasta do projeto". O pacote foi copiado para o `site-packages`, e o que foi copiado é só o que o `pyproject.toml` declarou como pacote:

```
aurora/__init__.py
aurora/modelo.py
```

`utilitarios.py` estava na raiz, não dentro de `aurora/`, e portanto nunca foi parte do pacote. O código é idêntico; o **contexto** não é.

**(c) O que a cena 6 mostra que a cena 5 não mostra.** A cena 5 mostra o `src/` funcionando: `import aurora` falha antes de instalar, o que obriga a instalação. Isso poderia levar à conclusão de que o `src/` resolve o problema.

A cena 6 mostra que **não resolve inteiramente**. Depois de `pip install -e .`, rodando da pasta do projeto, o módulo solto ainda é encontrado — porque a pasta atual continua no `sys.path`. O `src/` garante que **o pacote** venha da instalação; não garante que nada mais vaze.

É a diferença entre "este layout impede a classe inteira de defeitos" e "este layout impede o caso mais comum e você ainda precisa de disciplina". A segunda afirmação é a verdadeira, e a cena 6 existe para não deixar a primeira passar.

## D1 — O pacote publicável

Não há gabarito de código — o pacote é seu. Há gabarito das três perguntas.

**(1) Como descobrir se um módulo importa algo de fora do pacote.** Três caminhos, do mais barato ao mais confiável:

- `cd` para fora da pasta e importar. Pega o caso do módulo solto (AP1).
- `pip install .` sem `-e`, em ambiente novo, e importar. Pega também arquivos de dados faltando e erro de configuração de empacotamento.
- Ler os imports com `ast` e conferir cada um contra a lista de módulos do pacote e das dependências declaradas. É o mini projeto, e é o único que dá a resposta **completa** sem depender de o código ser executado.

**(2) O custo do submódulo mais barato.** No projeto de referência:

```
import aurora            -> 21,3 ms
import aurora.formato    -> 20,2 ms
formato.py fora do pacote -> 1,6 ms
```

**Importar um submódulo executa o `__init__.py` do pacote primeiro.** Como o nosso reexporta `Produto`, ele traz `dataclasses` (18,7 ms sozinho), e quem só queria `formatar_reais` paga tudo. Não dá para escapar escolhendo o submódulo.

A resposta boa não é "reexportar é ruim" — é reconhecer o custo e decidir: em pacote pequeno, 20 ms uma vez não importam e a legibilidade vale; em biblioteca grande, reexportar pouco é a diferença entre um `import` instantâneo e meio segundo.

**(3) Apagando todos os `__init__.py`.**

**Continua funcionando:** os imports, porque pastas sem `__init__.py` são pacotes de espaço de nomes desde o Python 3.3.

**Para de funcionar:** o `from aurora import Produto`, porque não há mais quem reexporte; o `aurora.__version__`; e `aurora.__file__` passa a ser `None`.

**E passa a ser possível o que não deveria:** uma pasta chamada `aurora` em qualquer outro ponto do `sys.path` **se funde** com a sua, contribuindo módulos para o seu pacote sem aviso.

**Um detalhe que costuma surpreender:** o empacotamento com setuptools moderno **continua incluindo** os subpacotes sem `__init__.py`. A resposta "o pacote quebraria ao instalar" era verdadeira anos atrás e não é mais — vale conferir na sua versão em vez de repetir.

## MP — A auditoria de estrutura

O núcleo, com `ast`:

```python
import ast
from pathlib import Path

def imports_de(arquivo: Path) -> set[str]:
    arvore = ast.parse(arquivo.read_text(encoding="utf-8"), filename=str(arquivo))
    nomes: set[str] = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            nomes.update(alias.name.split(".")[0] for alias in no.names)
        elif isinstance(no, ast.ImportFrom) and no.level == 0 and no.module:
            nomes.add(no.module.split(".")[0])
    return nomes
```

E a checagem do vazamento:

```python
raiz_pacote = Path("src") / nome_do_pacote
internos = {p.stem for p in raiz_pacote.rglob("*.py")} | {nome_do_pacote}
for arquivo in raiz_pacote.rglob("*.py"):
    for importado in imports_de(arquivo):
        if importado in soltos_na_raiz and importado not in internos:
            print("VAZAMENTO:", arquivo, "importa", importado)
```

**Dois detalhes de método.** O `no.level == 0` separa import absoluto de relativo — num `from .precos import TAXA`, `level` é 1 e `module` é `"precos"`, que não é um módulo de topo. E comparar contra a lista de dependências declaradas no `pyproject.toml` evita acusar `pydantic` de vazamento.

**A pergunta que fecha: por que `ast`?**

**Segurança:** `import` **executa** o módulo. Auditar um projeto desconhecido importando os arquivos dele significa rodar código de terceiros — inclusive o que estiver no nível do módulo, que roda na hora. Uma ferramenta de auditoria que executa o que audita é uma contradição.

**Correção:** expressão regular não lê Python. Este import é válido e nenhuma expressão razoável o casa:

```python
from a.b import (
    c,
    d,
)
```

E o problema não para aí: há `import a as b`, imports dentro de função, imports dentro de `try`, imports em uma linha separados por vírgula, e a palavra `import` dentro de uma string ou de um comentário — que a expressão regular vai casar alegremente. O `ast` resolve todos pelo mesmo mecanismo, porque ele **é** o analisador do Python: se o arquivo é Python válido, o `ast` o entende exatamente como o interpretador entenderia, sem executar nada.

É o mesmo princípio do 04.14: uma ferramenta que lê a estrutura do código dá respostas que nenhuma busca por texto dá.
