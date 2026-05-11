import type { KpiCard as Kpi } from '@/lib/api';

const statusClass: Record<Kpi['status'], string> = {
  improving: 'border-emerald-500/40 bg-emerald-500/10 text-emerald-100',
  neutral: 'border-sky-500/40 bg-sky-500/10 text-sky-100',
  warning: 'border-amber-500/40 bg-amber-500/10 text-amber-100'
};

export function KpiCard({ kpi }: { kpi: Kpi }) {
  return (
    <section className={`rounded-2xl border p-5 shadow-xl ${statusClass[kpi.status]}`}>
      <p className="text-sm opacity-80">{kpi.label}</p>
      <p className="mt-3 text-3xl font-semibold tracking-tight">{kpi.value}</p>
      <p className="mt-3 text-sm leading-6 opacity-75">{kpi.helper}</p>
    </section>
  );
}
