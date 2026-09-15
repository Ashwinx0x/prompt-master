# Prompt Master

**Universal, provider-neutral prompt engineering for any LLM.**

Prompt Master turns a rough request into a structured, robust prompt that can be pasted into ChatGPT, Claude, Gemini, Copilot, Cursor, local models, or another LLM.

## 1.2.0 — faster core, stronger linting, deterministic compression

The deterministic core has **no runtime dependencies and no network calls**. It normalizes the request, classifies the task, audits missing context, constructs a practical prompt, lints quality/security issues locally, and can conservatively compress repeated instructions.

Semantic optimization is explicitly opt-in and uses an OpenAI-compatible endpoint only when requested.

### Pipeline

```text
rough request
    ↓
normalize → classify → completeness audit → construct → compress → lint → render
    ↓
(optional semantic optimizer)
    ↓
evaluate / compare
```

## GitHub is the source of truth

Prompt Master is maintained as a **versioned GitHub project**, not as a VS Code extension.

The intended model is:

```text
GitHub release/version
        ↓
clone that version into VS Code
        ↓
use the local workspace
        ↓
when a new release is wanted
        ↓
checkout the new GitHub version
```

GitHub owns the canonical source and version history. The VS Code folder is only a local copy of the selected version.

## Use a GitHub version in VS Code

### Latest development version

In VS Code:

1. Open **Command Palette** (`Ctrl+Shift+P`).
2. Choose **Git: Clone**.
3. Paste:

```text
https://github.com/Ashwinx0x/prompt-master.git
```

4. Choose the local folder.
5. Open the cloned `prompt-master` folder.

Terminal equivalent:

```bash
git clone https://github.com/Ashwinx0x/prompt-master.git
cd prompt-master
code .
```

### A specific released version

Use a Git tag when you want a stable, reproducible workspace:

```bash
git clone https://github.com/Ashwinx0x/prompt-master.git
cd prompt-master
git checkout v1.2.0
code .
```

The workspace is now pinned to that GitHub version. Verify it with:

```bash
prompt-master --version
```

**Recommended:** use a tagged release for normal use; use `main` only when you intentionally want development changes.

See **[VERSIONING.md](VERSIONING.md)** for the version policy.

## Install in the cloned workspace

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install:

```bash
python -m pip install -e .
```

For development/test tools:

```bash
python -m pip install -e ".[dev]"
```

## Updating the workspace

For the moving development branch:

```bash
git pull
```

For a version-controlled release workspace, explicitly select the next version:

```bash
git fetch --tags
git checkout v1.3.0
```

If packaging/dependencies changed, reinstall:

```bash
python -m pip install -e ".[dev]"
```

You do **not** need to maintain a second version system inside VS Code. GitHub tags and the package version are the source of truth.

## First commands

```bash
prompt-master "Create a BigQuery query to find customers with more than 3 orders"
pm "Explain this Python error and give me a production-safe fix"
python -m prompt_master "Rewrite this email to sound professional and polite"
```

### Lint

```bash
prompt-master "Create a SQL query to find customers with more than 3 orders" --lint
```

### Compress

```bash
prompt-master "Make this SQL request concise without losing requirements" --compress
```

Compression is deliberately conservative and local; it is not a proof of semantic equivalence.

### Evaluate

```bash
prompt-master "Make this SQL query faster" --evaluate
```

The local score measures prompt-construction quality, not model-answer correctness.

### Compare

```bash
prompt-master "Make this SQL query faster" --compare-with candidate.txt
```

### Force a mode

```bash
prompt-master "Make this query faster" --mode sql
prompt-master "Write a professional project update" --mode writing
prompt-master "Create a cinematic portrait prompt" --mode image
```

### JSON

```bash
prompt-master "Explain this Python error and give me a production-safe fix" --lint --evaluate --compress --json
```

### Stdin

```bash
echo "Make this SQL faster" | prompt-master --mode sql
```

### Optional semantic optimization

Set credentials only in the environment:

```powershell
$env:PROMPT_MASTER_API_KEY="your-key"
$env:PROMPT_MASTER_MODEL="gpt-4.1-mini"
```

Then explicitly opt in:

```bash
prompt-master "Rewrite this technical request to be clearer" --semantic
```

Use `PROMPT_MASTER_BASE_URL` for an OpenAI-compatible endpoint. Semantic mode is not enabled by default.

## Supported modes

`auto`, `coding`, `sql`, `data`, `research`, `writing`, `analysis`, `creative`, `image`, `agent`

## Python API

```python
from prompt_master import compress, compare, evaluate, optimize

result = optimize("Create a BigQuery query to find duplicate customer IDs")
print(result.rendered)
print(result.prompt.mode)

compressed = compress(result.rendered)
print(compressed.compressed)

assessment = evaluate(result.rendered)
print(assessment.score)

comparison = compare("Tell me about SQL", result.rendered)
print(comparison.winner, comparison.margin)
```

## Architecture

```text
src/prompt_master/
├── core.py           # optimization, normalization, rendering, adapters
├── classification.py # cached, explainable task classification
├── audit.py          # completeness / missing-context audit
├── compression.py    # conservative local compression
├── evaluation.py     # local scoring and A/B comparison
├── adapters.py       # optional LLM adapter protocol
├── schemas.py        # portable prompt/result models
├── lint.py           # local quality and secret checks
├── cli.py            # prompt-master / pm CLI
└── __main__.py       # python -m prompt_master
```

## Development

```bash
python -m pytest
python -m build
```

Python **3.10+** is supported. There are no required runtime dependencies.

## Roadmap

### Completed through Phase 4

- [x] Provider-neutral prompt IR
- [x] Explainable task classification and confidence/signals
- [x] Completeness and assumption audit
- [x] Prompt construction and rendering
- [x] Deterministic linting and local secret detection
- [x] Deeper lint checks for duplicates, conflicts, vague references, and question-heavy prompts
- [x] Fast deterministic pipeline with shared normalization
- [x] Conservative deterministic compression
- [x] CLI, `pm` alias, stdin, JSON, lint, compression, evaluation
- [x] Optional semantic optimizer and provider-neutral adapter protocol
- [x] Local evaluation rubric and A/B comparison
- [x] Packaging, tests, and CI foundation

### Next

- [ ] Semantic evaluation against actual model outputs
- [ ] MCP server
- [ ] Web UI
- [ ] GitHub release/tag automation
- [ ] Telemetry-free local prompt history
- [ ] Optional smart routing

## Philosophy

A better prompt is not necessarily a longer prompt. Prompt Master aims for **the smallest prompt that reliably communicates the user's intent and quality bar**.

## License

MIT — see [LICENSE](LICENSE).
