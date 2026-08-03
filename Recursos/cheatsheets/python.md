# Cheatsheet — Python fundamental (Módulo 01)

Gerada no fechamento do módulo 01. Índice de memória, não substituto de estudo — cada linha referencia o capítulo de origem.

## Tipos e conversões

| Operação | Exemplo | Ref. |
|---|---|---|
| Tipo do objeto | `type(x)` | 01.03 |
| Identidade × valor | `a is b` (mesmo objeto) · `a == b` (mesmo valor) | 01.03 |
| Converter | `int(t)` · `float(t)` · `str(n)` · `list(s)` · `tuple(l)` · `set(l)` | 01.04, 01.12 |
| Truncar × arredondar | `int(9.9)` → 9 · `round(9.9)` → 10 | 01.04 |
| Dinheiro | centavos como `int`; `/100` só na exibição | 01.04 |

## Operadores

| Operador | Efeito | Ref. |
|---|---|---|
| `/` | divisão real — **sempre float** | 01.04 |
| `//` `%` | piso e resto — "grupos completos + sobra" | 01.04 |
| `**` | potência | 01.04 |
| `+=` `-=` `*=` | atribuição com operação | 01.04 |
| `in` / `not in` | pertencimento (string, lista, dict-chaves, set) | 01.08, 01.16 |
| `and` `or` `not` | lógicos com **curto-circuito** (guarda primeiro) | 01.08 |

## Strings

| Operação | Exemplo | Ref. |
|---|---|---|
| Fatia | `s[inicio:fim:passo]` — fim **exclusivo** | 01.05 |
| Último caractere | `s[-1]` | 01.05 |
| Canônica | `s.strip().lower()` | 01.06 |
| Exibição | `s.title()` | 01.06 |
| Trocar | `s.replace(velho, novo)` (todas as ocorrências) | 01.06 |
| Desmontar / montar | `s.split(sep)` → lista · `sep.join(lista)` | 01.06 |
| Laudos | `startswith`, `endswith`, `find` (-1 se ausente), `isdigit` | 01.06 |
| f-string | `f"{v:.2f}"` `f"{s:<10}"` `f"{s:>10}"` `f"{n:05d}"` `f"{n:,.2f}"` | 01.06 |
| Reais BR | `f"{c/100:,.2f}".replace(",","@").replace(".",",").replace("@",".")` | 01.06 |

## Fluxo

| Estrutura | Forma | Ref. |
|---|---|---|
| Condicional | `if` / `elif` / `else` — primeira verdadeira executa | 01.09 |
| Guarda | `if not valido: return` (early return) | 01.09, 01.18 |
| Repetir por condição | `while cond:` (inicializa/testa/avança) | 01.10 |
| Insistir | `while True:` + `break` na validação | 01.10 |
| Percorrer | `for item in colecao:` | 01.11 |
| Contagem | `range(inicio, fim, passo)` — fim exclusivo | 01.11 |
| Com posição | `for i, item in enumerate(seq, start=1):` | 01.12 |

## Estruturas

| Estrutura | Quando | Operações-chave | Ref. |
|---|---|---|---|
| `list` | coleção ordenada que cresce | `append`, `sort()`/`sorted()`, `copy()`, fatias | 01.12, 01.13 |
| `tuple` | registro imutável de campos | desempacotamento `a, b = t` | 01.14 |
| `dict` | chave → valor | `d.get(k, 0)`, `d.setdefault(k, [])`, `.items()` | 01.15 |
| `set` | unicidade e pertinência | `add`, `|`, `&`, `-`, `^` | 01.16 |

**Padrões:** acumular `d[k] = d.get(k, 0) + v` · agrupar `d.setdefault(k, []).append(x)` · dedupe com ordem: conjunto de vistos + lista.

## Comprehensions

```python
[expr for item in seq if cond]        # lista
{k: v for k, v in pares if cond}      # dicionário
{expr for item in seq}                # conjunto
```

Limite: um `for`, um `if`, uma linha legível (senão, laço explícito). Ref. 01.17

## Funções e módulos

| Item | Forma | Ref. |
|---|---|---|
| Definir | `def nome(param, opcional=None):` + docstring | 01.18 |
| Retornar vários | `return a, b` → `x, y = f()` | 01.18 |
| Padrão mutável | **nunca** `=[]`; use `None` + criação interna | 01.19 |
| Escopo | LEGB; ler é livre, escrever é local | 01.19 |
| Importar | `import mod` · `from mod import nome` · nunca `import *` | 01.20 |
| Entrada do programa | `if __name__ == "__main__": main()` | 01.20 |

## Exceções

```python
try:
    valor = int(texto)
except ValueError as erro:
    ...
else:
    ...          # só se nada falhou
finally:
    ...          # sempre
raise ValueError(f"esperava X, recebi {valor}")
```

Tipos: `ValueError`, `TypeError`, `KeyError`, `IndexError`, `ZeroDivisionError`, `FileNotFoundError`, `AttributeError`. Regra: específico sempre; **miolo levanta, borda trata**. Ref. 01.21

## Arquivos e formatos

```python
with open(caminho, encoding="utf-8") as f:      # sempre with + encoding
    for linha in f: ...

import csv
with open(p, encoding="utf-8", newline="") as f:
    for linha in csv.DictReader(f, delimiter=";"): ...

import json
json.dump(obj, f, ensure_ascii=False, indent=2) / json.load(f)

from pathlib import Path
Path(__file__).parent / "dados" / "x.csv"
```

Modos: `r` lê · `w` **trunca** · `a` acrescenta · `x` cria se não existir. Ref. 01.22, 01.23

## Depuração (VS Code)

| Ação | Tecla | Ref. |
|---|---|---|
| Continuar | F5 | 01.24 |
| Passar por cima | F10 | 01.24 |
| Entrar na função | F11 | 01.24 |
| Sair da função | Shift+F11 | 01.24 |
| Laço longo | breakpoint **condicional** ou logpoint | 01.24 |

Método: sintoma → reprodução mínima → hipótese → experimento → conclusão.

## PEP 8 (essencial)

`snake_case` funções/variáveis · `MAIUSCULAS` constantes · `PascalCase` classes · 4 espaços · espaços em volta de operadores e após vírgulas · imports agrupados no topo · docstring por função · linhas curtas. Ref. 01.25
