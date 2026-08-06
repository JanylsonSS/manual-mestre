# Simulado CP2 — Módulo 04 (variante B)

**Quando usar:** depois de 6–7/10 na [variante A](modulo-04.md), com revisão dirigida entre as duas. Mesmo formato, questões diferentes, mesmos objetivos.

**Tempo:** 90–120 min · **Aprovação:** ≥ 8/10 objetivas **e** prático ≥ 3.

## Objetivas

**Q1.** `def f(x, acc=[]): acc.append(x); return acc`. `print(f(1), f(2), f(3))` imprime:
a) `[1] [2] [3]` · b) `[1] [1,2] [1,2,3]` · c) **`[1,2,3] [1,2,3] [1,2,3]`** · d) `[3] [3] [3]`

**Q2.** Definir `__eq__` numa classe, sem `__hash__`, faz o objeto:
a) Comparar por identidade · b) **Não entrar em `set` nem servir de chave** · c) Perder o `__repr__` · d) Levantar erro na definição

**Q3.** `@dataclass(frozen=True)` com um campo `itens: list`. `objeto.itens.append("x")`:
a) Levanta `FrozenInstanceError` · b) **Funciona — e `hash(objeto)` falha** · c) Cria uma cópia da lista · d) Funciona e o hash também

**Q4.** Um campo `datetime` num modelo Pydantic recebendo `"2026-07-15T14:30:00"` (sem fuso):
a) É recusado · b) **É aceito, com `tzinfo=None`** · c) Recebe UTC automaticamente · d) Recebe o fuso local

**Q5.** No layout `src/`, `import aurora` antes de `pip install -e .`:
a) Funciona de dentro da pasta do projeto · b) **Falha com `ModuleNotFoundError`** · c) Funciona só com `PYTHONPATH` · d) Funciona, mas importa a versão instalada

**Q6.** O nível padrão do `logging`, sem nenhuma configuração, é:
a) `DEBUG` · b) `INFO` · c) **`WARNING`** · d) Não há nível padrão

**Q7.** `log.debug("x %s", objeto_caro)` com `DEBUG` **desligado**, comparado a `log.debug(f"x {objeto_caro}")`:
a) Mesmo custo · b) A f-string é mais rápida · c) **A vírgula é ~2,5× mais barata, e o custo dela não muda com o valor** · d) As duas formatam sempre

**Q8.** 4 esperas de 0,5 s com `ThreadPoolExecutor(4)`, comparadas ao sequencial:
a) ~1× · b) ~2× · c) **~4×** · d) ~0,25×

**Q9.** `asyncio.wait_for(tarefa(), timeout=0.1)` sobre uma tarefa de 0,5 s:
a) Levanta `TimeoutError` e a tarefa continua rodando · b) **Levanta `TimeoutError` e a tarefa é cancelada** · c) Espera a tarefa terminar · d) Devolve `None`

**Q10.** `__exit__` devolvendo `True` quando o bloco levanta uma exceção:
a) Relança a exceção · b) Converte em `RuntimeError` · c) **Suprime a exceção — o programa continua** · d) Registra e relança

## Discursivas

**D1.** Explique a diferença entre `Semaphore` e limite de taxa ("5 requisições por segundo"), e por que um não substitui o outro. *(máx. 8 linhas)*

**D2.** Um relatório de vendas agrupa pedidos por dia usando `datetime` em UTC. O time do Brasil reclama que o dia 3 de novembro de 2018 está com menos vendas. Explique o defeito e a correção. *(máx. 8 linhas)*

**D3.** Você tem uma função que faz 300 requisições HTTP num script existente que usa `requests`. Alguém sugere reescrever em asyncio. Argumente a favor ou contra, com números. *(máx. 10 linhas)*

## Prático (~60 min · consulta livre)

**Enunciado.** Refatore um script procedural para o padrão do módulo:

1. Layout `src/` com `pyproject.toml`, comando de terminal e `tests/` fora de `src/`.
2. Camadas separadas: modelo (dataclass congelada), esquemas (Pydantic), serviço, tempo, registro, entrada.
3. Um gerenciador de contexto próprio que meça e registre a duração de uma operação, **inclusive quando ela falha**.
4. Log estruturado em JSON, carimbo em UTC, contexto no `extra`.
5. `mypy --strict` limpo e ao menos cinco testes.

**Rubrica (0–4):** igual à da variante A, trocando "coleta concorrente" por "camadas separadas e gerenciador próprio".

---

## Gabarito

**Objetivas:** 1-c · 2-b · 3-b · 4-b · 5-b · 6-c · 7-c · 8-c · 9-b · 10-c

**D1 — pontos-chave** `[04.23]`: `Semaphore` limita **simultaneidade** — quantas ao mesmo tempo. Limite de taxa é sobre **janela de tempo**. Com semáforo de 5 e requisições de 10 ms, você manda dez em 20 ms, muito acima de "cinco por segundo". Um não substitui o outro porque medem coisas diferentes: um conta o que está em voo, o outro conta o que passou. Limite por janela exige um mecanismo próprio (`aiolimiter`, ou contador com relógio), e respeitar `Retry-After` quando o serviço o envia.

**D2 — pontos-chave** `[04.18]`: agrupar por dia **em UTC** joga as vendas do fim do dia local para o dia seguinte — uma venda às 23:30 de 3/11 em São Paulo aconteceu às 02:30 de 4/11 em UTC. O total geral fecha, e por isso ninguém nota. A correção é **guardar em UTC e agrupar no fuso de quem lê**: `quando.astimezone(SP).date()`. "Dia" é um conceito local. Mencionar que aquele dia teve **23 horas** (início do horário de verão) vale ponto extra.

**D3 — pontos-chave** `[04.21 e 04.22]`: **argumente contra**, com números. Trezentas requisições cabem em threads com `ThreadPoolExecutor`, que dá 3,99× medido em espera e **não exige trocar a biblioteca**. Asyncio ganharia em memória (16,9 MB contra 43,2 MB por 10 mil esperas) e em tempo (747 × 3410 ms) — mas em **300** itens essa diferença é irrelevante, e o custo é alto: trocar `requests` por `httpx`, marcar a árvore inteira com `async` e mudar a raiz para `asyncio.run`, porque **asyncio contamina a árvore de chamadas**. A resposta muda em escala de milhares, ou se o projeto já for assíncrono.
