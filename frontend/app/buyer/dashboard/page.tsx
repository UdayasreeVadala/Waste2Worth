"use client";

import Link from "next/link";
import { Leaf, Users } from "lucide-react";
import { Shell } from "@/components/Shell";
import { Button, Card, EmptyState, StatCard, Spinner } from "@/components/ui";
import { http } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useData } from "@/lib/hooks";
import { money, num } from "@/lib/format";

export default function BuyerDashboard() {
  const { token } = useAuth();
  const available = useData<any[]>(
    () => (token ? http.get("/waste/available") : Promise.resolve([])),
    [token]
  );
  const recommended = useData<{ listings: any[] }>(
    () => (token ? http.get("/buyers/recommended") : Promise.resolve({ listings: [] })),
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

  if (available.loading || recommended.loading || matches.loading || txns.loading) {
    return (
      <Shell>
        <Spinner />
      </Shell>
    );
  }

  const avail = available.data ?? [];
  const recs = recommended.data?.listings ?? [];
  const myMatches = matches.data?.matches ?? [];
  const myTxns = txns.data?.transactions ?? [];

  return (
    <Shell>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-forest-900">Dashboard</h1>
          <p className="mt-1 text-sm text-ink-muted">
            Find waste you can process and track your deals.
          </p>
        </div>
        <Link href="/buyer/requirements">
          <Button variant="outline">
            <Users className="h-4 w-4" /> Manage requirements
          </Button>
        </Link>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Available waste" value={num(avail.length)} />
        <StatCard label="Recommended" value={num(recs.length)} tone="accent" />
        <StatCard label="Matches" value={num(myMatches.length)} />
        <StatCard label="Transactions" value={num(myTxns.length)} />
      </div>

      <h2 className="mb-3 mt-8 text-lg font-semibold text-ink">
        Recommended for your profile
      </h2>
      {recs.length === 0 ? (
        <EmptyState
          title="No recommendations yet"
          message="Add your buyer requirements to get AI-matched waste."
        />
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {recs.slice(0, 4).map((r, i) => (
            <Card key={i}>
              <p className="font-medium capitalize text-ink">
                {r.waste.produce_type} · {num(r.waste.quantity_kg)} kg
              </p>
              <p className="text-sm text-ink-muted">{r.waste.location}</p>
              <p className="mt-2 text-sm text-ink">{r.match.explanation}</p>
              <div className="mt-3 flex flex-wrap gap-4 text-sm">
                <span>
                  Est. earnings:{" "}
                  <strong>
                    {money(r.match.margin.estimated_supplier_earnings, r.match.margin.currency || "INR")}
                  </strong>
                </span>
                <span>Distance: {r.match.distance_km?.toFixed?.(1)} km</span>
              </div>
              <Link
                href="/buyer/available"
                className="mt-3 inline-block text-sm font-medium text-forest-900 hover:underline"
              >
                View in available waste →
              </Link>
            </Card>
          ))}
        </div>
      )}
    </Shell>
  );
}
