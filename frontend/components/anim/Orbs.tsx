import { cn } from "@/lib/cn";

const ORBS = [
  { className: "left-[-8%] top-[-6%] h-72 w-72 bg-lime-400/25", delay: "0s" },
  { className: "right-[-6%] top-[18%] h-96 w-96 bg-forest-500/30", delay: "-6s" },
  { className: "bottom-[-12%] left-[22%] h-80 w-80 bg-emerald-300/20", delay: "-12s" },
];

export function Orbs({ className }: { className?: string }) {
  return (
    <div className={cn("pointer-events-none absolute inset-0 overflow-hidden", className)} aria-hidden="true">
      {ORBS.map((o, i) => (
        <div key={i} className={cn("orb", o.className)} style={{ animationDelay: o.delay }} />
      ))}
    </div>
  );
}
