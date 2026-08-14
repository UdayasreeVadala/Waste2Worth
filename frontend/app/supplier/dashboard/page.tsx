"use client";

import Link from "next/link";
import { Plus, Sparkles } from "lucide-react";
import { Shell } from "@/components/Shell";
import { ImpactBanner } from "@/components/ImpactBanner";
import { Button, Card, EmptyState, StatCard, StatusPill, Spinner } from "@/components/ui";
import { http } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useData } from "@/lib/hooks";
import { money, num } from "@/lib/format";

export default function SupplierDashboard() {
  const { token } = useAuth();
  const listings = useData<any[]>(
    () => (token ? http.get("/waste/my-listings") : Promise.resolve([])),
    [token]
  );
  const matches = useData<{ matches: any[] }>(
    () => (token ? http.get("/matches/") : Promise.resolve({ matches: [] })),
    [token]
  );
  const txns = useData<{ transactions: any[] }>(
    () => (token ? http.get("/transactions/my") : Promise.resolve({ transactions: [] })),
    [token]
  );

  if (listings.loading || matches.loading || txns.loading) {
    return (
      <Shell>
        <Spinner />
      </Shell>
    );
  }

  const myListings = listings.data ?? [];
  const myMatches = matches.data?.matches ?? [];
  const myTxns = txns.data?.transactions ?? [];
  const earnings = myTxns
    .filter((t) => t.status === "completed")
    .reduce((s, t) => s + (t.supplier_earning || 0), 0);

  return (
    <Shell>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="font-display text-2xl font-medium text-forest-900">Dashboard</h1>
          <p className="mt-1 text-sm text-ink-muted">
            Overview of your waste, matches and earnings.
          </p>
        </div>
        <Link href="/supplier/add-waste">
          <Button>
            <Plus className="h-4 w-4" /> Add waste
          </Button>
        </Link>
      </div>

      <ImpactBanner />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Active listings" value={num(myListings.filter((l) => l.status === "available").length)} />
        <StatCard label="Matches" value={num(myMatches.length)} />
        <StatCard label="Transactions" value={num(myTxns.length)} />
        <StatCard label="Earnings (completed)" value={money(earnings)} tone="success" />
      </div>

      <h2 className="mb-3 mt-8 text-lg font-semibold text-ink">Your waste listings</h2>
      {myListings.length === 0 ? (
        <EmptyState title="No waste listed yet" message="Add your first waste listing to get AI recommendations." />
      ) : (
        <div className="space-y-3">
          {myListings.map((l) => (
            <Card key={l.id}>
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="font-medium capitalize text-ink">
                    {l.produce_type} · {num(l.quantity_kg)} kg
                  </p>
                  <div className="mt-1">
                    <StatusPill status={l.status} />
                  </div>
                </div>
                <Link href={`/supplier/analysis?waste=${l.id}`}>
                  <Button variant="outline">
                    <Sparkles className="h-4 w-4" /> Analyze &amp; match
                  </Button>
                </Link>
              </div>
            </Card>
          ))}
        </div>
      )}
    </Shell>
  );
}
