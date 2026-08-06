"""Threads, processos e o GIL: onde cada um ganha, e quanto.

ATENÇÃO ao `if __name__ == "__main__"` no fim: com processos ele NÃO é
opcional. Em Windows e macOS o Python cria o processo filho reimportando
este arquivo, e sem a guarda cada filho criaria outros filhos, sem parar.

Seis cenas:
    [1] CPU-bound: sequencial × threads × processos
    [2] I/O-bound: os mesmos três, e a inversão
    [3] a condição de corrida — e por que ela não aparece quando você testa
    [4] a trava, e o `with` do 04.20
    [5] o custo de partida e o custo de ENVIAR dados
    [6] a tabela de decisão, com os números do seu computador

Uso:
    python codigo/cap21/concorrencia.py
    mypy --strict codigo/cap21/concorrencia.py
"""

import os
import pickle
import sys
import threading
import time
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

TAREFAS = 4
TAMANHO = 3_000_000
ESPERA = 0.5


# ---------------------------------------------------------------
# As duas tarefas. A primeira só usa processador; a segunda só
# espera. É a distinção que decide tudo neste capítulo.
# ---------------------------------------------------------------
def tarefa_cpu(n: int) -> int:
    """Trabalho puro de processador — o GIL não é liberado aqui."""
    total = 0
    for i in range(n):
        total += i * i
    return total


def tarefa_io(segundos: float) -> float:
    """Espera — representa rede, disco, banco. O GIL É liberado aqui."""
    time.sleep(segundos)
    return segundos


def soma_lista(dados: list[int]) -> int:
    return sum(dados)


def medir(rotulo: str, funcao: Callable[[], object]) -> float:
    inicio = time.perf_counter()
    funcao()
    ms = (time.perf_counter() - inicio) * 1000
    print("    %-34s %8.1f ms" % (rotulo, ms))
    return ms


def cena_1_cpu() -> tuple[float, float, float]:
    print("[1] CPU-BOUND — %d tarefas de %d iterações" % (TAREFAS, TAMANHO))
    sequencial = medir("sequencial",
                       lambda: [tarefa_cpu(TAMANHO) for _ in range(TAREFAS)])
    with ThreadPoolExecutor(TAREFAS) as fios:
        com_threads = medir("ThreadPoolExecutor(4)",
                            lambda: list(fios.map(tarefa_cpu,
                                                  [TAMANHO] * TAREFAS)))
    with ProcessPoolExecutor(TAREFAS) as processos:
        com_processos = medir("ProcessPoolExecutor(4)",
                              lambda: list(processos.map(tarefa_cpu,
                                                         [TAMANHO] * TAREFAS)))
    print("    ganho: threads %.2fx · processos %.2fx"
          % (sequencial / com_threads, sequencial / com_processos))
    print("    >>> threads não ganham NADA: o GIL deixa uma rodar por vez")
    print()
    return sequencial, com_threads, com_processos


def cena_2_io() -> tuple[float, float, float]:
    print("[2] I/O-BOUND — %d esperas de %.1f s" % (TAREFAS, ESPERA))
    sequencial = medir("sequencial",
                       lambda: [tarefa_io(ESPERA) for _ in range(TAREFAS)])
    with ThreadPoolExecutor(TAREFAS) as fios:
        com_threads = medir("ThreadPoolExecutor(4)",
                            lambda: list(fios.map(tarefa_io,
                                                  [ESPERA] * TAREFAS)))
    with ProcessPoolExecutor(TAREFAS) as processos:
        com_processos = medir("ProcessPoolExecutor(4)",
                              lambda: list(processos.map(tarefa_io,
                                                         [ESPERA] * TAREFAS)))
    print("    ganho: threads %.2fx · processos %.2fx"
          % (sequencial / com_threads, sequencial / com_processos))
    print("    >>> agora threads ganham quase 4x: quem espera SOLTA o GIL")
    print()
    return sequencial, com_threads, com_processos


def somar_concorrente(forcar_troca: bool, usar_trava: bool,
                      n_fios: int = 4, por_fio: int = 1000) -> tuple[int, int]:
    saldo = 0
    trava = threading.Lock()

    def somar() -> None:
        nonlocal saldo
        for _ in range(por_fio):
            if usar_trava:
                with trava:                      # 04.20: o with garante o release
                    atual = saldo
                    if forcar_troca:
                        time.sleep(0)
                    saldo = atual + 1
            else:
                atual = saldo                    # LÊ
                if forcar_troca:
                    time.sleep(0)                # entrega a vez aqui no meio
                saldo = atual + 1                # ESCREVE

    fios = [threading.Thread(target=somar) for _ in range(n_fios)]
    for fio in fios:
        fio.start()
    for fio in fios:
        fio.join()
    return saldo, n_fios * por_fio


