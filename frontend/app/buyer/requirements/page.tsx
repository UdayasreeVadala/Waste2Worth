"use client";

import { useState } from "react";
import { Pencil, Plus } from "lucide-react";
import { Shell } from "@/components/Shell";
import { Button, Card, EmptyState, Field, Input, Select, Spinner, Textarea } from "@/components/ui";
import { http } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useData } from "@/lib/hooks";
import { money, num } from "@/lib/format";

const EMPTY = {
  business_name: "",
  buyer_type: "composting",
  location: "",
  price_per_kg: "",
  max_capacity_kg: "",
  min_quantity_kg: "0",
  accepted_waste_types: "organic,vegetable,fruit,food,crop,produce",
  current_capacity_kg: "",
  pickup_available: true,
  service_radius_km: "",
  currency: "INR",
  requirement_notes: "",
};

export default function BuyerRequirements() {
  const { token } = useAuth();
  const { data, loading, reload } = useData<any[]>(
    () => (token ? http.get("/buyers/my-profile") : Promise.resolve([])),
    [token]
  );
  const [editing, setEditing] = useState<number | null>(null);
  const [form, setForm] = useState<any>(EMPTY);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function set(k: string, v: any) {
    setForm((f: any) => ({ ...f, [k]: v }));
  }

  function startNew() {
    setEditing(null);
    setForm(EMPTY);
    setError(null);
  }

  function startEdit(p: any) {
    setEditing(p.id);
    setForm({
      ...EMPTY,
      ...p,
      price_per_kg: String(p.price_per_kg),
      max_capacity_kg: String(p.max_capacity_kg),
      min_quantity_kg: String(p.min_quantity_kg),
      current_capacity_kg: p.current_capacity_kg != null ? String(p.current_capacity_kg) : "",
      service_radius_km: p.service_radius_km != null ? String(p.service_radius_km) : "",
    });
    setError(null);
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    const body = {
      ...form,
      price_per_kg: Number(form.price_per_kg),
      max_capacity_kg: Number(form.max_capacity_kg),
      min_quantity_kg: Number(form.min_quantity_kg),
      current_capacity_kg: form.current_capacity_kg === "" ? null : Number(form.current_capacity_kg),
      service_radius_km: form.service_radius_km === "" ? null : Number(form.service_radius_km),
    };
    try {
      if (editing != null) await http.put(`/buyers/${editing}`, body);
      else await http.post("/buyers/", body);
      setEditing(null);
      setForm(EMPTY);
      reload();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Save failed");
    } finally {
      setBusy(false);
    }
  }

  if (loading) {
    return (
      <Shell>
        <Spinner />
      </Shell>
    );
  }
  const profiles = data ?? [];

  return (
    <Shell>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-forest-900">Buyer requirements</h1>
          <p className="mt-1 text-sm text-ink-muted">
            Define what waste you accept and how much you can process. This powers your AI
            recommendations.
          </p>
        </div>
        <Button variant="outline" onClick={startNew}>
          <Plus className="h-4 w-4" /> New profile
        </Button>
      </div>

      {profiles.length === 0 && (
        <EmptyState
          title="No buyer profile yet"
          message="Create your first requirements profile below to receive matched waste."
        />
      )}

      <div className="space-y-3">
        {profiles.map((p) => (
          <Card key={p.id}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <p className="font-semibold text-ink">{p.business_name}</p>
                <p className="text-sm capitalize text-ink-muted">
                  {p.buyer_type} · {p.location}
                </p>
                <p className="mt-1 text-sm text-ink">
                  {money(p.price_per_kg, p.currency)}/kg · capacity {num(p.max_capacity_kg)} kg
                </p>
              </div>
              <Button variant="outline" onClick={() => startEdit(p)}>
                <Pencil className="h-4 w-4" /> Edit
              </Button>
            </div>
          </Card>
        ))}
      </div>

      <Card title={editing != null ? "Edit profile" : "New profile"} className="mt-6">
        <form onSubmit={submit} className="space-y-4">
          {error && (
            <div className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800">
              {error}
            </div>
          )}
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Business name">
              <Input required value={form.business_name} onChange={(e) => set("business_name", e.target.value)} />
            </Field>
            <Field label="Buyer type">
              <Select value={form.buyer_type} onChange={(e) => set("buyer_type", e.target.value)}>
                {["composting", "biogas", "vermicompost", "biochar", "animal_feed", "other"].map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </Select>
            </Field>
            <Field label="Location">
              <Input value={form.location} onChange={(e) => set("location", e.target.value)} />
            </Field>
            <Field label="Price per kg">
              <Input type="number" step="0.01" value={form.price_per_kg} onChange={(e) => set("price_per_kg", e.target.value)} />
            </Field>
            <Field label="Max capacity (kg)">
              <Input type="number" value={form.max_capacity_kg} onChange={(e) => set("max_capacity_kg", e.target.value)} />
            </Field>
            <Field label="Min quantity (kg)">
              <Input type="number" value={form.min_quantity_kg} onChange={(e) => set("min_quantity_kg", e.target.value)} />
            </Field>
            <Field label="Current capacity (kg)">
              <Input type="number" value={form.current_capacity_kg} onChange={(e) => set("current_capacity_kg", e.target.value)} />
            </Field>
            <Field label="Service radius (km)">
              <Input type="number" value={form.service_radius_km} onChange={(e) => set("service_radius_km", e.target.value)} />
            </Field>
          </div>
          <Field label="Accepted waste types">
            <Input value={form.accepted_waste_types} onChange={(e) => set("accepted_waste_types", e.target.value)} />
          </Field>
          <Field label="Notes">
            <Textarea rows={2} value={form.requirement_notes} onChange={(e) => set("requirement_notes", e.target.value)} />
          </Field>
          <label className="flex items-center gap-2 text-sm text-ink">
            Pickup available
            <input
              type="checkbox"
              checked={form.pickup_available}
              onChange={(e) => set("pickup_available", e.target.checked)}
            />
          </label>
          <div className="flex gap-2">
            <Button type="submit" loading={busy}>
              {editing != null ? "Save changes" : "Create profile"}
            </Button>
            {editing != null && (
              <Button variant="ghost" onClick={startNew}>
                Cancel
              </Button>
            )}
          </div>
        </form>
      </Card>
    </Shell>
  );
}
