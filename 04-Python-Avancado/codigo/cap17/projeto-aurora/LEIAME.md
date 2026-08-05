# Aurora — projeto de referência do capítulo 04.17

Layout `src/`, `pyproject.toml`, testes que importam o pacote instalado.

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate          # .venv\Scripts\activate no Windows

pip install -e ".[dev]"            # instala o pacote em modo editável

aurora                             # o comando declarado em [project.scripts]
aurora "Mouse Sem Fio"

pytest
mypy src
```

## Por que `pip install -e .` é obrigatório aqui

Com layout `src/`, `import aurora` **não funciona** antes da instalação —
nem de dentro da pasta do projeto. É de propósito: o pacote passa a ser
alcançado do mesmo jeito que quem o instalar vai alcançá-lo (§6.3).
