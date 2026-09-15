# Prompt Master

**Universal, provider-neutral prompt engineering for any LLM.**

Prompt Master turns a rough request into a structured, robust prompt that can be pasted into ChatGPT, Claude, Gemini, Copilot, Cursor, local models, or another LLM.

## 1.0.0 — install once, use anywhere

Prompt Master is intentionally lightweight: the core package has **no runtime dependencies and no network calls**. The deterministic engine preserves the user's intent, identifies likely missing context, adds a practical quality bar, and can lint the original request for common quality and credential-leakage problems.

### What it does

`rough request → classify → completeness audit → construct → lint → render`

- **Universal:** provider-neutral output instead of vendor-specific syntax.
- **Outcome-first:** keeps the user's actual goal as the objective.
- **Minimal assumptions:** flags missing context instead of inventing facts.
- **Structured:** separates objective, context, constraints, approach, quality, and output.
- **Safe:** detects likely credentials locally; prompt text is not sent anywhere.
- **Practical:** supports coding, SQL/data, research, writing, analysis, creative, image, and agent tasks.
- **Automation-friendly:** human-readable Markdown or machine-readable JSON.

## Install in VS Code

You do **not** need to copy the files manually. Clone the repository into your PC and install it in editable mode:

```bash
git clone https://github.com/Ashwinx0x/prompt-master.git
cd prompt-master
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**

```cmd
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

Then install:

```bash
python -m pip install -e .
```

Or install development/test tools too:

```bash
python -m pip install -e ".[dev]"
```

After installation, open this folder in VS Code. The `prompt-master` command will be available in the activated terminal.

## First commands

```bash
prompt-master "Create a BigQuery query to find customers with more than 3 orders"
```

Short alias:

```bash
pm "Explain this Python error and give me a production-safe fix"
```

Module form also works:

```bash
python -m prompt_master "Rewrite this email to sound professional and polite"
```

### Lint a request

```bash
prompt-master "Create a SQL query to find customers with more than 3 orders" --lint
```

### Force a task mode

```bash
prompt-master "Make this query faster" --mode sql
prompt-master "Write a professional project update" --mode writing
prompt-master "Create a cinematic portrait prompt" --mode image
```

### JSON for scripts and automation

```bash
prompt-master "Explain this Python error and give me a production-safe fix" --lint --json
```

### Read from stdin

```bash
echo "Make this SQL faster" | prompt-master --mode sql
```

### Check the installed version

```bash
prompt-master --version
```

## Supported modes

`auto`, `coding`, `sql`, `data`, `research`, `writing`, `analysis`, `creative`, `image`, `agent`

## Python API

```python
from prompt_master import optimize, lint

result = optimize("Create a BigQuery query to find duplicate customer IDs")
print(result.rendered)
print(result.prompt.mode)
print(result.score)

issues = lint("Create a SQL query. api_key=sk-example1234567890")
for issue in issues:
    print(issue.code, issue.severity, issue.message)
```

## Example

Input:

> make this SQL faster

Prompt Master does not pretend to know the schema or query. It identifies SQL as the task, preserves the request, adds safe instructions, and asks for the missing query/schema or sample data when needed.

## Architecture

The project is split into small, dependency-free layers:

```text
src/prompt_master/
├── core.py       # classification, optimization, rendering
├── schemas.py    # portable Prompt / OptimizationResult models
├── lint.py       # local quality and secret checks
├── cli.py        # prompt-master / pm command line interface
└── __main__.py   # python -m prompt_master
```

This keeps the core provider-neutral. A future LLM adapter, MCP server, VS Code extension, or web UI can build on the same Prompt representation without changing the deterministic safety layer.

## Development

Run the test suite:

```bash
python -m pytest
```

Build the package locally:

```bash
python -m build
```

The project targets Python **3.10+** and has no runtime dependencies.

## Roadmap

The 1.0.0 foundation is complete. Future integrations can be added without making the core dependent on a specific AI provider:

- [x] Provider-neutral prompt IR
- [x] Task classification
- [x] Completeness and assumption audit
- [x] Prompt construction and Markdown rendering
- [x] Deterministic linting and local secret detection
- [x] CLI, `pm` alias, stdin, and JSON output
- [x] Python module entry point
- [x] Packaging metadata, MIT license, tests, and CI foundation
- [ ] Optional LLM-backed semantic optimizer
- [ ] Prompt evaluation / A-B testing
- [ ] MCP server
- [ ] VS Code extension
- [ ] Web UI
- [ ] Prompt versioning and telemetry-free local history

## Philosophy

A better prompt is not necessarily a longer prompt. Prompt Master aims for **the smallest prompt that reliably communicates the user's intent and quality bar**.

## License

MIT — see [LICENSE](LICENSE).
