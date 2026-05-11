import { KpiCard } from '@/components/KpiCard';
import { ReportPanel } from '@/components/ReportPanel';
import { formatKrw, getDashboardSummary } from '@/lib/api';

export const dynamic = 'force-dynamic';

export default async function DashboardPage() {
  const summary = await getDashboardSummary();
  return (
    <main className="min-h-screen px-6 py-8 text-slate-950 md:px-10">
      <header className="mx-auto max-w-7xl">
        <p className="text-sm font-semibold text-sky-700">Real Estate Risk Operations</p>
        <div className="mt-3 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <h1 className="text-4xl font-black tracking-tight text-slate-950 md:text-5xl">풍무 해링턴 74A 모니터링</h1>
            <p className="mt-4 max-w-3xl text-slate-600">
              가격 예측이 아니라 실거래, 전세, 5호선 이벤트, 뉴스 흐름을 매일 점검하는 리스크 대시보드입니다.
            </p>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-700 shadow-sm">
            생성 시각: {new Date(summary.generated_at).toLocaleString('ko-KR')}
          </div>
        </div>
      </header>

      <section className="mx-auto mt-8 grid max-w-7xl gap-4 md:grid-cols-3">
        {summary.kpis.map((kpi) => (
          <KpiCard key={kpi.label} kpi={kpi} />
        ))}
      </section>

      <section className="mx-auto mt-8 max-w-7xl">
        <ReportPanel report={summary.daily_report} />
      </section>

      <section className="mx-auto mt-8 grid max-w-7xl gap-6 lg:grid-cols-[1.4fr_1fr]">
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
            <h2 className="text-xl font-bold text-slate-950">최근 시장 지표</h2>
            <p className="text-sm text-slate-500">로컬 데모 데이터 또는 수집 배치 결과</p>
          </div>
          <div className="mt-5 overflow-hidden rounded-2xl border border-slate-200">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50 text-slate-700">
                <tr>
                  <th className="px-4 py-3">일자</th>
                  <th className="px-4 py-3">지역</th>
                  <th className="px-4 py-3">면적</th>
                  <th className="px-4 py-3">중위 매매</th>
                  <th className="px-4 py-3">전세가율</th>
                  <th className="px-4 py-3">거래</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {summary.latest_metrics.length === 0 ? (
                  <tr>
                    <td className="px-4 py-8 text-center text-slate-500" colSpan={6}>
                      수집된 지표가 없습니다. 로컬에서는 <code>POST /api/dev/seed-demo</code> 또는 <code>SEED_DEMO_DATA=true</code>로 샘플을 적재하세요.
                    </td>
                  </tr>
                ) : (
                  summary.latest_metrics.map((metric) => (
                    <tr key={`${metric.metric_date}-${metric.region_key}-${metric.area_bucket}`} className="hover:bg-slate-50">
                      <td className="px-4 py-3">{metric.metric_date}</td>
                      <td className="px-4 py-3">{metric.region_key}</td>
                      <td className="px-4 py-3">{metric.area_bucket}</td>
                      <td className="px-4 py-3 font-semibold text-slate-900">{formatKrw(metric.median_sale_price_krw)}</td>
                      <td className="px-4 py-3">{metric.jeonse_ratio ? `${(Number(metric.jeonse_ratio) * 100).toFixed(1)}%` : '-'}</td>
                      <td className="px-4 py-3">{metric.transaction_count}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-bold text-slate-950">관련 뉴스</h2>
          <div className="mt-5 space-y-3">
            {summary.latest_news.length === 0 ? (
              <p className="rounded-2xl border border-slate-200 bg-slate-50 p-5 text-sm text-slate-500">아직 수집된 뉴스가 없습니다.</p>
            ) : (
              summary.latest_news.map((article) => (
                <a key={article.id} href={article.url} className="block rounded-2xl border border-slate-200 bg-white p-4 shadow-sm transition hover:border-sky-200 hover:bg-sky-50/50">
                  <p className="text-sm font-semibold text-slate-950">{article.title}</p>
                  <p className="mt-2 line-clamp-2 text-sm text-slate-600">{article.snippet}</p>
                </a>
              ))
            )}
          </div>
        </div>
      </section>
    </main>
  );
}
