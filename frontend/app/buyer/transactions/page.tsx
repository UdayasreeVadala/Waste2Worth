"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { CheckCircle2, HandHeart, Truck, XCircle } from "lucide-react";
import { Shell } from "@/components/Shell";
import { Button, Card, EmptyState, Field, Input, Spinner, StatusPill } from "@/components/ui";
import { TransactionDetail } from "@/components/TransactionDetail";
import { http } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useData } from "@/lib/hooks";
import { money, num } from "@/lib/format";

const ACTIVE = ["match_found", "buyer_contacted", "offer_received", "deal_confirmed", "pickup_scheduled", "collected"];

function TransactionsInner() {
  const params = useSearchParams();
  const txnId = params.get("txn");
  const { token } = useAuth();
  const list = useData<{ transactions: any[] }>(
    () => (token ? http.get("/transactions/my") : Promise.resolve({ transactions: [] })),
    [token]
  );
  const detail = useData<any>(
    () => (token && txnId ? http.get(`/transactions/${txnId}`) : Promise.resolve(null)),
    [token, txnId]
  );
  const [busy, setBusy] = useState(false);
  const [offerOpen, setOfferOpen] = useState(false);
  const [price, setPrice] = useState("");

  async function respond(action: string, p?: number) {
    if (!txnId) return;
    setBusy(true);
    try {
      await http.post(`/transactions/${txnId}/respond`, { action, price: p });
      list.reload();
      detail.reload();
      setOfferOpen(false);
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    } finally {
      setBusy(false);
    }
  }

  async function act(path: string, body?: any) {
    if (!txnId) return;
    setBusy(true);
    try {
      await http.post(path, body);
      list.reload();
      detail.reload();
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed");
    } finally {
      setBusy(false);
    }
  }

  if (list.loading) {
    return (
      <Shell>
        <Spinner />
      </Shell>
    );
  }
  const txns = list.data?.transactions ?? [];

  return (
    <Shell>
      <h1 className="mb-1 text-2xl font-semibold text-forest-900">Transactions</h1>
      <p className="mb-6 text-sm text-ink-muted">Track each deal you&apos;re part of.</p>

      {txns.length === 0 ? (
        <EmptyState title="No transactions yet" message="Matches you accept become transactions here." />
      ) : (
        <div className="space-y-3">
          {txns.map((t) => (
            <Card key={t.id}>
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <div className="flex items-center gap-2">
                    <p className="font-semibold text-ink">
                      #{t.id} · {t.waste_type}
                    </p>
                    <StatusPill status={t.status} />
                  </div>
                  <p className="text-sm text-ink-muted">{num(t.quantity_kg)} kg</p>
                </div>
                <div className="text-right">
                  <p className="text-lg font-semibold text-forest-900">
                    {money(t.final_price, t.currency)}
                  </p>
                  <p className="text-xs text-ink-muted">deal value</p>
                </div>
              </div>
              <div className="mt-4 flex flex-wrap gap-3">
                <Link href={`/buyer/transactions?txn=${t.id}`}>
                  <Button variant="outline">Details</Button>
                </Link>
                {["match_found", "buyer_contacted", "offer_received"].includes(t.status) && (
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
                {t.status === "deal_confirmed" && (
                  <Button
                    loading={busy}
                    onClick={() =>
                      act(`/transactions/${t.id}/schedule-pickup`, {
                        pickup_method: "buyer_pickup",
                        pickup_date: undefined,
                      })
                    }
                  >
                    <Truck className="h-4 w-4" /> Schedule pickup
                  </Button>
                )}
                {t.status === "pickup_scheduled" && (
                  <Button loading={busy} onClick={() => act(`/transactions/${t.id}/confirm-collected`)}>
                    Confirm collected
                  </Button>
                )}
                {t.status === "collected" && (
                  <Button loading={busy} onClick={() => act(`/transactions/${t.id}/complete`)}>
                    <CheckCircle2 className="h-4 w-4" /> Complete
                  </Button>
                )}
                {ACTIVE.includes(t.status) && (
                  <Button variant="danger" loading={busy} onClick={() => act(`/transactions/${t.id}/cancel`)}>
                    <XCircle className="h-4 w-4" /> Cancel
                  </Button>
                )}
              </div>
              {offerOpen && Number(t.id) === Number(txnId) && (
                <div className="mt-4 rounded-lg border border-ink/10 bg-parchment p-4">
                  <Field label="Your offer (total)">
                    <Input
                      type="number"
                      value={price}
                      onChange={(e) => setPrice(e.target.value)}
                      placeholder={String(t.final_price ?? 0)}
                    />
                  </Field>
                  <div className="mt-3 flex gap-2">
                    <Button loading={busy} onClick={() => respond("offer", Number(price || t.final_price))}>
                      Send offer
                    </Button>
                    <Button variant="ghost" onClick={() => setOfferOpen(false)}>
                      Cancel
                    </Button>
                  </div>
                </div>
              )}
            </Card>
          ))}
        </div>
      )}

      {txnId && detail.data && (
        <div className="mt-6">
          <TransactionDetail detail={detail.data} />
        </div>
      )}
    </Shell>
  );
}

export default function BuyerTransactions() {
  return (
    <Suspense
      fallback={
        <Shell>
          <Spinner />
        </Shell>
      }
    >
      <TransactionsInner />
    </Suspense>
  );
}
