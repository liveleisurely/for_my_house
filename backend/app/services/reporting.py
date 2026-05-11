from datetime import UTC, date, datetime

from sqlalchemy.orm import Session

from app.models.market import DailyAiReport, DailyMarketMetric, NewsArticle


def build_kpis(metrics: list[DailyMarketMetric], news: list[NewsArticle]) -> list[dict[str, str]]:
    transaction_count = sum(metric.transaction_count for metric in metrics)
    latest_jeonse = next((metric.jeonse_ratio for metric in metrics if metric.jeonse_ratio), None)
    official_news_count = sum(
        1 for article in news if "국토" in article.title or "김포" in article.title
    )
    return [
        {
            "label": "최근 거래 표본",
            "value": f"{transaction_count}건",
            "status": "warning" if transaction_count < 3 else "neutral",
            "helper": "표본이 3건 미만이면 가격 신뢰도를 낮게 봅니다.",
        },
        {
            "label": "전세가율",
            "value": "확인 필요" if latest_jeonse is None else f"{float(latest_jeonse) * 100:.1f}%",
            "status": "warning" if latest_jeonse is None else "neutral",
            "helper": "입주장 리스크 판단의 핵심 지표입니다.",
        },
        {
            "label": "교통/지역 뉴스",
            "value": f"{official_news_count}건",
            "status": "improving" if official_news_count > 0 else "neutral",
            "helper": "5호선·김포 정책성 키워드가 포함된 최신 기사 수입니다.",
        },
    ]


def generate_rule_based_report(
    db: Session,
    *,
    target_asset_name: str,
    report_date: date,
    metrics: list[DailyMarketMetric],
    news: list[NewsArticle],
) -> DailyAiReport:
    """Create a deterministic MVP report.

    This intentionally avoids speculative price prediction. A future LLM implementation should take
    this deterministic report as grounded context, not replace the calculations.
    """

    transaction_count = sum(metric.transaction_count for metric in metrics)
    data_quality_notes: list[str] = []
    if transaction_count < 3:
        data_quality_notes.append("최근 거래 표본이 적어 평균가와 변동률 신뢰도가 낮습니다.")
    if not any(metric.jeonse_ratio for metric in metrics):
        data_quality_notes.append("전세가율 산출에 필요한 매매/전세 짝 데이터가 부족합니다.")

    report = DailyAiReport(
        report_date=report_date,
        target_asset_name=target_asset_name,
        summary=(
            "오늘 리포트는 실거래·전세·뉴스 원천 데이터를 기반으로 한 리스크 "
            "모니터링 요약입니다. 현재 MVP는 가격 예측을 하지 않고, 표본 수와 "
            "전세 방어력 및 5호선 관련 이벤트 확인에 집중합니다."
        ),
        positive_factors=[
            "5호선·김포권 키워드 뉴스를 지속 추적할 수 있는 자동화 기반을 마련했습니다."
        ],
        negative_factors=[
            "분양권 및 주변 실거래 표본이 부족한 날에는 가격 판단을 보수적으로 봐야 합니다."
        ],
        watch_points=[
            "풍무동 74/84㎡ 실거래",
            "주변 신축 전세가율",
            "5호선 공식 보도자료",
            "입주장 전세 물량",
        ],
        confidence_level="low" if data_quality_notes else "medium",
        data_quality_notes=data_quality_notes or ["필수 데이터 품질 경고는 없습니다."],
        model_name="rule-based-mvp",
        prompt_version="v1",
    )
    db.add(report)
    return report


def now_utc() -> datetime:
    return datetime.now(UTC)
