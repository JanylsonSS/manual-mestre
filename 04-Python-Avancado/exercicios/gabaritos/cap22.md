# Gabarito — Capítulo 04.22: Asyncio — fundamentos

Leia depois de tentar. Enunciados em [`../cap22.md`](../cap22.md).

> Toda saída abaixo é execução real, numa máquina de **2 núcleos**, Python 3.10.

## A1 — Roda ou não?

| # | Trecho | Roda? |
|---|---|---|
| 1 | `tarefa()` solto | **não** — devolve corrotina, e `RuntimeWarning` ao descartar |
| 2 | `asyncio.run(tarefa())` | **sim** |
| 3 | `await` no nível do módulo | **não** — `SyntaxError` |
| 4 | `await` dentro de `async def` | **sim** |
| 5 | `create_task` sem `await` nenhum depois | **começa** — e pode ser cancelada |
| 6 | `create_task` + `await asyncio.sleep(0)` | **sim** |
| 7 | `gather(tarefa(), tarefa())` | **sim**, as duas |
| 8 | `asyncio.run(tarefa)` sem parênteses | **não** — `ValueError` |

**O 5 é o mais instrutivo, e a resposta curta engana.** Com uma corrotina que só imprime, ela roda. Com uma que tem `await` dentro, o final é outro:

```
comecou
principal acabou
>>> 'terminou' não apareceu: a task foi cancelada no fim do run
```

`asyncio.run` espera **a corrotina principal**, não as tarefas soltas — e ao terminar, cancela o que sobrou. A tarefa começou, chegou ao `await`, e morreu ali. **É o problema da tarefa órfã**, e o sintoma é trabalho que "às vezes acontece".

**O 8 dá uma mensagem clara**, e vale conhecê-la porque esquecer os parênteses acontece o tempo todo:

```
ValueError: a coroutine was expected, got <function tarefa at 0x…>
```

**E o 3 é `SyntaxError`, não erro de execução** — `await` só existe dentro de `async def`. É a primeira manifestação do "asyncio contamina a árvore de chamadas".

## A2 — Preveja o tempo

| # | Trecho | Tempo |
|---|---|---|
| 1 | `gather` de 3 × 0,2 s | **201 ms** |
| 2 | três `await` em sequência | **601 ms** |
| 3 | `gather` de 0,1 / 0,3 / 0,2 | **301 ms** — o mais lento |
| 4 | `create_task` × 3, depois `await` um a um | **201 ms** |
| 5 | `gather` aninhado | **203 ms** |
| 6 | duas corrotinas sem `await` | **0 ms** — nada aconteceu |

**O contraste 2/4 é o ponto do exercício**, e ele corrige o que a §6.2 poderia deixar entender pela metade.

No **2**, cada `await` cria e espera uma corrotina por vez: 601 ms. No **4**, as três tarefas foram **agendadas** por `create_task` antes de qualquer espera — elas já estavam correndo quando o primeiro `await` chegou, e aguardá-las uma a uma só coleta os resultados: 201 ms.

**A lição precisa é que o problema nunca foi o `await` em sequência**, e sim **criar** a corrotina no momento de aguardá-la. `gather` resolve isso porque cria todas antes; `create_task` resolve do mesmo jeito, de forma explícita.

**O 6 é o silêncio completo:** duas corrotinas criadas, nenhuma aguardada, zero milissegundos e zero trabalho — com dois `RuntimeWarning` que ninguém vê se os avisos estiverem desligados.

## A3 — Ache o erro

**1. `[await buscar(u) for u in urls]` — funciona, e é sequencial.** O erro da §6.2, na forma exata em que ele aparece na vida real. Correção: `await asyncio.gather(*[buscar(u) for u in urls])`.

**2. `open()` e `json.dump` dentro de corrotina — funciona, e trava o laço.** Escrita em disco é bloqueante; num arquivo pequeno o efeito é invisível, num grande ele para tudo. Correção: `await asyncio.to_thread(salvar_sincrono, dados)`, ou `aiofiles`.

**3. `create_task` sem guardar a referência — funciona quase sempre.** Duas coisas podem dar errado: a tarefa é cancelada se `servir()` terminar antes dela (A1.5), e — mais sutil — o coletor de lixo pode destruir a tarefa no meio, porque o laço guarda apenas uma referência fraca. Correção: guardar num conjunto e removê-la ao terminar, ou usar `asyncio.TaskGroup` (3.11+).

**4. Um `AsyncClient` por item — funciona, e é lento.** Além de ser sequencial (o `for` com `await` dentro), ele refaz a conexão TCP e o handshake TLS a cada item. Correção: um cliente para todos, criado com `async with` fora do laço, e `gather` no lugar do `for`.

**5. `gather` sem `return_exceptions` num lote de mil — funciona até o primeiro item ruim.** Aí a exceção sobe e **os 999 resultados bons somem**. Correção: `return_exceptions=True` e separação.

