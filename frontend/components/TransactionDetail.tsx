"use client";

import { Bot } from "lucide-react";
import { Card } from "@/components/ui";
import { money, num, statusLabel, dateLabel } from "@/lib/format";

const STATUSES = [
  "match_found",
  "buyer_contacted",
  "offer_received",
  "deal_confirmed",
  "pickup_scheduled",
  "collected",
  "completed",
];

export function TransactionDetail({ detail }: { detail: any }) {
  if (!detail) return null;
  return (
    <Card title="Transaction detail">
      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <p className="text-sm text-ink-muted">Counterparty</p>
          <p className="font-medium text-ink">
            {detail.buyer_business_name || detail.supplier_name || "—"}
          </p>
        </div>
        <div>
          <p className="text-sm text-ink-muted">Waste</p>
          <p className="font-medium capitalize text-ink">
            {detail.waste?.produce_type} · {num(detail.waste?.quantity_kg)} kg
          </p>
        </div>
        <div>
          <p className="text-sm text-ink-muted">Final price</p>
          <p className="font-medium text-ink">{money(detail.final_price, detail.currency)}</p>
        </div>
        <div>
          <p className="text-sm text-ink-muted">Your position</p>
          <p className="font-medium text-ink">{money(detail.supplier_earning, detail.currency)}</p>
        </div>
        <div>
          <p className="text-sm text-ink-muted">Pickup</p>
          <p className="font-medium text-ink">
            {detail.pickup_method || "—"}
            {detail.pickup_date ? ` · ${dateLabel(detail.pickup_date)}` : ""}
          </p>
        </div>
        <div>
          <p className="text-sm text-ink-muted">Created</p>
          <p className="font-medium text-ink">{dateLabel(detail.created_at)}</p>
        </div>
      </div>

      <p className="mt-5 text-sm font-medium text-ink">Progress</p>
      <div className="mt-2 flex flex-wrap gap-2">
        {STATUSES.map((s) => {
          const reached = STATUSES.indexOf(detail.status) >= STATUSES.indexOf(s);
          return (
            <span
              key={s}
              className={`rounded-full px-2.5 py-0.5 text-xs ${
                reached ? "bg-forest-900 text-white" : "bg-ink/5 text-ink-muted"
              }`}
            >
              {statusLabel(s)}
            </span>
          );
        })}
      </div>

      <p className="mt-5 text-sm font-medium text-ink">Agent &amp; system events</p>
      <ol className="mt-2 space-y-2 text-sm">
        {(detail.events ?? []).map((e: any) => (
          <li key={e.id} className="flex items-start gap-2">
            <Bot className="mt-0.5 h-4 w-4 text-forest-700" />
            <span className="text-ink">{e.message}</span>
          </li>
        ))}
      </ol>
    </Card>
  );
}
