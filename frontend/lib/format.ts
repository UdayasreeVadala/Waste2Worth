export function money(value: number | null | undefined, currency: string = "INR"): string {
  if (value === null || value === undefined || Number.isNaN(value)) return "—";
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(value);
}

export function num(value: number | null | undefined): string {
  if (value === null || value === undefined) return "—";
  return new Intl.NumberFormat("en-IN").format(value);
}

const LABELS: Record<string, string> = {
  available: "Available",
  matched: "Matched",
  completed: "Completed",
  match_found: "Match found",
  waiting_for_supplier_approval: "Awaiting your approval",
  buyer_contacted: "Buyer contacted",
  offer_received: "Offer received",
  counter_offer_sent: "Counter offer sent",
  deal_confirmed: "Deal confirmed",
  pickup_scheduled: "Pickup scheduled",
  collected: "Collected",
  offer_rejected: "Offer rejected",
  cancelled: "Cancelled",
  limited: "Limited",
  unavailable: "Unavailable",
};

export function statusLabel(status: string | null | undefined): string {
  if (!status) return "—";
  return LABELS[status] ?? status.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export function dateLabel(value: string | null | undefined): string {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}