"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { HandHeart } from "lucide-react";
import { Shell } from "@/components/Shell";
import { Button, Card, EmptyState, Spinner, StatusPill } from "@/components/ui";
import { http } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useData } from "@/lib/hooks";
import { num } from "@/lib/format";

export default function BuyerAvailable() {
  const { token } = useAuth();
  const router = useRouter();
  const { data, loading, reload } = useData<any[]>(
    () => (token ? http.get("/waste/available") : Promise.resolve([])),
    [token]
  );
  const [busy, setBusy] = useState<number | null>(null);
  const [msg, setMsg] = useState<string | null>(null);

  async function express(wasteId: number) {
    setBusy(wasteId);
    setMsg(null);
    try {
      await http.post("/buyers/express-interest", { waste_id: wasteId });
      setMsg("Interest registered — a match was created. View it in Matches.");
      reload();
      setTimeout(() => router.push("/buyer/matches"), 900);
    } catch (e) {
      setMsg(e instanceof Error ? e.message : "Could not register interest");
    } finally {
      setBusy(null);
    }
  }

  if (loading) {
    return (
      <Shell>
        <Spinner />
      </Shell>
    );
  }
  const listings = data ?? [];

  return (
    <Shell>
      <h1 className="mb-1 text-2xl font-semibold text-forest-900">Available waste</h1>
      <p className="mb-6 text-sm text-ink-muted">
        Browse organic waste listings from suppliers. Express interest to start a match.
      </p>
      {msg && (
        <div className="mb-4 rounded-lg border border-lime-400/50 bg-moss-100 px-4 py-3 text-sm text-forest-900">
          {msg}
        </div>
      )}
      {listings.length === 0 ? (
        <EmptyState title="No waste available" message="Check back later for new supplier listings." />
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {listings.map((w) => (
            <Card key={w.id}>
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="font-semibold capitalize text-ink">
                    {w.produce_type} · {num(w.quantity_kg)} kg
                  </p>
                  <p className="text-sm text-ink-muted">{w.location}</p>
                  <div className="mt-2">
                    <StatusPill status={w.status} />
                  </div>
                </div>
              </div>
              {w.notes && <p className="mt-3 text-sm text-ink-muted">{w.notes}</p>}
              <div className="mt-4">
                <Button loading={busy === w.id} onClick={() => express(w.id)}>
                  <HandHeart className="h-4 w-4" /> Express interest
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </Shell>
  );
}
