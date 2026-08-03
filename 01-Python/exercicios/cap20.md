# Exercícios — Capítulo 01.20: Módulos e imports

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap20.md`](gabaritos/cap20.md).

## Aquecimento

### A1 — Previsão de importação `[Aquecimento · ~10 min · o que executa]`

**Tarefa.** Para cada par de arquivos, diga o que `python programa.py` imprime e em que ordem:

```python
# 1 — util.py
print("A")
def f(): print("B")
# 1 — programa.py
import util
util.f()
```

```python
# 2 — util.py
def f(): print("B")
if __name__ == "__main__":
    print("A")
# 2 — programa.py
import util
util.f()
```

```python
# 3 — util.py
def f(): print("B")
print("A")
# 3 — programa.py
from util import f
print("C")
```

```python
# 4 — util.py (executado diretamente: python util.py)
def f(): print("B")
if __name__ == "__main__":
    f()
    print("A")
```

### A2 — O valor de `__name__` `[Aquecimento · ~5 min · o interruptor]`

**Tarefa.** Qual o valor de `__name__` em cada situação?

1. Dentro de `util.py`, executado com `python util.py`.
2. Dentro de `util.py`, quando importado por `programa.py`.
3. Dentro de `programa.py`, executado com `python programa.py`.
4. Dentro de um módulo da biblioteca padrão que você importou.

### A3 — Formas de importar `[Aquecimento · ~10 min · o que funciona]`

**Tarefa.** Após cada import, qual chamada funciona?

1. `import biblioteca_aurora` → `formatar_reais(100)` ou `biblioteca_aurora.formatar_reais(100)`?
2. `from biblioteca_aurora import formatar_reais` → as duas formas acima?
3. `import biblioteca_aurora as ba` → `ba.formatar_reais(100)`?
4. `from biblioteca_aurora import formatar_reais as fr` → `fr(100)`?
5. Após a forma 2, `biblioteca_aurora.calcular_frete(...)` funciona?
6. Qual das formas é proibida pela spec — e por quê?

### A4 — Diagnóstico `[Aquecimento · ~5 min · erros de import]`

**Tarefa.** Causa e correção:

```text
ModuleNotFoundError: No module named 'biblioteca_aurora'
```

```text
AttributeError: module 'random' has no attribute 'randint'
```

```text
ImportError: cannot import name 'formatar_real' from 'biblioteca_aurora'
```

## Aplicação

### AP1 — A biblioteca importável `[Aplicação · ~20 min · o interruptor na prática]`

**Tarefa.** Converta sua `biblioteca_aurora_v2.py` (01.19) em módulo: definições no nível do arquivo, autoteste dentro de `if __name__ == "__main__":`. Crie `usa_biblioteca.py` que a importa e chama 3 funções. Prove (com as duas execuções) que o autoteste não aparece no segundo.

### AP2 — Dois programas, uma biblioteca `[Aplicação · ~20 min · zero duplicação]`

**Tarefa.** Escreva `relatorio.py` (imprime a tabela de pedidos com totais) e `balcao.py` (simula um parcelamento) — ambos com `main()` e `if __name__`, ambos consumindo o **mesmo** módulo, nenhum com função duplicada.

### AP3 — A biblioteca padrão `[Aplicação · ~20 min · o que vem de fábrica]`

**Tarefa.** Em `explorando_padrao.py`, use: `datetime` (data de hoje no formato brasileiro), `random` (sorteie 3 pedidos de uma lista de 8), `pathlib` (imprima o caminho da pasta atual) e `statistics` (média e mediana dos valores). Para cada um, escreva 1 linha: quanto código você economizou em relação a fazer à mão?

## Desafio

### D1 — O pacote da Aurora `[Desafio · ~50 min · arquitetura em três módulos]`

**Tarefa.** Divida a biblioteca em `formatacao.py`, `regras.py` e `validacao.py` (cada um com autoteste protegido) + `sistema.py` que importa os três e gera um relatório. Regras: zero duplicação, imports no topo, nenhum `import *`. Fecho: diagrama textual das dependências + 5 linhas sobre import circular (teste `regras.py` importando `sistema.py` e leia o erro).

<details><summary>💡 Dica 1 (conceito)</summary>
Dependência saudável aponta para baixo: formatação e validação não conhecem regras nem sistema.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Se `regras.py` "precisa formatar", questione: formatar é responsabilidade de quem apresenta, não de quem calcula (01.18).
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
formatacao (base) → validacao (base) → regras (usa validacao) → sistema (usa os três) → diagrama + experimento circular.
</details>
