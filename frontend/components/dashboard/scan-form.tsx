"use client";

import { Loader2, ScanSearch } from "lucide-react";
import { useState } from "react";

interface ScanFormProps {
  onScan: (path: string, name?: string) => void;
  isLoading: boolean;
  defaultPath?: string;
}

export function ScanForm({ onScan, isLoading, defaultPath = "demo/sample-repo" }: ScanFormProps) {
  const [path, setPath] = useState(defaultPath);
  const [name, setName] = useState("");

  return (
    <form
      className="glass rounded-xl p-6 flex flex-col gap-4"
      onSubmit={(e) => {
        e.preventDefault();
        onScan(path, name || undefined);
      }}
    >
      <div className="flex items-center gap-2">
        <ScanSearch className="w-5 h-5 text-atlas-accent" />
        <h2 className="text-lg font-semibold">Scan Repository</h2>
      </div>
      <p className="text-sm text-atlas-muted">
        Enter a local path to analyze. RepoAtlas only reads files on your machine — nothing is uploaded.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-xs text-atlas-muted mb-1">Repository Path</label>
          <input
            type="text"
            value={path}
            onChange={(e) => setPath(e.target.value)}
            placeholder="demo/sample-repo"
            className="w-full bg-atlas-bg border border-atlas-border rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-atlas-accent/50"
            required
          />
        </div>
        <div>
          <label className="block text-xs text-atlas-muted mb-1">Display Name (optional)</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="My Project"
            className="w-full bg-atlas-bg border border-atlas-border rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-atlas-accent/50"
          />
        </div>
      </div>
      <div className="flex gap-3">
        <button
          type="submit"
          disabled={isLoading}
          className="inline-flex items-center gap-2 bg-atlas-accent hover:bg-atlas-accentHover disabled:opacity-50 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition-colors"
        >
          {isLoading && <Loader2 className="w-4 h-4 animate-spin" />}
          {isLoading ? "Scanning..." : "Start Scan"}
        </button>
        <button
          type="button"
          onClick={() => {
            setPath("demo/sample-repo");
            setName("Demo Sample Repo");
            onScan("demo/sample-repo", "Demo Sample Repo");
          }}
          disabled={isLoading}
          className="px-5 py-2.5 rounded-lg text-sm font-medium border border-atlas-border hover:bg-atlas-border/50 transition-colors disabled:opacity-50"
        >
          Run Demo
        </button>
      </div>
    </form>
  );
}
