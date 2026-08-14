"use client";

import { Shell } from "@/components/Shell";
import { Card, Spinner, StatCard } from "@/components/ui";
import { http } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useData } from "@/lib/hooks";
import { money, num, statusLabel } from "@/lib/format";

export default function AdminPage() {
  const { token } = useAuth();
  const stats = useData<any>(
    () => (token ? http.get("/admin/stats") : Promise.resolve(null)),
    [token]
  );
  const txns = useData<{ transactions: any[] }>(
    () => (token ? http.get("/admin/transactions") : Promise.resolve({ transactions: [] })),
    [token]
  );
  const users = useData<{ users: any[] }>(
    () => (token ? http.get("/admin/users") : Promise.resolve({ users: [] })),
    [token]
  );
  const listings = useData<{ listings: any[] }>(
    () => (token ? http.get("/admin/listings") : Promise.resolve({ listings: [] })),
    [token]
  );

  if (stats.loading || !stats.data) {
    return (
      <Shell>
        <Spinner />
      </Shell>
    );
  }
  const s = stats.data;

  return (
    <Shell>
      <h1 className="mb-1 font-display text-2xl font-medium text-forest-900">Platform overview</h1>
      <p className="mb-6 text-sm text-ink-muted">
        Impact, users and activity across Waste2Worth.
      </p>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          label="Users"
          value={num(s.total_users)}
          hint={`${s.total_suppliers} suppliers · ${s.total_buyers} buyers`}
        />
        <StatCard label="Active listings" value={num(s.active_listings)} />
        <StatCard label="Active matches" value={num(s.active_matches)} />
        <StatCard label="Completed" value={num(s.completed_transactions)} tone="success" />
        <StatCard label="Waste recovered (kg)" value={num(s.waste_recovered_kg)} />
        <StatCard label="Waste listed (kg)" value={num(s.waste_redirected_kg)} />
        <StatCard label="Supplier earnings" value={money(s.supplier_earnings_total)} />
      </div>

      <h2 className="mb-3 mt-8 text-lg font-semibold text-ink">Recent transactions</h2>
      <Card>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-ink-muted">
                <th className="py-2 pr-4">ID</th>
                <th className="py-2 pr-4">Waste</th>
                <th className="py-2 pr-4">Qty</th>
                <th className="py-2 pr-4">Price</th>
                <th className="py-2 pr-4">Status</th>
              </tr>
            </thead>
            <tbody>
              {(txns.data?.transactions ?? []).slice(0, 10).map((t) => (
                <tr key={t.id} className="border-t border-ink/10">
                  <td className="py-2 pr-4">#{t.id}</td>
                  <td className="py-2 pr-4 capitalize">{t.waste_type}</td>
                  <td className="py-2 pr-4">{num(t.quantity_kg)}</td>
                  <td className="py-2 pr-4">{money(t.final_price, t.currency)}</td>
                  <td className="py-2 pr-4 text-forest-900">{statusLabel(t.status)}</td>
                </tr>
              ))}
              {(txns.data?.transactions ?? []).length === 0 && (
                <tr>
                  <td colSpan={5} className="py-3 text-ink-muted">
                    No transactions yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>

      <h2 className="mb-3 mt-8 text-lg font-semibold text-ink">Users</h2>
      <Card>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-ink-muted">
                <th className="py-2 pr-4">Name</th>
                <th className="py-2 pr-4">Email</th>
                <th className="py-2 pr-4">Role</th>
                <th className="py-2 pr-4">Location</th>
              </tr>
            </thead>
            <tbody>
              {(users.data?.users ?? []).slice(0, 15).map((u) => (
                <tr key={u.id} className="border-t border-ink/10">
                  <td className="py-2 pr-4">{u.name}</td>
                  <td className="py-2 pr-4">{u.email}</td>
                  <td className="py-2 pr-4 capitalize">{u.role}</td>
                  <td className="py-2 pr-4">{u.location || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      <h2 className="mb-3 mt-8 text-lg font-semibold text-ink">Listings</h2>
      <Card>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-ink-muted">
                <th className="py-2 pr-4">ID</th>
                <th className="py-2 pr-4">Waste</th>
                <th className="py-2 pr-4">Qty</th>
                <th className="py-2 pr-4">Condition</th>
                <th className="py-2 pr-4">Status</th>
              </tr>
            </thead>
            <tbody>
              {(listings.data?.listings ?? []).slice(0, 15).map((l) => (
                <tr key={l.id} className="border-t border-ink/10">
                  <td className="py-2 pr-4">#{l.id}</td>
                  <td className="py-2 pr-4 capitalize">{l.produce_type}</td>
                  <td className="py-2 pr-4">{num(l.quantity_kg)}</td>
                  <td className="py-2 pr-4">{l.condition}</td>
                  <td className="py-2 pr-4 text-forest-900">{statusLabel(l.status)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </Shell>
  );
}
