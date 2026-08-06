"""A configuração de log do projeto (04.19 / D-030)."""

import json
import logging
import sys
import time
from typing import Any, Literal

CAMPOS_PADRAO = frozenset(
    logging.LogRecord("", 0, "", 0, "", (), None).__dict__
) | {"asctime", "message", "taskName"}


class FormatadorJSON(logging.Formatter):
    converter = staticmethod(time.gmtime)

    def format(self, registro: logging.LogRecord) -> str:
        dados: dict[str, Any] = {
            "quando": self.formatTime(registro, "%Y-%m-%dT%H:%M:%S") + "Z",
            "nivel": registro.levelname,
            "origem": registro.name,
            "mensagem": registro.getMessage(),
        }
        for chave, valor in registro.__dict__.items():
            if chave not in CAMPOS_PADRAO:
                dados[chave] = valor
        if registro.exc_info:
            dados["excecao"] = self.formatException(registro.exc_info)
        return json.dumps(dados, ensure_ascii=False)


def configurar(nivel: str = "INFO",
               formato: Literal["texto", "json"] = "texto") -> None:
    manipulador = logging.StreamHandler(sys.stderr)
    if formato == "json":
        manipulador.setFormatter(FormatadorJSON())
    else:
        logging.Formatter.converter = time.gmtime
        manipulador.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)-8s %(name)s: %(message)s"))
    logging.basicConfig(level=nivel, handlers=[manipulador], force=True)
