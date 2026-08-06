"""Asyncio: uma thread só, e mil esperas ao mesmo tempo.

ATENÇÃO ao nome (D-021): `asyncio.py` sombrearia a biblioteca padrão.

Seis cenas:
    [1] chamar uma corrotina NÃO a executa
    [2] `await` em sequência × `asyncio.gather` — o erro mais comum
    [3] `time.sleep` dentro de corrotina TRAVA o laço inteiro
    [4] `create_task`: quando a tarefa começa de verdade
    [5] exceções no `gather`, e as que somem
    [6] escala: 10 mil esperas em corrotinas × em threads

Uso:
    python codigo/cap22/corrotinas.py
    mypy --strict codigo/cap22/corrotinas.py
"""

import asyncio
import gc
import resource
import threading
import time
import warnings
from typing import Any


async def esperar(nome: str, segundos: float) -> str:
    """Espera de mentira, no lugar de uma requisição de rede."""
    await asyncio.sleep(segundos)
    return nome


async def esperar_bloqueando(segundos: float) -> float:
    """Errada de propósito: `time.sleep` não entrega a vez ao laço."""
    time.sleep(segundos)
    return segundos


async def anunciar(nome: str, segundos: float) -> str:
    print("       %s começou" % nome)
    await asyncio.sleep(segundos)
    print("       %s terminou" % nome)
    return nome


async def falhar(numero: int) -> int:
    await asyncio.sleep(0.05)
    raise ValueError("item %d ruim" % numero)


def cena_1_corrotina_nao_executa() -> None:
    print("[1] CHAMAR UMA CORROTINA NÃO A EXECUTA")

    async def saudacao() -> int:
        print("       (o corpo rodou)")
        return 42

    objeto = saudacao()
    print("    saudacao() devolveu:", type(objeto).__name__)
    print("    o corpo NÃO rodou — nada foi impresso acima")

    with warnings.catch_warnings(record=True) as avisos:
        warnings.simplefilter("always")
        del objeto
        gc.collect()
        for aviso in avisos:
            print("    ao descartá-la:", aviso.category.__name__, "-", aviso.message)

    print("    com asyncio.run ->", asyncio.run(saudacao()))
    print("    >>> `async def` devolve um plano; quem executa é o laço")
    print()


async def _sequencial() -> tuple[list[str], float]:
    inicio = time.perf_counter()
    resultados = [await esperar("a", 0.3),
                  await esperar("b", 0.3),
                  await esperar("c", 0.3)]
    return resultados, (time.perf_counter() - inicio) * 1000


async def _concorrente() -> tuple[list[str], float]:
    inicio = time.perf_counter()
    resultados = list(await asyncio.gather(esperar("a", 0.3),
                                           esperar("b", 0.3),
                                           esperar("c", 0.3)))
    return resultados, (time.perf_counter() - inicio) * 1000


def cena_2_sequencial_x_gather() -> None:
    print("[2] `await` EM SEQUÊNCIA × asyncio.gather")
    seq, ms_seq = asyncio.run(_sequencial())
    con, ms_con = asyncio.run(_concorrente())
    print("    await um após o outro: %s · %6.0f ms" % (seq, ms_seq))
    print("    asyncio.gather:        %s · %6.0f ms" % (con, ms_con))
    print("    >>> resultados idênticos, 3x de diferença.")
    print("        `await` ESPERA; quem dispara junto é o gather")
    print()


async def _gather_de(corrotinas: list[Any]) -> float:
    inicio = time.perf_counter()
    await asyncio.gather(*corrotinas)
    return (time.perf_counter() - inicio) * 1000


async def _com_to_thread() -> float:
    inicio = time.perf_counter()
    await asyncio.gather(*[asyncio.to_thread(time.sleep, 0.3) for _ in range(3)])
    return (time.perf_counter() - inicio) * 1000


def cena_3_bloqueio() -> None:
    print("[3] time.sleep DENTRO DE CORROTINA TRAVA O LAÇO")
    com_await = asyncio.run(_gather_de([esperar("x", 0.3) for _ in range(3)]))
    bloqueando = asyncio.run(_gather_de([esperar_bloqueando(0.3) for _ in range(3)]))
    com_thread = asyncio.run(_com_to_thread())
    print("    3 × asyncio.sleep(0.3):        %6.0f ms" % com_await)
    print("    3 × time.sleep(0.3):           %6.0f ms  <- SOMOU" % bloqueando)
    print("    3 × asyncio.to_thread(sleep):  %6.0f ms" % com_thread)
    print("    >>> há UMA thread. Uma chamada bloqueante para o laço inteiro,")
    print("        e todas as outras corrotinas ficam esperando por ela")
    print()


async def _com_task() -> list[str]:
    print("    criando as tasks…")
    primeira = asyncio.create_task(anunciar("A", 0.2))
    segunda = asyncio.create_task(anunciar("B", 0.1))
    print("    tasks criadas — repare que nada rodou ainda")
    await asyncio.sleep(0)
    print("    …e o primeiro `await` deu a vez ao laço")
    return list(await asyncio.gather(primeira, segunda))


def cena_4_create_task() -> None:
    print("[4] create_task: QUANDO A TAREFA COMEÇA")
    print("   ", asyncio.run(_com_task()))
    print("    >>> create_task AGENDA; o laço só roda quando você dá a vez")
    print()


async def _gather_padrao() -> str:
    try:
        await asyncio.gather(esperar("1", 0.1), falhar(2), esperar("3", 0.1))
    except ValueError as erro:
        return "levantou: %s" % erro
    return "não levantou"


async def _gather_tolerante() -> list[Any]:
    return list(await asyncio.gather(esperar("1", 0.1), falhar(2),
                                     esperar("3", 0.1),
                                     return_exceptions=True))


def cena_5_excecoes() -> None:
    print("[5] EXCEÇÕES NO gather")
    print("    padrão:                ", asyncio.run(_gather_padrao()))
    print("    return_exceptions=True:", asyncio.run(_gather_tolerante()))
    print("    >>> no padrão, a PRIMEIRA exceção aborta e os outros")
    print("        resultados somem — inclusive os que deram certo")
    print()


async def _dez_mil_corrotinas() -> tuple[float, float]:
    antes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    inicio = time.perf_counter()
    await asyncio.gather(*[asyncio.sleep(0.5) for _ in range(10_000)])
    ms = (time.perf_counter() - inicio) * 1000
    depois = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return ms, (depois - antes) / 1024


def cena_6_escala() -> None:
    print("[6] ESCALA — 10 MIL ESPERAS DE 0,5 s")
    ms_async, mb_async = asyncio.run(_dez_mil_corrotinas())
    print("    corrotinas: %6.0f ms · +%5.1f MB" % (ms_async, mb_async))

    antes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    inicio = time.perf_counter()
    fios = [threading.Thread(target=time.sleep, args=(0.5,))
            for _ in range(10_000)]
    for fio in fios:
        fio.start()
    for fio in fios:
        fio.join()
    ms_fios = (time.perf_counter() - inicio) * 1000
    mb_fios = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - antes) / 1024
    print("    threads:    %6.0f ms · +%5.1f MB" % (ms_fios, mb_fios))
    print("    >>> as duas funcionam. A diferença é o CUSTO por espera —")
    print("        e é ela que decide entre dezenas e dezenas de milhares")


def main() -> None:
    cena_1_corrotina_nao_executa()
    cena_2_sequencial_x_gather()
    cena_3_bloqueio()
    cena_4_create_task()
    cena_5_excecoes()
    cena_6_escala()


if __name__ == "__main__":
    main()
