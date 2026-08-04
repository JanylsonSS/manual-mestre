"""Closures: funções que lembram do ambiente em que nasceram.

Cinco cenas:
    [1] o enigma do 04.02 — [lambda: i for i in range(3)] devolve [2,2,2]
    [2] a closure é INSPECIONÁVEL: __closure__ e cell_contents
    [3] a captura é da VARIÁVEL, não do valor — e as duas correções
    [4] nonlocal: estado que sobrevive entre chamadas
    [5] sem nonlocal: UnboundLocalError

Uso:
    python codigo/cap03/closures.py
"""


# ---------------------------------------------------------------
# [2] A fábrica clássica: multiplicador(2) devolve uma função que
#     multiplica por 2. O `fator` sobrevive ao fim de multiplicador.
# ---------------------------------------------------------------
def multiplicador(fator):
    def multiplicar(x):
        return x * fator              # `fator` é uma VARIÁVEL LIVRE
    return multiplicar


# ---------------------------------------------------------------
# [4] Estado entre chamadas. Sem `nonlocal`, o `n += 1` criaria uma
#     variável LOCAL nova — e leria antes de atribuir (cena [5]).
# ---------------------------------------------------------------
def contador(inicio=0):
    n = inicio

    def incrementar(passo=1):
        nonlocal n
        n += passo
        return n

    return incrementar


def contador_sem_nonlocal():
    n = 0

    def incrementar():
        n += 1                        # sem nonlocal: UnboundLocalError
        return n

    return incrementar


def cena_1_enigma():
    print("[1] O ENIGMA")
    funcoes = [lambda: i for i in range(3)]
    print("    [lambda: i for i in range(3)] ->", [f() for f in funcoes])
    print("    >>> esperava [0, 1, 2]")
    print()


def cena_2_inspecao():
    print("[2] A CLOSURE É INSPECIONÁVEL")
    dobro = multiplicador(2)
    triplo = multiplicador(3)
    print("    dobro(5):", dobro(5), "· triplo(5):", triplo(5))
    print("    dobro is triplo:", dobro is triplo, "(objetos diferentes)")
    print("    variáveis livres:", dobro.__code__.co_freevars)
    print("    célula guarda:  ", dobro.__closure__[0].cell_contents)
    print("    a mesma, no triplo:", triplo.__closure__[0].cell_contents)
    print()


def cena_3_captura():
    print("[3] CAPTURA A VARIÁVEL, NÃO O VALOR")

    # Errado: as três funções olham a MESMA variável `i`, que no fim
    # do laço vale 2.
    ruins = []
    for i in range(3):
        ruins.append(lambda: i)
    print("    sem correção:", [f() for f in ruins])

    # Correção 1: default avaliado na DEFINIÇÃO (04.01 §6.4) — aqui a
    # armadilha do capítulo anterior vira ferramenta.
    com_default = [lambda i=i: i for i in range(3)]
    print("    com i=i:     ", [f() for f in com_default])

    # Correção 2: uma fábrica cria um ESCOPO NOVO por chamada.
    def fabricar(valor):
        return lambda: valor

    com_fabrica = [fabricar(i) for i in range(3)]
    print("    com fábrica: ", [f() for f in com_fabrica])
    print()


def cena_4_nonlocal():
    print("[4] nonlocal — ESTADO ENTRE CHAMADAS")
    c = contador()
    print("    c(), c(), c():", c(), c(), c())
    outro = contador(inicio=100)
    print("    contador novo, independente:", outro(), outro())
    print("    o primeiro continua de onde parou:", c())
    print()


def cena_5_sem_nonlocal():
    print("[5] SEM nonlocal")
    incrementar = contador_sem_nonlocal()
    try:
        incrementar()
    except UnboundLocalError as erro:
        print("    UnboundLocalError:", erro)
    print("    >>> o `n += 1` tornou `n` LOCAL, e ele é lido antes de existir")


def main() -> None:
    cena_1_enigma()
    cena_2_inspecao()
    cena_3_captura()
    cena_4_nonlocal()
    cena_5_sem_nonlocal()


if __name__ == "__main__":
    main()
