"""Aurora — catálogo de produtos.

Este arquivo é a API pública do pacote: o que ele reexporta é o que
alguém de fora deve usar. `__all__` declara isso explicitamente, e
serve tanto para quem lê quanto para `from aurora import *`.
"""

from aurora.formato import formatar_reais
from aurora.modelo import Produto

__all__ = ["Produto", "formatar_reais"]
__version__ = "0.1.0"
