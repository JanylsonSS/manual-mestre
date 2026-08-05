"""Seis cenas sobre logging — cada uma num processo separado.

Por que subprocessos: a configuração de log é **global ao processo**.
Uma cena que chama `basicConfig` afeta todas as seguintes, e a segunda
chamada não teria efeito (§6.3). Isolar em processos é a única forma
honesta de mostrar configurações diferentes no mesmo arquivo — e o fato
de isso ser necessário já é parte do conteúdo.

    [1] o nível padrão: por que o seu `logger.info` não aparece
    [2] `basicConfig` só funciona uma vez
    [3] formatação preguiçosa × f-string
    [4] `exception()` × `error()` dentro do `except`
    [5] `extra=` — e o que acontece quando ele falta
    [6] a mesma mensagem em texto e em JSON

Uso:
    python codigo/cap19/demonstracao.py
"""

import subprocess
import sys
import textwrap

PYTHON = sys.executable


def cena(titulo: str, programa: str, comentario: str = "") -> None:
    print("[%s]" % titulo)
    resultado = subprocess.run([PYTHON, "-c", textwrap.dedent(programa)],
                               capture_output=True, text=True)
    saida = (resultado.stdout + resultado.stderr).strip()
    for linha in saida.splitlines():
        print("    " + linha)
    if comentario:
        for linha in comentario.strip().splitlines():
            print("    " + linha.strip())
    print()


def main() -> None:
    cena("1 O NÍVEL PADRÃO", """
        import logging
        log = logging.getLogger("aurora")
        log.debug("chamada de debug")
        log.info("pedido criado")
        log.warning("estoque baixo")
        log.error("falha ao cobrar")
        print("nível efetivo:", logging.getLevelName(log.getEffectiveLevel()))
        print("handlers do root:", logging.getLogger().handlers)
    """, """
        >>> debug e info NÃO apareceram: o nível padrão é WARNING
            e sem configuração o formato é 'NÍVEL:origem:mensagem',
            impresso em stderr pelo handler de último recurso
    """)

    cena("2 basicConfig SÓ FUNCIONA UMA VEZ", """
        import logging
        logging.basicConfig(level=logging.DEBUG, format="[1] %(levelname)s %(message)s")
        logging.basicConfig(level=logging.ERROR, format="[2] %(levelname)s %(message)s")
        log = logging.getLogger("aurora")
        log.debug("mensagem de debug")
        log.error("mensagem de erro")
    """, """
        >>> as duas saíram com o formato [1]: a segunda chamada não
            fez nada, sem erro nenhum. `force=True` remove os handlers
            anteriores e faz a segunda valer
    """)

    cena("3 FORMATAÇÃO PREGUIÇOSA × f-STRING", """
        import logging, timeit
        preparo = (
            "import logging\\n"
            "logging.basicConfig(level=logging.WARNING,"
            " handlers=[logging.NullHandler()])\\n"
            "log = logging.getLogger('p')\\n"
            "class Caro:\\n"
            "    def __str__(self): return 'x' * 1000\\n"
            "caro = Caro()\\n"
            "barato = 42\\n")
        for rotulo, trecho in [
            ("barato · '%s', valor", "log.debug('pedido %s', barato)"),
            ("barato · f-string   ", "log.debug(f'pedido {barato}')"),
            ("caro   · '%s', valor", "log.debug('pedido %s', caro)"),
            ("caro   · f-string   ", "log.debug(f'pedido {caro}')"),
        ]:
            t = min(timeit.repeat(trecho, preparo, number=200000, repeat=3))
            print("%-24s %6.1f ms por 200 mil chamadas" % (rotulo, t * 1000))
    """, """
        >>> as quatro chamadas produzem ZERO saída (DEBUG desligado).
            O custo do `%s` não muda com o valor — ele nem formata.
            O da f-string cresce com o valor, porque ela formata antes
    """)

    cena("4 exception() × error() DENTRO DO except", """
        import logging, sys
        logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                            format="%(levelname)-8s %(message)s")
        log = logging.getLogger("aurora")
        try:
            total = 100 / 0
        except ZeroDivisionError as erro:
            log.error("falha ao calcular o total: %s", erro)
        try:
            total = 100 / 0
        except ZeroDivisionError:
            log.exception("falha ao calcular o total")
    """, """
        >>> o primeiro registra a frase; o segundo registra o RASTRO,
            com arquivo e linha. `exception()` só funciona dentro de
            um `except`, e equivale a `error(..., exc_info=True)`
    """)

    cena("5 extra= E O QUE ACONTECE QUANDO ELE FALTA", """
        import logging, sys
        manipulador = logging.StreamHandler(sys.stdout)
        manipulador.setFormatter(logging.Formatter(
            "%(levelname)-8s pedido=%(pedido)s %(message)s"))
        log = logging.getLogger("aurora")
        log.addHandler(manipulador)
        log.propagate = False
        log.setLevel(logging.INFO)
        log.info("pedido criado", extra={"pedido": "P-123"})
        log.info("esta mensagem some")
    """, """
        >>> a segunda mensagem NÃO aparece: o formatador exigia `pedido`,
            não achou, e o erro foi para stderr. Um formatador com campo
            obrigatório perde toda mensagem que não o traga
    """)

    cena("6 A MESMA MENSAGEM, EM TEXTO E EM JSON", """
        import logging, sys
        sys.path.insert(0, "codigo/cap19")
        from registro import configurar

        configurar(nivel="INFO", formato="texto")
        logging.getLogger("aurora.pedidos").info(
            "pedido criado", extra={"pedido": "P-123", "cliente_id": 7})

        configurar(nivel="INFO", formato="json")
        log = logging.getLogger("aurora.pedidos")
        log.info("pedido criado", extra={"pedido": "P-123", "cliente_id": 7})
        try:
            100 / 0
        except ZeroDivisionError:
            log.exception("falha ao cobrar", extra={"pedido": "P-123"})
    """, """
        >>> o texto é para quem lê no terminal; o JSON é para quem
            consulta depois — `pedido=P-123` vira campo pesquisável.
            E os dois carimbam a hora em UTC (04.18)
    """)


if __name__ == "__main__":
    main()
