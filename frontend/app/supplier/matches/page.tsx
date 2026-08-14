"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { Bot, CheckCircle2, RefreshCw } from "lucide-react";
import { Shell } from "@/components/Shell";
import { Button, Card, EmptyState, Input, Spinner, StatusPill } from "@/components/ui";
import { http } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useData } from "@/lib/hooks";
import { money, num } from "@/lib/format";

function MatchCard({ match, onUpdate }: { match: any; onUpdate: () => void }) {
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const [form, setForm] = useState({
    minimum_total_price: match.supplier_earning ?? 0,
    requires_pickup: true,
    allow_counter_offer: true,
  });

  async function retry() {
    setBusy(true);
    try {
      await http.post(`/agent/matches/${match.id}/retry`, form);
      onUpdate();
      setOpen(false);
    } catch (e) {
      alert(e instanceof Error ? e.message : "Retry failed");
    } finally {
      setBusy(false);
    }
  }

  async function acceptOffer() {
    setBusy(true);
    try {
      await http.post(`/transactions/${match.transaction_id}/accept-offer`);
      onUpdate();
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    } finally {
      setBusy(false);
    }
  }

  const canRespond = ["match_found", "buyer_contacted", "offer_received"].includes(match.status);

  return (
    <Card>
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2">
            <p className="font-semibold text-ink">{match.buyer_name}</p>
            <StatusPill status={match.status} />
          </div>
          <p className="text-sm capitalize text-ink-muted">
            {match.waste?.produce_type} · {num(match.waste?.quantity_kg)} kg
          </p>
          <p className="mt-2 text-sm text-ink">{match.explanation}</p>
          <div className="mt-3 flex flex-wrap gap-4 text-sm">
            <span>
              Offer: <strong>{money(match.buyer_offer, match.currency)}</strong>
            </span>
            <span>
              Your earning: <strong>{money(match.supplier_earning, match.currency)}</strong>
            </span>
            <span>Score: {typeof match.score === "number" ? match.score.toFixed(1) : match.score}</span>
          </div>
        </div>
      </div>
      <div className="mt-4 flex flex-wrap gap-3">
        <Link href={`/supplier/transactions?txn=${match.transaction_id}`}>
          <Button variant="outline">View transaction</Button>
        </Link>
        {match.status === "offer_received" && (
          <Button loading={busy} onClick={acceptOffer}>
            <CheckCircle2 className="h-4 w-4" /> Accept offer
          </Button>
        )}
        {canRespond && (
          <Button variant="secondary" onClick={() => setOpen((o) => !o)}>
            <RefreshCw className="h-4 w-4" /> Retry agent
          </Button>
        )}
      </div>
      {open && (
        <div className="mt-4 rounded-lg border border-ink/10 bg-parchment p-4">
          <div className="grid gap-3 sm:grid-cols-3">
            <label className="text-sm text-ink">
              Min total price
              <Input
                type="number"
                value={form.minimum_total_price}
                onChange={(e) =>
                  setForm((f) => ({ ...f, minimum_total_price: Number(e.target.value) }))
                }
              />
            </label>
            <label className="flex items-center gap-2 text-sm text-ink">
              Pickup
              <input
                type="checkbox"
                checked={form.requires_pickup}
                onChange={(e) => setForm((f) => ({ ...f, requires_pickup: e.target.checked }))}
              />
            </label>
            <label className="flex items-center gap-2 text-sm text-ink">
              Counter-offer
              <input
                type="checkbox"
                checked={form.allow_counter_offer}
                onChange={(e) => setForm((f) => ({ ...f, allow_counter_offer: e.target.checked }))}
              />
            </label>
          </div>
          <div className="mt-3 flex gap-2">
            <Button loading={busy} onClick={retry}>
              <Bot className="h-4 w-4" /> Run agent
            </Button>
            <Button variant="ghost" onClick={() => setOpen(false)}>
              Cancel
            </Button>
          </div>
        </div>
      )}
    </Card>
  );
}

function MatchesInner() {
  const { token } = useAuth();
  const { data, loading, reload } = useData<{ matches: any[] }>(
    () => (token ? http.get("/matches/") : Promise.resolve({ matches: [] })),
    [token]
  );

  if (loading) {
    return (
      <Shell>
        <Spinner />
      </Shell>
    );
  }
  const matches = data?.matches ?? [];
  if (matches.length === 0) {
    return (
      <Shell>
        <EmptyState
          title="No matches yet"
          message="Analyze a waste listing to contact buyers and create matches."
        />
      </Shell>
    );
  }

  return (
    <Shell>
      <h1 className="mb-1 font-display text-2xl font-medium text-forest-900">Buyer matches</h1>
      <p className="mb-6 text-sm text-ink-muted">
        Matches matched to your waste, with the AI agent negotiation status.
      </p>
      <div className="space-y-4">
        {matches.map((m) => (
          <MatchCard key={m.id} match={m} onUpdate={reload} />
        ))}
      </div>
    </Shell>
  );
}

export default function SupplierMatches() {
  return (
    <Suspense
      fallback={
        <Shell>
          <Spinner />
        </Shell>
      }
    >
      <MatchesInner />
    </Suspense>
  );
}
