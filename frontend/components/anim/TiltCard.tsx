"use client";

import { useRef, type ReactNode, type MouseEvent } from "react";
import { cn } from "@/lib/cn";

export function TiltCard({
  children,
  className,
  intensity = 10,
}: {
  children: ReactNode;
  className?: string;
  intensity?: number;
}) {
  const ref = useRef<HTMLDivElement>(null);

  function onMove(e: MouseEvent<HTMLDivElement>) {
    const el = ref.current;
    if (!el || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const rect = el.getBoundingClientRect();
    const px = (e.clientX - rect.left) / rect.width - 0.5;
    const py = (e.clientY - rect.top) / rect.height - 0.5;
    el.style.transform = `rotateX(${(-py * intensity).toFixed(2)}deg) rotateY(${(px * intensity).toFixed(2)}deg) translateY(-4px)`;
    el.classList.add("is-tilting");
  }

  function onLeave() {
    const el = ref.current;
    if (!el) return;
    el.style.transform = "";
    el.classList.remove("is-tilting");
  }

  return (
    <div className="perspective-1200">
      <div
        ref={ref}
        onMouseMove={onMove}
        onMouseLeave={onLeave}
        className={cn("tilt-card", className)}
      >
        {children}
      </div>
    </div>
  );
}
