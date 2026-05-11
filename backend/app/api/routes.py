from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.dashboard import DashboardSummary, NewsArticleOut, TransactionOut
from app.services.reporting import build_kpis, generate_rule_based_report, now_utc
from app.services.repositories import (
    get_daily_report,
    list_latest_metrics,
    list_latest_news,
    list_latest_transactions,
)

router = APIRouter()
DEFAULT_TARGET_ASSET = "풍무 해링턴 74A"
DbSession = Annotated[Session, Depends(get_db)]


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/dashboard/summary", response_model=DashboardSummary)
def dashboard_summary(
    db: DbSession,
    target_asset_name: Annotated[str, Query()] = DEFAULT_TARGET_ASSET,
) -> DashboardSummary:
    metrics = list_latest_metrics(db)
    news = list_latest_news(db)
    today = date.today()
    report = get_daily_report(db, target_asset_name, today)
    if report is None:
        report = generate_rule_based_report(
            db,
            target_asset_name=target_asset_name,
            report_date=today,
            metrics=metrics,
            news=news,
        )
        db.commit()
        db.refresh(report)
    return DashboardSummary(
        generated_at=now_utc(),
        target_asset_name=target_asset_name,
        kpis=build_kpis(metrics, news),
        latest_metrics=metrics,
        latest_news=news,
        daily_report=report,
    )


@router.get("/transactions", response_model=list[TransactionOut])
def transactions(db: DbSession, limit: Annotated[int, Query(ge=1, le=200)] = 50):
    return list_latest_transactions(db, limit=limit)


@router.get("/news", response_model=list[NewsArticleOut])
def news(db: DbSession, limit: Annotated[int, Query(ge=1, le=100)] = 20):
    return list_latest_news(db, limit=limit)
