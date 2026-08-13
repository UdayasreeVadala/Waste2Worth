"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { CheckCircle2, HandHeart, XCircle } from "lucide-react";
import { Shell } from "@/components/Shell";
import { Button, Card, EmptyState, Field, Input, Spinner, StatusPill } from "@/components/ui";
import { http } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useData } from "@/lib/hooks";
import { money, num } from "@/lib/format";

function BuyerMatchCard({ match, onUpdate }: { match: any; onUpdate: () => void }) {
  const [busy, setBusy] = useState(false);
  const [offerOpen, setOfferOpen] = useState(false);
  const [price, setPrice] = useState<string>(
    String(match.supplier_earning ?? match.buyer_offer ?? 0)
  );

  async function respond(action: string, p?: number) {
    setBusy(true);
    try {
      await http.post(`/transactions/${match.transaction_id}/respond`, { action, price: p });
      onUpdate();
      setOfferOpen(false);
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    } finally {
      setBusy(false);
    }
  }

  async function act(path: string) {
    setBusy(true);
    try {
      await http.post(path);
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
            <p className="font-semibold capitalize text-ink">{match.waste?.produce_type}</p>
            <StatusPill status={match.status} />
          </div>
          <p className="text-sm text-ink-muted">
            {num(match.waste?.quantity_kg)} kg · supplier #{match.waste_id}
          </p>
          <p className="mt-2 text-sm text-ink">{match.explanation}</p>
          <div className="mt-3 flex flex-wrap gap-4 text-sm">
            <span>
              Offer: <strong>{money(match.buyer_offer, match.currency)}</strong>
            </span>
            <span>
              Your earnings: <strong>{money(match.supplier_earning, match.currency)}</strong>
            </span>
          </div>
        </div>
      </div>
      <div className="mt-4 flex flex-wrap gap-3">
        <Link href={`/buyer/transactions?txn=${match.transaction_id}`}>
          <Button variant="outline">View transaction</Button>
        </Link>
        {canRespond && (
          <>
            <Button loading={busy} onClick={() => respond("accept")}>
              <CheckCircle2 className="h-4 w-4" /> Accept
            </Button>
            <Button variant="secondary" onClick={() => setOfferOpen((o) => !o)}>
              <HandHeart className="h-4 w-4" /> Make offer
            </Button>
            <Button variant="danger" onClick={() => respond("reject")}>
              <XCircle className="h-4 w-4" /> Reject
            </Button>
          </>
        )}
        {match.status === "pickup_scheduled" && (
          <Button loading={busy} onClick={() => act(`/transactions/${match.transaction_id}/confirm-collected`)}>
            Confirm collected
          </Button>
        )}
        {match.status === "collected" && (
          <Button loading={busy} onClick={() => act(`/transactions/${match.transaction_id}/complete`)}>
            <CheckCircle2 className="h-4 w-4" /> Complete
          </Button>
        )}
      </div>
      {offerOpen && (
        <div className="mt-4 rounded-lg border border-ink/10 bg-parchment p-4">
          <Field label="Your offer (total)">
            <Input type="number" value={price} onChange={(e) => setPrice(e.target.value)} />
          </Field>
          <div className="mt-3 flex gap-2">
            <Button loading={busy} onClick={() => respond("offer", Number(price))}>
              Send offer
            </Button>
            <Button variant="ghost" onClick={() => setOfferOpen(false)}>
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
          message="Express interest in available waste to create matches."
        />
      </Shell>
    );
  }

  return (
    <Shell>
      <h1 className="mb-1 text-2xl font-semibold text-forest-900">Matches</h1>
      <p className="mb-6 text-sm text-ink-muted">
        Waste you&apos;re matched with and the status of each deal.
      </p>
      <div className="space-y-4">
        {matches.map((m) => (
          <BuyerMatchCard key={m.id} match={m} onUpdate={reload} />
        ))}
      </div>
    </Shell>
  );
}

export default function BuyerMatchesPage() {
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
