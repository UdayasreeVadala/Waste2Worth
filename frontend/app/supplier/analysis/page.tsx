"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Bot, Sparkles } from "lucide-react";
import { Shell } from "@/components/Shell";
import { Button, Card, EmptyState, Field, Input, Spinner, StatusPill } from "@/components/ui";
import { http } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useData } from "@/lib/hooks";
import { money, num, statusLabel } from "@/lib/format";

function AnalysisInner() {
  const params = useSearchParams();
  const router = useRouter();
  const wasteId = params.get("waste");
  const { token } = useAuth();
  const { data, loading, error } = useData<any>(
    () =>
      token && wasteId
        ? http.get(`/waste/${wasteId}/analysis`)
        : Promise.resolve(null),
    [token, wasteId]
  );
  const [busy, setBusy] = useState(false);
  const [min, setMin] = useState<number>(0);
  const [pickup, setPickup] = useState(true);
  const [counter, setCounter] = useState(true);

  if (!wasteId) {
    return (
      <Shell>
        <EmptyState
          title="No waste selected"
          message="Open a listing and choose Analyze & match."
        />
      </Shell>
    );
  }
  if (loading) {
    return (
      <Shell>
        <Spinner />
      </Shell>
    );
  }
  if (error) {
    return (
      <Shell>
        <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800">
          {error}
        </div>
      </Shell>
    );
  }
  if (!data) {
    return (
      <Shell>
        <Spinner />
      </Shell>
    );
  }

  const best = data.best_buyer;

  async function runAgent() {
    if (!best) return;
    setBusy(true);
    try {
      await http.post<any>("/agent/contact", {
        waste_id: Number(wasteId),
        buyer_id: Number(best.buyer_id),
        minimum_total_price: min || best.estimated_margin?.estimated_supplier_earnings || 0,
        requires_pickup: pickup,
        allow_counter_offer: counter,
      });
      router.push("/supplier/matches");
    } catch (e) {
      alert(e instanceof Error ? e.message : "Agent failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <Shell>
      <h1 className="mb-1 text-2xl font-semibold text-forest-900">AI analysis</h1>
      <p className="mb-6 text-sm text-ink-muted">Waste #{wasteId}</p>
      {data.error && (
        <div className="mb-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800">
          {data.error.message || "Analysis failed"}
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-2">
        <Card title="Recommended use">
          {data.recommended_use ? (
            <div>
              <p className="text-lg font-semibold text-ink">
                {data.recommended_use.recommended_label}
              </p>
              <p className="mt-1 text-sm text-ink-muted">
                Route: {data.recommended_use.recommended_route}
              </p>
              <p className="mt-2 text-sm text-ink">{data.recommended_use.reason}</p>
              {data.recommended_use.route_scores && (
                <pre className="mt-3 max-h-48 overflow-auto rounded-lg bg-parchment p-3 text-xs">
                  {JSON.stringify(data.recommended_use.route_scores, null, 2)}
                </pre>
              )}
            </div>
          ) : (
            <p className="text-sm text-ink-muted">—</p>
          )}
          {data.analysis && (
            <pre className="mt-3 max-h-72 overflow-auto rounded-lg bg-parchment p-3 text-xs">
              {JSON.stringify(data.analysis, null, 2)}
            </pre>
          )}
        </Card>
        <Card title="Best buyer">
          {best ? (
            <div>
              <p className="text-lg font-semibold text-ink">{best.name}</p>
              <p className="text-sm capitalize text-ink-muted">
                {best.business_type} · {best.distance_km?.toFixed?.(1)} km
              </p>
              <p className="mt-2 text-sm text-ink">{best.explanation}</p>
              <div className="mt-3 flex flex-wrap gap-4 text-sm">
                <span>
                  Offer: <strong>{money(best.estimated_margin?.buyer_offer, best.currency)}</strong>
                </span>
                <span>
                  Your earning:{" "}
                  <strong>{money(best.estimated_margin?.estimated_supplier_earnings, best.currency)}</strong>
                </span>
              </div>
              <p className="mt-2 text-xs text-ink-muted">
                Agent needs approval: {String(data.requires_supplier_approval)} · Status:{" "}
                {statusLabel(data.agent_status)}
              </p>
            </div>
          ) : (
            <p className="text-sm text-ink-muted">No suitable buyer found.</p>
          )}
        </Card>
      </div>

      {data.ranked_buyers?.length > 0 && (
        <Card title="Ranked buyers" className="mt-6">
          <ul className="divide-y divide-ink/10">
            {data.ranked_buyers.map((b: any) => (
              <li key={b.buyer_id} className="flex items-center justify-between py-2 text-sm">
                <span>
                  {b.name}{" "}
                  <span className="text-ink-muted">— {b.distance_km?.toFixed?.(1)} km</span>
                </span>
                <span className="font-medium text-forest-900">
                  {money(b.estimated_margin?.estimated_supplier_earnings, b.currency)}
                </span>
              </li>
            ))}
          </ul>
        </Card>
      )}

      {best && (
        <div className="mt-6 rounded-xl border border-forest-900/20 bg-moss-50 p-5">
          <h3 className="font-semibold text-ink">Run the AI agent</h3>
          <p className="mt-1 text-sm text-ink-muted">
            The agent will contact {best.name} and negotiate within your limits.
          </p>
          <div className="mt-4 grid gap-4 sm:grid-cols-3">
            <Field label="Minimum total price">
              <Input type="number" value={min} onChange={(e) => setMin(Number(e.target.value))} />
            </Field>
            <label className="flex items-center gap-2 text-sm text-ink">
              Pickup included
              <input type="checkbox" checked={pickup} onChange={(e) => setPickup(e.target.checked)} />
            </label>
            <label className="flex items-center gap-2 text-sm text-ink">
              Allow counter-offer
              <input
                type="checkbox"
                checked={counter}
                onChange={(e) => setCounter(e.target.checked)}
              />
            </label>
          </div>
          <Button className="mt-4" loading={busy} onClick={runAgent}>
            <Bot className="h-4 w-4" /> Contact buyer with AI agent
          </Button>
        </div>
      )}

      <div className="mt-6">
        <Link href="/supplier/dashboard" className="text-sm text-forest-900 hover:underline">
          ← Back to dashboard
        </Link>
      </div>
    </Shell>
  );
}

export default function AnalysisPage() {
  return (
    <Suspense
      fallback={
        <Shell>
          <Spinner />
        </Shell>
      }
    >
      <AnalysisInner />
    </Suspense>
  );
}
