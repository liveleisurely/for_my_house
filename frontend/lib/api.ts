export type KpiCard = {
  label: string;
  value: string;
  status: 'improving' | 'neutral' | 'warning';
  helper: string;
};

export type MarketMetric = {
  metric_date: string;
  region_key: string;
  apartment_name: string | null;
  area_bucket: string;
  avg_sale_price_krw: number | null;
  median_sale_price_krw: number | null;
  avg_jeonse_price_krw: number | null;
  jeonse_ratio: string | null;
  transaction_count: number;
  high_price_krw: number | null;
  low_price_krw: number | null;
  price_change_30d: string | null;
  price_change_90d: string | null;
};

export type NewsArticle = {
  id: number;
  provider: string;
  title: string;
  url: string;
  published_at: string | null;
  snippet: string | null;
  query: string;
  relevance_score: string | null;
  sentiment: string | null;
  summary: string | null;
};

export type DailyReport = {
  report_date: string;
  target_asset_name: string;
  summary: string;
  positive_factors: string[];
  negative_factors: string[];
  watch_points: string[];
  confidence_level: string;
  data_quality_notes: string[];
};

export type DashboardSummary = {
  generated_at: string;
  target_asset_name: string;
  kpis: KpiCard[];
  latest_metrics: MarketMetric[];
  latest_news: NewsArticle[];
  daily_report: DailyReport | null;
};

const fallbackSummary: DashboardSummary = {
  generated_at: new Date().toISOString(),
  target_asset_name: '풍무 해링턴 74A',
  kpis: [
    {
      label: '최근 거래 표본',
      value: '수집 전',
      status: 'warning',
      helper: '공공데이터포털 API 키 연결 후 자동 갱신됩니다.'
    },
    {
      label: '전세가율',
      value: '확인 필요',
      status: 'warning',
      helper: '입주장 리스크 판단을 위해 전세 데이터를 먼저 확보합니다.'
    },
    {
      label: '5호선 이벤트',
      value: '모니터링',
      status: 'neutral',
      helper: '공식 보도자료와 뉴스 검색 결과를 분리해서 추적합니다.'
    }
  ],
  latest_metrics: [],
  latest_news: [],
  daily_report: {
    report_date: new Date().toISOString().slice(0, 10),
    target_asset_name: '풍무 해링턴 74A',
    summary: '백엔드 또는 원천 API 연결 전 상태입니다. 현재 화면은 MVP 기본 설계와 리스크 지표 구성을 보여줍니다.',
    positive_factors: ['실거래, 전세, 뉴스, AI 리포트를 분리한 운영 구조로 시작합니다.'],
    negative_factors: ['원천 데이터 적재 전까지 가격 판단은 할 수 없습니다.'],
    watch_points: ['풍무동 74/84㎡ 실거래', '주변 전세가율', '5호선 공식 일정', '입주장 물량'],
    confidence_level: 'low',
    data_quality_notes: ['아직 수집된 DB 데이터가 없습니다.']
  }
};

export async function getDashboardSummary(): Promise<DashboardSummary> {
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://backend:8000';
  try {
    const response = await fetch(`${baseUrl}/api/dashboard/summary`, {
      next: { revalidate: 60 }
    });
    if (!response.ok) return fallbackSummary;
    return (await response.json()) as DashboardSummary;
  } catch {
    return fallbackSummary;
  }
}

export function formatKrw(value: number | null): string {
  if (value === null) return '-';
  const eok = value / 100_000_000;
  return `${eok.toFixed(2)}억`;
}
