"use client";

import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Leaf, Recycle, Sparkles } from "lucide-react";
import { Button, Card, Field, Input, Select } from "@/components/ui";
import { Orbs } from "@/components/anim/Orbs";
import { ParticleField } from "@/components/anim/ParticleField";
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
    <main className="grid min-h-screen lg:grid-cols-2">
      <section className="relative hidden overflow-hidden bg-mission p-10 text-white lg:flex lg:flex-col lg:justify-between">
        <Orbs />
        <ParticleField className="absolute inset-0 h-full w-full" />
        <div className="anim-reveal-up relative flex items-center gap-2">
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-lime-400 text-forest-950">
            <Recycle className="h-5 w-5" />
          </span>
          <span className="text-lg font-semibold">Waste2Worth</span>
        </div>

        <div className="relative max-w-md">
          <div className="anim-reveal-up" style={{ animationDelay: "120ms" }}>
            <p className="text-xs font-medium uppercase tracking-[0.22em] text-lime-400">
              Join the recovery
            </p>
            <h1 className="mt-4 text-4xl font-semibold leading-tight tracking-tight">
              Every kilo you list is a kilo of <span className="text-mission">methane avoided</span>.
            </h1>
            <p className="mt-4 leading-7 text-white/75">
              A marketplace with a purpose: AI matches organic waste with the business that gives it
              the highest-value reuse — and prevents it from becoming disposal waste.
            </p>
          </div>

          <div className="mt-8 space-y-4">
            <Pillar icon={Leaf} title="Have waste?" text="List it in your own words — AI structures it, ranks buyers, and shows your net return." />
            <Pillar icon={Sparkles} title="Need waste?" text="Set requirements and get AI-matched feedstock, right for your process and location." />
            <Pillar icon={Leaf} title="Win for both sides" text="Suppliers earn, buyers get material, and the planet avoids landfill methane." />
          </div>
        </div>

        <p className="anim-reveal-up relative text-sm text-white/55" style={{ animationDelay: "240ms" }}>
          Waste2Worth turns surplus organic material into feedstock, not landfill.
        </p>
      </section>

      <section className="flex items-center justify-center bg-parchment p-5 py-10">
        <div className="anim-reveal-up w-full max-w-md" style={{ animationDelay: "180ms" }}>
          <Link href="/" className="mb-6 flex items-center justify-center gap-2 text-forest-900 lg:hidden">
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
              <Button type="submit" loading={busy} className="btn-3d w-full">
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
      </section>
    </main>
  );
}

function Pillar({
  icon: Icon,
  title,
  text,
}: {
  icon: React.ElementType;
  title: string;
  text: string;
}) {
  return (
    <div className="flex gap-3">
      <span className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-white/10 text-lime-400">
        <Icon className="h-4 w-4" />
      </span>
      <div>
        <p className="text-sm font-semibold">{title}</p>
        <p className="mt-0.5 text-sm leading-6 text-white/65">{text}</p>
      </div>
    </div>
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
