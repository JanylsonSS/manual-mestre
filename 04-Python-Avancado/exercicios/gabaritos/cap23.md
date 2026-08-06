# Gabarito — Capítulo 04.23: Asyncio na prática e projeto integrador

Leia depois de tentar. Enunciados em [`../cap23.md`](../cap23.md).

> Toda medição abaixo é execução real, numa máquina de **2 núcleos**, Python 3.10.

## A1 — Qual peça resolve?

| # | Problema | Peça |
|---|---|---|
| 1 | `429` acima de 10 simultâneas | **`Semaphore(10)`** |
| 2 | requisição pendurada | **prazo** (`wait_for`) |
| 3 | 3% de falhas de rede | **nova tentativa** |
| 4 | preciso dos 300 antes de gravar | **`gather`** |
| 5 | 5 requisições **por segundo** | **nenhuma das quatro** |
| 6 | categoria errada num item | **nenhuma** — é dado inválido |
| 7 | gravar antes de tudo terminar | **`as_completed`** |
| 8 | uma falhou e as outras seguem | **`TaskGroup`** (3.11+) ou cancelamento explícito |

**O 5 é a pegadinha do lote.** `Semaphore` limita **simultaneidade**, não taxa. Dez requisições instantâneas com semáforo de 5 fazem cinco, depois cinco — e se cada uma levar 10 ms, você mandou dez em 20 ms, muito acima de "cinco por segundo". Limite por janela de tempo exige outro mecanismo (`aiolimiter`, ou um contador com relógio).

**O 6 é a decisão da §6.3.** Categoria errada é erro **de conteúdo**: nenhuma das quatro peças ajuda, porque tentar de novo traz o mesmo dado. A resposta é registrar como falha e seguir — que é o que `coletar_um` faz.

**E o 8 mostra o limite do `gather`:** ele não cancela as irmãs quando uma falha (04.22/§6.5). No projeto do capítulo isso não aparece porque `coletar_um` nunca levanta; num desenho em que ela levanta, `TaskGroup` é a resposta.

## A2 — Preveja o resultado

| # | Resultado |
|---|---|
| 1 | pico = **20**, exatamente |
| 2 | `marcou` fica **vazia** — a corrotina foi cancelada |
| 3 | só `finally` — `except Exception` **não** pega |
| 4 | quem cancelou recebe **`"terminei"`**, não o cancelamento |
| 5 | **150 ms** de espera (50 + 100) |
| 6 | `['lento', 'rapido']` — ordem dos argumentos |

**O 2 e o 4 são o par que ensina.**

No **2**, `wait_for` cancelou a corrotina: ela nunca chegou à linha do `append`, mesmo com um segundo de folga depois do timeout. É a garantia da §6.2.

No **4**, a mesma garantia foi **quebrada** por três linhas de código bem-intencionadas. O `except asyncio.CancelledError` capturou o cancelamento, devolveu um valor, e quem chamou `task.cancel()` recebeu `"terminei"` em vez de `CancelledError`. **O prazo deixou de valer.**

**O 5 tem uma sutileza de contagem:** três tentativas geram **duas** esperas (depois da primeira e da segunda falhas; depois da terceira não há motivo para esperar). 50 + 100 = 150 ms.

**E o 3 é a proteção que a linguagem dá:** `CancelledError` herda de `BaseException` desde o 3.8 justamente para que o `except Exception` que você escreveu para tratar erros de rede não impeça o cancelamento. O `finally` roda, e a limpeza acontece.

## A3 — Ache o erro

**1. `gather` de 5000 sem limite — funciona no laboratório e derruba a fonte.** Cinco mil requisições simultâneas produzem `429`, esgotam o pool de conexões ou fazem o serviço bloquear seu endereço. Correção: `Semaphore` com o teto do serviço.

**2. Semáforo, mas sem prazo — funciona até uma requisição ficar pendurada.** Aí a vaga do semáforo **nunca é liberada**, e o efeito é pior que sem semáforo: com limite de 10, dez requisições penduradas param a coleta inteira, para sempre. Correção: `wait_for` dentro do `async with`.

**3. `except Exception: continue` — funciona, e esconde tudo.** Três problemas: repete erros de conteúdo (§6.3); não espera entre tentativas, martelando o serviço; e, ao esgotar as cinco, devolve `None` em silêncio, porque não há `return` nem `raise` depois do laço. Correção: erros nomeados, espera crescente, e uma falha explícita no fim.

**4. `except CancelledError` sem `raise` — funciona, e quebra o prazo.** É o A2.4 dentro de um `wait_for`: o cancelamento vira `None`, o `wait_for` não recebe o cancelamento que pediu, e o prazo perde o efeito. Correção: `raise` depois do log.

