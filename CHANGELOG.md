# Changelog

## 1.1.0 — 2026-09-15

Phases 1–3: smarter deterministic optimization, optional semantic optimization, and prompt evaluation.

### Added

- Explainable weighted task classification with confidence and matched signals.
- Deterministic completeness audit with mode-aware missing-context diagnostics.
- Optional LLM semantic optimizer through a provider-neutral adapter protocol.
- Stdlib OpenAI-compatible adapter with environment-based credentials and explicit opt-in.
- Deterministic local prompt evaluation rubric.
- Prompt A/B comparison with dimension-level reasons.
- CLI `--evaluate` and `--compare-with` options.
- JSON evaluation and comparison output.
- Expanded tests for classification and evaluation.

### Safety / design

- Deterministic mode remains offline and dependency-free.
- Semantic mode is opt-in and never enabled implicitly.
- Credentials are read from environment variables rather than stored in source.
- Evaluation scores prompt-construction quality; it does not claim to predict final model answer correctness.

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
