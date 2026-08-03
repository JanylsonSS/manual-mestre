# Exercícios — Capítulo 01.10: Laço `while`

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap10.md`](gabaritos/cap10.md).

## Aquecimento

### A1 — Previsão de voltas `[Aquecimento · ~10 min · a catraca]`

**Tarefa.** Para cada laço: quantas voltas, o que imprime, e o valor final da variável de controle:

```python
n = 10
while n > 0:
    print(n)
    n -= 3
```

```python
saldo = 100
while saldo >= 40:
    saldo = saldo - 25
print(saldo)
```

```python
x = 1
while x < 100:
    x = x * 2
print(x)
```

```python
i = 5
while i < 5:
    print("roda?")
    i += 1
print("depois:", i)
```

### A2 — Diagnóstico dos demônios `[Aquecimento · ~10 min · doentes e saudáveis]`

**Tarefa.** Classifique cada laço (saudável / infinito / zero-voltas / acumulador renascendo) e conserte os doentes:

```python
total = 0
n = 1
while n <= 5:
    total += n
```

```python
n = 1
while n <= 5:
    total = 0
    total += n
    n += 1
print(total)
```

```python
contador = 10
while contador <= 5:
    print(contador)
    contador += 1
```

```python
soma = 0
n = 1
while n <= 4:
    soma += n
    n += 1
print(soma)
```

### A3 — break e continue `[Aquecimento · ~5 min · saídas e atalhos]`

**Tarefa.** Preveja a saída exata:

```python
n = 0
while True:
    n += 1
    if n == 3:
        break
    print(n)
```

```python
n = 0
while n < 5:
    n += 1
    if n == 3:
        continue
    print(n)
```

```python
n = 0
while n < 3:
    print("a")
    n += 1
else_texto = "fim"
print(else_texto)
```

### A4 — while ou for? `[Aquecimento · ~5 min · a regra de bolso]`

**Tarefa.** Para cada situação, qual laço é o natural: (1) pedir CPF até vir válido; (2) imprimir as parcelas de 2× a 12×; (3) processar itens até o usuário digitar "fim"; (4) repetir uma cobrança até o gateway confirmar; (5) contar as vogais de um nome; (6) atender clientes até o caixa fechar.

## Aplicação

### AP1 — A borda que insiste `[Aplicação · ~20 min · pagando a pendência]`

**Tarefa.** `borda_insistente.py`: refatore as duas entradas do balcão v2 (valor e parcelas) para o padrão `while True` + break — cada recusa ensina o formato e **pergunta de novo**. Teste digitando lixo 3 vezes seguidas antes do valor válido.

### AP2 — Caixa com sentinela `[Aplicação · ~20 min · acumulador de verdade]`

**Tarefa.** `caixa_do_dia.py`: leia valores de itens em centavos até `"fim"`; acumule total e contagem; no fechamento imprima total, número de itens e ticket médio em reais — com o escudo do 01.08 para o caixa vazio (fechar sem nenhum item não pode explodir).

<details><summary>💡 Dica 1 (conceito)</summary>
Ticket médio = total / contagem — e contagem pode ser 0. Guarda primeiro: `contagem != 0 and ...`, ou um if para o caso vazio com mensagem própria.
</details>

### AP3 — Jogo da adivinhação `[Aplicação · ~20 min · o clássico]`

**Tarefa.** `adivinhacao.py`: número secreto fixo (ex.: 42), o usuário chuta até acertar; a cada erro, dica "maior" ou "menor"; entrada não numérica é recusada sem contar tentativa; ao acertar, o total de tentativas válidas.

## Desafio

### D1 — Simulador de senha `[Desafio · ~45 min · varredura com while]`

**Tarefa.** Cadastro que insiste até a senha cumprir: 8+ caracteres, ≥1 dígito, ≥1 maiúscula — mostrando TODOS os critérios que faltaram a cada recusa. Validada, pedir confirmação; não bateu, recomeça. Varredura da senha com while + índice (sem métodos novos: dígito via `"0" <= c <= "9"`, maiúscula via `"A" <= c <= "Z"`).

**Restrições.** Ferramentas até o 01.10. O desconforto do índice manual é proposital — anuncia o `for`.

<details><summary>💡 Dica 1 (conceito)</summary>
Laudos como acumuladores booleanos: `tem_digito = False` antes da varredura; vira True se achar. Ao final, ifs INDEPENDENTES para listar todas as faltas.
</details>
<details><summary>💡 Dica 2 (estratégia)</summary>
Estruture: while True (cadastro) → varredura → ifs das faltas → se ok: confirmação → bate? break.
</details>
<details><summary>💡 Dica 3 (esqueleto)</summary>
i = 0 / while i < len(senha): c = senha[i] / testes / i += 1 — o andaime completo, pela última vez.
</details>
