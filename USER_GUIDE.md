# Prompt Master — PC + VS Code User Guide

This guide explains how to install, run, test, and use Prompt Master on a Windows PC with VS Code. The same commands work on macOS/Linux with the activation command adjusted.

## 1. What Prompt Master is

Prompt Master is a local, provider-neutral prompt engineering toolkit. It takes a rough request and turns it into a structured prompt that can be pasted into ChatGPT, Claude, Gemini, Copilot, Cursor, or another LLM.

The default deterministic engine does not require an API key and does not send prompt content over the network.

```text
rough request
    ↓
classify
    ↓
completeness audit
    ↓
construct
    ↓
lint
    ↓
render
    ↓
optional semantic optimization
    ↓
evaluate / compare
```

## 2. What you need on your PC

- Windows 10/11, macOS, or Linux
- Python 3.10 or newer
- Git
- VS Code
- A terminal (PowerShell, Command Prompt, or VS Code Terminal)

Check the installations:

```powershell
python --version
git --version
```

If `python` is not recognized on Windows, try:

```powershell
py --version
```

## 3. Clone the project

Open VS Code and open **Terminal → New Terminal**.

Run:

```powershell
git clone https://github.com/Ashwinx0x/prompt-master.git
cd prompt-master
code .
```

You now have the project source code locally. Future changes can be pulled with:

```powershell
git pull
```

## 4. Create a Python virtual environment

From the project folder:

```powershell
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```cmd
.venv\Scripts\activate
```

When active, your terminal normally shows `(.venv)` at the beginning of the prompt.

## 5. Install Prompt Master

For normal use:

```powershell
python -m pip install -e .
```

For development, testing, and package building:

```powershell
python -m pip install -e ".[dev]"
```

The `-e` means **editable install**. When you change the source code in VS Code, the installed command uses your current local code without requiring a reinstall each time.

## 6. Verify the installation

Run:

```powershell
prompt-master --version
```

You can also use the shorter command:

```powershell
pm --version
```

Then try:

```powershell
pm "Create a BigQuery query to find duplicate customer IDs"
```

Or:

```powershell
python -m prompt_master "Rewrite this email to sound professional and polite"
```

## 7. Your normal workflow

The simplest workflow is:

```text
Write rough request
      ↓
pm "..."
      ↓
Review generated prompt
      ↓
Copy the prompt
      ↓
Paste into your preferred LLM
```

Example:

```powershell
pm "make this SQL faster"
```

Prompt Master will identify SQL as the likely mode, preserve the request, add safe constraints, and flag that the actual SQL/schema may be required.

## 8. Choose a mode yourself

Automatic classification is the default. You can override it when you know the task type.

```powershell
pm "Make this query faster" --mode sql
pm "Write a professional project update" --mode writing
pm "Create a cinematic portrait prompt" --mode image
pm "Design an ETL validation approach" --mode data
```

Supported modes:

- `auto`
- `coding`
- `sql`
- `data`
- `research`
- `writing`
- `analysis`
- `creative`
- `image`
- `agent`

## 9. Lint a request

Use lint when you want Prompt Master to look for common prompt-quality and security problems.

```powershell
pm "Create a SQL query to find customers with more than 3 orders" --lint
```

Typical checks include:

- missing output/action instruction
- missing constraints or quality guidance
- very short prompts
- unusually long prompts
- possible API keys, passwords, tokens, or secrets

Important: a lint warning is guidance, not proof that a prompt is bad.

## 10. Evaluate a prompt

Evaluate the construction quality of a prompt:

```powershell
pm "Make this SQL query faster" --evaluate
```

The evaluation is local and deterministic. It looks at characteristics such as objective clarity, output instructions, constraints, quality criteria, and structure.

The score is **not** a prediction that an LLM will answer correctly.

## 11. Compare two prompts

Create a text file such as `candidate.txt` containing another prompt.

Then:

```powershell
pm "Make this SQL query faster" --compare-with candidate.txt
```

Prompt Master evaluates both candidates with the same rubric and reports which one scores better and why.

## 12. JSON mode for automation

If you want to use Prompt Master from another script or tool:

```powershell
pm "Explain this Python error and give me a production-safe fix" --lint --evaluate --json
```

This produces machine-readable JSON containing the mode, score, generated prompt, diagnostics, lint issues, and clarification questions.

## 13. Pipe text into Prompt Master

You can use standard input:

```powershell
echo "Make this SQL faster" | pm --mode sql
```

This is useful for shell scripts and future automation.

## 14. Optional semantic optimization

The normal engine is deterministic and local. Semantic optimization is different: it sends the generated prompt to the configured OpenAI-compatible endpoint.

Only enable it when you intentionally want an external model involved.

Set the API key in your terminal environment rather than putting it in source code:

```powershell
$env:PROMPT_MASTER_API_KEY="your-key"
$env:PROMPT_MASTER_MODEL="gpt-4.1-mini"
```

Then:

```powershell
pm "Rewrite this technical request to be clearer" --semantic
```

You can also configure an OpenAI-compatible endpoint with `PROMPT_MASTER_BASE_URL`.

### Security rule

Never commit an API key into GitHub. Do not put credentials in `.py` files, README files, test files, or prompt examples.

## 15. Why semantic mode is slower

The deterministic path is designed to be very fast because it is local and dependency-light.

Semantic mode necessarily adds network/model latency:

```text
local request
   ↓
