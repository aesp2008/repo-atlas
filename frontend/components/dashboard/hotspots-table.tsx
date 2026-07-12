"use client";

import { riskBg, riskColor } from "@/lib/utils";
import type { HotspotItem } from "@/types";

interface HotspotsTableProps {
  hotspots: HotspotItem[];
  onSelect?: (filePath: string) => void;
  selectedPath?: string | null;
}

export function HotspotsTable({ hotspots, onSelect, selectedPath }: HotspotsTableProps) {
  if (hotspots.length === 0) {
    return (
      <p className="text-sm text-atlas-muted py-8 text-center">No hotspot data available.</p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-atlas-muted border-b border-atlas-border">
            <th className="pb-3 pr-4 font-medium">File</th>
            <th className="pb-3 pr-4 font-medium">Risk</th>
            <th className="pb-3 pr-4 font-medium">LOC</th>
            <th className="pb-3 pr-4 font-medium">Imports</th>
            <th className="pb-3 pr-4 font-medium">Dependents</th>
            <th className="pb-3 font-medium">Explanation</th>
          </tr>
        </thead>
        <tbody>
          {hotspots.map((h) => (
            <tr
              key={h.file_path}
              onClick={() => onSelect?.(h.file_path)}
              className={`border-b border-atlas-border/50 cursor-pointer hover:bg-atlas-border/20 ${
                selectedPath === h.file_path ? "bg-atlas-accent/10" : ""
              }`}
            >
              <td className="py-3 pr-4 font-mono text-xs">{h.file_path}</td>
              <td className={`py-3 pr-4 font-bold ${riskColor(h.risk_score)}`}>
                {h.risk_score.toFixed(0)}
              </td>
              <td className="py-3 pr-4">{h.lines_of_code}</td>
              <td className="py-3 pr-4">{h.import_count}</td>
              <td className="py-3 pr-4">{h.dependent_count}</td>
              <td className="py-3 text-xs text-atlas-muted max-w-xs truncate">{h.risk_explanation}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
