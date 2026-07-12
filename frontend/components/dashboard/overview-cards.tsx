"use client";

import { AlertTriangle, FileCode, GitBranch, Globe, Layers, RefreshCw } from "lucide-react";
import { Card, CardTitle, CardValue } from "@/components/ui/card";
import type { ProjectDetail } from "@/types";

interface OverviewCardsProps {
  project: ProjectDetail;
}

export function OverviewCards({ project }: OverviewCardsProps) {
  const cards = [
    {
      title: "Files Scanned",
      value: project.file_count,
      icon: FileCode,
      color: "text-indigo-400",
    },
    {
      title: "Languages",
      value: project.languages.length,
      subtitle: project.languages.join(", ") || "—",
      icon: Layers,
      color: "text-cyan-400",
    },
    {
      title: "API Endpoints",
      value: project.endpoint_count,
      icon: Globe,
      color: "text-emerald-400",
    },
    {
      title: "Dependencies",
      value: project.dependency_count,
      icon: GitBranch,
      color: "text-violet-400",
    },
    {
      title: "Circular Deps",
      value: project.circular_dependency_count,
      icon: RefreshCw,
      color: project.circular_dependency_count > 0 ? "text-amber-400" : "text-emerald-400",
    },
    {
      title: "Top Risk Score",
      value: project.top_risky_files[0]?.risk_score?.toFixed(0) ?? "—",
      icon: AlertTriangle,
      color: "text-red-400",
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
      {cards.map((card) => (
        <Card key={card.title}>
          <div className="flex items-start justify-between">
            <CardTitle>{card.title}</CardTitle>
            <card.icon className={`w-4 h-4 ${card.color}`} />
          </div>
          <CardValue>{card.value}</CardValue>
          {"subtitle" in card && card.subtitle && (
            <p className="text-xs text-atlas-muted mt-1 truncate">{card.subtitle}</p>
          )}
        </Card>
      ))}
    </div>
  );
}
