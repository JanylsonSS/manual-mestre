# Exercícios — Capítulo 04.23: Asyncio na prática e projeto integrador

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap23.md`](gabaritos/cap23.md).

> O projeto de referência está em [`../codigo/cap23/coletor/`](../codigo/cap23/coletor/). Use-o como consulta, não como cópia.

## Aquecimento

### A1 — Qual peça resolve? `[Aquecimento · ~10 min]`

Para cada problema, diga qual das quatro peças (`Semaphore`, prazo, nova tentativa, `gather`) resolve — e se alguma **não** resolve.

1. A API devolve `429` quando recebo mais de 10 requisições ao mesmo tempo.
2. Uma requisição ficou pendurada e o programa não termina.
3. 3% das requisições falham por queda momentânea de rede.
4. Preciso dos 300 resultados antes de gravar.
5. O serviço aceita 5 requisições **por segundo**.
6. Um item veio com a categoria errada.
7. Quero começar a gravar antes de tudo terminar.
8. Uma corrotina falhou e as outras continuam consumindo rede.

### A2 — Preveja o resultado `[Aquecimento · ~12 min]`

```python
# 1  — 100 tarefas de 50 ms, Semaphore(20). Qual o pico de simultâneas?

# 2
async def t():
    await asyncio.sleep(0.5)
    marcou.append(1)
await asyncio.wait_for(t(), timeout=0.1)
# depois de 1 s, quanto tem em `marcou`?

# 3
try:
    await asyncio.sleep(10)
except Exception:
    print("peguei")
finally:
    print("finally")
# a tarefa é cancelada. O que aparece?

# 4
try:
    await asyncio.sleep(10)
except asyncio.CancelledError:
    return "terminei"
# a tarefa é cancelada. O que quem cancelou recebe?

# 5  — 3 tentativas, espera base 50 ms, todas falham. Tempo total de espera?

# 6
resultados = await asyncio.gather(e("lento", .3), e("rapido", .05))
# em que ordem?
```

### A3 — Ache o erro `[Aquecimento · ~12 min]`

```python
# 1
async def coletar(skus):
    return await asyncio.gather(*[buscar(s) for s in skus])   # 5000 skus

# 2
async def buscar(sku):
    async with sem:
        return await cliente.get(f"/p/{sku}")

# 3
async def com_tentativas(sku):
    for _ in range(5):
        try:
            return await buscar(sku)
        except Exception:
            continue

# 4
async def buscar(sku):
    try:
        return await asyncio.wait_for(consultar(sku), timeout=1)
    except asyncio.CancelledError:
        log.warning("cancelada")
        return None

# 5
async def coletar(skus):
    for sku in skus:
        asyncio.create_task(processar(sku))
    return "disparado"

# 6
async def com_tentativas(sku):
    for n in range(3):
        try:
            return await buscar(sku)
        except (ConnectionError, ValidationError):
            await asyncio.sleep(0.05)
```

### A4 — Repete ou não? `[Aquecimento · ~10 min]`

Para cada erro, diga se vale nova tentativa:

1. `ConnectionError: connection refused`
2. `ValidationError: preco_centavos deve ser maior que 0`
3. `asyncio.TimeoutError`
4. HTTP `500 Internal Server Error`
5. HTTP `404 Not Found`
6. HTTP `401 Unauthorized`

---

## Aplicação

### AP1 — O semáforo `[Aplicação · ~20 min]`

Escreva um experimento que **meça o pico real** de tarefas simultâneas sob um `Semaphore`.

Requisitos: um contador incrementado ao entrar e decrementado ao sair; o pico registrado; e uma tabela com limites 1, 5, 20 e 100 sobre 100 tarefas.

**A pergunta que fecha:** o pico bateu exatamente com o limite em todos os casos? Se sim, o que isso permite prometer a um serviço externo?

### AP2 — O prazo `[Aplicação · ~25 min]`

Prove que `wait_for` **cancela** a corrotina interna, e não apenas desiste de esperá-la.

Requisitos: uma corrotina que acrescente a uma lista **depois** do `sleep`; um `wait_for` com prazo menor; e uma espera generosa depois do timeout, para dar chance de ela terminar.

Depois, escreva a versão que **quebra o cancelamento** (capturando `CancelledError` sem relançar) e mostre a diferença.

### AP3 — As tentativas `[Aplicação · ~20 min]`

Escreva `com_tentativas(fn, tentativas, base)` com espera crescente.

Requisitos: devolve o resultado e o número da tentativa que funcionou; relança depois de esgotar; espera `base * 2 ** n`; e conta as chamadas feitas.

Teste com uma fonte que falha 0, 2 e 5 vezes, e monte a tabela de tempo e de chamadas.

**A pergunta que fecha:** com 3 tentativas e base de 50 ms, qual é o tempo **máximo** que uma coleta de um item pode levar? Escreva a fórmula antes de medir.

---

## Desafio

### D1 — O coletor completo `[Desafio · ~90 min · projeto integrador]`

Construa o projeto do capítulo **do zero**, usando o de referência apenas quando travar.

**Requisitos:**

- Layout `src/` com `pyproject.toml` e comando de terminal.
- Camadas separadas: borda (Pydantic), domínio (dataclasses), coletor, tempo, registro, entrada.
- `Semaphore`, prazo e tentativas com espera crescente.
- `coletar_um` que **nunca levanta** — devolve `Produto | Falha`.
- Log estruturado em JSON, com o identificador em toda mensagem.
- `mypy --strict` limpo.
- Ao menos oito testes, **incluindo um que afirme desempenho**.

**A prova:** rode com `--limite` valendo 1, 5, 20 e o total, e monte a tabela. Depois rode com taxa de falha em 0,5 e compare o número de **consultas** com o de itens.

**As três perguntas que valem a nota:**

1. Introduza um `time.sleep(0.05)` dentro de `coletar_um`. **Qual dos seus testes falha, e por quê?**
2. O que acontece se você trocar `Semaphore(10)` por `Semaphore(1000)` numa fonte que aceita dez?
3. Seu `coletar_um` devolve `Produto | Falha`. Qual seria o custo de ele levantar exceções, e o que mudaria no `gather`?

---

## Mini projeto

### MP — O painel de coleta `[Mini projeto · ~50 min]`

Estenda o coletor com observabilidade em tempo real.

**Requisitos:**

- Corrotina de progresso que imprima, a cada 500 ms: terminados, em andamento e taxa de sucesso parcial.
- Métricas finais: tempo médio por item, p50, p95, tentativas por item e distribuição dos motivos de falha.
- Opção `--exportar` gravando o relatório em JSON.
- A corrotina de progresso **não pode atrapalhar** o coletor.

**E a pergunta que fecha:** o p95 do seu coletor é muito maior que o p50.

Qual das quatro peças da §4 é a responsável — e o que aconteceria com o p95 se você **aumentasse** o número de tentativas?