Prompt Master
   ↓
Internet / API
   ↓
LLM processing
   ↓
response
```

For the fastest response, use the default deterministic mode. Use semantic mode only when its additional reasoning is worth the latency.

## 16. Development workflow in VS Code

If you want to modify Prompt Master itself:

1. Open the repository folder in VS Code.
2. Select the `.venv` Python interpreter when VS Code asks.
3. Make your change under `src/prompt_master/`.
4. Add or update tests under `tests/`.
5. Run:

```powershell
python -m pytest
```

6. If the package builds successfully:

```powershell
python -m build
```

7. Check your Git changes:

```powershell
git status
git diff
```

8. Commit your work:

```powershell
git add .
git commit -m "Describe the change"
```

9. Push it:

```powershell
git push
```

## 17. Updating to the latest GitHub version

Before working on an existing checkout:

```powershell
git pull
```

If the project changed its dependencies or packaging configuration, rerun:

```powershell
python -m pip install -e ".[dev]"
```

## 18. Useful commands cheat sheet

| Goal | Command |
|---|---|
| Check version | `pm --version` |
| Basic optimization | `pm "your request"` |
| Force mode | `pm "your request" --mode sql` |
| Lint | `pm "your request" --lint` |
| Evaluate | `pm "your request" --evaluate` |
| Compare | `pm "your request" --compare-with candidate.txt` |
| JSON | `pm "your request" --json` |
| Semantic | `pm "your request" --semantic` |
| Read stdin | `echo "your request" \| pm` |
| Run tests | `python -m pytest` |
| Build package | `python -m build` |
| Update repo | `git pull` |
| See changes | `git diff` |
| Push changes | `git push` |

## 19. Troubleshooting

### `prompt-master` or `pm` is not recognized

Make sure the virtual environment is active and Prompt Master is installed:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -e .
```

You can always bypass the command entry point with:

```powershell
python -m prompt_master "your request"
```

### `python` is not recognized

Try:

```powershell
py --version
```

If that works, create the environment with:

```powershell
py -m venv .venv
```

### PowerShell refuses to activate the environment

Use Command Prompt and run:

```cmd
.venv\Scripts\activate
```

Or use the VS Code Python interpreter directly and run commands through its configured terminal.

### Semantic mode fails

Check that:

- `PROMPT_MASTER_API_KEY` is set in the current terminal.
- The configured model name is valid for your endpoint.
- `PROMPT_MASTER_BASE_URL` is correct if you use a custom endpoint.
- Your network can reach the endpoint.

The normal deterministic mode should still work without any API key.

## 20. What is implemented vs planned

### Implemented

- Deterministic prompt optimization
- Explainable task classification
- Completeness audit
- Structured prompt construction
- Local linting and credential detection
- Optional semantic optimization
- Local prompt evaluation
- A/B comparison
- CLI and Python API

### Planned next

- Deeper, rule-based prompt linter
- Prompt compression and redundancy reduction
- Semantic evaluation using actual model outputs
- VS Code extension
- MCP server
- Web UI

## 21. Design principle

Prompt Master is not trying to make every prompt longer.

The target is:

> **The smallest prompt that reliably communicates intent, constraints, and the desired quality bar.**
