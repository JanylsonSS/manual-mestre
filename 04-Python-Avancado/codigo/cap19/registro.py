"""A configuração de log do projeto — um módulo, uma função.

ATENÇÃO ao nome (D-021): `logging.py` sombrearia a biblioteca padrão.

Duas coisas moram aqui, e nada mais:

    configurar()      chamada UMA vez, no ponto de entrada do programa
    FormatadorJSON    uma linha de JSON por registro, com carimbo em UTC

Nenhum outro módulo do projeto configura log. Todos apenas fazem
`log = logging.getLogger(__name__)` e usam.

Uso:
    from aurora.registro import configurar
    configurar(nivel="INFO", formato="json")
"""

import json
import logging
import sys
import time
from typing import Any, Literal

# Os campos que todo LogRecord já tem. Serve para descobrir quais vieram
# do `extra=` de quem chamou (§6.6).
CAMPOS_PADRAO = frozenset(
    logging.LogRecord("", 0, "", 0, "", (), None).__dict__
) | {"asctime", "message", "taskName"}

FORMATO_TEXTO = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"


class FormatadorJSON(logging.Formatter):
    """Uma linha de JSON por registro, com os campos de `extra=` juntos."""

    # Carimbo em UTC, e não na hora local da máquina (04.18).
    # `staticmethod` porque `converter` é um atributo de classe que o
    # `Formatter` chama como função — sem ele, o verificador (04.14)
    # o trata como método e reclama da assinatura.
    converter = staticmethod(time.gmtime)

    def format(self, registro: logging.LogRecord) -> str:
        dados: dict[str, Any] = {
            "quando": self.formatTime(registro, "%Y-%m-%dT%H:%M:%S") + "Z",
            "nivel": registro.levelname,
            "origem": registro.name,
            "mensagem": registro.getMessage(),
        }
        # Tudo o que veio de `extra=` entra como campo próprio.
        for chave, valor in registro.__dict__.items():
            if chave not in CAMPOS_PADRAO:
                dados[chave] = valor
        if registro.exc_info:
            dados["excecao"] = self.formatException(registro.exc_info)
        return json.dumps(dados, ensure_ascii=False)


def configurar(nivel: str = "INFO",
               formato: Literal["texto", "json"] = "texto") -> None:
    """Configura o log do processo. Chame UMA vez, no ponto de entrada.

    `force=True` remove handlers já instalados — sem ele, uma segunda
    chamada não teria efeito nenhum e a primeira configuração venceria,
    em silêncio (§6.3).
    """
    manipulador = logging.StreamHandler(sys.stderr)
    if formato == "json":
        manipulador.setFormatter(FormatadorJSON())
    else:
        manipulador.setFormatter(logging.Formatter(FORMATO_TEXTO))
        # Carimbo em UTC também no formato de texto.
        logging.Formatter.converter = time.gmtime

    logging.basicConfig(level=nivel, handlers=[manipulador], force=True)

    # Bibliotecas barulhentas ficam num nível mais alto que o do projeto.
    for barulhenta in ("urllib3", "asyncio", "botocore"):
        logging.getLogger(barulhenta).setLevel(logging.WARNING)
