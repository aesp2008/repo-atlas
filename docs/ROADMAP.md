# Roadmap

## v0.1 — MVP (Current)

- [x] Local repository scanner (Python, JS/TS)
- [x] Dependency graph with circular detection
- [x] API endpoint discovery (FastAPI, Flask, Express)
- [x] Risk hotspot scoring
- [x] Interactive React Flow dashboard
- [x] SQLite persistence
- [x] Demo repository
- [x] Docker & Makefile dev experience

## v0.2 — Enhanced Analysis

- [ ] Go, Rust, and Java import parsing
- [ ] Tree-sitter integration for robust JS/TS parsing
- [ ] Git history integration (churn, recency, author count)
- [ ] Test coverage overlay (pytest, jest coverage reports)
- [ ] Monorepo / workspace-aware module resolution

## v0.3 — Collaboration & Export

- [ ] Export reports as PDF/HTML
- [ ] Share scan snapshots (metadata only, no source)
- [ ] Compare scans over time (diff view)
- [ ] Team annotations on nodes

## v0.4 — Advanced Intelligence

- [ ] Blast-radius impact simulation ("what if I change this file?")
- [ ] Architecture layer detection (controller/service/repository)
- [ ] Dead code detection
- [ ] Config and env variable mapping

## v1.0 — Production Ready

- [ ] Plugin system for custom parsers
- [ ] CLI tool (`repo-atlas scan ./my-repo`)
- [ ] VS Code / Cursor extension
- [ ] Optional cloud sync (encrypted, opt-in only)

## Non-Goals (for now)

- AI-generated code summaries (deterministic analysis first)
- Remote repository cloning (local-first only)
- Code upload to external services
