"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  ArrowLeft,
  Bot,
  Inbox,
  LayoutDashboard,
  Leaf,
  ListTree,
  LogOut,
  PackagePlus,
  Recycle,
  Users,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth";
import { cn } from "@/lib/cn";

const NAV: Record<string, Array<{ href: string; label: string; icon: React.ElementType }>> = {
  supplier: [
    { href: "/supplier/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { href: "/supplier/add-waste", label: "Add Waste", icon: PackagePlus },
    { href: "/supplier/matches", label: "Buyer Matches", icon: ListTree },
    { href: "/supplier/transactions", label: "Transactions", icon: Recycle },
    { href: "/supplier/messages", label: "Messages", icon: Inbox },
    { href: "/supplier/agent", label: "AI Agent Activity", icon: Bot },
  ],
  buyer: [
    { href: "/buyer/dashboard", label: "Dashboard", icon: LayoutDashboard },
    { href: "/buyer/requirements", label: "Requirements", icon: Users },
    { href: "/buyer/available", label: "Available Waste", icon: Leaf },
    { href: "/buyer/matches", label: "Matches", icon: ListTree },
    { href: "/buyer/transactions", label: "Transactions", icon: Recycle },
    { href: "/buyer/messages", label: "Messages", icon: Inbox },
  ],
  admin: [
    { href: "/admin", label: "Overview", icon: LayoutDashboard },
  ],
};

export function Shell({ children }: { children: React.ReactNode }) {
  const { user, token, clear } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);
  useEffect(() => {
    if (!mounted) return;
    if (!token || !user) {
      router.replace("/login");
      return;
    }
    const role = user.role;
    const prefix = `/${role}`;
    if (pathname && !pathname.startsWith(prefix)) {
      router.replace(`${prefix}/dashboard`);
    }
  }, [mounted, token, user, pathname, router]);

  if (!mounted) return null;

  if (!token || !user) return null;

  const nav = NAV[user.role] ?? [];

  const logout = () => {
    clear();
    router.replace("/");
  };

  return (
    <div className="flex min-h-screen bg-parchment">
      <aside className="hidden w-60 shrink-0 flex-col border-r border-ink/10 bg-forest-900 text-white md:flex">
        <Link href="/" className="flex items-center gap-2 px-5 py-5">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-lime-400 text-forest-950">
            <Recycle className="h-5 w-5" />
          </span>
          <span className="font-semibold tracking-wide">Waste2Worth</span>
        </Link>

        <nav className="flex-1 space-y-1 px-3 py-2">
          {nav.map((item) => {
            const active = pathname === item.href || pathname?.startsWith(`${item.href}/`);
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors",
                  active ? "bg-white/15 text-lime-400" : "text-white/75 hover:bg-white/10 hover:text-white"
                )}
              >
                <item.icon className="h-4 w-4" />
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="border-t border-white/15 px-4 py-4">
          <p className="text-sm font-medium">{user.name}</p>
          <p className="text-xs capitalize text-white/60">{user.role}</p>
          <button
            onClick={logout}
            className="mt-3 flex items-center gap-2 text-sm text-white/75 hover:text-white"
          >
            <LogOut className="h-4 w-4" /> Sign out
          </button>
        </div>
      </aside>

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex items-center justify-between border-b border-ink/10 bg-white px-5 py-3 md:hidden">
          <Link href="/" className="flex items-center gap-2 text-sm font-semibold text-forest-900">
            <Recycle className="h-4 w-4" /> Waste2Worth
          </Link>
          <button onClick={logout} className="text-xs text-ink-muted">
            Sign out
          </button>
        </header>

        <main className="flex-1 p-5 lg:p-8">{children}</main>

        <footer className="border-t border-ink/10 px-5 py-3 text-xs text-ink-muted">
          <Link href="/" className="inline-flex items-center gap-1 hover:text-forest-900">
            <ArrowLeft className="h-3 w-3" /> Back to home
          </Link>
        </footer>
      </div>
    </div>
  );
}