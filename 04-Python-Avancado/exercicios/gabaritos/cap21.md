# Gabarito — Capítulo 04.21: Concorrência, threads, processos e GIL

Leia depois de tentar. Enunciados em [`../cap21.md`](../cap21.md).

> Toda medição abaixo é execução real, numa máquina de **2 núcleos**, Python 3.10.

## A1 — Espera ou conta?

| # | Tarefa | Tipo | Ferramenta |
|---|---|---|---|
| 1 | baixar 500 páginas | **I/O** | threads (ou asyncio) |
| 2 | hash de 10 mil senhas | **CPU** | processos |
| 3 | ler 200 CSV e contar linhas | **os dois** | threads primeiro; meça |
| 4 | redimensionar 300 imagens | **CPU** | processos — ou threads, se a biblioteca soltar o GIL |
| 5 | 50 consultas a banco remoto | **I/O** | threads |
| 6 | somar 10 milhões com laço `for` | **CPU** | processos |
| 7 | a mesma soma com NumPy | **CPU em C** | **threads servem** |
| 8 | esperar 30 webhooks | **I/O** | threads (ou asyncio) |

**O 3 é o mais interessante, e a resposta honesta é "os dois".** Ler do disco é espera; contar linhas é conta. Qual domina depende do tamanho dos arquivos e da velocidade do disco — num SSD rápido com arquivos pequenos, a conta domina; num disco de rede com arquivos grandes, a espera. **É um caso de medir, não de decidir por categoria.**

**O par 6/7 é o que mais surpreende.** A mesma operação matemática: com laço `for` é CPU-bound preso ao GIL; com NumPy o cálculo acontece em C, que **libera o GIL** — e threads passam a dar paralelismo real. É a exceção da §6.7, e é o motivo de bibliotecas numéricas serem escritas assim.

**O 4 tem a mesma nuance:** Pillow libera o GIL em várias operações. Vale medir antes de assumir que precisa de processos.

## A2 — Preveja o resultado

| # | Situação (4 núcleos) | Ganho |
|---|---|---|
| 1 | 8 cálculos, `ThreadPool(8)` | **~1×** (ou pior) |
| 2 | 8 cálculos, `ProcessPool(8)` | **~4×** — limitado pelos núcleos |
| 3 | 8 esperas de 1 s, `ThreadPool(8)` | **~8×** |
| 4 | 8 esperas de 1 s, `ProcessPool(8)` | ~8×, com mais custo de partida |
| 5 | 8 esperas de 1 s, `ThreadPool(2)` | **~2×** |
| 6 | **1** cálculo, `ProcessPool(8)` | **~1×**, ou pior |

**O contraste 2/3 é o coração do capítulo.** Com cálculo, o teto é o número de **núcleos** (4). Com espera, o teto é o número de **tarefas simultâneas** (8) — porque esperar não consome núcleo.

**O 5 mostra que o teto é o pool, não a tarefa:** oito esperas em duas threads viram quatro rodadas de uma, e o ganho cai para 2×.

**E o 6 é o erro de quem descobriu processos.** Uma tarefa só não tem o que paralelizar; o que sobra é o custo de criar o pool (8,2 ms medidos para quatro processos vazios, contra 0,8 ms para threads). O paralelismo precisa de **tarefas independentes**, no plural.

## A3 — Ache o erro

**1. `e.map(...)` sem consumir — funciona, e as exceções somem.**

```
map() devolveu sem erro: generator
ao consumir -> ValueError: item 2 ruim
```

`map` devolve um **gerador** (04.06): sem `list()`, o resultado não é consumido e qualquer exceção levantada dentro de uma tarefa **desaparece em silêncio**. O `with` espera as tarefas terminarem, então elas rodam — mas ninguém fica sabendo se falharam.

Correção: `list(e.map(...))`, ou `submit` com `as_completed` e checagem de cada resultado.

