"use client";

import { AlertCircle } from "lucide-react";
import type { CircularDependency } from "@/types";

interface CircularDepsProps {
  cycles: CircularDependency[];
}

export function CircularDeps({ cycles }: CircularDepsProps) {
  if (cycles.length === 0) {
    return (
      <div className="flex items-center gap-2 text-emerald-400 text-sm py-4">
        <span className="w-2 h-2 rounded-full bg-emerald-400" />
        No circular dependencies detected.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {cycles.map((cycle, idx) => (
        <div
          key={idx}
          className="flex items-start gap-3 p-4 rounded-lg bg-amber-500/10 border border-amber-500/30"
        >
          <AlertCircle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
          <div>
            <p className="text-sm font-medium text-amber-200 mb-1">Cycle {idx + 1}</p>
            <p className="font-mono text-xs text-atlas-muted break-all">
              {cycle.cycle.join(" → ")}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
}
