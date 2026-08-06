# Exercícios — Capítulo 04.22: Asyncio — fundamentos

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap22.md`](gabaritos/cap22.md).

> Rode tudo com `asyncio.run(...)` na raiz. Um `await` fora de uma função `async` é erro de sintaxe.

## Aquecimento

### A1 — Roda ou não? `[Aquecimento · ~10 min]`

Para cada trecho, diga se o corpo da corrotina é executado — e o que aparece na tela.

```python
async def tarefa():
    print("rodei")
    return 1

# 1
tarefa()

# 2
asyncio.run(tarefa())

# 3
await tarefa()                      # no nível do módulo

# 4
async def principal():
    await tarefa()
asyncio.run(principal())

# 5
async def principal():
    asyncio.create_task(tarefa())
asyncio.run(principal())

# 6
async def principal():
    t = asyncio.create_task(tarefa())
    await asyncio.sleep(0)
asyncio.run(principal())

# 7
async def principal():
    await asyncio.gather(tarefa(), tarefa())
asyncio.run(principal())

# 8
asyncio.run(tarefa)                 # sem os parênteses
```

### A2 — Preveja o tempo `[Aquecimento · ~12 min]`

Com `async def e(s): await asyncio.sleep(s)`:

```python
# 1
await asyncio.gather(e(0.2), e(0.2), e(0.2))

# 2
await e(0.2); await e(0.2); await e(0.2)

# 3
await asyncio.gather(e(0.1), e(0.3), e(0.2))

# 4
tarefas = [asyncio.create_task(e(0.2)) for _ in range(3)]
for t in tarefas:
    await t

# 5
await asyncio.gather(asyncio.gather(e(0.2), e(0.2)), e(0.2))

# 6
e(0.2); e(0.2)
```

### A3 — Ache o erro `[Aquecimento · ~12 min]`

```python
# 1
async def coletar(urls):
    return [await buscar(u) for u in urls]

# 2
async def salvar(dados):
    with open("saida.json", "w") as f:
        json.dump(dados, f)

# 3
async def principal():
    asyncio.create_task(processar_em_segundo_plano())
    await servir()

# 4
async def buscar_tudo(skus):
    resultados = []
    for sku in skus:
        async with httpx.AsyncClient() as cliente:
            resultados.append(await cliente.get(f"/p/{sku}"))
    return resultados

# 5
async def lote(itens):
    return await asyncio.gather(*[processar(i) for i in itens])
    # um item ruim entre mil

# 6
async def calcular(numeros):
    total = 0
    for n in numeros:            # 50 milhões de números
        total += n * n
    return total
```

### A4 — Asyncio, threads ou processos? `[Aquecimento · ~10 min]`

1. 30 mil conexões WebSocket abertas ao mesmo tempo.
2. 20 requisições HTTP num script que já usa `requests`.
3. Calcular o hash de 5 mil arquivos.
4. Um servidor FastAPI consultando banco a cada requisição.
5. Ler 100 arquivos do disco local e somar as colunas.
6. Um bot que atende 200 conversas simultâneas.

---

## Aplicação

### AP1 — O `gather` `[Aplicação · ~20 min]`

Escreva uma função que busque 20 itens com espera simulada de 0,2 s, primeiro em sequência e depois com `gather`. Meça as duas.

Requisitos: as duas devolvem **exatamente** a mesma lista, na mesma ordem; a medição usa `perf_counter`; e a diferença é exibida como razão.

**A pergunta que separa:** `gather` preserva a ordem dos resultados mesmo que as tarefas terminem fora de ordem? Prove com tempos diferentes por item.

### AP2 — O bloqueio `[Aplicação · ~25 min]`

Este código deveria levar ~0,3 s e leva ~3 s:

```python
async def processar(item):
    dados = await buscar(item)          # 0,3 s
    return transformar(dados)           # ???

async def principal():
    return await asyncio.gather(*[processar(i) for i in range(10)])
```

Escreva um `transformar` que **bloqueie** por 0,27 s (com `time.sleep`) e confirme o problema. Depois conserte de duas formas diferentes e meça as duas.

**A pergunta que fecha:** as duas correções dão tempos parecidos? Se sim, como escolher entre elas — e o que mudaria se `transformar` fosse cálculo puro em vez de espera?

### AP3 — Exceções em lote `[Aplicação · ~20 min]`

Processe 20 itens, dos quais 3 falham por motivos diferentes.

Requisitos: usar `return_exceptions=True`; separar sucessos de falhas; registrar cada falha com `log.exception` e o índice do item; e devolver um resumo com as duas contagens.

Depois, **repita com `return_exceptions=False`** e responda: quantos resultados bons você perdeu, e o que aconteceu com as corrotinas que ainda estavam rodando?

---

## Desafio

### D1 — O coletor assíncrono `[Desafio · ~50 min]`

Reescreva o coletor do 04.21 em asyncio, com controle de concorrência.

**Requisitos:**

- 300 itens, espera simulada de ~200 ms.
- `asyncio.Semaphore` limitando a concorrência, com valor configurável.
- `return_exceptions=True`, com separação de sucessos e falhas.
- Log estruturado (04.19) por item e um resumo no fim.
- Tempo medido por etapa.
- `mypy --strict` limpo.

**A prova:** rode com o semáforo valendo 1, 10, 50 e 300 e faça a tabela.

**As três perguntas que valem a nota:**

1. Compare sua tabela com a do 04.21/AP2, feita com threads. Os tetos são iguais?
2. Introduza um `time.sleep(0.1)` em **uma** das corrotinas e meça de novo. O que acontece com as **outras 299**?
3. Com `return_exceptions=False`, se uma corrotina falhar, o que acontece com as que ainda estavam rodando?

---

## Mini projeto

### MP — O detector de bloqueio `[Mini projeto · ~40 min]`

Uma ferramenta que descubra se o laço de eventos está sendo travado — e por quanto tempo.

**Requisitos:**

- Uma corrotina "vigia" que acorde a cada 50 ms e meça o **atraso** em relação ao esperado.
- Registro de todo atraso acima de um limite, com a duração.
- Relatório final: pior atraso e quantas vezes o limite foi ultrapassado.
- Demonstração com três casos: sem bloqueio, com `time.sleep(0.5)` e com um cálculo pesado.
- Só biblioteca padrão.

O cálculo do atraso é a parte que ensina: compare o tempo que **deveria** ter passado com o que passou de fato.

**E a pergunta que fecha:** o seu vigia detecta o bloqueio **depois** que ele termina, nunca durante.

Por quê? E o que isso diz sobre a possibilidade de um programa asyncio se defender sozinho de uma corrotina mal-comportada?
