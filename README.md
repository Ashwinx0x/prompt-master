# Prompt Master

**Universal prompt engineering for any LLM.**

Prompt Master turns a rough request into a clear, robust, provider-neutral prompt that can be used with ChatGPT, Claude, Gemini, Copilot, Cursor, local models, or other LLMs.

## Design goals

- **Universal:** optimize the task, not a single vendor.
- **Outcome-first:** preserve what the user actually wants.
- **Minimal assumptions:** identify missing information instead of inventing it.
- **Structured:** separate objective, context, constraints, inputs, process, and output.
- **Efficient:** remove filler and redundant instructions.
- **Practical:** produce copy-ready prompts, not prompt-theory lectures.
- **Extensible:** support coding, SQL/data, research, writing, analysis, creative work, image generation, and agent workflows.

## Pipeline

`request → classify → completeness audit → strategy → construct → compress → lint → render`

The core package is intentionally provider-neutral. An LLM-backed optimizer can be added later without changing the prompt representation or validation layer.

## Quick start

```bash
pip install -e .
prompt-master "Create a SQL query to find customers with more than 3 orders"
```

Or:

```bash
python -m prompt_master.cli "Explain this Python error and give me a production-safe fix"
```

## Modes

`auto`, `coding`, `sql`, `data`, `research`, `writing`, `analysis`, `creative`, `image`, `agent`

## Example

Input:

> make this SQL faster

Output will identify the missing context and produce a useful prompt with explicit placeholders rather than pretending to know the schema, engine, data volume, or current query.

## Roadmap

- [x] Provider-neutral prompt IR
- [x] Task classification
- [x] Completeness and assumption audit
- [x] Prompt construction and linting
- [x] CLI
- [x] Tests and CI
- [ ] LLM-backed semantic optimizer adapters
- [ ] MCP server
- [ ] VS Code extension
- [ ] Web UI
- [ ] Prompt evaluation / A-B testing
- [ ] Prompt versioning and telemetry-free local history

## Philosophy

A better prompt is not necessarily a longer prompt. Prompt Master aims for **the smallest prompt that reliably communicates the user's intent and quality bar**.

## License

MIT
