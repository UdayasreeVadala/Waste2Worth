"use client";

import { Suspense, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Send } from "lucide-react";
import { Card, EmptyState, Input, Spinner } from "@/components/ui";
import { http } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useData } from "@/lib/hooks";

interface Conversation {
  transaction_id: number;
  status: string;
  waste_label: string;
  other_party: string;
  message_count: number;
  last_message?: string | null;
  last_message_sender_role?: string | null;
}

function MessagesInner() {
  const params = useSearchParams();
  const txn = params.get("txn");
  const { token, user } = useAuth();
  const convos = useData<{ conversations: Conversation[] }>(
    () => (token ? http.get("/messages/conversations") : Promise.resolve({ conversations: [] })),
    [token]
  );
  const thread = useData<any[]>(
    () => (token && txn ? http.get(`/messages/transactions/${txn}`) : Promise.resolve([])),
    [token, txn]
  );
  const [text, setText] = useState("");
  const [busy, setBusy] = useState(false);

  async function send() {
    if (!txn || !text.trim()) return;
    setBusy(true);
    try {
      await http.post(`/messages/transactions/${txn}/messages`, { content: text.trim() });
      setText("");
      thread.reload();
      convos.reload();
    } catch (err) {
      alert(err instanceof Error ? err.message : "Send failed");
    } finally {
      setBusy(false);
    }
  }

  if (convos.loading) return <Spinner />;
  const list = convos.data?.conversations ?? [];

  return (
    <div className="grid gap-6 lg:grid-cols-3">
      <Card title="Conversations" className="lg:col-span-1">
        {list.length === 0 ? (
          <EmptyState title="No conversations" message="Matches create a conversation thread automatically." />
        ) : (
          <ul className="space-y-2">
            {list.map((c) => (
              <li key={c.transaction_id}>
                <Link
                  href={`?txn=${c.transaction_id}`}
                  className={`block rounded-lg border p-3 text-sm ${
                    Number(txn) === c.transaction_id
                      ? "border-forest-700 bg-moss-50"
                      : "border-ink/10 hover:bg-moss-50"
                  }`}
                >
                  <p className="font-medium text-ink">{c.other_party}</p>
                  <p className="text-xs text-ink-muted">{c.waste_label}</p>
                  <p className="mt-1 truncate text-xs text-ink-muted">
                    {c.last_message || "No messages yet"}
                  </p>
                </Link>
              </li>
            ))}
          </ul>
        )}
      </Card>

      <Card title="Thread" className="lg:col-span-2">
        {!txn ? (
          <EmptyState title="Select a conversation" message="Choose a conversation on the left to view messages." />
        ) : (
          <div className="space-y-3">
            {(thread.data ?? []).map((m, i) => (
              <div key={i} className={`flex ${m.sender_role === user?.role ? "justify-end" : "justify-start"}`}>
                <div
                  className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm ${
                    m.sender_role === user?.role
                      ? "bg-forest-900 text-white"
                      : m.sender_role === "buyer" || m.sender_role === "supplier"
                        ? "bg-moss-100 text-ink"
                        : "bg-ink/5 text-ink"
                  }`}
                >
                  {m.content}
                </div>
              </div>
            ))}
            {thread.data?.length === 0 && (
              <p className="text-sm text-ink-muted">No messages yet. Start the conversation.</p>
            )}
            <div className="flex items-center gap-2 pt-2">
              <Input
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Type a message..."
                onKeyDown={(e) => {
                  if (e.key === "Enter") send();
                }}
              />
              <button
                onClick={send}
                disabled={busy || !text.trim()}
                className="inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-forest-900 text-white hover:bg-forest-700 disabled:opacity-60"
              >
                <Send className="h-4 w-4" />
              </button>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
}

export function MessagesView() {
  return (
    <Suspense fallback={<Spinner />}>
      <MessagesInner />
    </Suspense>
  );
}