**2. Contador global sem trava — passa no teste e falha em produção.** É a §6.4 inteira: cinco execuções podem não perder nada, e a operação continua sendo três instruções sem proteção. Correção: `with trava:` em volta, ou uma `queue.Queue`, ou cada thread devolvendo o próprio total para somar no fim (o desenho que evita o problema em vez de protegê-lo).

**3. `lambda` num `ProcessPoolExecutor` — falha na hora, com uma mensagem ruim:**

```
PicklingError: Can't pickle <function <lambda> at 0x…>: attribute lookup <lambda> on __main__ failed
```

Processos precisam **serializar** a função para enviá-la ao filho, e uma `lambda` não tem nome pelo qual ser reencontrada. Correção: uma função de módulo, definida no nível superior. **A mensagem não diz "use uma função nomeada"**, e é por isso que ela merece tratamento próprio (é a pergunta do mini projeto).

**4. `return` antes do `release()` — funciona até o saldo ser insuficiente, e aí trava tudo.** No caminho em que `de.saldo < valor`, a função devolve `False` **sem liberar a trava** — e a próxima thread que a pedir espera para sempre. É o erro do 04.20/A3.2, agora com o `return` no lugar da exceção. Correção: `with trava:`, que libera nos dois caminhos.

**5. Sem `if __name__ == "__main__"` — em Windows e macOS, cria processos indefinidamente.** O filho é criado **reimportando o arquivo**, e a reimportação executa o `with ProcessPoolExecutor` de novo. Em Linux (que usa `fork` por padrão) funciona, o que é pior: o defeito só aparece na máquina de outra pessoa. Correção: a guarda, sempre.

**6. 200 threads contra uma API de 5 requisições por segundo — funciona, e derruba o outro lado.** O gargalo não é a sua máquina: `max_workers` alto produz erros `429`, bloqueio de IP ou timeouts, não velocidade. Correção: `max_workers` pelo limite do serviço, com espera entre lotes se necessário.

**A leitura do lote:** os erros 1, 2 e 6 **funcionam** — e o 1 é especialmente traiçoeiro, porque ele esconde exceções em vez de causá-las.

## A4 — Qual ferramenta?

| # | Situação | Resposta |
|---|---|---|
| 1 | 300 requisições de ~200 ms | **threads**, `max_workers` pelo limite da API |
| 2 | cálculo de 10 s sobre 3 números | **processos** — caso ideal: conta grande, dados mínimos |
| 3 | 8 ms sobre lista de 1 M, 4 vezes | **sequencial** — a cópia custa 9× o trabalho |
| 4 | 5 mil conexões simultâneas | **asyncio** (04.22) |
| 5 | comprimir 50 arquivos grandes | **threads** — `gzip` solta o GIL; meça |
| 6 | contador entre 4 threads | **nenhuma das duas: repense** |

**O 3 é o caso medido no capítulo**, e a resposta é a que ninguém quer: não paralelize. 33,6 ms sequencial contra 304,8 ms em processos.

**O 4 antecipa o próximo capítulo.** Cinco mil threads são possíveis — medimos ~11 KB por thread, então 5 mil custariam uns 55 MB — mas cada uma é uma thread do sistema operacional, com troca de contexto e limites do sistema. Corrotinas custam muito menos, e é para isso que o asyncio existe.

**E o 6 é a resposta que o exercício quer.** Um contador compartilhado entre threads é um problema de **desenho**, não de ferramenta. As saídas, em ordem de qualidade: cada thread devolve o próprio total e você soma no fim; uma `queue.Queue` recebendo os incrementos; e, por último, uma trava. A trava é a resposta certa quando não há alternativa — e a pergunta "por que existe um contador compartilhado?" costuma ter resposta melhor.

## AP1 — Meça o seu

Não há gabarito de números; há o que esperar da **forma** das tabelas:

- **CPU-bound com threads** deve ficar entre 0,9× e 1,05×. Abaixo de 1 é normal: é o custo da troca sem ganho.
- **CPU-bound com processos** deve chegar perto do número de núcleos, e **nunca** passar dele.
- **I/O-bound com threads** deve chegar perto do número de tarefas simultâneas.
- **Alguma linha pior que o sequencial** é esperada: no laboratório do capítulo, threads em CPU (0,94×) e processos com dados grandes (9,1× pior).

**A pergunta que importa: quanto os números variaram entre duas execuções?**

Medições de concorrência variam muito mais que medições sequenciais, e o motivo é que elas dependem do que **mais** está rodando na máquina. Uma execução com o navegador aberto e outra sem podem diferir em 30%.

A consequência prática: **uma medição de concorrência feita uma vez não é uma medição.** Rode três vezes, use a **melhor** (que é a menos contaminada por ruído externo), e desconfie de qualquer diferença menor que 20%. É o mesmo cuidado que o 03.14 exigiu para índices, e pelo mesmo motivo.

## AP2 — O coletor

200 tarefas de `sleep(0.1)`:

| `max_workers` | Tempo |
|---|---|
| 1 | 20 080 ms |
| 5 | 4 017 ms |
| 20 | 1 016 ms |
| 100 | 234 ms |
| 200 | 165 ms |
| 400 | **158 ms** |

**O tempo para de cair em 200** — o número de **tarefas**, não de núcleos.

O motivo é o da §6.3: esperar não consome processador, então o limite não é o hardware. Com 200 trabalhadores, todas as 200 esperas acontecem ao mesmo tempo, e o total é o de **uma** espera (mais o custo de criar as threads). Acrescentar mais trabalhadores não tem o que fazer: eles ficam ociosos.

**Note também que 100 → 200 rendeu menos que o esperado** (234 → 165 ms, e não 234 → 117). O custo de criar e coordenar 200 threads começa a aparecer, e é o primeiro sinal do problema que o asyncio resolve.

**E o número que não está na tabela é o que decide na vida real:** um serviço externo com limite de 5 requisições por segundo torna todos esses valores irrelevantes. O teto costuma ser do outro lado, não seu.

## AP3 — A corrida

```
sem forçar a troca:
    4000 de  4000 · perdeu 0     (cinco vezes)

forçando a troca entre ler e escrever:
    1017 de  4000 · perdeu 2983 (75%)
    1007 de  4000 · perdeu 2993 (75%)
    1000 de  4000 · perdeu 3000 (75%)

com trava, forçando a troca do mesmo jeito:
    4000 de  4000 · perdeu 0
```

**A pergunta que fecha: o que cinco execuções sem perda provam sobre a correção do código?**

**Nada.** E essa é a resposta inteira do capítulo.

O defeito não é probabilístico no sentido de "às vezes o código está errado". Ele está **sempre** errado; o que varia é se a troca de thread cai no ponto exato entre a leitura e a escrita. Nas suas cinco execuções não caiu. Vai cair quando a máquina tiver mais núcleos, quando houver carga, quando alguém acrescentar uma linha que muda o ritmo, ou quando o volume for mil vezes maior — e o resultado será um número errado, sem erro, sem log e sem forma de reproduzir.

**A conclusão de método é a que vale levar:** para essa classe de defeito, **teste não é evidência**. A confiança vem da **construção** — estado compartilhado e mutável protegido por trava, ou, melhor, um desenho em que não existe estado compartilhado. É o mesmo raciocínio do 04.14 sobre tipos: há defeitos que se evitam por estrutura, e não por verificação.

## D1 — O pipeline híbrido

**(1) Onde o tempo parou de cair.** Na etapa de busca, no número de tarefas (AP2). Na etapa de cálculo, no número de núcleos. **São dois tetos diferentes no mesmo programa**, e reconhecer isso é o ponto do desafio: aumentar `max_workers` da busca depois de 200 não faz nada, e aumentar o pool de processos além dos núcleos também não.

