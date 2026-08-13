"use client";

import { useState } from "react";
import Link from "next/link";
import { Shell } from "@/components/Shell";
import { Button, Card, Field, Input, Select, Textarea } from "@/components/ui";
import { http } from "@/lib/api";
import { useAuth } from "@/lib/auth";

const CONDITIONS = ["fresh", "spoiled", "mixed", "processed", "unknown"];

export default function AddWaste() {
  const { token, user } = useAuth();
  const [form, setForm] = useState({
    produce_type: "",
    quantity_kg: "",
    condition: "unknown",
    location: user?.location ?? "",
    notes: "",
  });
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [createdId, setCreatedId] = useState<number | null>(null);

  function set(k: string, v: string) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      const body = {
        produce_type: form.produce_type,
        quantity_kg: Number(form.quantity_kg),
        condition: form.condition,
        location: form.location || null,
        notes: form.notes || null,
      };
      const data = await http.post<{ id: number }>("/waste/", body);
      setCreatedId(data.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create listing");
    } finally {
      setBusy(false);
    }
  }

  if (createdId !== null) {
    return (
      <Shell>
        <Card>
          <p className="font-medium text-ink">Waste listed successfully.</p>
          <div className="mt-4 flex gap-3">
            <Link href={`/supplier/analysis?waste=${createdId}`}>
              <Button>Analyze &amp; find buyers</Button>
            </Link>
            <Link href="/supplier/add-waste">
              <Button variant="outline">Add another</Button>
            </Link>
          </div>
        </Card>
      </Shell>
    );
  }

  return (
    <Shell>
      <h1 className="mb-1 text-2xl font-semibold text-forest-900">Add waste</h1>
      <p className="mb-6 text-sm text-ink-muted">
        Describe the organic waste you have available.
      </p>
      <Card>
        <form onSubmit={submit} className="space-y-4">
          {error && (
            <div className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800">
              {error}
            </div>
          )}
          <Field label="Waste type">
            <Input
              required
              placeholder="e.g. tomato waste"
              value={form.produce_type}
              onChange={(e) => set("produce_type", e.target.value)}
            />
          </Field>
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Quantity (kg)">
              <Input
                required
                type="number"
                min="0"
                step="0.1"
                value={form.quantity_kg}
                onChange={(e) => set("quantity_kg", e.target.value)}
              />
            </Field>
            <Field label="Condition">
              <Select value={form.condition} onChange={(e) => set("condition", e.target.value)}>
                {CONDITIONS.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </Select>
            </Field>
          </div>
          <Field label="Location">
            <Input
              placeholder="City, Country"
              value={form.location}
              onChange={(e) => set("location", e.target.value)}
            />
          </Field>
          <Field label="Notes">
            <Textarea
              rows={3}
              value={form.notes}
              onChange={(e) => set("notes", e.target.value)}
              placeholder="Anything buyers should know"
            />
          </Field>
          <Button type="submit" loading={busy}>
            Create listing
          </Button>
        </form>
      </Card>
    </Shell>
  );
}
