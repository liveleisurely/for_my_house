import type { KpiCard as Kpi } from '@/lib/api';

const statusClass: Record<Kpi['status'], string> = {
  improving: 'border-emerald-200 bg-emerald-50 text-emerald-950 shadow-emerald-100/70',
  neutral: 'border-sky-200 bg-sky-50 text-sky-950 shadow-sky-100/70',
  warning: 'border-amber-200 bg-amber-50 text-amber-950 shadow-amber-100/70'
};

export function KpiCard({ kpi }: { kpi: Kpi }) {
  return (
    <section className={`rounded-2xl border p-5 shadow-sm ${statusClass[kpi.status]}`}>
      <p className="text-sm font-medium opacity-75">{kpi.label}</p>
      <p className="mt-3 text-3xl font-bold tracking-tight">{kpi.value}</p>
      <p className="mt-3 text-sm leading-6 opacity-75">{kpi.helper}</p>
    </section>
  );
}
