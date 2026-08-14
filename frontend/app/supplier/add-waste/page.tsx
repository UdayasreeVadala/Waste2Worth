"use client";

import { useState } from "react";
import Link from "next/link";
import { Sparkles, Camera } from "lucide-react";
import { Shell } from "@/components/Shell";
import { Button, Card, Field, Input, Select, Textarea, Alert } from "@/components/ui";
import { http } from "@/lib/api";
import { useAuth } from "@/lib/auth";

const CONDITIONS = ["fresh", "spoiled", "mixed", "processed", "unknown"];

type ExtractedFields = {
  waste_type?: string;
  quantity_kg?: number;
  estimated_quantity_kg?: number;
  condition?: string;
  location?: string | null;
  notes?: string;
  confidence?: number;
  source?: string;
};

export default function AddWaste() {
  const { user } = useAuth();
  const [form, setForm] = useState({
    produce_type: "",
    quantity_kg: "",
    condition: "unknown",
    location: user?.location ?? "",
    notes: "",
  });
  const [description, setDescription] = useState("");
  const [photoUrl, setPhotoUrl] = useState<string | null>(null);
  const [aiNote, setAiNote] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [aiBusy, setAiBusy] = useState(false);
  const [createdId, setCreatedId] = useState<number | null>(null);

  function set(k: string, v: string) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  function applyFields(fields: ExtractedFields) {
    setForm((f) => ({
      ...f,
      produce_type: fields.waste_type ?? f.produce_type,
      quantity_kg: fields.quantity_kg != null ? String(fields.quantity_kg) : f.quantity_kg,
      condition: fields.condition && fields.condition !== "unknown" ? fields.condition : f.condition,
      location: fields.location ?? f.location,
    }));
  }

  async function autoFill() {
    if (!description.trim()) {
      setError("Describe your waste first, e.g. \"around 700 kg of spoiled tomatoes from Nashik\".");
      return;
    }
    setError(null);
    setAiBusy(true);
    try {
      const result = await http.post<ExtractedFields>("/waste/extract", { text: description });
      applyFields(result);
      setAiNote(`AI filled the fields from your description (${result.source ?? "rules"}).`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Auto-fill failed");
    } finally {
      setAiBusy(false);
    }
  }

  async function onPhoto(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setError(null);
    setAiBusy(true);
    try {
      const result = await http.upload<{ url: string; detection?: ExtractedFields }>("/waste/upload", file);
      setPhotoUrl(result.url);
      if (result.detection?.waste_type) {
        applyFields({
          waste_type: result.detection.waste_type,
          quantity_kg: result.detection.estimated_quantity_kg,
          condition: result.detection.condition,
        });
        setAiNote(
          `AI identified ${result.detection.waste_type} from the photo (${result.detection.source ?? "vision"}).`
        );
      } else {
        setAiNote("Photo uploaded. Describe it or fill the fields manually to continue.");
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Photo upload failed");
    } finally {
      setAiBusy(false);
    }
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      const body = {
        produce_type: form.produce_type,
        quantity_kg: form.quantity_kg ? Number(form.quantity_kg) : null,
        condition: form.condition,
        location: form.location || null,
        notes: form.notes || null,
        photo_url: photoUrl,
        description: description || null,
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
      <h1 className="mb-1 font-display text-2xl font-medium text-forest-900">Add waste</h1>
      <p className="mb-6 text-sm text-ink-muted">
        Describe the organic waste in your own words — AI fills the details for you.
      </p>

      <Card className="mb-6">
        <Field
          label="Describe your waste in plain language"
          hint="Example: “I have around 700 kg of spoiled tomatoes from my vegetable farm near Nashik.”"
        >
          <Textarea
            rows={3}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Type naturally — no technical terms needed"
          />
        </Field>
        <div className="mt-3 flex flex-wrap items-center gap-4">
          <Button type="button" variant="secondary" loading={aiBusy} onClick={autoFill}>
            <Sparkles className="h-4 w-4" /> Auto-fill with AI
          </Button>
          <label className="inline-flex cursor-pointer items-center gap-2 rounded-md border border-forest-900/20 bg-white px-4 py-2 text-sm font-medium text-forest-900 hover:bg-moss-50">
            <Camera className="h-4 w-4" /> Upload a photo
            <input type="file" accept="image/*" className="hidden" onChange={onPhoto} />
          </label>
          {photoUrl && (
            <span className="inline-flex items-center gap-2 text-sm text-ink-muted">
              <span className="h-3 w-3 rounded-full bg-lime-400" /> photo attached
            </span>
          )}
        </div>
        {aiNote && (
          <div className="mt-3">
            <Alert tone="success">{aiNote}</Alert>
          </div>
        )}
      </Card>

      <Card>
        <form onSubmit={submit} className="space-y-4">
          {error && (
            <Alert tone="error">{error}</Alert>
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
