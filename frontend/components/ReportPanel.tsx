import type { DailyReport } from '@/lib/api';

function FactorList({ title, items }: { title: string; items: string[] }) {
  return (
    <div>
      <h3 className="text-sm font-semibold text-slate-300">{title}</h3>
      <ul className="mt-3 space-y-2 text-sm text-slate-400">
        {items.map((item) => (
          <li key={item} className="rounded-lg bg-white/5 px-3 py-2">{item}</li>
        ))}
      </ul>
    </div>
  );
}

export function ReportPanel({ report }: { report: DailyReport | null }) {
  if (!report) return null;
  return (
    <section className="rounded-3xl border border-white/10 bg-white/[0.04] p-6 shadow-2xl">
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm text-slate-400">오늘의 AI/룰 기반 브리핑</p>
          <h2 className="mt-1 text-2xl font-bold">{report.target_asset_name}</h2>
        </div>
        <span className="rounded-full border border-white/10 px-3 py-1 text-sm text-slate-300">
          신뢰도: {report.confidence_level}
        </span>
      </div>
      <p className="mt-5 leading-7 text-slate-300">{report.summary}</p>
      <div className="mt-6 grid gap-5 md:grid-cols-3">
        <FactorList title="긍정 요인" items={report.positive_factors} />
        <FactorList title="부정 요인" items={report.negative_factors} />
        <FactorList title="관찰 포인트" items={report.watch_points} />
      </div>
      <div className="mt-6 rounded-2xl bg-amber-500/10 p-4 text-sm text-amber-100">
        <strong>데이터 품질:</strong> {report.data_quality_notes.join(' / ')}
      </div>
    </section>
  );
}
