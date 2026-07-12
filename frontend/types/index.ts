export interface ScanRunSummary {
  id: number;
  status: string;
  files_scanned: number;
  started_at: string;
  completed_at: string | null;
}

export interface HotspotItem {
  file_path: string;
  risk_score: number;
  lines_of_code: number;
  import_count: number;
  dependent_count: number;
  function_count: number;
  class_count: number;
  cyclomatic_complexity: number;
  blast_radius: number;
  risk_explanation: string;
}

export interface ProjectSummary {
  id: number;
  name: string;
  path: string;
  created_at: string;
  updated_at: string;
  latest_scan: ScanRunSummary | null;
  file_count: number;
  endpoint_count: number;
  dependency_count: number;
  circular_dependency_count: number;
}

export interface ProjectDetail extends ProjectSummary {
  languages: string[];
  top_risky_files: HotspotItem[];
}

export interface FileItem {
  id: number;
  relative_path: string;
  language: string;
  size_bytes: number;
  lines_of_code: number;
  function_count: number;
  class_count: number;
  import_count: number;
  is_entry_point: boolean;
}

export interface EndpointItem {
  id: number;
  method: string;
  path: string;
  file_path: string;
  line_number: number;
  framework: string;
}

export interface GraphNode {
  id: string;
  label: string;
  language: string;
  risk_score: number;
  blast_radius: number;
  is_entry_point: boolean;
}

export interface GraphEdge {
  id: string;
  source: string;
  target: string;
  label: string;
}

export interface CircularDependency {
  cycle: string[];
}

export interface GraphResponse {
  nodes: GraphNode[];
  edges: GraphEdge[];
  circular_dependencies: CircularDependency[];
}
