from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.market import (
    DailyAiReport,
    DailyMarketMetric,
    NewsArticle,
    RealEstateTransaction,
    TradeType,
)
from app.services.normalization import stable_hash

TARGET_ASSET_NAME = "풍무 해링턴 74A"


def _upsert_metric(db: Session, row: dict) -> None:
    stmt = select(DailyMarketMetric).where(
        DailyMarketMetric.metric_date == row["metric_date"],
        DailyMarketMetric.region_key == row["region_key"],
        DailyMarketMetric.apartment_name == row["apartment_name"],
        DailyMarketMetric.area_bucket == row["area_bucket"],
    )
    existing = db.scalar(stmt)
    if existing is None:
        db.add(DailyMarketMetric(**row))
        return
    for key, value in row.items():
        setattr(existing, key, value)


def _upsert_news(db: Session, row: dict) -> None:
    existing = db.scalar(select(NewsArticle).where(NewsArticle.source_hash == row["source_hash"]))
    if existing is None:
        db.add(NewsArticle(**row))
        return
    for key, value in row.items():
        setattr(existing, key, value)


def _upsert_transaction(db: Session, row: dict) -> None:
    existing = db.scalar(
        select(RealEstateTransaction).where(
            RealEstateTransaction.source_hash == row["source_hash"]
        )
    )
    if existing is None:
        db.add(RealEstateTransaction(**row))
        return
    for key, value in row.items():
        setattr(existing, key, value)


def seed_demo_data(db: Session) -> dict[str, int]:
    """Insert deterministic local demo data for first-run UI verification.

    The rows are intentionally labelled as demo/source synthetic. They are not investment data and
    must not be mixed with production ingestion without an explicit source filter.
    """

    today = date.today()
    metrics = [
        {
            "metric_date": today,
            "region_key": "김포시 풍무동",
            "apartment_name": TARGET_ASSET_NAME,
            "area_bucket": "74A",
            "avg_sale_price_krw": 705_000_000,
            "median_sale_price_krw": 700_000_000,
            "avg_jeonse_price_krw": 430_000_000,
            "jeonse_ratio": Decimal("0.6143"),
            "transaction_count": 3,
            "high_price_krw": 720_000_000,
            "low_price_krw": 690_000_000,
            "price_change_30d": Decimal("0.0145"),
            "price_change_90d": Decimal("0.0280"),
        },
        {
            "metric_date": today - timedelta(days=1),
            "region_key": "김포시 풍무동",
            "apartment_name": "풍무역 푸르지오",
            "area_bucket": "84",
            "avg_sale_price_krw": 755_000_000,
            "median_sale_price_krw": 750_000_000,
            "avg_jeonse_price_krw": 465_000_000,
            "jeonse_ratio": Decimal("0.6200"),
            "transaction_count": 5,
            "high_price_krw": 780_000_000,
            "low_price_krw": 730_000_000,
            "price_change_30d": Decimal("0.0068"),
            "price_change_90d": Decimal("0.0180"),
        },
        {
            "metric_date": today - timedelta(days=2),
            "region_key": "인천 서구 검단",
            "apartment_name": "검단 신축 비교군",
            "area_bucket": "84",
            "avg_sale_price_krw": 690_000_000,
            "median_sale_price_krw": 685_000_000,
            "avg_jeonse_price_krw": 400_000_000,
            "jeonse_ratio": Decimal("0.5839"),
            "transaction_count": 4,
            "high_price_krw": 705_000_000,
            "low_price_krw": 665_000_000,
            "price_change_30d": Decimal("-0.0040"),
            "price_change_90d": Decimal("0.0095"),
        },
    ]

    published_at = datetime.now(UTC).replace(microsecond=0)
    news = [
        {
            "provider": "demo",
            "title": "[데모] 김포 5호선 연장 공식 일정 모니터링 필요",
            "url": "https://example.com/demo/gimpo-line5",
            "published_at": published_at,
            "snippet": (
                "실제 뉴스 수집 전 화면 검증용 데모 기사입니다. "
                "운영에서는 네이버 뉴스 API와 공식 보도자료를 분리 저장합니다."
            ),
            "query": "김포 5호선 연장",
            "relevance_score": Decimal("0.95"),
            "sentiment": "neutral",
            "summary": "5호선 이벤트는 보도자료와 언론 보도를 구분해서 추적해야 합니다.",
            "source_hash": stable_hash("demo", "news", "gimpo-line5"),
        },
        {
            "provider": "demo",
            "title": "[데모] 풍무동 전세가율과 입주장 리스크 체크",
            "url": "https://example.com/demo/pungmu-jeonse",
            "published_at": published_at - timedelta(hours=3),
            "snippet": (
                "전세가율, 전세 거래량, 주변 신축 입주 물량을 함께 확인하는 "
                "화면 검증용 데이터입니다."
            ),
            "query": "풍무동 전세",
            "relevance_score": Decimal("0.88"),
            "sentiment": "warning",
            "summary": "입주장에는 전세 방어력을 별도 KPI로 추적하는 편이 안전합니다.",
            "source_hash": stable_hash("demo", "news", "pungmu-jeonse"),
        },
    ]

    transactions = [
        {
            "source": "demo",
            "trade_type": TradeType.PRE_SALE_RIGHT,
            "apartment_name": TARGET_ASSET_NAME,
            "legal_dong_code": "41570101",
            "legal_dong_name": "풍무동",
            "contract_date": today - timedelta(days=7),
            "area_m2": Decimal("74.900"),
            "floor": 12,
            "price_krw": 700_000_000,
            "deposit_krw": None,
            "monthly_rent_krw": None,
            "built_year": None,
            "raw_payload": {"source": "local-demo", "notice": "not-real-transaction"},
            "source_hash": stable_hash("demo", "transaction", TARGET_ASSET_NAME, "74A", "1"),
        },
        {
            "source": "demo",
            "trade_type": TradeType.JEONSE,
            "apartment_name": TARGET_ASSET_NAME,
            "legal_dong_code": "41570101",
            "legal_dong_name": "풍무동",
            "contract_date": today - timedelta(days=5),
            "area_m2": Decimal("74.900"),
            "floor": 9,
            "price_krw": None,
            "deposit_krw": 430_000_000,
            "monthly_rent_krw": None,
            "built_year": None,
            "raw_payload": {"source": "local-demo", "notice": "not-real-transaction"},
            "source_hash": stable_hash("demo", "transaction", TARGET_ASSET_NAME, "74A", "jeonse"),
        },
    ]

    for metric in metrics:
        _upsert_metric(db, metric)
    for article in news:
        _upsert_news(db, article)
    for transaction in transactions:
        _upsert_transaction(db, transaction)

    stale_report = db.scalar(
        select(DailyAiReport).where(
            DailyAiReport.report_date == today,
            DailyAiReport.target_asset_name == TARGET_ASSET_NAME,
            DailyAiReport.model_name == "rule-based-mvp",
        )
    )
    if stale_report is not None:
        db.delete(stale_report)

    db.commit()
    return {"metrics": len(metrics), "news": len(news), "transactions": len(transactions)}