**6. Cálculo pesado numa corrotina — funciona, e trava tudo.** 50 milhões de multiplicações não têm `await` nenhum: o laço não recupera o controle até acabar. Correção: `ProcessPoolExecutor` via `loop.run_in_executor`, porque é conta e não espera (04.21).

**A leitura do lote: os seis funcionam.** Nenhum levanta exceção — três produzem lentidão (1, 2, 6), dois perdem trabalho (3, 5) e um desperdiça conexões (4). É o padrão do capítulo: em asyncio, o erro comum não quebra, **desacelera**.

## A4 — Asyncio, threads ou processos?

| # | Situação | Resposta |
|---|---|---|
| 1 | 30 mil WebSockets | **asyncio** — 30 mil threads custariam ~330 MB e a troca de contexto |
| 2 | 20 requisições com `requests` | **threads** — trocar a biblioteca não compensa |
| 3 | hash de 5 mil arquivos | **processos** — é conta |
| 4 | FastAPI consultando banco | **asyncio** — o framework já é assíncrono |
| 5 | 100 arquivos locais e somar colunas | **meça** — leitura é espera, soma é conta |
| 6 | bot com 200 conversas | **os dois servem** |

**O 2 é a resposta que o exercício quer**, e ela é contraintuitiva: com vinte requisições, o ganho de asyncio sobre threads é irrelevante, e o custo — trocar `requests` por `httpx`, marcar a árvore com `async`, mudar a raiz para `asyncio.run` — é alto. **Threads são a escolha pragmática em escala pequena.**

**O 6 é honesto ao dizer "os dois".** Duzentas conversas cabem em duas centenas de threads sem problema. A decisão passa a ser de arquitetura: se a biblioteca do bot já é assíncrona, asyncio; se não, threads.

**E o 5 repete a lição do 04.21/A1.3:** ler é espera e somar é conta, e qual domina depende do tamanho dos arquivos e da velocidade do disco. É caso de medir.

## AP1 — O `gather`

**Sim, `gather` preserva a ordem** — e a prova precisa de tempos diferentes:

```python
await asyncio.gather(e("lento", 0.3), e("rapido", 0.05), e("medio", 0.15))
```

```
['lento', 'rapido', 'medio']
```

O `rapido` terminou primeiro e aparece **em segundo**, na posição em que foi passado. `gather` devolve os resultados na ordem dos **argumentos**, não na de conclusão.

**Isso importa mais do que parece.** Um `gather` sobre `[buscar(sku) for sku in skus]` devolve preços na ordem dos SKUs, e você pode fazer `zip(skus, precos)` com segurança — sem precisar que cada corrotina devolva o próprio identificador.

**E quando você quer a ordem de conclusão**, o instrumento é outro: `asyncio.as_completed`, que entrega cada resultado assim que fica pronto. Ele serve para começar a processar antes de tudo terminar.

## AP2 — O bloqueio

```
com bloqueio:          3006 ms
com to_thread:          845 ms
com run_in_executor:    577 ms
```

**As duas correções funcionam, e não dão tempos parecidos** — e a diferença é a resposta do exercício.

`asyncio.to_thread` usa o **executor padrão** do laço, cujo tamanho é `min(32, núcleos + 4)`. Nesta máquina de dois núcleos, são **6 threads**. Com dez chamadas bloqueantes de 0,27 s, quatro esperam a segunda rodada — daí os 845 ms.

O limite se confirma em quatro medições:

```
 3 chamadas com to_thread:    305 ms
 6 chamadas com to_thread:    304 ms
10 chamadas com to_thread:    604 ms
20 chamadas com to_thread:   1204 ms
```

**Três e seis custam o mesmo; dez custam o dobro.** O degrau está exatamente no tamanho do executor padrão.

`loop.run_in_executor` com um `ThreadPoolExecutor(10)` seu não tem esse teto: 577 ms.

**O critério de escolha:** `to_thread` para chamadas bloqueantes ocasionais — é uma linha e resolve. Executor próprio quando a quantidade for grande ou previsível, porque aí você controla o tamanho.

**E a última parte da pergunta:** se `transformar` fosse **cálculo puro**, nenhuma das duas resolveria de verdade. Threads não ajudam em cálculo (04.21: 0,94×), então o tempo continuaria dominado pela conta. A resposta seria `run_in_executor` com um **`ProcessPoolExecutor`** — e aí voltam os custos de serialização do 04.21/§6.6.

## AP3 — Exceções em lote

```python
resultados = await asyncio.gather(*[processar(i) for i in itens],
                                  return_exceptions=True)

sucessos = [r for r in resultados if not isinstance(r, Exception)]
falhas = [(i, r) for i, r in enumerate(resultados) if isinstance(r, Exception)]
for indice, erro in falhas:
    log.error("item %d falhou", indice, exc_info=erro)
```

