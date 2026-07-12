# Contributing to RepoAtlas

Thank you for your interest in contributing! RepoAtlas is designed as a portfolio-quality open-source project.

## Getting Started

1. Fork the repository
2. Clone locally
3. Run `make install`
4. Run `make dev` to start backend + frontend
5. Run `make test` before submitting changes

## Development Setup

```bash
cp .env.example .env
make install
make dev
```

Backend API docs: http://localhost:8000/docs  
Frontend dashboard: http://localhost:3000

## Code Style

### Python
- Use type hints on all public functions
- Follow existing module boundaries (`scanner/`, `parsers/`, `graph/`, etc.)
- Run `pytest -v` before submitting

### TypeScript
- Strict mode enabled
- Use existing component patterns in `components/`
- Run `npm test` before submitting

## Pull Request Guidelines

1. Keep PRs focused — one feature or fix per PR
2. Include tests for new parsing or analysis logic
3. Update docs if adding API endpoints or changing behavior
4. Ensure `make test` passes

## Adding a New Language Parser

1. Create `backend/app/services/parsers/{lang}_parser.py`
2. Implement `parse_{lang}_file()` returning `ParsedFile`
3. Add import resolution logic
4. Register in `repository_scanner.py`
5. Add tests in `backend/tests/`
6. Add sample files to `demo/sample-repo/`

## Reporting Issues

Include:
- Steps to reproduce
- Expected vs actual behavior
- Sample file snippets (no proprietary code)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