def cena_3_corrida() -> None:
    print("[3] A CONDIÇÃO DE CORRIDA")
    print("    -- sem forçar a troca (o que você testaria) --")
    for _ in range(3):
        obtido, esperado = somar_concorrente(forcar_troca=False, usar_trava=False)
        print("       %5d de %5d · perdeu %d" % (obtido, esperado, esperado - obtido))
    print("    >>> zero perdas em três execuções. O defeito ESTÁ lá")

    print("    -- forçando a troca entre ler e escrever --")
    for _ in range(3):
        obtido, esperado = somar_concorrente(forcar_troca=True, usar_trava=False)
        perdeu = esperado - obtido
        print("       %5d de %5d · perdeu %d (%.0f%%)"
              % (obtido, esperado, perdeu, 100 * perdeu / esperado))
    print("    >>> a MESMA operação, com o mesmo código, perde 75%")
    print()


def cena_4_trava() -> None:
    print("[4] A TRAVA")
    for _ in range(3):
        obtido, esperado = somar_concorrente(forcar_troca=True, usar_trava=True)
        print("       %5d de %5d · perdeu %d" % (obtido, esperado, esperado - obtido))
    print("    >>> com `with trava:`, forçando a troca do mesmo jeito: exato")
    print("        e o `with` garante o release mesmo se o corpo falhar (04.20)")
    print()


def cena_5_custo() -> None:
    print("[5] O CUSTO DE PARTIDA E O DE ENVIAR DADOS")
    with ThreadPoolExecutor(4) as fios:
        medir("4 tarefas vazias em threads", lambda: list(fios.map(int, range(4))))
    with ProcessPoolExecutor(4) as processos:
        medir("4 tarefas vazias em processos",
              lambda: list(processos.map(int, range(4))))

    dados = list(range(1_000_000))
    print("    -- somar uma lista de 1 milhão, 4 vezes --")
    sequencial = medir("sequencial", lambda: [soma_lista(dados) for _ in range(4)])
    with ThreadPoolExecutor(2) as fios:
        medir("threads(2)", lambda: list(fios.map(soma_lista, [dados] * 4)))
    with ProcessPoolExecutor(2) as processos:
        com_processos = medir("processos(2)",
                              lambda: list(processos.map(soma_lista, [dados] * 4)))

    inicio = time.perf_counter()
    serializado = pickle.dumps(dados)
    ms = (time.perf_counter() - inicio) * 1000
    print("    serializar a lista UMA vez: %.1f ms · %.1f MB"
          % (ms, len(serializado) / 1024 / 1024))
    print("    >>> processos ficaram %.1fx MAIS LENTOS que o sequencial:"
          % (com_processos / sequencial))
    print("        cada chamada copia a lista inteira para o outro processo")
    print()


def cena_6_decisao(cpu: tuple[float, float, float],
                   io: tuple[float, float, float]) -> None:
    print("[6] A TABELA DE DECISÃO — com os números DESTE computador")
    print("    máquina com %d núcleos · Python %s"
          % (os.cpu_count() or 0, sys.version.split()[0]))
    print()
    print("    %-12s %12s %12s %12s" % ("", "sequencial", "threads", "processos"))
    print("    %-12s %10.0f ms %10.0f ms %10.0f ms" % ("CPU-bound", *cpu))
    print("    %-12s %10.0f ms %10.0f ms %10.0f ms" % ("I/O-bound", *io))
    print()
    print("    espera (rede, disco, banco) -> THREADS")
    print("    conta (cálculo, laço)       -> PROCESSOS, se os dados forem pequenos")
    print("    conta com dados grandes     -> meça antes: a cópia pode dominar")


def main() -> None:
    cpu = cena_1_cpu()
    io = cena_2_io()
    cena_3_corrida()
    cena_4_trava()
    cena_5_custo()
    cena_6_decisao(cpu, io)


# A guarda NÃO é opcional aqui: com `spawn` (Windows e macOS), cada
# processo filho reimporta este arquivo, e sem ela criaria outros.
if __name__ == "__main__":
    main()
