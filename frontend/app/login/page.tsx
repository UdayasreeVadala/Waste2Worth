"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Recycle } from "lucide-react";
import { Button, Card, Field, Input } from "@/components/ui";
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
    <main className="flex min-h-screen items-center justify-center bg-parchment p-5">
      <div className="w-full max-w-md">
        <Link href="/" className="mb-6 flex items-center justify-center gap-2 text-forest-900">
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
            <Button type="submit" loading={busy} className="w-full">
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
    </main>
  );
}
