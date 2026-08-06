# Desafios de entrevista — Módulo 04: Python Avançado

Cinco exercícios do tipo que se pede num processo seletivo — com tempo, com alguém olhando,
e com a pergunta de acompanhamento que separa quem entendeu de quem decorou.

Faça cronometrado. Depois compare com o critério, que descreve o que um avaliador procura.

---

## DE1 — O decorador de cache `[~25 min · sênior júnior]`

**Enunciado.** Escreva um decorador `@memoria` que guarde os resultados de uma função pura,
com limite de tamanho e descarte do menos usado recentemente. Não use `functools.lru_cache`.

**Requisitos:** funciona com argumentos posicionais e nomeados; preserva `__name__` e `__doc__`;
expõe `funcao.estatisticas()` com acertos e erros; e o limite é configurável.

**As perguntas que vêm depois:**

1. O que acontece se um argumento não for hasheável? Qual a sua mensagem?
2. Duas chamadas — `f(1, b=2)` e `f(1, 2)` — batem no mesmo cache? Deveriam?
3. Isto é seguro entre threads? Prove ou conserte.

**Critério.** A chave do cache é a parte que separa: `(args, tuple(sorted(kwargs.items())))`
é o mínimo, e reconhecer que ela **não** unifica posicional com nomeado é o que se espera —
a `lru_cache` real também não unifica, e isso é uma decisão documentada, não um descuido.
Na 3, a resposta certa é que **não é seguro** e que o conserto é uma trava em volta da leitura
e da escrita — com o custo de serializar as chamadas.

---

## DE2 — O `LOG` que some `[~20 min · depuração ao vivo]`

**Enunciado.** Recebe-se este código, que "não registra nada":

```python
# app/servico.py
import logging
logging.basicConfig(level=logging.INFO)

def processar(pedido):
    logging.info("processando %s", pedido)
```

```python
# app/main.py
import logging
from app.servico import processar

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")
processar("P-1")
```

**A tarefa:** explique por que o formato configurado no `main.py` não aparece, e conserte.

**Critério.** Duas coisas precisam ser ditas. Primeira: `basicConfig` **desiste** se o raiz já
tiver handlers, e o `import` do `servico` roda o `basicConfig` dele **antes**, na importação —
então o formato do `main` nunca vale. Segunda: `logging.info` escreve no raiz, sem origem
ajustável. O conserto é remover a configuração do módulo, usar `getLogger(__name__)`, e deixar
`basicConfig` só no ponto de entrada. Quem menciona `force=True` como **remendo** e não como
solução ganha ponto.

---

## DE3 — A corrida que não reproduz `[~20 min · discussão]`

**Enunciado.** Um colega diz: "rodei o teste dez vezes e o contador deu certo em todas, então
o código está correto". O código é `saldo = saldo + 1` em quatro threads, sem trava.

**A tarefa:** convença-o do contrário, com uma demonstração.

**Critério.** A demonstração é forçar a troca com `time.sleep(0)` entre a leitura e a escrita,
e mostrar 75% de perda. Mas o que se avalia é o **argumento**: o código está sempre errado, e
o que varia é se a troca cai no ponto exato — carga, mais núcleos, uma linha a mais mudam isso.
A frase que fecha é que, para essa classe de defeito, **teste não é evidência**; a confiança vem
da construção. Quem propõe "rodar mais vezes" como solução não entendeu a pergunta.

---

## DE4 — Coletor de 10 mil URLs `[~30 min · sistema]`

**Enunciado.** Projete (não implemente inteiro) um coletor que busque 10 mil URLs de uma API
com limite de 20 requisições simultâneas, 2% de falhas transitórias e latência média de 300 ms.
Estime o tempo total e descreva as peças.

**As perguntas que vêm depois:**

1. Threads ou asyncio? Justifique com números.
2. Quanto tempo, aproximadamente? Mostre a conta.
3. Onde você poria o prazo, e qual valor?

**Critério.** A conta é `10.000 / 20 × 0,3 s ≈ 150 s`, mais ~2% de repetições. Na 1, as duas
funcionam — 20 threads não pesam nada —, e a resposta madura diz que a **escolha depende do resto
do sistema**, não do número de URLs: se já é assíncrono, asyncio; se não, threads e pronto.
Na 3, prazo por requisição, alguns múltiplos da latência média (1 a 2 s), **nunca** ausente —
e quem menciona que sem prazo o programa pode não terminar ganha ponto.

---

## DE5 — Revisão de código `[~25 min · o mais realista]`

**Enunciado.** Revise este trecho e liste os problemas, do mais grave ao menos:

```python
from datetime import datetime

@dataclass
class Pedido:
    cliente: str
    itens: list = []
    criado_em = datetime.utcnow()

    def total(self):
        return sum(i.preco for i in self.itens)

def processar(pedidos):
    with ThreadPoolExecutor(200) as ex:
        ex.map(salvar, pedidos)
```

**Critério.** São seis problemas, e a **ordem** importa tanto quanto a lista:

1. `ex.map` sem `list()` — **as exceções somem**; é o mais grave, porque esconde os outros.
2. `criado_em = datetime.utcnow()` — sem anotação, **não é campo**: é um valor de classe,
   avaliado **uma vez na importação**, compartilhado por todos os pedidos. Dois defeitos numa linha.
3. `itens: list = []` — `ValueError` na definição (o Python barra este).
4. `utcnow()` é ingênuo e está obsoleto — `datetime.now(timezone.utc)`.
5. `max_workers=200` sem saber o limite do destino.
6. `total()` sem anotação de retorno, e `list` sem o conteúdo.

Quem lista os seis mas põe o `utcnow` em primeiro lugar acertou os fatos e errou a prioridade:
o `map` sem consumir é o que impede de **descobrir** os outros.
