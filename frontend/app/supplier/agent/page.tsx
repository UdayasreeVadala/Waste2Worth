"use client";

import { Bot } from "lucide-react";
import { Shell } from "@/components/Shell";
import { Card, EmptyState, Spinner } from "@/components/ui";
import { http } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useData } from "@/lib/hooks";

export default function SupplierAgent() {
  const { token } = useAuth();
  const { data, loading } = useData<{ events: any[] }>(
    () => (token ? http.get("/agent/activity") : Promise.resolve({ events: [] })),
    [token]
  );

  if (loading) {
    return (
      <Shell>
        <Spinner />
      </Shell>
    );
  }
  const events = data?.events ?? [];

  return (
    <Shell>
      <h1 className="mb-1 font-display text-2xl font-medium text-forest-900">AI Agent Activity</h1>
      <p className="mb-6 text-sm text-ink-muted">
        Every action the agent takes on your behalf is logged here.
      </p>

      {events.length === 0 ? (
        <EmptyState
          title="No agent activity yet"
          message="Analyze a listing and run the agent to see its work."
        />
      ) : (
        <Card>
          <ol className="relative space-y-4 border-l border-ink/10 pl-6">
            {events.map((e) => (
              <li key={e.id} className="relative">
                <span className="absolute -left-[1.65rem] top-1 flex h-3 w-3 items-center justify-center rounded-full bg-forest-900">
                  <Bot className="h-2 w-2 text-lime-400" />
                </span>
                <p className="text-sm font-medium text-ink">{e.message}</p>
                <p className="text-xs text-ink-muted">
                  {e.actor} · {e.event_type}
                </p>
              </li>
            ))}
          </ol>
        </Card>
      )}
    </Shell>
  );
}