**5. `create_task` em laço, sem guardar nem aguardar — funciona, e perde trabalho.** As tarefas começam, `coletar` devolve `"disparado"`, e quando o `asyncio.run` da raiz terminar elas são **canceladas no meio** (04.22/A1.5). Correção: `gather`, ou `TaskGroup`.

**6. `ValidationError` na tupla de temporários — funciona, e desperdiça.** Um dado inválido é repetido três vezes, com espera entre cada, para chegar exatamente ao mesmo resultado. Correção: separar os dois `except`, como o projeto faz.

**A leitura do lote: os seis funcionam.** Nenhum levanta erro na sua máquina com dez itens — e todos falham em escala, com fonte instável, ou quando alguém tenta cancelar. É o padrão de defeito de código concorrente: **ele aparece quando as condições mudam**, não quando o código é escrito.

## A4 — Repete ou não?

| # | Erro | Repete? | Por quê |
|---|---|---|---|
| 1 | `connection refused` | **sim** | canal — pode ser momentâneo |
| 2 | `ValidationError` | **não** | conteúdo — virá igual |
| 3 | `asyncio.TimeoutError` | **sim** | canal |
| 4 | HTTP `500` | **sim** | erro do servidor, geralmente temporário |
| 5 | HTTP `404` | **não** | o recurso não existe |
| 6 | HTTP `401` | **não** | credencial errada — repetir pode **bloquear a conta** |

**A regra que organiza a tabela é a da §6.3: canal sim, conteúdo não.**

**O 6 merece destaque porque o custo de errar é assimétrico.** Repetir um `401` não vai autenticar por insistência, e muitos serviços bloqueiam a conta após N tentativas de autenticação falhas. A repetição transforma um erro de configuração num incidente.

**E o 4 tem uma nuance de mercado:** `500` costuma valer nova tentativa, mas `503 Service Unavailable` com cabeçalho `Retry-After` diz **quanto** esperar — e respeitar esse valor é melhor que a sua espera crescente. Uma implementação madura lê o cabeçalho quando ele existe.

## AP1 — O semáforo

```python
async def tarefa(sem, ativos, pico):
    async with sem:
        ativos[0] += 1
        pico[0] = max(pico[0], ativos[0])
        await asyncio.sleep(0.05)
        ativos[0] -= 1
```

```
limite=1    pico real=1     5036 ms
limite=5    pico real=5     1009 ms
limite=20   pico real=20     253 ms
limite=100  pico real=100     53 ms
```

**Sim, o pico bate exatamente com o limite** — nos quatro casos, sem exceção.

**E o que isso permite prometer é o ponto do exercício:** você pode dizer a um serviço externo, com garantia, que nunca fará mais de N requisições simultâneas. Não é uma estimativa nem um esforço de melhor caso; é uma propriedade do código.

Isso importa porque contratos de API costumam ser escritos nesses termos, e porque a alternativa — "vou tentar não passar de dez" — não é verificável. O semáforo transforma uma intenção em invariante.

**Um detalhe do experimento:** o contador precisa ser mutável e compartilhado (uma lista, ou um objeto), porque uma variável comum reatribuída dentro da corrotina não seria vista de fora. E note que **não é preciso trava**: entre dois `await`, o código é atômico em asyncio (04.22/§6.7).

## AP2 — O prazo

```python
marcou: list[int] = []

async def demorada():
    await asyncio.sleep(0.5)
    marcou.append(1)              # só chega aqui se NÃO for cancelada

try:
    await asyncio.wait_for(demorada(), timeout=0.1)
except asyncio.TimeoutError:
    pass
await asyncio.sleep(0.6)          # folga generosa
```

```
terminou depois do timeout? []      <- vazia: foi cancelada
```

**A folga é o que torna o experimento válido.** Sem ela, a lista estaria vazia de qualquer jeito — porque não teria dado tempo. Esperar 600 ms depois de um timeout de 100 ms sobre uma tarefa de 500 ms elimina essa explicação alternativa.

E a versão que **quebra** o cancelamento:

```python
async def demorada():
    try:
        await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        return                    # sem raise
    marcou.append(1)
```

Aqui a corrotina "sobrevive" ao cancelamento e volta normalmente. Dependendo do que houver depois do `except`, ela pode até completar o trabalho — e o `wait_for` já desistiu dela, então esse trabalho é **invisível**: ninguém recebe o resultado, e ninguém sabe que ele aconteceu.

**É o pior desfecho possível para um prazo**: o custo foi pago e o benefício não.

## AP3 — As tentativas

```
0 falhas -> ok na tentativa 1 ·   10 ms
2 falhas -> ok na tentativa 3 ·  182 ms
5 falhas -> desistiu após 4 tentativas · 392 ms
```

**A fórmula do tempo máximo**, que o enunciado pede antes de medir:

```
T = tentativas × prazo  +  base × (2^(tentativas−1) − 1)
```

