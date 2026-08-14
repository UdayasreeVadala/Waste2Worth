"use client";

import { Bot, FlaskConical, Leaf, Recycle, Sparkles, Sprout } from "lucide-react";
import { cn } from "@/lib/cn";

const FACES = [Recycle, Leaf, Sparkles, FlaskConical, Sprout, Bot];

export function Cube3D({ size = 120 }: { size?: number }) {
  const half = size / 2;
  const transforms = [
    `translateZ(${half}px)`,
    `rotateY(90deg) translateZ(${half}px)`,
    `rotateY(180deg) translateZ(${half}px)`,
    `rotateY(270deg) translateZ(${half}px)`,
    `rotateX(90deg) translateZ(${half}px)`,
    `rotateX(-90deg) translateZ(${half}px)`,
  ];

  return (
    <div className="perspective-1200" style={{ perspective: size * 6 }}>
      <div
        className="anim-spin-slow preserve-3d relative"
        style={{ width: size, height: size, animationDuration: "18s" }}
      >
        {transforms.map((t, i) => {
          const Icon = FACES[i];
          return (
            <div
              key={i}
              className="preserve-3d absolute inset-0 flex items-center justify-center rounded-lg border border-white/20 bg-forest-900/70 backdrop-blur-md"
              style={{ transform: t, boxShadow: "0 0 24px rgb(182 216 122 / 0.25) inset" }}
            >
              <Icon
                className={cn("text-lime-400")}
                style={{ width: size * 0.42, height: size * 0.42, transform: "translateZ(1px)" }}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
}
