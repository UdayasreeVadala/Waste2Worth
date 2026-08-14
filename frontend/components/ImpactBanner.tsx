"use client";

import { Cloud, Recycle, TreePine } from "lucide-react";
import { http } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useData } from "@/lib/hooks";

type ImpactSummary = {
  total_co2e_avoided_kg_gwp100?: number;
  total_methane_avoided_kg?: number;
  equivalencies?: { tree_years_equivalent?: number };
};

export function ImpactBanner() {
  const { token } = useAuth();
  const impact = useData<ImpactSummary | null>(
    () => (token ? http.get<ImpactSummary>("/impact/summary") : Promise.resolve(null)),
    [token]
  );

  if (!impact.data) return null;

  const s = impact.data;
  const co2e = Math.round(s.total_co2e_avoided_kg_gwp100 ?? 0);
  const methane = Math.round(s.total_methane_avoided_kg ?? 0);
  const trees = s.equivalencies?.tree_years_equivalent ?? 0;

  return (
    <section className="anim-reveal-up relative mb-6 overflow-hidden rounded-xl bg-mission p-5 text-white shadow-soft">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-start gap-3">
          <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-white/10 text-lime-400">
            <Recycle className="h-5 w-5" />
          </span>
          <div>
            <p className="text-xs font-medium uppercase tracking-wider text-lime-400">
              Live environmental impact
            </p>
            <p className="mt-1 max-w-lg text-sm leading-6 text-white/80">
              Waste listed on Waste2Worth is being kept out of landfill — every kilo is methane
              avoided.
            </p>
          </div>
        </div>
        <div className="grid shrink-0 grid-cols-3 gap-3">
          <Metric icon={Cloud} value={`${num(co2e)} kg`} label="CO₂e avoided" />
          <Metric icon={Recycle} value={`${num(methane)} kg`} label="Methane avoided" />
          <Metric icon={TreePine} value={`${num(trees)}`} label="Tree-years equity" />
        </div>
      </div>
    </section>
  );
}

function num(n: number | string) {
  const v = Number(n ?? 0);
  return v >= 1000 ? `${(v / 1000).toFixed(1)}k` : v.toLocaleString("en-IN");
}

function Metric({
  icon: Icon,
  value,
  label,
}: {
  icon: React.ElementType;
  value: string;
  label: string;
}) {
  return (
    <div className="rounded-lg border border-white/15 bg-forest-950/40 px-3 py-2 text-center">
      <Icon className="mx-auto h-4 w-4 text-lime-400" />
      <p className="mt-1 text-sm font-semibold text-white">{value}</p>
      <p className="text-[10px] uppercase tracking-wider text-white/55">{label}</p>
    </div>
  );
}
