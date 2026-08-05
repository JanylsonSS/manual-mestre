"""Datas, horas e fusos: o que o relógio diz e o que aconteceu.

ATENÇÃO ao nome (D-021): `datetime.py` sombrearia a biblioteca padrão.

Seis cenas:
    [1] ingênuo × consciente, e o `utcnow()` que engana
    [2] o fuso do Brasil — e o horário de verão que existiu até 2019
    [3] a hora que aconteceu duas vezes e a que nunca existiu
    [4] aritmética: somar um dia não é somar 24 horas
    [5] guardar e ler: UTC, ISO 8601 e a ordenação por texto
    [6] medir duração: relógio de parede × relógio monotônico

Uso:
    python codigo/cap18/tempo.py
    mypy --strict codigo/cap18/tempo.py
"""

import sqlite3
import time
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

SP = ZoneInfo("America/Sao_Paulo")
UTC = timezone.utc


def agora() -> datetime:
    """A única forma de pegar 'agora' neste manual (§6.2)."""
    return datetime.now(UTC)


def para_exibir(momento: datetime, fuso: ZoneInfo = SP) -> str:
    """Converte para o fuso de quem lê — só na hora de mostrar."""
    return momento.astimezone(fuso).strftime("%d/%m/%Y %H:%M")


def de_texto_brasileiro(texto: str, fuso: ZoneInfo = SP) -> datetime:
    """'15/07/2026 14:30' -> datetime consciente no fuso informado.

    `strptime` devolve SEMPRE um datetime ingênuo; o fuso é decisão de
    quem chama, e por isso ele é um parâmetro e não um valor fixo.
    """
    ingenuo = datetime.strptime(texto, "%d/%m/%Y %H:%M")
    return ingenuo.replace(tzinfo=fuso)


def cena_1_ingenuo_x_consciente() -> None:
    print("[1] INGÊNUO × CONSCIENTE")
    local = datetime.now()
    utc_ingenuo = datetime.utcnow()
    consciente = datetime.now(UTC)
    print("    datetime.now()       ", local, "· tzinfo:", local.tzinfo)
    print("    datetime.utcnow()    ", utc_ingenuo, "· tzinfo:", utc_ingenuo.tzinfo)
    print("    datetime.now(utc)    ", consciente, "· tzinfo:", consciente.tzinfo)
    print("    >>> utcnow() devolve a hora de UTC sem DIZER que é UTC")

    try:
        local < consciente
    except TypeError as erro:
        print("    comparar os dois ->", erro)
    print("    >>> a mistura falha na hora, e isso é uma sorte:")
    print("        um ingênuo marcado à mão com o fuso errado NÃO falha")
    print()


def cena_2_fuso_do_brasil() -> None:
    print("[2] O FUSO DO BRASIL, E O QUE ELE JÁ FOI")
    momento = datetime(2026, 7, 15, 14, 30, tzinfo=SP)
    print("    15/07/2026 14:30 em SP:", momento.isoformat())
    print("    o mesmo instante em UTC:", momento.astimezone(UTC).isoformat())
    print("    o mesmo instante em Tóquio:",
          momento.astimezone(ZoneInfo("Asia/Tokyo")).isoformat())

    print("    -- 15 de janeiro ao meio-dia, ano a ano --")
    for ano in (2017, 2018, 2019, 2020, 2026):
        instante = datetime(ano, 1, 15, 12, 0, tzinfo=SP)
        print("       %d -> %s" % (ano, instante.isoformat()))
    print("    >>> o Brasil teve horário de verão até 2019. Quem fixou")
    print("        '-03:00' no código erra em uma hora todo dado de verão")
    print()


def cena_3_horas_impossiveis() -> None:
    print("[3] A HORA QUE ACONTECEU DUAS VEZES")
    # 17/02/2018, 23:30: o relógio voltou de 00:00 para 23:00.
    primeira = datetime(2018, 2, 17, 23, 30, tzinfo=SP)
    segunda = primeira.replace(fold=1)
    print("    fold=0 ->", primeira.isoformat(), "· UTC", primeira.astimezone(UTC))
    print("    fold=1 ->", segunda.isoformat(), "· UTC", segunda.astimezone(UTC))
    print("    primeira == segunda?", primeira == segunda,
          "· diferença real:", segunda.timestamp() - primeira.timestamp(), "s")
    print("    num set:", len({primeira, segunda}), "elemento — um sumiu")
    print("    >>> comparados pelo RELÓGIO são iguais; pelo INSTANTE, 1h")
    print("        em UTC eles ficam distintos, e é essa a saída (§6.6)")

    print("    -- e a hora que nunca existiu --")
    # 04/11/2018: o relógio pulou de 00:00 para 01:00.
    inexistente = datetime(2018, 11, 4, 0, 30, tzinfo=SP)
    print("    04/11/2018 00:30 ->", inexistente.isoformat())
    print("    em UTC:", inexistente.astimezone(UTC).isoformat())
    print("    >>> o Python aceita sem reclamar e escolhe um instante")
    print()


