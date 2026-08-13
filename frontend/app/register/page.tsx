"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Recycle } from "lucide-react";
import { Button, Card, Field, Input, Select } from "@/components/ui";
import { http } from "@/lib/api";
import { useAuth } from "@/lib/auth";

function RegisterInner() {
  const router = useRouter();
  const params = useSearchParams();
  const initialRole = params.get("role") === "buyer" ? "buyer" : "supplier";
  const { token, user, setAuth } = useAuth();
  const [mounted, setMounted] = useState(false);
  useEffect(() => {
    setMounted(true);
  }, []);
  useEffect(() => {
    if (mounted && token && user) {
      router.replace(`/${user.role}/dashboard`);
    }
  }, [mounted, token, user, router]);
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    role: initialRole,
    business_type: "",
    country: "India",
    location: "",
    phone: "",
  });
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  function set(k: string, v: string) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      const data = await http.post<{ access_token: string; user: any }>("/auth/signup", form);
      setAuth(data.access_token, data.user);
      router.push(`/${data.user.role}/dashboard`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Sign up failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-parchment p-5">
      <div className="w-full max-w-md">
        <Link href="/" className="mb-6 flex items-center justify-center gap-2 text-forest-900">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-lime-400 text-forest-950">
            <Recycle className="h-5 w-5" />
          </span>
          <span className="text-lg font-semibold">Waste2Worth</span>
        </Link>
        <Card title="Create your account">
          <form onSubmit={submit} className="space-y-4">
            {error && (
              <div className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800">
                {error}
              </div>
            )}
            <Field label="Full name">
              <Input required value={form.name} onChange={(e) => set("name", e.target.value)} placeholder="Jane Supplier" />
            </Field>
            <Field label="Email">
              <Input type="email" required value={form.email} onChange={(e) => set("email", e.target.value)} placeholder="you@example.com" />
            </Field>
            <Field label="Password">
              <Input type="password" required minLength={6} value={form.password} onChange={(e) => set("password", e.target.value)} placeholder="At least 6 characters" />
            </Field>
            <Field label="I am a">
              <Select value={form.role} onChange={(e) => set("role", e.target.value)}>
                <option value="supplier">Supplier (I have waste)</option>
                <option value="buyer">Buyer (I need waste)</option>
              </Select>
            </Field>
            <div className="grid gap-4 sm:grid-cols-2">
              <Field label="Business type">
                <Input value={form.business_type} onChange={(e) => set("business_type", e.target.value)} placeholder="Farm, restaurant…" />
              </Field>
              <Field label="Location">
                <Input value={form.location} onChange={(e) => set("location", e.target.value)} placeholder="City, Country" />
              </Field>
            </div>
            <Field label="Phone">
              <Input value={form.phone} onChange={(e) => set("phone", e.target.value)} placeholder="+91…" />
            </Field>
            <Button type="submit" loading={busy} className="w-full">
              Create account
            </Button>
          </form>
          <p className="mt-4 text-center text-sm text-ink-muted">
            Already registered?{" "}
            <Link href="/login" className="font-medium text-forest-900 hover:underline">
              Sign in
            </Link>
          </p>
        </Card>
      </div>
    </main>
  );
}

export default function RegisterPage() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen items-center justify-center bg-parchment text-ink-muted">
          Loading…
        </div>
      }
    >
      <RegisterInner />
    </Suspense>
  );
}
