import hashlib
from datetime import date
from decimal import Decimal
from typing import Any


def parse_korean_money_to_krw(value: str | int | None) -> int | None:
    """Convert MOLIT-style amount strings in ten-thousand KRW units to KRW.

    The open APIs commonly return strings such as "73,500" meaning 735,000,000 KRW.
    """

    if value is None:
        return None
    if isinstance(value, int):
        return value * 10_000
    cleaned = value.replace(",", "").strip()
    if cleaned == "":
        return None
    return int(cleaned) * 10_000


def area_bucket(area_m2: Decimal | float | str) -> str:
    area = Decimal(str(area_m2))
    if area < Decimal("65"):
        return "59"
    if area < Decimal("80"):
        return "74"
    if area < Decimal("95"):
        return "84"
    return "95+"


def source_hash(parts: list[Any]) -> str:
    canonical = "|".join("" if part is None else str(part).strip() for part in parts)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def contract_date_from_parts(year_month: str, day: str | int) -> date:
    year = int(year_month[:4])
    month = int(year_month[4:6])
    return date(year, month, int(day))
