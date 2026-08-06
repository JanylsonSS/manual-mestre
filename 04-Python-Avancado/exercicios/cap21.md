# Exercícios — Capítulo 04.21: Concorrência, threads, processos e GIL

Regra dos 15 minutos antes da Dica 1. Gabaritos em [`gabaritos/cap21.md`](gabaritos/cap21.md).

> Todo experimento com processos precisa de `if __name__ == "__main__":`. Sem ele, em Windows e macOS, o programa cria processos indefinidamente.

## Aquecimento

### A1 — Espera ou conta? `[Aquecimento · ~10 min]`

Classifique cada tarefa em **I/O-bound** (espera) ou **CPU-bound** (conta) — e diga qual ferramenta ganha.

1. Baixar 500 páginas de uma API.
2. Calcular o hash SHA-256 de 10 mil senhas.
3. Ler 200 arquivos CSV do disco e contar as linhas.
4. Redimensionar 300 imagens com Pillow.
5. Consultar 50 vezes um banco de dados remoto.
6. Somar uma coluna de 10 milhões de números com um laço `for`.
7. Somar a mesma coluna com NumPy.
8. Esperar 30 webhooks chegarem.

### A2 — Preveja o resultado `[Aquecimento · ~12 min]`

Numa máquina de 4 núcleos, diga o ganho aproximado em relação ao sequencial:

```python
# 1  — 8 tarefas de cálculo puro, ThreadPoolExecutor(8)
# 2  — 8 tarefas de cálculo puro, ProcessPoolExecutor(8)
# 3  — 8 esperas de 1 s, ThreadPoolExecutor(8)
# 4  — 8 esperas de 1 s, ProcessPoolExecutor(8)
# 5  — 8 esperas de 1 s, ThreadPoolExecutor(2)
# 6  — 1 tarefa de cálculo puro, ProcessPoolExecutor(8)
```

### A3 — Ache o erro `[Aquecimento · ~12 min]`

```python
# 1
with ThreadPoolExecutor(4) as e:
    e.map(processar, itens)

# 2
contador = 0
def trabalhar():
    global contador
    for _ in range(100_000):
        contador += 1

# 3
with ProcessPoolExecutor(4) as e:
    resultados = list(e.map(lambda x: x * 2, range(100)))

# 4
trava = threading.Lock()
def transferir(de, para, valor):
    trava.acquire()
    if de.saldo < valor:
        return False
    de.saldo -= valor
    para.saldo += valor
    trava.release()
    return True

# 5
# arquivo processar.py, sem nenhuma guarda
from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor(4) as e:
    list(e.map(calcular, range(100)))

# 6
with ThreadPoolExecutor(200) as e:
    list(e.map(consultar_api, skus))     # a API aceita 5 requisições por segundo
```

### A4 — Qual ferramenta? `[Aquecimento · ~10 min]`

1. 300 requisições HTTP de ~200 ms cada.
2. Um cálculo de 10 segundos sobre três números.
3. Um cálculo de 8 ms sobre uma lista de 1 milhão de itens, 4 vezes.
4. 5 mil conexões simultâneas num servidor.
5. Comprimir 50 arquivos grandes com `gzip`.
6. Um contador compartilhado entre 4 threads.

---

## Aplicação

### AP1 — Meça o seu `[Aplicação · ~20 min]`

Rode [`../codigo/cap21/concorrencia.py`](../codigo/cap21/concorrencia.py) na sua máquina e monte a tabela.

Depois responda, por escrito: (a) quantos núcleos você tem, e o ganho dos processos em CPU bateu com esse número? (b) o ganho das threads em I/O bateu com o número de tarefas? (c) alguma linha ficou **pior** que o sequencial?

**E a pergunta que importa:** rode duas vezes. Quanto os números variaram? Se variaram muito, o que isso diz sobre medições de concorrência feitas uma vez só?

### AP2 — O coletor `[Aplicação · ~25 min]`

Escreva um coletor que busque 200 itens de uma fonte lenta (simule com `time.sleep(0.1)`).

Requisitos: `ThreadPoolExecutor` com `max_workers` configurável; medição com `perf_counter`; e uma tabela com `max_workers` valendo 1, 5, 20, 100 e 400.

**A pergunta que separa:** o tempo para de cair em algum ponto. Onde, e por quê? A resposta tem a ver com o número de **tarefas**, e não com o número de núcleos — e o motivo é o mesmo que faz threads valerem para espera.

### AP3 — A corrida `[Aplicação · ~20 min]`

Reproduza a condição de corrida da §6.4 em três etapas:

1. Escreva o incremento sem trava e rode **cinco** vezes. Anote quantos incrementos se perderam.
2. Force a troca com `time.sleep(0)` entre a leitura e a escrita. Rode cinco vezes e anote de novo.
3. Ponha a trava e repita a etapa 2.

**E a pergunta que fecha:** se a etapa 1 não perdeu nada em cinco execuções, o que você pode concluir sobre a correção daquele código? Escreva a resposta antes de olhar o gabarito — ela é o ponto do capítulo inteiro.

---

## Desafio

### D1 — O pipeline híbrido `[Desafio · ~50 min]`

Um processamento em duas etapas, com a ferramenta certa em cada uma.

**Requisitos:**

- 200 itens; busca lenta (simulada) e cálculo pesado.
- Busca com `ThreadPoolExecutor`, `max_workers` configurável.
- Cálculo com `ProcessPoolExecutor`.
- Medição de cada etapa com `perf_counter`.
- Log estruturado (04.19) com a duração de cada etapa.
- Tratamento das exceções que vierem de dentro dos trabalhadores.

**A prova:** rode com `max_workers` valendo 1, 5, 20 e 100 e faça a tabela.

**As três perguntas que valem a nota:**

1. Onde o tempo parou de cair, e por quê?
2. Trocando as duas ferramentas de lugar (processos para buscar, threads para calcular), quanto piora — e as duas pioram igual?
3. Uma exceção dentro de uma tarefa: **onde** ela aparece, e o que acontece se você **não** consumir o resultado do `map`?

---

## Mini projeto

### MP — O medidor de concorrência `[Mini projeto · ~40 min]`

Um script que receba uma função e descubra sozinho a melhor forma de executá-la N vezes.

**Requisitos:**

- Mede sequencial, threads e processos, em vários tamanhos de pool.
- **Classifica** a tarefa como I/O-bound ou CPU-bound pelos resultados, não por declaração.
- Relata a recomendação com os números que a sustentam.
- **Avisa quando paralelizar piora.**
- Inclui o número de núcleos e o tempo de partida de cada forma.

**E a pergunta que fecha:** o seu medidor precisa que a função seja **serializável** para testar processos — e uma `lambda` não é.

Como o seu script lida com isso: recusa, avisa, ou testa só as formas possíveis? **Descubra a mensagem de erro exata antes de decidir** — ela é ruim o bastante para valer um tratamento próprio.
