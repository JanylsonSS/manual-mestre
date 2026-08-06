"""Aurora — coletor concorrente de preços.

Projeto integrador do módulo 04: dataclasses no domínio, Pydantic na
borda, tipos verificados, log estruturado, tempo em UTC, layout `src/`
e concorrência com limite.
"""

from aurora_coletor.coletor import Coletor
from aurora_coletor.fonte import FonteSimulada
from aurora_coletor.modelo import Falha, Produto, Relatorio

__all__ = ["Coletor", "FonteSimulada", "Falha", "Produto", "Relatorio"]
__version__ = "1.0.0"
