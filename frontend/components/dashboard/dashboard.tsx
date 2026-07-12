"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Map, Shield } from "lucide-react";
import { useMemo, useState } from "react";
import { CircularDeps } from "@/components/dashboard/circular-deps";
import { DetailPanel } from "@/components/dashboard/detail-panel";
import { EndpointsTable } from "@/components/dashboard/endpoints-table";
import { FileExplorer } from "@/components/dashboard/file-explorer";
import { HotspotsTable } from "@/components/dashboard/hotspots-table";
import { OverviewCards } from "@/components/dashboard/overview-cards";
import { ScanForm } from "@/components/dashboard/scan-form";
import { DependencyGraph } from "@/components/graph/dependency-graph";
import { Card, CardTitle } from "@/components/ui/card";
import {
  getEndpoints,
  getFiles,
  getGraph,
  getHotspots,
  getProject,
  scanProject,
} from "@/lib/api";
import type { GraphNode, ProjectDetail } from "@/types";

interface DashboardProps {
  initialProject?: ProjectDetail | null;
}

export function Dashboard({ initialProject = null }: DashboardProps) {
  const queryClient = useQueryClient();
  const [projectId, setProjectId] = useState<number | null>(initialProject?.id ?? null);
  const [selectedPath, setSelectedPath] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const scanMutation = useMutation({
    mutationFn: ({ path, name }: { path: string; name?: string }) => scanProject(path, name),
    onSuccess: (project) => {
      setProjectId(project.id);
      setError(null);
      queryClient.invalidateQueries({ queryKey: ["project", project.id] });
    },
    onError: (err: Error) => setError(err.message),
  });

  const { data: project } = useQuery({
    queryKey: ["project", projectId],
    queryFn: () => getProject(projectId!),
    enabled: projectId !== null,
    initialData: initialProject ?? undefined,
  });

  const { data: graph } = useQuery({
    queryKey: ["graph", projectId],
    queryFn: () => getGraph(projectId!),
    enabled: projectId !== null,
  });

  const { data: files = [] } = useQuery({
    queryKey: ["files", projectId],
    queryFn: () => getFiles(projectId!),
    enabled: projectId !== null,
  });

  const { data: endpoints = [] } = useQuery({
    queryKey: ["endpoints", projectId],
    queryFn: () => getEndpoints(projectId!),
    enabled: projectId !== null,
  });

  const { data: hotspots = [] } = useQuery({
    queryKey: ["hotspots", projectId],
    queryFn: () => getHotspots(projectId!),
    enabled: projectId !== null,
  });

  const selectedNode = useMemo(
    () => graph?.nodes.find((n) => n.id === selectedPath) ?? null,
    [graph, selectedPath]
  );
  const selectedFile = useMemo(
    () => files.find((f) => f.relative_path === selectedPath) ?? null,
    [files, selectedPath]
  );
  const selectedHotspot = useMemo(
    () => hotspots.find((h) => h.file_path === selectedPath) ?? null,
    [hotspots, selectedPath]
  );

  const handleNodeSelect = (node: GraphNode) => setSelectedPath(node.id);

  return (
    <div className="space-y-6">
      <ScanForm
        onScan={(path, name) => scanMutation.mutate({ path, name })}
        isLoading={scanMutation.isPending}
      />

      {error && (
        <div className="glass rounded-xl p-4 border border-red-500/40 text-red-300 text-sm">
          {error}
        </div>
      )}

      {project && (
        <>
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold">{project.name}</h2>
              <p className="text-xs text-atlas-muted font-mono mt-1">{project.path}</p>
            </div>
            <div className="flex items-center gap-2 text-xs text-atlas-muted">
              <Shield className="w-4 h-4 text-emerald-400" />
              Local-only · No code uploaded
            </div>
          </div>

          <OverviewCards project={project} />

          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
            <Card className="xl:col-span-2">
              <div className="flex items-center gap-2 mb-4">
                <Map className="w-5 h-5 text-atlas-accent" />
                <CardTitle>Architecture & Dependency Graph</CardTitle>
              </div>
              {graph && (
                <DependencyGraph
                  graph={graph}
                  onNodeSelect={handleNodeSelect}
                  selectedNodeId={selectedPath}
                />
              )}
            </Card>

            <Card>
              <CardTitle className="mb-4">File Explorer</CardTitle>
              <FileExplorer
                files={files}
                onSelect={setSelectedPath}
                selectedPath={selectedPath}
              />
            </Card>
          </div>

          {(selectedNode || selectedFile || selectedHotspot) && (
            <DetailPanel
              node={selectedNode}
              file={selectedFile}
              hotspot={selectedHotspot}
              onClose={() => setSelectedPath(null)}
            />
          )}

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardTitle className="mb-4">API Endpoints</CardTitle>
              <EndpointsTable endpoints={endpoints} />
            </Card>

            <Card>
              <CardTitle className="mb-4">Risk Hotspots</CardTitle>
              <HotspotsTable
                hotspots={hotspots}
                onSelect={setSelectedPath}
                selectedPath={selectedPath}
              />
            </Card>
          </div>

          <Card>
            <CardTitle className="mb-4">Circular Dependencies</CardTitle>
            <CircularDeps cycles={graph?.circular_dependencies ?? []} />
          </Card>
        </>
      )}
    </div>
  );
}
