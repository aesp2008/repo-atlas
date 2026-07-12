"use client";

import {
  Background,
  Controls,
  MiniMap,
  ReactFlow,
  useEdgesState,
  useNodesState,
  type Edge,
  type Node,
  type NodeMouseHandler,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { useCallback, useEffect, useMemo } from "react";
import { languageColor } from "@/lib/utils";
import type { GraphNode, GraphResponse } from "@/types";

interface DependencyGraphProps {
  graph: GraphResponse;
  onNodeSelect?: (node: GraphNode) => void;
  selectedNodeId?: string | null;
}

function layoutNodes(nodes: GraphNode[]): Node[] {
  const cols = Math.ceil(Math.sqrt(nodes.length));
  return nodes.map((node, index) => {
    const row = Math.floor(index / cols);
    const col = index % cols;
    const risk = node.risk_score;
    const borderColor =
      risk >= 70 ? "#ef4444" : risk >= 40 ? "#f59e0b" : languageColor(node.language);

    return {
      id: node.id,
      position: { x: col * 220, y: row * 100 },
      data: { label: node.label, node },
      style: {
        background: node.is_entry_point ? "#064e3b" : "#111827",
        border: `2px solid ${borderColor}`,
        borderRadius: 8,
        padding: "8px 12px",
        color: "#f3f4f6",
        fontSize: 11,
        minWidth: 120,
      },
    };
  });
}

export function DependencyGraph({ graph, onNodeSelect, selectedNodeId }: DependencyGraphProps) {
  const initialNodes = useMemo(() => layoutNodes(graph.nodes), [graph.nodes]);
  const initialEdges: Edge[] = useMemo(
    () =>
      graph.edges.map((e) => ({
        id: e.id,
        source: e.source,
        target: e.target,
        label: e.label,
        animated: true,
        style: { stroke: "#6366f1", strokeWidth: 1.5 },
        labelStyle: { fill: "#9ca3af", fontSize: 9 },
      })),
    [graph.edges]
  );

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  useEffect(() => {
    setNodes(layoutNodes(graph.nodes));
    setEdges(
      graph.edges.map((e) => ({
        id: e.id,
        source: e.source,
        target: e.target,
        label: e.label,
        animated: true,
        style: { stroke: "#6366f1", strokeWidth: 1.5 },
        labelStyle: { fill: "#9ca3af", fontSize: 9 },
      }))
    );
  }, [graph, setNodes, setEdges]);

  useEffect(() => {
    setNodes((nds) =>
      nds.map((n) => ({
        ...n,
        style: {
          ...n.style,
          boxShadow: n.id === selectedNodeId ? "0 0 20px rgba(99,102,241,0.6)" : undefined,
        },
      }))
    );
  }, [selectedNodeId, setNodes]);

  const onNodeClick: NodeMouseHandler = useCallback(
    (_event, node) => {
      const graphNode = (node.data as { node: GraphNode }).node;
      onNodeSelect?.(graphNode);
    },
    [onNodeSelect]
  );

  if (graph.nodes.length === 0) {
    return (
      <div className="h-[500px] flex items-center justify-center text-atlas-muted">
        No dependency graph data. Scan a repository with import relationships.
      </div>
    );
  }

  return (
    <div className="h-[500px] rounded-xl overflow-hidden border border-atlas-border">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        fitView
        proOptions={{ hideAttribution: true }}
      >
        <Background color="#1f2937" gap={20} />
        <Controls />
        <MiniMap
          nodeColor={(n) => {
            const gn = (n.data as { node?: GraphNode })?.node;
            if (!gn) return "#6366f1";
            const score = gn.risk_score;
            if (score >= 70) return "#ef4444";
            if (score >= 40) return "#f59e0b";
            return languageColor(gn.language);
          }}
          maskColor="rgba(10, 14, 23, 0.8)"
        />
      </ReactFlow>
    </div>
  );
}
