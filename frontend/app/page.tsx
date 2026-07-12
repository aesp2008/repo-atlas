import { Dashboard } from "@/components/dashboard/dashboard";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-atlas-bg">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-900/20 via-atlas-bg to-atlas-bg pointer-events-none" />
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <header className="mb-10">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center text-white font-bold text-lg">
              R
            </div>
            <h1 className="text-3xl font-bold">
              <span className="gradient-text">RepoAtlas</span>
            </h1>
          </div>
          <p className="text-atlas-muted max-w-2xl">
            Understand unfamiliar codebases in minutes. Scan locally, visualize architecture,
            discover APIs, and identify risk hotspots — your code never leaves your machine.
          </p>
        </header>
        <Dashboard />
      </div>
    </main>
  );
}
