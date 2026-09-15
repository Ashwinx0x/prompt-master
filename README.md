# Prompt Master

**Universal, provider-neutral prompt engineering for any LLM.**

Prompt Master turns a rough request into a structured, robust prompt that can be pasted into ChatGPT, Claude, Gemini, Copilot, Cursor, local models, or another LLM.

## 1.2.0 — faster core, stronger linting, deterministic compression

Prompt Master is intentionally lightweight: the deterministic core has **no runtime dependencies and no network calls**. It preserves the user's intent, classifies the task, audits missing context, constructs a practical prompt, lints quality and credential-leakage problems locally, and can conservatively compress repeated instructions.

An **explicitly opt-in** semantic mode can then pass the generated prompt through an OpenAI-compatible endpoint. This is an optional layer; the deterministic core remains usable offline.

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

### What it does

- **Universal:** provider-neutral prompt structure instead of vendor-specific syntax.
- **Outcome-first:** keeps the user's actual goal as the objective.
- **Explainable classification:** exposes detected mode, confidence, and matching signals.
- **Minimal assumptions:** flags missing context instead of inventing facts.
- **Structured:** separates objective, context, constraints, approach, quality, and output.
- **Safe by default:** deterministic mode does not send prompt text anywhere; likely credentials are detected locally.
- **Fast local path:** classification patterns are compiled once and normalized text is reused across pipeline stages.
- **Stronger linting:** detects missing instructions, duplicates, conflicting length guidance, vague references, and question-heavy prompts.
- **Deterministic compression:** removes duplicate instruction lines and redundant whitespace without an LLM.
- **Optional semantic optimization:** use an OpenAI-compatible endpoint only when explicitly requested.
- **Local evaluation:** scores prompt-construction quality with an explainable rubric.
- **A/B comparison:** compare two prompt candidates and see which scores better and why.
- **Automation-friendly:** human-readable Markdown or machine-readable JSON.

## PC + VS Code User Manual

For the complete Windows/macOS/Linux setup guide, everyday workflow, troubleshooting, semantic-mode notes, and development commands, see **[USER_GUIDE.md](USER_GUIDE.md)**.

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
pm "Explain this Python error and give me a production-safe fix"
python -m prompt_master "Rewrite this email to sound professional and polite"
```

### Lint a request

```bash
prompt-master "Create a SQL query to find customers with more than 3 orders" --lint
```

### Compress the generated prompt

```bash
prompt-master "Make this SQL request concise without losing requirements" --compress
```

Compression is deliberately conservative and local. It reports before/after word counts and should be treated as a heuristic, not a proof of semantic equivalence.

### Evaluate the generated prompt

```bash
prompt-master "Make this SQL query faster" --evaluate
```

The local score measures prompt-construction properties such as explicit output, constraints, quality criteria, and structure. **It is not a guarantee of model answer correctness.**

### Compare against another prompt

Save a candidate prompt in `candidate.txt`, then:

```bash
prompt-master "Make this SQL query faster" --compare-with candidate.txt
```

Prompt Master compares the generated candidate (A) with the file candidate (B) using the same rubric.

### Force a task mode

```bash
prompt-master "Make this query faster" --mode sql
prompt-master "Write a professional project update" --mode writing
prompt-master "Create a cinematic portrait prompt" --mode image
```

### JSON for scripts and automation

```bash
prompt-master "Explain this Python error and give me a production-safe fix" --lint --evaluate --compress --json
```

### Read from stdin

```bash
echo "Make this SQL faster" | prompt-master --mode sql
```

### Optional semantic optimization

Set credentials only in your environment, never in the repository:

```powershell
$env:PROMPT_MASTER_API_KEY="your-key"
$env:PROMPT_MASTER_MODEL="gpt-4.1-mini"
```

Then explicitly opt in:

```bash
prompt-master "Rewrite this technical request to be clearer" --semantic
```

You can point the adapter at an OpenAI-compatible endpoint with `PROMPT_MASTER_BASE_URL`. This can also be used with compatible local servers. Semantic mode is intentionally **not** enabled by default.

**Performance note:** the default deterministic path is local and avoids network latency. `--semantic` adds model/API latency by design. If speed matters, use the default path and enable semantic optimization only when the extra reasoning is worth the wait.

### Check the installed version

```bash
prompt-master --version
```

## Supported modes

`auto`, `coding`, `sql`, `data`, `research`, `writing`, `analysis`, `creative`, `image`, `agent`

## Python API

```python
from prompt_master import compress, compare, evaluate, optimize

result = optimize("Create a BigQuery query to find duplicate customer IDs")
print(result.rendered)
print(result.prompt.mode)
print(result.score)

compressed = compress(result.rendered)
print(compressed.compressed)
print(compressed.reduction_percent)

assessment = evaluate(result.rendered)
print(assessment.score)

comparison = compare("Tell me about SQL", result.rendered)
print(comparison.winner, comparison.margin)
```

## Architecture

```text
src/prompt_master/
├── core.py           # optimization, normalization, rendering, adapter orchestration
├── classification.py # cached, explainable task classification
├── audit.py          # completeness / missing-context audit
├── compression.py    # conservative local compression
├── evaluation.py     # local scoring and A/B comparison
├── adapters.py       # optional LLM adapter protocol + OpenAI-compatible adapter
├── schemas.py        # portable Prompt / OptimizationResult models
├── lint.py           # local quality and secret checks
├── cli.py            # prompt-master / pm command line interface
└── __main__.py       # python -m prompt_master
```

The architecture keeps provider-specific behavior at the edge. The deterministic core remains safe and portable, while semantic optimization and future MCP / VS Code / web integrations can be layered on top.

## Development

Run the test suite:

```bash
python -m pytest
```

Build the package locally:

```bash
python -m build
```

The project targets Python **3.10+** and has no required runtime dependencies.

## Roadmap

### Completed through Phase 4

- [x] Provider-neutral prompt IR
- [x] Task classification
- [x] Explainable classification confidence and signals
- [x] Completeness and assumption audit
- [x] Prompt construction and Markdown rendering
- [x] Deterministic linting and local secret detection
- [x] Deeper deterministic lint checks for duplicates, conflicts, vague references, and question-heavy prompts
- [x] Fast deterministic pipeline: compiled classification patterns + shared normalization
- [x] Conservative deterministic prompt compression
- [x] CLI, `pm` alias, stdin, JSON output, compression, lint, evaluation
- [x] Python module entry point
- [x] Packaging metadata, MIT license, tests, and CI foundation
- [x] Optional LLM-backed semantic optimizer
- [x] Provider-neutral LLM adapter protocol
- [x] Local prompt evaluation rubric
- [x] Prompt A/B comparison

### Next

- [ ] Semantic evaluation against actual model outputs
- [ ] VS Code extension
- [ ] MCP server
- [ ] Web UI
- [ ] Prompt versioning and telemetry-free local history
- [ ] Optional smart routing for simple vs. complex requests

## Philosophy

A better prompt is not necessarily a longer prompt. Prompt Master aims for **the smallest prompt that reliably communicates the user's intent and quality bar**.

## License

MIT — see [LICENSE](LICENSE).
