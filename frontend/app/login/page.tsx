"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Bot, Leaf, Recycle, Sparkles } from "lucide-react";
import { Button, Card, Field, Input } from "@/components/ui";
import { Orbs } from "@/components/anim/Orbs";
import { ParticleField } from "@/components/anim/ParticleField";
import { http } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const { token, user, setAuth } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const [mounted, setMounted] = useState(false);
  useEffect(() => {
    setMounted(true);
  }, []);
  useEffect(() => {
    if (mounted && token && user) {
      router.replace(`/${user.role}/dashboard`);
    }
  }, [mounted, token, user, router]);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setBusy(true);
    try {
      const data = await http.post<{ access_token: string; user: any }>("/auth/login", {
        email,
        password,
      });
      setAuth(data.access_token, data.user);
      router.push(`/${data.user.role}/dashboard`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
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
              Give waste a second life
            </p>
            <h1 className="mt-4 text-4xl font-semibold leading-tight tracking-tight">
              Preventing usable organic waste from becoming <span className="text-mission">disposal waste</span>.
            </h1>
            <p className="mt-4 leading-7 text-white/75">
              AI finds the highest-value reuse pathway and autonomously connects it with a suitable
              buyer — biogas, compost, vermicompost and more.
            </p>
          </div>

          <div className="mt-8 space-y-4">
            <Pillar icon={Leaf} title="Environmental by design" text="Every recovered kilo keeps methane — a gas ~28x stronger than CO₂ — out of the air." />
            <Pillar icon={Sparkles} title="AI determines the best use" text="Not just the nearest buyer: the highest-value reuse pathway for your waste." />
            <Pillar icon={Bot} title="A trusted agent closes the deal" text="Negotiates only within your limits, and only after you approve." />
          </div>
        </div>

        <p className="anim-reveal-up relative text-sm text-white/55" style={{ animationDelay: "240ms" }}>
          Waste2Worth turns surplus organic material into feedstock, not landfill.
        </p>
      </section>

      <section className="flex items-center justify-center bg-parchment p-5">
        <div className="anim-reveal-up w-full max-w-md" style={{ animationDelay: "180ms" }}>
          <Link href="/" className="mb-6 flex items-center justify-center gap-2 text-forest-900 lg:hidden">
            <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-lime-400 text-forest-950">
              <Recycle className="h-5 w-5" />
            </span>
            <span className="text-lg font-semibold">Waste2Worth</span>
          </Link>
          <Card title="Sign in">
            <form onSubmit={submit} className="space-y-4">
              {error && (
                <div className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-800">
                  {error}
                </div>
              )}
              <Field label="Email">
                <Input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                />
              </Field>
              <Field label="Password">
                <Input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                />
              </Field>
              <Button type="submit" loading={busy} className="btn-3d w-full">
                Sign in
              </Button>
            </form>
            <p className="mt-4 text-center text-sm text-ink-muted">
              No account?{" "}
              <Link href="/register" className="font-medium text-forest-900 hover:underline">
                Create one
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
