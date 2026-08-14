import { Recycle } from "lucide-react";

export default function Loading() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-parchment">
      <span className="anim-spin-slow flex h-12 w-12 items-center justify-center rounded-xl bg-forest-900 text-lime-400">
        <Recycle className="h-6 w-6" />
      </span>
      <div className="h-1 w-40 overflow-hidden rounded-full bg-forest-900/10">
        <div className="anim-gradient h-full w-full rounded-full bg-gradient-to-r from-lime-400 via-forest-500 to-lime-400" />
      </div>
      <p className="font-display text-sm text-ink-muted">Finding the highest-value reuse pathway...</p>
    </div>
  );
}
