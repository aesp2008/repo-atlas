"use client";

import { FileCode, FolderOpen } from "lucide-react";
import { languageColor } from "@/lib/utils";
import type { FileItem } from "@/types";

interface FileExplorerProps {
  files: FileItem[];
  onSelect?: (path: string) => void;
  selectedPath?: string | null;
}

export function FileExplorer({ files, onSelect, selectedPath }: FileExplorerProps) {
  const sorted = [...files].sort((a, b) => a.relative_path.localeCompare(b.relative_path));

  return (
    <div className="space-y-1 max-h-96 overflow-y-auto">
      {sorted.map((file) => (
        <button
          key={file.id}
          onClick={() => onSelect?.(file.relative_path)}
          className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-left text-sm hover:bg-atlas-border/30 transition-colors ${
            selectedPath === file.relative_path ? "bg-atlas-accent/15 border border-atlas-accent/30" : ""
          }`}
        >
          <FileCode className="w-4 h-4 shrink-0" style={{ color: languageColor(file.language) }} />
          <span className="font-mono text-xs truncate flex-1">{file.relative_path}</span>
          {file.is_entry_point && (
            <span className="text-[10px] uppercase tracking-wide text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded">
              entry
            </span>
          )}
        </button>
      ))}
      {files.length === 0 && (
        <div className="flex flex-col items-center py-8 text-atlas-muted">
          <FolderOpen className="w-8 h-8 mb-2 opacity-50" />
          <p className="text-sm">No files scanned yet.</p>
        </div>
      )}
    </div>
  );
}
