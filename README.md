# Prompt Master

**Universal prompt engineering for any LLM.**

Prompt Master turns a rough request into a clear, robust, provider-neutral prompt that can be used with ChatGPT, Claude, Gemini, Copilot, Cursor, local models, or other LLMs.

## Why this version matters

Prompt Master **0.2.0** adds a deterministic quality/safety layer. It can now lint generated prompts for missing output direction, missing constraints, excessive length, and possible credential leakage—without sending prompt content to an external service.

## Design goals

- **Universal:** optimize the task, not a single vendor.
- **Outcome-first:** preserve what the user actually wants.
- **Minimal assumptions:** identify missing information instead of inventing it.
- **Structured:** separate objective, context, constraints, inputs, process, and output.
- **Efficient:** remove filler and redundant instructions.
- **Safe by default:** flag likely secrets and treat missing context as uncertainty.
- **Extensible:** support coding, SQL/data, research, writing, analysis, creative work, image generation, and agent workflows.

## Pipeline

`request → classify → completeness audit → strategy → construct → compress → lint → render`

The core package is intentionally provider-neutral. Semantic optimization can later be connected through pluggable LLM adapters without changing the prompt representation or validation layer.

## Quick start

```bash
pip install -e .
prompt-master "Create a SQL query to find customers with more than 3 orders"
```

Run quality and safety checks:

```bash
prompt-master "Create a SQL query to find customers with more than 3 orders" --lint
```

For automation and CI pipelines:

```bash
prompt-master "Explain this Python error and give me a production-safe fix" --lint --json
```

## Modes

`auto`, `coding`, `sql`, `data`, `research`, `writing`, `analysis`, `creative`, `image`, `agent`

## Example

Input:

> make this SQL faster

Output identifies the missing context and produces a useful prompt with explicit clarification points rather than pretending to know the schema, engine, data volume, or current query.

## Roadmap

- [x] Provider-neutral prompt IR
- [x] Task classification
- [x] Completeness and assumption audit
- [x] Prompt construction
- [x] Deterministic linting and secret detection
- [x] CLI and JSON output
- [x] Tests and CI
- [ ] Pluggable LLM-backed semantic optimizer
- [ ] Prompt evaluation / A-B testing
- [ ] MCP server
- [ ] VS Code extension
- [ ] Web UI
- [ ] Prompt versioning and telemetry-free local history

## Philosophy

A better prompt is not necessarily a longer prompt. Prompt Master aims for **the smallest prompt that reliably communicates the user's intent and quality bar**.

## License

MIT
