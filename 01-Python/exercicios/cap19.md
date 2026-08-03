# Exercícios — Capítulo 01.19: Funções parte 2

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap19.md`](gabaritos/cap19.md).

## Aquecimento

### A1 — LEGB `[Aquecimento · ~10 min · onde o nome vive]`

**Tarefa.** Preveja a saída de cada trecho:

```python
# 1
x = 5
def f(): print(x)
f()
```

```python
# 2
x = 5
def f(): x = 9; print(x)
f(); print(x)
```

```python
# 3
def f(): print(y)
f()
```

```python
# 4
len = 3
def f(): print(len)
f()
```

```python
# 5
x = 5
def f(x): x = x + 1; return x
print(f(x), x)
```

```python
# 6
total = 0
def somar(v):
    total = total + v      # o que acontece?
    return total
somar(10)
```

### A2 — Muta ou não? `[Aquecimento · ~10 min · o verbo decide]`

**Tarefa.** Cada função recebe `dados` (lista) ou `mapa` (dicionário). A estrutura de quem chamou é alterada?

1. `def f(dados): dados.append(1)`
2. `def f(dados): dados = dados + [1]`
3. `def f(dados): dados = [1]; return dados`
4. `def f(dados): return sorted(dados)`
5. `def f(mapa): mapa["novo"] = 1`
6. `def f(dados): dados[0] = 99`

### A3 — Padrão mutável `[Aquecimento · ~5 min · seguro ou bomba?]`

**Tarefa.** Classifique cada assinatura:

1. `def f(x, itens=[])`
2. `def f(x, itens=None)`
3. `def f(x, nome="")`
4. `def f(x, config={})`

### A4 — Diagnóstico `[Aquecimento · ~10 min · três tracebacks]`

**Tarefa.** Para cada erro: causa e correção.

```text
UnboundLocalError: cannot access local variable 'total' where it is not associated with a value
```

```text
NameError: name 'resultado' is not defined
```

```text
TypeError: 'NoneType' object is not iterable
```

(o último ocorre em `for x in minha_funcao():`)

## Aplicação

### AP1 — O contador consertado `[Aplicação · ~20 min · três versões]`

**Tarefa.** Escreva um contador de pedidos em 3 versões: (a) com `global`; (b) com parâmetro/retorno; (c) com um dicionário de estado passado como argumento. Para cada uma, escreva 2 linhas sobre testabilidade — qual você conseguiria testar sem rodar o programa inteiro?

### AP2 — Funções que não surpreendem `[Aplicação · ~25 min · eliminando mutação]`

**Tarefa.** Reescreva sem mutar os argumentos:

```python
def normalizar(cidades):
    for i in range(len(cidades)):
        cidades[i] = cidades[i].strip().lower()

def adicionar_taxa(mapa, taxa):
    for k in mapa:
        mapa[k] = mapa[k] + taxa

def top3(valores):
    valores.sort(reverse=True)
    return valores[:3]

def limpar_invalidos(registros):
    for r in registros[:]:
        if r[2] <= 0:
            registros.remove(r)
```

Para cada uma, prove com o teste "antes e depois" que o original ficou intacto.

### AP3 — A prova do `__defaults__` `[Aplicação · ~20 min · experimento]`

**Tarefa.** Escreva a função com padrão mutável, chame-a 3 vezes (duas sem argumento, uma com lista própria), imprima `funcao.__defaults__` após cada chamada, e depois a versão corrigida com as mesmas 3 chamadas. Escreva 3 linhas explicando o que o `__defaults__` revelou.

## Desafio

### D1 — A auditoria de pureza `[Desafio · ~50 min · tribunal das funções]`

**Tarefa.** Para as 8 funções da sua `biblioteca_aurora.py` (01.18): (a) lê global? (b) muta argumento? (c) tem efeito colateral? → classifique em pura / impura controlada / impura acidental; corrija as acidentais. Acrescente 2 funções deliberadamente impuras e bem nomeadas. Fecho: 5 linhas sobre "pura por padrão, impura por decisão".

<details><summary>💡 Dica 1 (conceito)</summary>
Teste da pureza: duas chamadas iguais dão o mesmo resultado E deixam o mundo igual?
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Formatação e cálculo tendem a ser puros; input e print são impuros por natureza — e tudo bem, desde que o nome avise.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
Tabela de auditoria (função | global? | muta? | efeito? | classificação | ação) → correções → 2 novas impuras → reflexão.
</details>