def cena_4_aritmetica() -> None:
    print("[4] SOMAR UM DIA NÃO É SOMAR 24 HORAS")
    vespera = datetime(2018, 11, 3, 12, 0, tzinfo=SP)
    relogio = vespera + timedelta(days=1)
    instante = (vespera.astimezone(UTC) + timedelta(days=1)).astimezone(SP)

    print("    ponto de partida:      ", vespera.isoformat())
    print("    + timedelta(days=1):   ", relogio.isoformat())
    print("    horas REAIS decorridas:",
          (relogio.astimezone(UTC) - vespera.astimezone(UTC)))
    print("    24 horas de verdade:   ", instante.isoformat())
    print("    >>> some no fuso local para 'mesma hora amanhã';")
    print("        some em UTC para 'daqui a 24 horas'. São coisas diferentes")
    print()


def cena_5_guardar_e_ler() -> None:
    print("[5] GUARDAR E LER")
    momento = datetime(2026, 7, 15, 14, 30, tzinfo=SP)

    conexao = sqlite3.connect(":memory:")
    conexao.execute("CREATE TABLE eventos (id INTEGER PRIMARY KEY, quando TEXT)")
    conexao.execute("INSERT INTO eventos (quando) VALUES (?)",
                    (momento.astimezone(UTC).isoformat(),))
    conexao.execute("INSERT INTO eventos (quando) VALUES (?)",
                    (momento.isoformat(),))

    for identificador, texto in conexao.execute("SELECT id, quando FROM eventos"):
        lido = datetime.fromisoformat(texto)
        print("    %d: %-30s -> em SP: %s"
              % (identificador, texto, para_exibir(lido)))

    ordem = [linha[0] for linha
             in conexao.execute("SELECT id FROM eventos ORDER BY quando")]
    print("    os dois são o MESMO instante; ordenados como texto:", ordem)
    print("    >>> ISO 8601 sempre em UTC ordena certo como texto.")
    print("        Com offsets diferentes, a ordenação mente")

    print("    -- o 'Z' que o Python 3.10 não aceita --")
    for texto in ("2026-07-15T17:30:00+00:00", "2026-07-15T17:30:00Z"):
        try:
            print("       %-28r -> %s" % (texto, datetime.fromisoformat(texto)))
        except ValueError as erro:
            print("       %-28r -> ValueError: %s" % (texto, erro))
    print("       contorno: texto.replace('Z', '+00:00')")

    print("    -- data sem hora é `date`, e isso é correto --")
    nascimento = date(1990, 7, 15)
    print("       nascimento:", nascimento, "· sem hora, sem fuso")
    print()


def cena_6_medir_duracao() -> None:
    print("[6] MEDIR DURAÇÃO")
    inicio_relogio = agora()
    inicio_monotonico = time.perf_counter()
    time.sleep(0.05)
    por_relogio = (agora() - inicio_relogio).total_seconds() * 1000
    por_monotonico = (time.perf_counter() - inicio_monotonico) * 1000

    print("    com datetime.now(utc): %.1f ms" % por_relogio)
    print("    com perf_counter():    %.1f ms" % por_monotonico)
    print("    time.time() é sempre crescente? ",
          time.get_clock_info("time").monotonic)
    print("    time.monotonic() é sempre crescente?",
          time.get_clock_info("monotonic").monotonic)
    print("    >>> o relógio de parede pode andar PARA TRÁS — ajuste de NTP,")
    print("        troca de fuso, alguém mexendo no sistema. Duração medida")
    print("        com ele pode dar negativa")


def main() -> None:
    cena_1_ingenuo_x_consciente()
    cena_2_fuso_do_brasil()
    cena_3_horas_impossiveis()
    cena_4_aritmetica()
    cena_5_guardar_e_ler()
    cena_6_medir_duracao()


if __name__ == "__main__":
    main()
