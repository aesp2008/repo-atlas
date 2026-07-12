"use client";

import { X } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { riskBg, riskColor } from "@/lib/utils";
import type { FileItem, GraphNode, HotspotItem } from "@/types";

interface DetailPanelProps {
  node: GraphNode | null;
  file: FileItem | null;
  hotspot: HotspotItem | null;
  onClose: () => void;
}

export function DetailPanel({ node, file, hotspot, onClose }: DetailPanelProps) {
  if (!node && !file && !hotspot) return null;

  const path = node?.id ?? file?.relative_path ?? hotspot?.file_path ?? "";

  return (
    <div className="glass rounded-xl p-5 border-l-4 border-l-atlas-accent">
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="font-semibold text-white">File Details</h3>
          <p className="font-mono text-xs text-atlas-muted mt-1 break-all">{path}</p>
        </div>
        <button onClick={onClose} className="p-1 hover:bg-atlas-border rounded">
          <X className="w-4 h-4" />
        </button>
      </div>

      <div className="grid grid-cols-2 gap-3 text-sm">
        {(node || file) && (
          <>
            <div>
              <span className="text-atlas-muted">Language</span>
              <p className="capitalize">{node?.language ?? file?.language}</p>
            </div>
            <div>
              <span className="text-atlas-muted">Entry Point</span>
              <p>{(node?.is_entry_point ?? file?.is_entry_point) ? "Yes" : "No"}</p>
            </div>
          </>
        )}
        {file && (
          <>
            <div>
              <span className="text-atlas-muted">Lines of Code</span>
              <p>{file.lines_of_code}</p>
            </div>
            <div>
              <span className="text-atlas-muted">Imports</span>
              <p>{file.import_count}</p>
            </div>
            <div>
              <span className="text-atlas-muted">Functions</span>
              <p>{file.function_count}</p>
            </div>
            <div>
              <span className="text-atlas-muted">Classes</span>
              <p>{file.class_count}</p>
            </div>
          </>
        )}
        {(hotspot || node) && (
          <>
            <div>
              <span className="text-atlas-muted">Risk Score</span>
              <p className={`font-bold ${riskColor(hotspot?.risk_score ?? node?.risk_score ?? 0)}`}>
                {(hotspot?.risk_score ?? node?.risk_score ?? 0).toFixed(0)} / 100
              </p>
            </div>
            <div>
              <span className="text-atlas-muted">Blast Radius</span>
              <p>{(hotspot?.blast_radius ?? node?.blast_radius ?? 0).toFixed(0)}</p>
            </div>
          </>
        )}
      </div>

      {hotspot && (
        <div className={`mt-4 p-3 rounded-lg border text-sm ${riskBg(hotspot.risk_score)}`}>
          {hotspot.risk_explanation}
        </div>
      )}

      {node?.is_entry_point && (
        <Badge className="mt-3 bg-emerald-500/20 text-emerald-300">Entry Point</Badge>
      )}
    </div>
  );
}