O primeiro termo é o pior caso de cada tentativa (todas estourando o prazo); o segundo é a soma das esperas, que é uma progressão geométrica.

Com 3 tentativas, prazo de 1 s e base de 50 ms:

```
T = 3 × 1000 + 50 × (2² − 1) = 3000 + 150 = 3150 ms
```

**E a leitura que importa é que o prazo domina.** As esperas somam 150 ms; os prazos somam 3 segundos. Quem quer limitar o tempo total de um item precisa olhar primeiro para o prazo, não para a espera entre tentativas — e a conta explica por que três tentativas com prazo de 30 s podem deixar um item pendurado por um minuto e meio.

**O outro número que a fórmula revela:** cada tentativa a mais **dobra** a contribuição da espera e soma um prazo inteiro. Aumentar de 3 para 5 tentativas leva o pior caso de 3150 ms para 5750 ms — quase o dobro, para ganhar os poucos casos que falham três vezes seguidas.

## D1 — O coletor completo

**(1) O `time.sleep(0.05)` dentro de `coletar_um`.**

**Falha o teste de desempenho** — aquele que afirma que a versão com limite 20 é pelo menos três vezes mais rápida que a com limite 1.

O motivo é o do 04.22/§6.3: `time.sleep` bloqueia o laço, e o semáforo deixa de importar — as vinte "simultâneas" viram vinte sequenciais, e a diferença entre limite 1 e limite 20 desaparece.

**E é por isso que aquele teste vale mais que os outros oito.** Os testes de correção continuam passando: os SKUs são normalizados, os produtos são congelados, as falhas viram `Falha`. Nada quebra. Só o desempenho — que é exatamente o sintoma de uma chamada bloqueante em asyncio, e o mais difícil de detectar sem um teste que o afirme.

**(2) `Semaphore(1000)` numa fonte que aceita dez.**

O programa passa a mandar mil requisições simultâneas. Três coisas acontecem, em ordem: a fonte devolve `429` para a maioria; a sua lógica de nova tentativa **repete todas**, multiplicando a carga; e o serviço pode bloquear seu endereço.

**O resultado é mais lento que com limite 10**, e é o caso em que "aumentar a concorrência" piora tudo. É a mesma forma do 04.21/§6.6, em que processos ficaram 9× mais lentos que o sequencial — otimizar sem medir é apostar.

**(3) O custo de `coletar_um` levantar exceções.**

Mudaria três coisas. O `gather` precisaria de `return_exceptions=True`, ou a primeira falha abortaria a coleta e **descartaria os resultados bons** (04.22/§6.5). A separação de sucessos e falhas passaria a ser um `isinstance(r, Exception)` no lugar de `isinstance(r, Produto)` — e perderia informação, porque uma exceção não carrega o número de tentativas nem o SKU sem trabalho extra. E o tipo de retorno viraria `list[Produto | BaseException]`, que o `mypy` obrigaria a tratar em todo lugar.

**Devolver `Produto | Falha` é uma decisão de projeto, não de estilo:** ela move o tratamento de erro para dentro da tarefa, onde há contexto, e deixa a camada de cima com um tipo simples. É o mesmo raciocínio do 04.14/§6.3 sobre `X | None` — tornar a possibilidade de falha **visível no tipo**.

## MP — O painel de coleta

**A pergunta que fecha: por que o p95 é muito maior que o p50?**

**A responsável é a nova tentativa.**

O p50 é o tempo de um item que funcionou de primeira: uma latência da fonte, e pronto. O p95 é o tempo de um item que falhou uma ou duas vezes — e ele carrega **as tentativas anteriores, os prazos e as esperas crescentes** somados.

Com a fórmula do AP3, a diferença é previsível: um item de primeira leva ~200 ms; um que precisou de três tentativas leva `3 × prazo + 150 ms`. A cauda não é ruído; é uma segunda população de itens misturada à primeira.

**E aumentar o número de tentativas piora o p95, não melhora.** Ele aumenta a taxa de sucesso (menos itens na lista de falhas) ao preço de fazer os itens problemáticos demorarem ainda mais — cada tentativa extra acrescenta um prazo inteiro e dobra a espera acumulada.

**É um trade-off que precisa ser escolhido, e não descoberto:** se o que importa é não perder itens, mais tentativas; se o que importa é o tempo total previsível, menos tentativas e uma lista de falhas para reprocessar depois. **A segunda opção costuma ser melhor em lote grande**, porque separa o caminho rápido do caminho problemático em vez de misturá-los.

**Sobre a corrotina de progresso não atrapalhar:** ela precisa ser toda `await` — nada de cálculo pesado nem de escrita síncrona no meio. Um `print` a cada 500 ms é barato; formatar um relatório completo de mil itens a cada 500 ms não é, e o vigia do 04.22 mediria o atraso que isso causa. **A ferramenta de observar não pode ser o que atrapalha.**
