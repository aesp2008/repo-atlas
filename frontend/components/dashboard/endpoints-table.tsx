"use client";

import { Badge } from "@/components/ui/badge";
import { methodColor } from "@/lib/utils";
import type { EndpointItem } from "@/types";

interface EndpointsTableProps {
  endpoints: EndpointItem[];
}

export function EndpointsTable({ endpoints }: EndpointsTableProps) {
  if (endpoints.length === 0) {
    return (
      <p className="text-sm text-atlas-muted py-8 text-center">No API endpoints detected.</p>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-atlas-muted border-b border-atlas-border">
            <th className="pb-3 pr-4 font-medium">Method</th>
            <th className="pb-3 pr-4 font-medium">Path</th>
            <th className="pb-3 pr-4 font-medium">Framework</th>
            <th className="pb-3 pr-4 font-medium">File</th>
            <th className="pb-3 font-medium">Line</th>
          </tr>
        </thead>
        <tbody>
          {endpoints.map((ep) => (
            <tr key={ep.id} className="border-b border-atlas-border/50 hover:bg-atlas-border/20">
              <td className="py-3 pr-4">
                <Badge className={methodColor(ep.method)}>{ep.method}</Badge>
              </td>
              <td className="py-3 pr-4 font-mono text-indigo-300">{ep.path}</td>
              <td className="py-3 pr-4 capitalize">{ep.framework}</td>
              <td className="py-3 pr-4 font-mono text-xs text-atlas-muted">{ep.file_path}</td>
              <td className="py-3 text-atlas-muted">{ep.line_number}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
