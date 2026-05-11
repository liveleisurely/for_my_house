from collections.abc import Sequence
from datetime import date

from sqlalchemy import desc, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.market import DailyAiReport, DailyMarketMetric, NewsArticle, RealEstateTransaction


def upsert_transactions(db: Session, rows: Sequence[dict]) -> int:
    if not rows:
        return 0
    stmt = insert(RealEstateTransaction).values(list(rows))
    update_columns = {
        "raw_payload": stmt.excluded.raw_payload,
        "observed_at": stmt.excluded.observed_at,
    }
    db.execute(stmt.on_conflict_do_update(index_elements=["source_hash"], set_=update_columns))
    return len(rows)


def upsert_news_articles(db: Session, rows: Sequence[dict]) -> int:
    if not rows:
        return 0
    stmt = insert(NewsArticle).values(list(rows))
    db.execute(
        stmt.on_conflict_do_update(
            index_elements=["source_hash"],
            set_={
                "title": stmt.excluded.title,
                "snippet": stmt.excluded.snippet,
                "published_at": stmt.excluded.published_at,
            },
        )
    )
    return len(rows)


def list_latest_metrics(db: Session, limit: int = 8) -> list[DailyMarketMetric]:
    stmt = select(DailyMarketMetric).order_by(desc(DailyMarketMetric.metric_date)).limit(limit)
    return list(db.scalars(stmt))


def list_latest_transactions(db: Session, limit: int = 50) -> list[RealEstateTransaction]:
    stmt = (
        select(RealEstateTransaction)
        .order_by(desc(RealEstateTransaction.contract_date))
        .limit(limit)
    )
    return list(db.scalars(stmt))


def list_latest_news(db: Session, limit: int = 10) -> list[NewsArticle]:
    stmt = select(NewsArticle).order_by(desc(NewsArticle.published_at)).limit(limit)
    return list(db.scalars(stmt))


def get_daily_report(
    db: Session, target_asset_name: str, report_date: date
) -> DailyAiReport | None:
    stmt = select(DailyAiReport).where(
        DailyAiReport.target_asset_name == target_asset_name,
        DailyAiReport.report_date == report_date,
    )
    return db.scalar(stmt)
