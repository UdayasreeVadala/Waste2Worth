"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { CheckCircle2, Truck, XCircle } from "lucide-react";
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
  const [pickupDate, setPickupDate] = useState("");

  async function act(path: string, body?: any) {
    setBusy(true);
    try {
      await http.post(path, body);
      list.reload();
      if (txnId) detail.reload();
    } catch (e) {
      alert(e instanceof Error ? e.message : "Action failed");
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
      <p className="mb-6 text-sm text-ink-muted">
        Track each deal from match to completed collection.
      </p>

      {txns.length === 0 ? (
        <EmptyState
          title="No transactions yet"
          message="When a buyer is matched and the deal is confirmed, it appears here."
        />
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
                    {money(t.supplier_earning, t.currency)}
                  </p>
                  <p className="text-xs text-ink-muted">your earnings</p>
                </div>
              </div>
              <div className="mt-4 flex flex-wrap gap-3">
                <Link href={`/supplier/transactions?txn=${t.id}`}>
                  <Button variant="outline">Details</Button>
                </Link>
                {t.status === "offer_received" && (
                  <Button loading={busy} onClick={() => act(`/transactions/${t.id}/accept-offer`)}>
                    <CheckCircle2 className="h-4 w-4" /> Accept offer
                  </Button>
                )}
                {t.status === "deal_confirmed" && (
                  <div className="flex items-end gap-2">
                    <Field label="Pickup date">
                      <Input type="date" value={pickupDate} onChange={(e) => setPickupDate(e.target.value)} />
                    </Field>
                    <Button
                      loading={busy}
                      onClick={() =>
                        act(`/transactions/${t.id}/schedule-pickup`, {
                          pickup_method: "buyer_pickup",
                          pickup_date: pickupDate || undefined,
                        })
                      }
                    >
                      <Truck className="h-4 w-4" /> Schedule pickup
                    </Button>
                  </div>
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
                  <Button
                    variant="danger"
                    loading={busy}
                    onClick={() => act(`/transactions/${t.id}/cancel`)}
                  >
                    <XCircle className="h-4 w-4" /> Cancel
                  </Button>
                )}
              </div>
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

export default function SupplierTransactions() {
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
