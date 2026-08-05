"""Como o Python encontra o que você importa.

Cinco cenas, todas em pastas temporárias que o próprio script cria e
apaga — nada é gravado no seu projeto.

    [1] sys.path: quem entra na lista, e em que ordem
    [2] a diferença entre `python arquivo.py` e `python -m pacote.modulo`
    [3] import relativo: por que ele quebra ao rodar o arquivo direto
    [4] __init__.py: o que ele faz de verdade em 2026
    [5] import circular, e por que a mensagem fala em "partially initialized"

Uso:
    python codigo/cap17/imports.py
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

PYTHON = sys.executable


def rodar(argumentos: list[str], cwd: Path,
          extra_path: str | None = None) -> str:
    """Roda o Python num subprocesso e devolve a saída (com o erro junto)."""
    ambiente = dict(os.environ)
    if extra_path is not None:
        ambiente["PYTHONPATH"] = extra_path
    resultado = subprocess.run([PYTHON, *argumentos], cwd=cwd, env=ambiente,
                               capture_output=True, text=True)
    bruto = (resultado.stdout + resultado.stderr).strip()
    # Indenta a saída inteira para ela não se confundir com a do script.
    return "\n".join("    " + linha.strip() for linha in bruto.splitlines())


def escrever(caminho: Path, conteudo: str) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(conteudo, encoding="utf-8")


def cena_1_sys_path(base: Path) -> None:
    print("[1] sys.path — QUEM ENTRA, E EM QUE ORDEM")
    escrever(base / "sub" / "mostrar.py",
             "import os, sys\n"
             "print('    cwd:        ', os.getcwd())\n"
             "print('    sys.path[0]:', repr(sys.path[0]))\n")

    print("    python sub/mostrar.py  (chamado da pasta de cima):")
    print(rodar(["sub/mostrar.py"], base))
    print("    python -c '…'          (mesma pasta):")
    print(rodar(["-c", "import os, sys;"
                 " print('    cwd:        ', os.getcwd());"
                 " print('    sys.path[0]:', repr(sys.path[0]))"], base))
    print("    >>> ao rodar um ARQUIVO, entra a pasta DELE — não a sua")
    print("        com -c e -m, entra a pasta atual (o '' da lista)")
    print()


def cena_2_arquivo_x_modulo(base: Path) -> None:
    print("[2] `python arquivo.py` × `python -m pacote.modulo`")
    pacote = base / "loja"
    escrever(pacote / "__init__.py", "")
    escrever(pacote / "precos.py", "TAXA = 0.15\n")
    escrever(pacote / "relatorio.py",
             "from loja.precos import TAXA\n"
             "print('    TAXA =', TAXA, '· __name__ =', __name__)\n")

    print("    python loja/relatorio.py:")
    print(rodar(["loja/relatorio.py"], base).splitlines()[-1])
    print("    python -m loja.relatorio:")
    print(rodar(["-m", "loja.relatorio"], base).splitlines()[-1])
    print("    >>> no primeiro, sys.path[0] vira `loja/` — e de dentro do")
    print("        pacote o próprio pacote não é encontrável. O segundo põe")
    print("        a pasta de cima, e o módulo sabe a que pacote pertence")
    print()


def cena_3_import_relativo(base: Path) -> None:
    print("[3] IMPORT RELATIVO")
    pacote = base / "loja"
    escrever(pacote / "resumo.py",
             "from .precos import TAXA\n"
             "print('    relativo funcionou · TAXA =', TAXA)\n")

    print("    python loja/resumo.py:")
    print(rodar(["loja/resumo.py"], base).splitlines()[-1])
    print("    python -m loja.resumo:")
    print(rodar(["-m", "loja.resumo"], base).splitlines()[-1])
    print("    >>> o ponto significa 'o pacote deste módulo'. Rodando o")
    print("        arquivo direto, não há pacote nenhum — daí a mensagem")
    print()


def cena_4_init(base: Path) -> None:
    print("[4] __init__.py — O QUE ELE FAZ DE VERDADE")
    escrever(base / "a" / "pacote" / "mod_a.py", "def de_a(): return 'A'\n")
    escrever(base / "b" / "pacote" / "mod_b.py", "def de_b(): return 'B'\n")
    caminhos = "%s%s%s" % (base / "a", os.pathsep, base / "b")

    programa = ("import pacote\n"
                "print('    __path__:', [p.split('/')[-2] + '/pacote'"
                " for p in pacote.__path__])\n"
                "try:\n"
                "    import pacote.mod_b\n"
                "    print('    achou mod_b, que está na OUTRA pasta')\n"
                "except ModuleNotFoundError as erro:\n"
                "    print('    mod_b ->', erro)\n")

    print("    sem __init__.py (as duas pastas se chamam `pacote`):")
    print(rodar(["-c", programa], base, extra_path=caminhos))
    (base / "a" / "pacote" / "__init__.py").write_text("", encoding="utf-8")
    print("    com __init__.py na primeira:")
    print(rodar(["-c", programa], base, extra_path=caminhos))
    print("    >>> sem ele, pastas de mesmo nome em lugares diferentes")
    print("        se FUNDEM num pacote só (PEP 420). Com ele, a primeira ganha")
    print()


def cena_5_circular(base: Path) -> None:
    print("[5] IMPORT CIRCULAR")
    escrever(base / "ciclo" / "__init__.py", "")
    escrever(base / "ciclo" / "a.py",
             "from ciclo.b import beta\n\ndef alfa(): return 'alfa'\n")
    escrever(base / "ciclo" / "b.py",
             "from ciclo.a import alfa\n\ndef beta(): return 'beta'\n")

    saida = rodar(["-c", "import ciclo.a"], base)
    print(saida.splitlines()[-1][:100])
    print("    >>> 'partially initialized' é a pista: quando `b` pediu `alfa`,")
    print("        o módulo `a` estava na linha 1 e ainda não tinha definido nada")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="cap17-") as temporaria:
        base = Path(temporaria)
        cena_1_sys_path(base)
        cena_2_arquivo_x_modulo(base)
        cena_3_import_relativo(base)
        cena_4_init(base)
        cena_5_circular(base)


if __name__ == "__main__":
    main()
