"""A política de tempo do projeto (04.18 / D-029)."""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

SP = ZoneInfo("America/Sao_Paulo")
UTC = timezone.utc


def agora() -> datetime:
    """A única forma de obter o instante atual neste projeto."""
    return datetime.now(UTC)


def para_exibir(momento: datetime, fuso: ZoneInfo = SP) -> str:
    return momento.astimezone(fuso).strftime("%d/%m/%Y %H:%M:%S")
