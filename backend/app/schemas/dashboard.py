from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class KpiCard(BaseModel):
    label: str
    value: str
    status: str = Field(description="one of: improving, neutral, warning")
    helper: str


class MarketMetricOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    metric_date: date
    region_key: str
    apartment_name: str | None
    area_bucket: str
    avg_sale_price_krw: int | None
    median_sale_price_krw: int | None
    avg_jeonse_price_krw: int | None
    jeonse_ratio: Decimal | None
    transaction_count: int
    high_price_krw: int | None
    low_price_krw: int | None
    price_change_30d: Decimal | None
    price_change_90d: Decimal | None


class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    trade_type: str
    apartment_name: str
    legal_dong_name: str | None
    contract_date: date
    area_m2: Decimal
    floor: int | None
    price_krw: int | None
    deposit_krw: int | None
    monthly_rent_krw: int | None


class NewsArticleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    provider: str
    title: str
    url: str
    published_at: datetime | None
    snippet: str | None
    query: str
    relevance_score: Decimal | None
    sentiment: str | None
    summary: str | None


class DailyReportOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    report_date: date
    target_asset_name: str
    summary: str
    positive_factors: list[str]
    negative_factors: list[str]
    watch_points: list[str]
    confidence_level: str
    data_quality_notes: list[str]


class DashboardSummary(BaseModel):
    generated_at: datetime
    target_asset_name: str
    kpis: list[KpiCard]
    latest_metrics: list[MarketMetricOut]
    latest_news: list[NewsArticleOut]
    daily_report: DailyReportOut | None
