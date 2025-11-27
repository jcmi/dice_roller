# Repository Guidelines

This repository holds a Python dice-roller tool. Follow the structure and practices below to keep contributions consistent and ready for Python 3.13.

## Project Structure & Module Organization
- Place application code in `src/`; keep the CLI entrypoint in `src/cli.py` and reusable logic in `src/lib/` (e.g., `roller.py` for dice math, `parser.py` for input handling).
- Mirror code with tests in `tests/` using the same filenames (`test_roller.py`), and put fixtures under `tests/fixtures/`.
- Assets such as sample configs or docs images belong in `assets/`; avoid committing generated binaries.

## Build, Test, and Development Commands
- `python3.13 -m venv .venv && source .venv/bin/activate` — create and enter the project virtual environment.
- `pip install -e .[dev]` — install the package and dev tools (pytest/ruff/black).
- `python -m pytest` — run unit tests; keep them fast and deterministic.
- `python -m ruff check .` and `python -m black .` — lint/format; ensure both are clean before pushing.
- `python -m build` — produce source and wheel distributions in `dist/`; run before publishing.

## Coding Style & Naming Conventions
- Target Python 3.13; use type hints and `from __future__ import annotations` when helpful.
- 4-space indentation; prefer snake_case for functions/variables, PascalCase for classes, and kebab-case for CLI scripts.
- Keep modules focused on a single concern; avoid large, stateful singletons.
- Ruff and Black are the formatting/linting source of truth; prefer autofix, then manual cleanup.

## Testing Guidelines
- Use pytest; name files `test_<module>.py` and describe behaviors, not implementations.
- Cover edge cases (min/max dice counts, invalid notation, seeded randomness); assert deterministic seeds.
- Add a regression test for every bug fix; avoid tests that depend on unseeded random output.

## Commit & Pull Request Guidelines
- Commits: imperative subjects (`Add roll notation parser`), concise scope, grouped by feature or fix.
- PRs: include a short summary, testing performed, screenshots/output for CLI help text, and links to related issues.
- Keep diffs small and focused; call out breaking changes explicitly.

## Security & Configuration Tips
- Keep secrets or API keys in `.env.local` and out of version control.
- Validate and sanitize all user input/flags; never eval untrusted strings.
- Remove dead code and unused dependencies to keep the CLI lean and auditable.
