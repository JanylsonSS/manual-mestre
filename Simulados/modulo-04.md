# Simulado CP2 — Módulo 04 (variante A)

**Tempo:** 90–120 min · **Composição:** 10 objetivas + 3 discursivas + 1 prático (~60 min)
**Aprovação:** ≥ 8/10 objetivas **e** prático ≥ 3 na rubrica. 6–7/10 ou prático = 2 → revisão dirigida + [variante B](modulo-04-b.md). ≤ 5/10 → refazer o módulo em ritmo de revisão.
**Regra de honestidade:** sem consultar durante as objetivas e discursivas; o prático é de consulta livre. Gabarito no fim — depois de terminar tudo.

## Objetivas

**Q1.** `class Y: total = 0`, e `self.total += 1` no `__init__`. Depois de duas instâncias, `Y.total` vale:
a) 2 · b) 1 · c) **0** · d) `AttributeError`

**Q2.** Numa `@dataclass`, `preco_centavos = 0` (sem anotação) faz o campo:
a) Ser obrigatório no `__init__` · b) Aparecer no `repr` com valor 0 · c) **Não ser campo — some do `__init__`, do `repr` e do `__eq__`** · d) Levantar `ValueError` na definição

**Q3.** O `mypy` devolve "Success: no issues found" num arquivo com `def f(n): return n.nao_existe()`. Por quê?
a) O método existe em tempo de execução · b) **Função sem anotação não é verificada** · c) O mypy só verifica assinaturas · d) Falta o `--strict` para achar erros de sintaxe

**Q4.** Num modelo Pydantic sem `extra` configurado, `Pedido(cliente="Ana", descconto=5000)` (com erro de digitação):
a) Levanta `ValidationError` · b) **Descarta o campo em silêncio e usa o default** · c) Cria o atributo `descconto` · d) Emite um aviso

**Q5.** 15 de janeiro ao meio-dia em `America/Sao_Paulo` produz offset:
a) Sempre `-03:00` · b) Sempre `-02:00` · c) **`-02:00` até 2019 e `-03:00` a partir de 2020** · d) Depende do sistema operacional

**Q6.** `with conexao:` numa conexão `sqlite3`:
a) Fecha a conexão · b) **Faz `COMMIT` no fim normal e `ROLLBACK` na exceção** · c) Abre uma transação e não a encerra · d) Fecha o cursor

**Q7.** Quatro threads em quatro tarefas de cálculo puro, numa máquina de 2 núcleos, rendem em relação ao sequencial:
a) ~4× · b) ~2× · c) **~1× (ou pior)** · d) ~0,25×

**Q8.** `saldo = saldo + 1` em 4 threads, 1000 vezes cada, sem trava. Rodando três vezes, o resultado mais provável é:
a) Sempre errado · b) **4000 nas três, sem perda** · c) Erro de execução · d) Números aleatórios entre 1000 e 4000

**Q9.** `[await buscar(u) for u in urls]` com 3 urls de 0,3 s leva:
a) ~300 ms · b) **~900 ms** · c) ~100 ms · d) Depende do número de núcleos

**Q10.** `asyncio.CancelledError` herda de:
a) `Exception` · b) `RuntimeError` · c) **`BaseException`** · d) `asyncio.TimeoutError`

## Discursivas

**D1.** Explique por que um teste que roda cinco vezes sem falhar **não prova** que um contador compartilhado entre threads está correto — e diga o que prova. *(máx. 8 linhas)*

**D2.** Um coletor precisa buscar 300 preços numa API que aceita 10 requisições simultâneas, falha em 3% das vezes por queda de rede, e às vezes não responde. Descreva as quatro peças que resolvem isso e diga **de onde vem o número 10**. *(máx. 10 linhas)*

**D3.** Você tem duas medições: `import aurora` custa 21,3 ms e `import aurora.formato` custa 20,2 ms, embora `formato.py` tenha cinco linhas e nenhuma dependência. Explique, e diga que decisão de projeto isso informa. *(máx. 8 linhas)*

## Prático (~60 min · consulta livre)

**Enunciado.** Escreva um pequeno coletor concorrente, no layout `src/`, que:

1. Busque N itens de uma fonte lenta simulada (`asyncio.sleep`), com taxa de falha configurável.
2. Valide o que chegou com Pydantic (**borda**) e converta para dataclass congelada (**domínio**).
3. Limite a concorrência com `Semaphore`, imponha prazo com `wait_for` e repita erros **de canal** com espera crescente.
4. Nunca levante de dentro da tarefa: devolva `Produto | Falha`.
5. Registre em log estruturado com o identificador do item em toda mensagem, e carimbo em UTC.
6. Passe em `mypy --strict` e tenha ao menos quatro testes — **um deles afirmando desempenho**.

**Rubrica (0–4):**

- **4** — tudo acima, com a tabela de `--limite` em quatro valores e o teste de desempenho falhando quando se introduz um `time.sleep`.
- **3** — tudo funcionando, com uma das seis exigências parcial.
- **2** — coleta concorrente funcionando, sem separação borda/domínio ou sem tentativas.
- **1** — código que roda, sequencial ou sem limite.
- **0** — não roda.

---

## Gabarito

**Objetivas:** 1-c · 2-c · 3-b · 4-b · 5-c · 6-b · 7-c · 8-b · 9-b · 10-c

**D1 — pontos-chave** `[04.21]`: o defeito não é intermitente, **o código está sempre errado**; o que varia é se a troca de thread cai entre a leitura e a escrita. Cinco execuções limpas não medem correção, medem sorte — e a sorte muda com carga, com mais núcleos, com uma linha a mais. O que prova é a **construção**: trava dentro de um `with`, ou um desenho sem estado compartilhado (cada thread devolve o próprio total, ou `queue.Queue`). Citar que forçar a troca com `time.sleep(0)` fez perder 75% vale ponto extra.

**D2 — pontos-chave** `[04.23]`: `Semaphore(10)` para simultaneidade; `wait_for` com prazo em toda requisição (sem ele o programa **nunca termina**); nova tentativa com espera **dobrando**, só para erros de canal (conexão, prazo, HTTP 500) e nunca para erro de conteúdo; `gather` para juntar. **O número 10 vem do limite do serviço** — documentação da API, pool de conexões —, nunca do número de núcleos nem do tamanho do lote: isto é espera, não conta.

**D3 — pontos-chave** `[04.17]`: importar **qualquer submódulo executa o `__init__.py` do pacote primeiro**, e o `__init__.py` reexporta `Produto`, que traz `dataclasses` (18,7 ms sozinho). Não dá para escapar escolhendo o submódulo. A decisão informada: reexportar no `__init__.py` é excelente para legibilidade e cobra a importação de tudo o que foi reexportado, **para todo mundo** — em pacote pequeno vale; em biblioteca grande, reexporte pouco e documente os caminhos completos.
