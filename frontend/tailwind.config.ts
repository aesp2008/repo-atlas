import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        atlas: {
          bg: "#0a0e17",
          surface: "#111827",
          border: "#1f2937",
          accent: "#6366f1",
          accentHover: "#818cf8",
          success: "#10b981",
          warning: "#f59e0b",
          danger: "#ef4444",
          muted: "#9ca3af",
        },
      },
      fontFamily: {
        sans: ["var(--font-geist-sans)", "system-ui", "sans-serif"],
        mono: ["var(--font-geist-mono)", "monospace"],
      },
      boxShadow: {
        glow: "0 0 40px rgba(99, 102, 241, 0.15)",
      },
    },
  },
  plugins: [],
};

export default config;
