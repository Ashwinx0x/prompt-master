# Changelog

## 1.0.0 — 2026-09-15

First all-rounder installable release.

### Added

- Provider-neutral prompt optimization engine.
- Automatic task classification across 9 practical modes.
- Explicit mode selection and validation.
- Completeness/clarification audit without inventing missing facts.
- Deterministic prompt rendering.
- Local quality and credential-leakage linting.
- Human-readable and JSON CLI output.
- `prompt-master` command and short `pm` alias.
- Stdin support for shell automation.
- `python -m prompt_master` entry point.
- Public Python API.
- Python 3.10–3.13 package metadata.
- Development extras for tests and package builds.
- MIT license, `.gitignore`, typed-package marker, and CI build verification.

### Design principle

The runtime remains dependency-free and does not send prompt content to an external service. Future LLM/MCP/VS Code integrations can be added as optional layers on top of the deterministic core.
