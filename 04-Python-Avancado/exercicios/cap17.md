# Exercícios — Capítulo 04.17: Organização de projetos

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap17.md`](gabaritos/cap17.md).

> Vários exercícios criam projetos. Faça numa pasta descartável.

## Aquecimento

### A1 — O import funciona? `[Aquecimento · ~10 min]`

Estrutura:

```
projeto/
├── loja/
│   ├── __init__.py
│   ├── precos.py         (TAXA = 0.15)
│   └── relatorio.py      (from loja.precos import TAXA)
└── util.py
```

Para cada comando, diga se funciona — e, se não, qual o erro.

1. `cd projeto && python -m loja.relatorio`
2. `cd projeto && python loja/relatorio.py`
3. `cd projeto && python -c "import loja"`
4. `cd / && python /caminho/projeto/loja/relatorio.py`
5. `cd projeto/loja && python relatorio.py`
6. `cd projeto && python -c "import util"`
7. `cd / && python -c "import util"`
8. `cd projeto && python -m loja` (sem `__main__.py`)

### A2 — Preveja a saída `[Aquecimento · ~12 min]`

```python
# 1  — relatorio.py, com `from .precos import TAXA`
#      rodado como: python loja/relatorio.py

# 2  — o mesmo, rodado como: python -m loja.relatorio

# 3
import aurora
print(aurora.__file__)          # pacote com __init__.py
print(aurora.__path__)

# 4  — pacote SEM __init__.py
import aurora
print(aurora.__file__)

# 5
import sys
print(sys.path[0])              # rodado como: python -m pacote.mod

# 6
# a.py:  from ciclo.b import beta
# b.py:  from ciclo.a import alfa
import ciclo.a
```

### A3 — Ache o erro `[Aquecimento · ~12 min]`

```
# 1
projeto/
├── aurora/
│   └── modelo.py     (from helpers import limpar)
├── helpers.py
└── pyproject.toml

# 2
projeto/
└── src/
    └── aurora/
        ├── __init__.py
        ├── modelo.py
        └── tests/
            └── test_modelo.py

# 3  — no topo de aurora/servico.py
import sys
sys.path.append("../outro-projeto")
from outro import coisa

# 4  — pyproject.toml
[project]
name = "aurora"
version = "0.1.0"
dependencies = ["pydantic==2.13.4"]

# 5  — aurora/__init__.py
from aurora.modelo import *
from aurora.catalogo import *
from aurora.formato import *

# 6
projeto/
├── src/aurora/...
└── tests/test_modelo.py    (from src.aurora.modelo import Produto)
```

### A4 — Onde mora? `[Aquecimento · ~10 min]`

Diga em que pasta cada arquivo vai, no layout do capítulo:

1. As dataclasses de domínio.
2. Os modelos Pydantic que recebem o JSON da API.
3. Uma função de formatação usada por todo o pacote.
4. Os testes.
5. A configuração do mypy.
6. Um script que você roda uma vez para carregar dados de exemplo.

---

## Aplicação

### AP1 — De plano para `src/` `[Aplicação · ~20 min]`

Pegue um projeto de layout plano (o do `vazamento.sh` serve) e converta para `src/`.

Requisitos: mover o pacote; ajustar o `pyproject.toml`; instalar com `-e`; e rodar os testes.

**Depois, a parte que ensina:** o defeito do módulo solto continua lá. Encontre-o **sem** instalar num ambiente novo — só mudando de pasta antes de rodar. Explique por que isso funciona.

### AP2 — O `pyproject.toml` `[Aplicação · ~25 min]`

Escreva um `pyproject.toml` do zero para um pacote seu.

Requisitos: nome, versão, descrição, `requires-python`, dependências, grupo `dev`, **um comando de terminal** que faça algo útil, `[tool.mypy]` com `strict = true` e `[tool.pytest.ini_options]` com `testpaths`.

Instale com `pip install -e ".[dev]"` e prove que o comando aparece no `PATH` do ambiente. Depois acrescente uma dependência ao arquivo, **sem reinstalar**, e veja o que acontece.

### AP3 — O vazamento `[Aplicação · ~20 min]`

Rode [`../codigo/cap17/vazamento.sh`](../codigo/cap17/vazamento.sh) e explique as seis cenas por escrito.

Três perguntas específicas: (a) por que a cena 2 passa? (b) por que a cena 3 falha, se o código é o mesmo? (c) o que a cena 6 mostra que a cena 5 não mostra?

---

## Desafio

### D1 — O pacote publicável `[Desafio · ~50 min]`

Transforme o código do módulo 04 que você quiser num pacote instalável, com layout `src/`.

**Requisitos:**

- `pyproject.toml` completo: `requires-python`, dependências, grupo `dev`, ao menos um `[project.scripts]`, `[tool.mypy]` e `[tool.pytest.ini_options]`.
- `__init__.py` com API pública e `__all__`.
- `tests/` fora de `src/`, importando pelo nome do pacote.
- `mypy --strict` e `pytest` limpos.

**A prova que vale metade da nota:** instale com `pip install .` (**sem** o `-e`) num ambiente novo, **saia da pasta do projeto** e importe. Precisa funcionar.

**As três perguntas que valem a outra metade:**

1. Algum módulo do seu pacote importa algo que não está dentro dele? Como você descobriu?
2. Quanto custa importar o **submódulo mais barato** do seu pacote? Meça com `python -X importtime` e explique o número.
3. Se você apagasse todos os `__init__.py`, o que pararia de funcionar e o que continuaria?

---

## Mini projeto

### MP — A auditoria de estrutura `[Mini projeto · ~40 min]`

Um `auditar.py` que receba a pasta de um projeto e aponte problemas de organização.

**Requisitos — o script deve detectar:**

- pastas de pacote sem `__init__.py`;
- imports de módulos que estão **fora** do pacote (o defeito da §3);
- imports circulares;
- testes dentro de `src/`;
- `pyproject.toml` sem `requires-python` ou sem `[build-system]`.

**A restrição:** apenas biblioteca padrão. Use `ast` para ler os imports e `pathlib` para caminhar na árvore.

**E a pergunta que fecha:** por que ler os imports com `ast` e não com `import` nem com expressão regular?

A resposta tem uma parte de **segurança** e uma de **correção**. A de correção você descobre tentando casar isto com uma expressão regular:

```python
from a.b import (
    c,
    d,
)
```
