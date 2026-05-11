from datetime import date
from decimal import Decimal

from app.services.normalization import (
    area_bucket,
    contract_date_from_parts,
    parse_korean_money_to_krw,
)


def test_parse_korean_money_to_krw() -> None:
    assert parse_korean_money_to_krw("73,500") == 735_000_000
    assert parse_korean_money_to_krw(10) == 100_000
    assert parse_korean_money_to_krw("") is None


def test_area_bucket() -> None:
    assert area_bucket(Decimal("59.98")) == "59"
    assert area_bucket("74.91") == "74"
    assert area_bucket("84.98") == "84"
    assert area_bucket("101.2") == "95+"


def test_contract_date_from_parts() -> None:
    assert contract_date_from_parts("202605", "11") == date(2026, 5, 11)
