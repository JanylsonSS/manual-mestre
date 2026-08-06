# Aurora — coletor concorrente

Projeto integrador do módulo 04. Ele junta, num programa só, o que os
vinte e dois capítulos anteriores construíram:

| Peça | Capítulo |
|---|---|
| `modelo.py` — dataclasses congeladas, no domínio | 04.13 |
| `esquemas.py` — Pydantic, na borda | 04.15 |
| tipos verificados por `mypy --strict` | 04.14 |
| layout `src/` e `pyproject.toml` | 04.17 |
| `tempo.py` — UTC em tudo | 04.18 |
| `registro.py` — log estruturado | 04.19 |
| `async with` e limpeza garantida | 04.20 |
| espera é I/O-bound → concorrência, não paralelismo | 04.21 |
| `gather`, `Semaphore`, `wait_for` | 04.22 · 04.23 |

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate          # .venv\Scripts\activate no Windows
pip install -e ".[dev]"

aurora-coletar --itens 50 --limite 10
aurora-coletar --itens 50 --limite 1        # compare a duração
aurora-coletar --formato json --nivel DEBUG

pytest
mypy src
```

## O experimento que vale fazer

Rode com `--limite` valendo 1, 5, 20 e 50 e monte a tabela. O tempo cai
até o número de itens, e não até o número de núcleos — porque isto é
espera, não conta (04.21).

Depois rode com `--falhas 0.5` e observe o número de **consultas**: ele
passa do número de itens, porque cada falha temporária gera uma nova
tentativa.
