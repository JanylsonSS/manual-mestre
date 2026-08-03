# Exercícios — Capítulo 01.21: Exceções

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap21.md`](gabaritos/cap21.md).

## Aquecimento

### A1 — Qual exceção? `[Aquecimento · ~10 min · o tipo importa]`

**Tarefa.** Qual tipo cada operação levanta?

1. `int("abc")`
2. `"2" + 2`
3. `{"a": 1}["b"]`
4. `[1, 2][5]`
5. `10 / 0`
6. `open("nao_existe.txt")`
7. `"texto".append("x")`
8. `int(None)`

### A2 — Previsão de fluxo `[Aquecimento · ~10 min · try/except/else/finally]`

**Tarefa.** Preveja a saída exata:

```python
# 1
try:
    print("A")
    x = 1 / 0
    print("B")
except ZeroDivisionError:
    print("C")
finally:
    print("D")
print("E")
```

```python
# 2
try:
    print("A")
except ValueError:
    print("B")
else:
    print("C")
finally:
    print("D")
```

```python
# 3
try:
    int("abc")
except TypeError:
    print("capturei")
print("cheguei aqui?")
```

```python
# 4
def f():
    try:
        return "try"
    finally:
        print("finally")
print(f())
```

```python
# 5
try:
    try:
        int("x")
    except ValueError:
        print("interno")
        raise
except ValueError:
    print("externo")
```

### A3 — Específico ou genérico? `[Aquecimento · ~5 min · o crime]`

**Tarefa.** Aponte o problema e corrija:

1. `try: ... except: pass`
2. `try: ... except Exception: print("erro")`
3. `try: valor = int(t); dados = abrir(p); calc(dados) except ValueError: print("erro")`
4. `try: mapa[k] except KeyError: valor = 0` (executado a cada volta de um laço)

### A4 — EAFP ou LBYL? `[Aquecimento · ~10 min · o critério]`

**Tarefa.** Qual estilo para cada caso, e por quê?

1. Converter entrada do usuário em número.
2. Verificar se uma lista está vazia antes de acessar `[0]`.
3. Abrir um arquivo que pode não existir.
4. Buscar uma chave opcional num dicionário.
5. Dividir por um valor que veio de fora.
6. Verificar se um número é positivo antes de calcular a raiz.

## Aplicação

### AP1 — A borda blindada `[Aplicação · ~20 min · pagando a pendência]`

**Tarefa.** Refaça a conversão de valores do balcão com `try/except ValueError`, dentro do `while True` de insistência (01.10). Teste com: `"1399,90"`, `"R$ 1.399,90"`, `"12.3.4"`, `""`, `"abc"`, `"  99  "` — nenhuma deve derrubar o programa, e as válidas devem passar.

### AP2 — Miolo levanta, borda trata `[Aplicação · ~25 min · contratos]`

**Tarefa.** Adicione `raise ValueError` com mensagem útil a 3 funções da sua biblioteca (frete com total negativo, parcelas < 1, código não-string). Escreva um programa que as chama com valores inválidos e trata **na borda**, imprimindo o erro com contexto — sem quebrar.

### AP3 — O processador tolerante `[Aplicação · ~20 min · try por linha]`

**Tarefa.** Dada a lista de 8 linhas abaixo, processe com `try/except` **por linha**, produzindo `processados` e `rejeitados` (com motivo):

```python
linhas = [
    "PED-1;Fone;46990;Campinas",
    "PED-2;Mouse;abc;Santos",
    "PED-3;Teclado;34900",
    "PED-4;Cabo;9890;Sorocaba",
    "",
    "PED-6;Webcam;47890;São Paulo",
    "PED-7;Headset;-100;Campinas",
    "PED-8;Monitor;129900;Santos",
]
```

## Desafio

### D1 — A quarentena `[Desafio · ~50 min · importador tolerante]`

**Tarefa.** Importador de 12 linhas (5 defeituosas, defeitos variados) produzindo: `registros`, `quarentena` (com número da linha, original, tipo do erro e mensagem) e relatório de importação com funil e quebra por tipo. Regras: um `try` por linha; captura específica por tipo esperado; `except Exception` final registrando o inesperado sem engolir. Fecho: 5 linhas comparando quarentena com (a) derrubar tudo e (b) ignorar em silêncio.

<details><summary>💡 Dica 1 (conceito)</summary>
O try envolve o processamento de UMA linha — dentro do laço, não em volta dele.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Cada defeito tem sua exceção natural: campo faltando → IndexError; valor não numérico → ValueError; regra de negócio → seu raise.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
for numero, linha in enumerate(linhas, 1): try: ... except IndexError: ... except ValueError: ... except Exception as e: (registra como NÃO PREVISTO) → relatório.
</details>
