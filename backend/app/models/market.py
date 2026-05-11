from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Any

from sqlalchemy import Date, DateTime, Enum, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class TradeType(StrEnum):
    SALE = "sale"
    JEONSE = "jeonse"
    MONTHLY_RENT = "monthly_rent"
    PRE_SALE_RIGHT = "pre_sale_right"


class Apartment(Base):
    __tablename__ = "apartments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    city: Mapped[str] = mapped_column(String(80), index=True)
    district: Mapped[str] = mapped_column(String(80), index=True)
    dong: Mapped[str] = mapped_column(String(80), index=True)
    road_address: Mapped[str | None] = mapped_column(String(300))
    jibun_address: Mapped[str | None] = mapped_column(String(300))
    completion_year: Mapped[int | None] = mapped_column(Integer)
    total_households: Mapped[int | None] = mapped_column(Integer)
    lat: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    lng: Mapped[Decimal | None] = mapped_column(Numeric(10, 7))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class RealEstateTransaction(Base):
    __tablename__ = "real_estate_transactions"
    __table_args__ = (
        UniqueConstraint("source_hash", name="uq_real_estate_transactions_source_hash"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String(80), default="molit")
    trade_type: Mapped[TradeType] = mapped_column(Enum(TradeType, name="trade_type"), index=True)
    apartment_name: Mapped[str] = mapped_column(String(200), index=True)
    legal_dong_code: Mapped[str] = mapped_column(String(10), index=True)
    legal_dong_name: Mapped[str | None] = mapped_column(String(120), index=True)
    contract_date: Mapped[date] = mapped_column(Date, index=True)
    area_m2: Mapped[Decimal] = mapped_column(Numeric(8, 3), index=True)
    floor: Mapped[int | None] = mapped_column(Integer)
    price_krw: Mapped[int | None] = mapped_column(Integer)
    deposit_krw: Mapped[int | None] = mapped_column(Integer)
    monthly_rent_krw: Mapped[int | None] = mapped_column(Integer)
    built_year: Mapped[int | None] = mapped_column(Integer)
    raw_payload: Mapped[dict[str, Any]] = mapped_column(JSONB)
    source_hash: Mapped[str] = mapped_column(String(64), index=True)
    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class DailyMarketMetric(Base):
    __tablename__ = "daily_market_metrics"
    __table_args__ = (
        UniqueConstraint(
            "metric_date",
            "region_key",
            "apartment_name",
            "area_bucket",
            name="uq_daily_market_metrics_natural_key",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    metric_date: Mapped[date] = mapped_column(Date, index=True)
    region_key: Mapped[str] = mapped_column(String(80), index=True)
    apartment_name: Mapped[str | None] = mapped_column(String(200), index=True)
    area_bucket: Mapped[str] = mapped_column(String(20), index=True)
    avg_sale_price_krw: Mapped[int | None] = mapped_column(Integer)
    median_sale_price_krw: Mapped[int | None] = mapped_column(Integer)
    avg_jeonse_price_krw: Mapped[int | None] = mapped_column(Integer)
    jeonse_ratio: Mapped[Decimal | None] = mapped_column(Numeric(6, 4))
    transaction_count: Mapped[int] = mapped_column(Integer, default=0)
    high_price_krw: Mapped[int | None] = mapped_column(Integer)
    low_price_krw: Mapped[int | None] = mapped_column(Integer)
    price_change_30d: Mapped[Decimal | None] = mapped_column(Numeric(8, 4))
    price_change_90d: Mapped[Decimal | None] = mapped_column(Numeric(8, 4))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class NewsArticle(Base):
    __tablename__ = "news_articles"
    __table_args__ = (UniqueConstraint("source_hash", name="uq_news_articles_source_hash"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    provider: Mapped[str] = mapped_column(String(80), index=True)
    title: Mapped[str] = mapped_column(String(500))
    url: Mapped[str] = mapped_column(String(1000))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    snippet: Mapped[str | None] = mapped_column(Text)
    query: Mapped[str] = mapped_column(String(200), index=True)
    relevance_score: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    sentiment: Mapped[str | None] = mapped_column(String(20))
    summary: Mapped[str | None] = mapped_column(Text)
    source_hash: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class DailyAiReport(Base):
    __tablename__ = "daily_ai_reports"
    __table_args__ = (
        UniqueConstraint("report_date", "target_asset_name", name="uq_daily_ai_reports_target"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    report_date: Mapped[date] = mapped_column(Date, index=True)
    target_asset_name: Mapped[str] = mapped_column(String(200), index=True)
    summary: Mapped[str] = mapped_column(Text)
    positive_factors: Mapped[list[str]] = mapped_column(JSONB)
    negative_factors: Mapped[list[str]] = mapped_column(JSONB)
    watch_points: Mapped[list[str]] = mapped_column(JSONB)
    confidence_level: Mapped[str] = mapped_column(String(20))
    data_quality_notes: Mapped[list[str]] = mapped_column(JSONB)
    model_name: Mapped[str] = mapped_column(String(100), default="rule-based-mvp")
    prompt_version: Mapped[str] = mapped_column(String(50), default="v1")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
