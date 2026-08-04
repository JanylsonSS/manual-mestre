#!/usr/bin/env python3
# ------------------------------------------------------------
# sql.py
# Módulo 03 — SQL · executor de consultas do laboratório
# O que este arquivo faz: roda um arquivo .sql (ou uma consulta
#   digitada) contra o banco aurora.db e mostra o resultado em tabela
# Como executar:
#     python sql.py consultas.sql
#     python sql.py "SELECT nome FROM clientes LIMIT 3"
#     python sql.py                       (modo interativo)
# ------------------------------------------------------------

import os
import sqlite3
import sys

# O banco fica em 03-SQL/dados/aurora.db, ache de onde o script for chamado
AQUI = os.path.dirname(os.path.abspath(__file__))
BANCO = os.environ.get("AURORA_BANCO", os.path.join(AQUI, "..", "dados", "aurora.db"))
LARGURA_MAXIMA = 28          # corta colunas muito largas na exibição


def formatar_tabela(colunas, linhas):
    """Devolve o texto de uma tabela alinhada (não imprime — 01.18)."""
    if not colunas:
        return "(sem colunas)"

    # Largura de cada coluna: o maior conteúdo, limitado pelo teto
    larguras = []
    for i, coluna in enumerate(colunas):
        maior = len(str(coluna))
        for linha in linhas:
            maior = max(maior, len(exibir(linha[i])))
        larguras.append(min(maior, LARGURA_MAXIMA))

    partes = []
    cabecalho = " | ".join(str(c).ljust(l) for c, l in zip(colunas, larguras))
    partes.append(cabecalho)
    partes.append("-+-".join("-" * l for l in larguras))

    for linha in linhas:
        celulas = []
        for valor, largura in zip(linha, larguras):
            texto = exibir(valor)
            if len(texto) > largura:
                texto = texto[: largura - 1] + "…"
            # Números alinham à direita; texto, à esquerda
            if isinstance(valor, (int, float)):
                celulas.append(texto.rjust(largura))
            else:
                celulas.append(texto.ljust(largura))
        partes.append(" | ".join(celulas))

    return "\n".join(partes)


def exibir(valor):
    """NULL precisa aparecer como NULL, não como vazio (03.03)."""
    if valor is None:
        return "NULL"
    return str(valor)


def executar(conexao, comando):
    """Executa um comando e devolve o texto do resultado."""
    cursor = conexao.cursor()
    cursor.execute(comando)

    if cursor.description is None:          # INSERT/UPDATE/DELETE/DDL
        # Sem commit() aqui: a conexão está em autocommit (veja main()),
        # então cada comando já vale sozinho — e BEGIN/ROLLBACK escritos
        # por você funcionam como funcionariam num cliente de verdade.
        return f"OK. Linhas afetadas: {cursor.rowcount}"

    linhas = cursor.fetchall()
    colunas = [d[0] for d in cursor.description]
    tabela = formatar_tabela(colunas, linhas)
    plural = "linha" if len(linhas) == 1 else "linhas"
    return f"{tabela}\n\n({len(linhas)} {plural})"


def separar_comandos(texto):
    """Quebra um arquivo .sql em comandos, ignorando comentários de linha."""
    limpo = []
    for linha in texto.splitlines():
        sem_comentario = linha.split("--")[0]
        limpo.append(sem_comentario)
    inteiro = "\n".join(limpo)
    return [c.strip() for c in inteiro.split(";") if c.strip()]


def main():
    if not os.path.exists(BANCO):
        print(f"Erro: banco nao encontrado em {BANCO}", file=sys.stderr)
        print("Rode antes: python codigo/cap01/criar_laboratorio.py", file=sys.stderr)
        sys.exit(1)

    conexao = sqlite3.connect(BANCO)
    # isolation_level=None desliga o gerenciamento automático de transações
    # do driver Python. Sem isso, ele abriria uma transação por conta própria
    # e o seu ROLLBACK não teria o que desfazer (03.11, 03.15).
    conexao.isolation_level = None
    conexao.execute("PRAGMA foreign_keys = ON")     # o SQLite exige ligar (03.13)

    try:
        if len(sys.argv) > 1:
            alvo = sys.argv[1]
            if os.path.exists(alvo):                # é um arquivo .sql
                with open(alvo, encoding="utf-8") as arquivo:
                    comandos = separar_comandos(arquivo.read())
                for numero, comando in enumerate(comandos, start=1):
                    print(f"--- [{numero}] {comando.splitlines()[0][:60]}")
                    print(executar(conexao, comando))
                    print()
            else:                                   # é a consulta em si
                print(executar(conexao, alvo))
        else:
            modo_interativo(conexao)
    except sqlite3.Error as erro:                   # captura específica (01.21)
        print(f"Erro de SQL: {erro}", file=sys.stderr)
        sys.exit(1)
    finally:
        conexao.close()


def modo_interativo(conexao):
    print(f"Laboratorio Aurora — {BANCO}")
    print("Digite uma consulta terminada em ';'. Vazio ou 'sair' encerra.\n")
    acumulado = ""
    while True:
        try:
            linha = input("sql> " if not acumulado else "...> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if linha.strip().lower() in ("sair", "exit", "quit"):
            break
        if not linha.strip() and not acumulado:
            break
        acumulado += " " + linha
        if ";" in acumulado:
            for comando in separar_comandos(acumulado):
                try:
                    print(executar(conexao, comando))
                except sqlite3.Error as erro:
                    print(f"Erro de SQL: {erro}")
                print()
            acumulado = ""


if __name__ == "__main__":
    main()
