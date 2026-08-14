"use client";

import { Loader2 } from "lucide-react";
import { cn } from "@/lib/cn";

export function Button({
  className,
  variant = "primary",
  loading,
  children,
  ...props
}: React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "ghost" | "outline" | "danger";
  loading?: boolean;
}) {
  const base =
    "inline-flex items-center justify-center gap-2 rounded-md px-4 py-2 text-sm font-medium transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-60";
  const variants = {
    primary: "bg-forest-900 text-white hover:bg-forest-700 shadow-sm",
    secondary: "bg-moss-100 text-forest-900 hover:bg-moss-200",
    outline: "border border-forest-900/20 bg-white text-forest-900 hover:bg-moss-50",
    ghost: "text-forest-900 hover:bg-moss-100",
    danger: "bg-red-700 text-white hover:bg-red-800",
  };
  return (
    <button className={cn(base, variants[variant], className)} disabled={loading || props.disabled} {...props}>
      {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
      {children}
    </button>
  );
}

export function Card({
  className,
  children,
  title,
  subtitle,
  action,
}: {
  className?: string;
  children: React.ReactNode;
  title?: React.ReactNode;
  subtitle?: React.ReactNode;
  action?: React.ReactNode;
}) {
  return (
    <section className={cn("rounded-xl border border-ink/10 bg-white p-5 shadow-soft transition-all duration-300 hover:shadow-lift", className)}>
      {(title || action) && (
        <div className="mb-4 flex items-start justify-between gap-3">
          <div>
            {title && <h3 className="text-base font-semibold text-ink">{title}</h3>}
            {subtitle && <p className="mt-0.5 text-sm text-ink-muted">{subtitle}</p>}
          </div>
          {action}
        </div>
      )}
      {children}
    </section>
  );
}

export function StatCard({
  label,
  value,
  hint,
  tone = "default",
}: {
  label: string;
  value: React.ReactNode;
  hint?: string;
  tone?: "default" | "accent" | "success";
}) {
  return (
    <div
      className={cn(
        "rounded-xl border border-ink/10 p-5 transition-all duration-300 hover:-translate-y-1 hover:shadow-lift",
        tone === "accent" && "border-forest-900/20 bg-forest-900 text-white",
        tone === "success" && "border-lime-400/40 bg-moss-100",
        tone === "default" && "bg-white"
      )}
    >
      <p className={cn("text-xs font-medium uppercase tracking-wide", tone === "accent" ? "text-lime-400" : "text-ink-muted")}>
        {label}
      </p>
      <p className={cn("mt-2 text-2xl font-semibold", tone === "accent" ? "text-white" : "text-ink")}>{value}</p>
      {hint && <p className={cn("mt-1 text-xs", tone === "accent" ? "text-white/70" : "text-ink-muted")}>{hint}</p>}
    </div>
  );
}

export function Input(props: React.InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      {...props}
      className={cn(
        "w-full rounded-md border border-ink/15 bg-white px-3 py-2 text-sm text-ink placeholder:text-ink-muted/70 focus:border-forest-700 focus:outline-none focus:ring-2 focus:ring-forest-700/20",
        props.className
      )}
    />
  );
}

export function Select(props: React.SelectHTMLAttributes<HTMLSelectElement>) {
  return (
    <select
      {...props}
      className={cn(
        "w-full rounded-md border border-ink/15 bg-white px-3 py-2 text-sm text-ink focus:border-forest-700 focus:outline-none focus:ring-2 focus:ring-forest-700/20",
        props.className
      )}
    />
  );
}

export function Textarea(props: React.TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      {...props}
      className={cn(
        "w-full rounded-md border border-ink/15 bg-white px-3 py-2 text-sm text-ink placeholder:text-ink-muted/70 focus:border-forest-700 focus:outline-none focus:ring-2 focus:ring-forest-700/20",
        props.className
      )}
    />
  );
}

export function Field({ label, children, hint }: { label: string; children: React.ReactNode; hint?: string }) {
  return (
    <div className="space-y-1.5">
      <label className="block text-sm font-medium text-ink">{label}</label>
      {children}
      {hint && <p className="text-xs text-ink-muted">{hint}</p>}
    </div>
  );
}

export function Badge({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <span className={cn("inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium", className)}>
      {children}
    </span>
  );
}

export function StatusPill({ status }: { status: string }) {
  const color =
    status === "available" || status === "match_found" || status === "deal_confirmed"
      ? "bg-moss-100 text-forest-900"
      : status === "completed" || status === "collected"
        ? "bg-forest-900 text-white"
        : status === "offer_rejected" || status === "cancelled"
          ? "bg-red-100 text-red-800"
          : "bg-parchment text-ink";
  return <Badge className={color}>{status.replace(/_/g, " ")}</Badge>;
}

export function Spinner() {
  return (
    <div className="flex items-center justify-center py-16">
      <Loader2 className="h-6 w-6 animate-spin text-forest-900" />
    </div>
  );
}

export function EmptyState({ title, message }: { title: string; message?: string }) {
  return (
    <div className="rounded-xl border border-dashed border-ink/20 bg-white py-12 text-center">
      <p className="font-medium text-ink">{title}</p>
      {message && <p className="mt-1 text-sm text-ink-muted">{message}</p>}
    </div>
  );
}

export function Alert({ tone = "info", children }: { tone?: "info" | "success" | "error"; children: React.ReactNode }) {
  const styles = {
    info: "border-forest-900/20 bg-moss-50 text-forest-900",
    success: "border-lime-400/50 bg-moss-100 text-forest-900",
    error: "border-red-200 bg-red-50 text-red-800",
  };
  return <div className={cn("rounded-lg border px-4 py-3 text-sm", styles[tone])}>{children}</div>;
}