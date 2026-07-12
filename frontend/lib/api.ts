import type {
  EndpointItem,
  FileItem,
  GraphResponse,
  HotspotItem,
  ProjectDetail,
  ProjectSummary,
} from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed: ${response.status}`);
  }

  return response.json();
}

export async function scanProject(path: string, name?: string): Promise<ProjectDetail> {
  return fetchJson<ProjectDetail>("/api/projects/scan", {
    method: "POST",
    body: JSON.stringify({ path, name }),
  });
}

export async function listProjects(): Promise<ProjectSummary[]> {
  return fetchJson<ProjectSummary[]>("/api/projects");
}

export async function getProject(id: number): Promise<ProjectDetail> {
  return fetchJson<ProjectDetail>(`/api/projects/${id}`);
}

export async function getGraph(id: number): Promise<GraphResponse> {
  return fetchJson<GraphResponse>(`/api/projects/${id}/graph`);
}

export async function getFiles(id: number): Promise<FileItem[]> {
  return fetchJson<FileItem[]>(`/api/projects/${id}/files`);
}

export async function getEndpoints(id: number): Promise<EndpointItem[]> {
  return fetchJson<EndpointItem[]>(`/api/projects/${id}/endpoints`);
}

export async function getHotspots(id: number): Promise<HotspotItem[]> {
  return fetchJson<HotspotItem[]>(`/api/projects/${id}/hotspots`);
}

export async function checkHealth(): Promise<{ status: string }> {
  return fetchJson<{ status: string }>("/health");
}
