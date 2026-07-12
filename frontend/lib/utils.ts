import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function riskColor(score: number): string {
  if (score >= 70) return "text-red-400";
  if (score >= 40) return "text-amber-400";
  return "text-emerald-400";
}

export function riskBg(score: number): string {
  if (score >= 70) return "bg-red-500/20 border-red-500/40";
  if (score >= 40) return "bg-amber-500/20 border-amber-500/40";
  return "bg-emerald-500/20 border-emerald-500/40";
}

export function languageColor(lang: string): string {
  const colors: Record<string, string> = {
    python: "#3776ab",
    typescript: "#3178c6",
    javascript: "#f7df1e",
  };
  return colors[lang] ?? "#6366f1";
}

export function methodColor(method: string): string {
  const colors: Record<string, string> = {
    GET: "bg-emerald-500/20 text-emerald-300",
    POST: "bg-blue-500/20 text-blue-300",
    PUT: "bg-amber-500/20 text-amber-300",
    PATCH: "bg-purple-500/20 text-purple-300",
    DELETE: "bg-red-500/20 text-red-300",
  };
  return colors[method.toUpperCase()] ?? "bg-gray-500/20 text-gray-300";
}
