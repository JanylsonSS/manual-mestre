"""Decoradores: o @ desmontado peça por peça.

Seis cenas:
    [1] o @ é açúcar — as duas formas produzem o mesmo objeto
    [2] o que se PERDE sem functools.wraps (nome, doc e ASSINATURA)
    [3] o decorador roda na DEFINIÇÃO, não na chamada
    [4] decorador com argumentos exige TRÊS níveis
    [5] empilhamento: o de baixo aplica primeiro
    [6] um decorador útil de verdade: cronometrar + contar

Uso:
    python codigo/cap04/decoradores.py
"""

import functools
import inspect
import time


# ---------------------------------------------------------------
# [1] O decorador mais simples possível. Recebe uma função, devolve
#     outra — que é o 04.02 (função como valor) mais o 04.03
#     (closure sobre `funcao`) mais o 04.01 (repasse com *args).
# ---------------------------------------------------------------
def dobrar_resultado(funcao):
    def envolvida(*args, **kwargs):
        return funcao(*args, **kwargs) * 2
    return envolvida


# ---------------------------------------------------------------
# [2] O mesmo decorador, sem e com wraps.
# ---------------------------------------------------------------
def sem_wraps(funcao):
    def envolvida(*args, **kwargs):
        return funcao(*args, **kwargs)
    return envolvida


def com_wraps(funcao):
    @functools.wraps(funcao)                 # copia nome, doc e __wrapped__
    def envolvida(*args, **kwargs):
        return funcao(*args, **kwargs)
    return envolvida


# ---------------------------------------------------------------
# [4] Decorador COM argumentos: uma fábrica (04.03) que devolve um
#     decorador. Três níveis, e cada um tem um nome próprio.
# ---------------------------------------------------------------
def repetir(vezes):
    def decorador(funcao):
        @functools.wraps(funcao)
        def envolvida(*args, **kwargs):
            return [funcao(*args, **kwargs) for _ in range(vezes)]
        return envolvida
    return decorador


def marcar(tag):
    def decorador(funcao):
        @functools.wraps(funcao)
        def envolvida(*args, **kwargs):
            return "<%s>%s</%s>" % (tag, funcao(*args, **kwargs), tag)
        return envolvida
    return decorador


# ---------------------------------------------------------------
# [6] O decorador que o capítulo entrega: cronometra e conta, e
#     expõe as estatísticas num ATRIBUTO da função (04.01 §7).
# ---------------------------------------------------------------
def instrumentar(funcao):
    chamadas = 0
    total_ms = 0.0

    @functools.wraps(funcao)
    def envolvida(*args, **kwargs):
        nonlocal chamadas, total_ms          # reatribui: exige nonlocal (04.03)
        inicio = time.perf_counter()
        try:
            return funcao(*args, **kwargs)
        finally:
            # finally: conta mesmo se a função levantar exceção.
            chamadas += 1
            total_ms += (time.perf_counter() - inicio) * 1000

    envolvida.estatisticas = lambda: (chamadas, round(total_ms, 3))
    return envolvida


def cena_1_acucar():
    print("[1] O @ É AÇÚCAR SINTÁTICO")

    @dobrar_resultado
    def com_arroba(x):
        return x

    def sem_arroba(x):
        return x
    sem_arroba = dobrar_resultado(sem_arroba)      # exatamente o que o @ faz

    print("    com @:", com_arroba(5), "· sem @:", sem_arroba(5))
    print()


def cena_2_wraps():
    print("[2] O QUE SE PERDE SEM functools.wraps")

    @sem_wraps
    def calcular_a(x, y=2):
        """Soma dois números."""
        return x + y

    @com_wraps
    def calcular_b(x, y=2):
        """Soma dois números."""
        return x + y

    for rotulo, funcao in [("sem wraps", calcular_a), ("com wraps", calcular_b)]:
        print("    %-10s __name__=%-11s sig=%-10s doc=%s" % (
            rotulo, funcao.__name__, inspect.signature(funcao),
            repr(funcao.__doc__)))
    print("    >>> wraps restaura ATÉ a assinatura, via __wrapped__")
    print()


def cena_3_quando_roda():
    print("[3] O DECORADOR RODA NA DEFINIÇÃO")

    def anunciar(funcao):
        print("    >>> decorando '%s' AGORA (a função ainda não foi chamada)"
              % funcao.__name__)
        return funcao

    @anunciar
    def alvo():
        return "resultado"

    print("    só agora chamamos:", alvo())
    print()


def cena_4_com_argumentos():
    print("[4] DECORADOR COM ARGUMENTOS — TRÊS NÍVEIS")

    @repetir(3)
    def cumprimentar():
        return "oi"

    print("    @repetir(3) ->", cumprimentar())
    print("    repetir(3) devolve o decorador; ELE recebe a função")
    print()


def cena_5_empilhamento():
    print("[5] EMPILHAMENTO")

    @marcar("externo")
    @marcar("interno")
    def texto():
        return "X"

    print("    resultado:", texto())
    print("    >>> o de BAIXO aplica primeiro e fica mais interno")
    print()


def cena_6_util():
    print("[6] UM DECORADOR ÚTIL")

    @instrumentar
    def somar_lento(n):
        time.sleep(0.001)
        if n < 0:
            raise ValueError("n negativo")
        return sum(range(n))

    somar_lento(100)
    somar_lento(200)
    try:
        somar_lento(-1)
    except ValueError:
        pass

    chamadas, ms = somar_lento.estatisticas()
    print("    chamadas: %d (inclui a que falhou) · total: %.3f ms" % (chamadas, ms))
    print("    __name__ preservado:", somar_lento.__name__)


def main() -> None:
    cena_1_acucar()
    cena_2_wraps()
    cena_3_quando_roda()
    cena_4_com_argumentos()
    cena_5_empilhamento()
    cena_6_util()


if __name__ == "__main__":
    main()