**(2) Trocando as ferramentas de lugar.** As duas pioram, e **não** igualmente.

**Processos para buscar** funciona e desperdiça: o ganho é quase o mesmo das threads (3,86× contra 3,99× medidos), com custo de partida 10× maior e serialização a cada tarefa. Piora pouco.

**Threads para calcular** não funciona: o ganho vai de ~1,5× para ~0,95×. Piora **completamente**, porque o GIL elimina o paralelismo.

**A assimetria é a lição:** usar processos onde threads bastam é ineficiente; usar threads onde processos são necessários é **inútil**. Se você tiver de errar, erre para o lado dos processos.

**(3) A exceção dentro de uma tarefa.**

```
map() devolveu sem erro: generator
ao consumir -> ValueError: item 2 ruim
```

Ela aparece **no `list()`**, não no `map()` nem no `with`. E se você não consumir o resultado, ela **desaparece** — a tarefa rodou, falhou, e ninguém ficou sabendo.

Dois detalhes que valem: o `map` **para no primeiro erro**, então itens posteriores não são entregues mesmo que tenham dado certo; e a exceção chega com o rastro **do trabalhador**, o que ajuda na investigação.

Quando você quer todos os resultados, incluindo os que falharam, o desenho é outro:

```python
futuros = {executor.submit(processar, item): item for item in itens}
for futuro in as_completed(futuros):
    try:
        resultado = futuro.result()
    except Exception:
        log.exception("item %s falhou", futuros[futuro])
```

## MP — O medidor de concorrência

**A pergunta que fecha: a `lambda` que não serializa.**

```
PicklingError: Can't pickle <function <lambda> at 0x7673ad3f9ea0>:
attribute lookup <lambda> on __main__ failed
```

**A mensagem é ruim por três motivos**, e vale nomear cada um: ela fala de `pickle`, que quem escreveu a `lambda` não mencionou; ela dá o endereço de memória, que é inútil; e ela **não diz o que fazer**.

Das três formas de lidar, a melhor é a terceira:

**Recusar** é honesto e frustrante: o medidor não testa nada, e o usuário não sabe por quê.

**Avisar e testar tudo** produz um relatório em que a linha dos processos tem um erro no meio, e obriga a interpretar `PicklingError`.

**Testar só as formas possíveis, com uma explicação** é o que uma ferramenta boa faz:

```python
try:
    pickle.dumps(funcao)
except (pickle.PicklingError, AttributeError, TypeError):
    print("Aviso: a função não pode ser enviada a outro processo "
          "(lambdas e funções aninhadas não são serializáveis).")
    print("Testando apenas sequencial e threads. Para incluir processos, "
          "defina a função no nível do módulo.")
```

**Note o teste antecipado com `pickle.dumps`**: descobrir o problema **antes** de criar o pool evita esperar 8 ms de partida para receber um erro, e permite a mensagem em português no lugar da original.

E note também as três exceções capturadas, porque o tipo do erro **muda com o que você tenta serializar**:

```
lambda              -> PicklingError
função aninhada     -> AttributeError
objeto com lambda   -> AttributeError
threading.Lock      -> TypeError: cannot pickle '_thread.lock' object
arquivo aberto      -> TypeError: cannot pickle '_io.TextIOWrapper' object
conexão sqlite      -> TypeError: cannot pickle 'sqlite3.Connection' object
função de módulo    -> serializa
```

Descobrir a lista exige testar os casos, e o resultado é um bom exemplo de por que a §18.3 da spec proíbe `except:` genérico mas não proíbe capturar **três exceções nomeadas**: aqui as três são necessárias, e nomeá-las documenta o que se espera.

**E as três últimas linhas antecipam um erro que aparece muito em produção:** uma conexão de banco, um arquivo aberto ou uma trava **não atravessam** a fronteira do processo. Passar um objeto que os contenha para um `ProcessPoolExecutor` falha — cada processo precisa abrir os seus.