```
return_exceptions=True: ['1', ValueError('item 2 ruim'), '3']
padrão:                 levantou: item 2 ruim
```

**Com `return_exceptions=False`, você perdeu os dois resultados bons** — e num lote de vinte, perde dezessete.

**E a segunda parte da pergunta é a que quase ninguém sabe: as corrotinas que ainda estavam rodando não são canceladas.** O `gather` propaga a primeira exceção imediatamente, mas as outras tarefas continuam vivas no laço, em segundo plano. Elas terminam (ou não), e os resultados são descartados.

Isso produz dois efeitos desagradáveis. O trabalho continua sendo feito — requisições continuam saindo, arquivos continuam sendo escritos — depois de o seu código já ter desistido. E se o laço terminar antes delas, aparecem avisos de "Task exception was never retrieved" para as que também falharam.

**Note o `exc_info=erro` no log** (04.19): como você tem o objeto da exceção e não está dentro de um `except`, `log.exception` não funcionaria — `exc_info` recebe a exceção diretamente e registra o rastro do mesmo jeito.

## D1 — O coletor assíncrono

**(1) Os tetos comparados com o 04.21/AP2.**

Eles são **parecidos em forma e diferentes em custo**. Nos dois casos o ganho cresce até o número de tarefas simultâneas e para ali — 300 itens, semáforo de 300, e aumentar não faz nada.

A diferença aparece **no meio da tabela**: com threads, subir de 100 para 200 workers já rendeu menos que o esperado (234 → 165 ms em vez de 117), porque criar e coordenar threads começa a pesar. Com corrotinas, a escala é praticamente linear até o fim.

**E há uma diferença que a tabela não mostra:** com threads, 300 workers significam 300 threads do sistema operacional. Com asyncio, o semáforo de 300 é um contador — não há nada de "300" existindo no sistema.

**(2) O `time.sleep(0.1)` em uma das corrotinas.**

**As outras 299 param durante aqueles 100 ms.** É o achado central do capítulo: uma thread só, e uma chamada bloqueante congela o laço inteiro. O tempo total sobe em 100 ms para *todo mundo*, não só para o item afetado.

Se o `sleep` estiver dentro de um laço que roda 300 vezes — um por item —, o coletor inteiro serializa, e você volta aos 60 segundos que veio evitar.

**É a diferença mais importante em relação a threads:** lá, uma tarefa lenta atrapalha uma thread; aqui, atrapalha todas.

**(3) Com `return_exceptions=False`.** As demais **continuam rodando** (ver AP3): o `gather` desiste, o seu código recebe a exceção, e as outras 299 seguem consumindo rede e produzindo resultados que ninguém vai ler. Se quiser realmente parar, é preciso cancelar as tarefas explicitamente — ou usar `asyncio.TaskGroup` (3.11+), que cancela as irmãs quando uma falha.

## MP — O detector de bloqueio

O núcleo do vigia:

```python
async def vigia(intervalo: float = 0.05, limite_ms: float = 20.0) -> list[float]:
    atrasos: list[float] = []
    while True:
        antes = time.perf_counter()
        await asyncio.sleep(intervalo)
        real = (time.perf_counter() - antes) * 1000
        atraso = real - intervalo * 1000
        if atraso > limite_ms:
            atrasos.append(atraso)
            log.warning("laço bloqueado por ~%.0f ms", atraso)
```

**A ideia é medir a diferença entre o que se pediu e o que se recebeu.** `asyncio.sleep(0.05)` promete acordar em 50 ms; se acordou em 550, alguém segurou o laço por meio segundo.

**A pergunta que fecha: por que só depois?**

Porque o vigia **é uma corrotina**, e corrotinas só rodam quando o laço tem o controle. Enquanto a corrotina mal-comportada está executando, o laço está parado — e o vigia, junto. Ele acorda quando o bloqueio termina, e só então consegue medir quanto durou.

**E a consequência é dura: um programa asyncio não consegue se defender sozinho de uma corrotina mal-comportada.** Não há preempção; não há como interromper código que não devolve o controle. É o outro lado da vantagem da §6.4 — o controle só troca no `await`, o que dá previsibilidade e elimina corridas, ao preço de tornar a cooperação **obrigatória**.

As defesas possíveis são todas de fora ou de projeto: uma thread comum vigiando o laço (ela é preemptada pelo sistema e continua rodando), um tempo limite no processo inteiro, ou — a que funciona — **não deixar código bloqueante entrar**, com revisão e com o próprio detector rodando em desenvolvimento.

O Python oferece um atalho para isso, e vale conhecer: `asyncio.run(main(), debug=True)` já registra um aviso quando uma corrotina segura o laço por mais de 100 ms. **O seu detector é uma versão configurável do que o modo de depuração faz** — e descobrir isso depois de escrevê-lo é a melhor forma de entender o que ele mede.
