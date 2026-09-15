# Prompt Master — PC + VS Code User Guide

This guide explains how to use Prompt Master as a **versioned GitHub project copied into a VS Code workspace**. Prompt Master is not a VS Code extension; GitHub is the source of truth for every version.

## 1. What Prompt Master is

Prompt Master is a local, provider-neutral prompt engineering toolkit. It takes a rough request and turns it into a structured prompt that can be pasted into ChatGPT, Claude, Gemini, Copilot, Cursor, or another LLM.

The default deterministic engine does not require an API key and does not send prompt content over the network.

```text
rough request
    ↓
normalize → classify → audit → construct → compress → lint → render
    ↓
optional semantic optimization
    ↓
evaluate / compare
```

## 2. What you need

- Windows 10/11, macOS, or Linux
- Python 3.10+
- Git
- VS Code
- A terminal

Check:

```powershell
python --version
git --version
```

If Windows does not recognize `python`, try:

```powershell
py --version
```

## 3. Copy the GitHub project into VS Code

The simplest method is through VS Code:

1. Open VS Code.
2. Press `Ctrl+Shift+P`.
3. Select **Git: Clone**.
4. Paste:

```text
https://github.com/Ashwinx0x/prompt-master.git
```

5. Select where you want the project copied.
6. Open the cloned `prompt-master` folder.

Terminal equivalent:

```powershell
git clone https://github.com/Ashwinx0x/prompt-master.git
cd prompt-master
code .
```

This creates the local workspace from GitHub. You do not need to manually copy individual source files.

## 4. Use a specific GitHub version

For reproducible use, select a release tag instead of using the moving `main` branch.

```powershell
git fetch --tags
git checkout v1.2.0
```

Then open the workspace:

```powershell
code .
```

Check the selected version:

```powershell
prompt-master --version
```

**Recommended:** use a tagged version for normal work. Use `main` only when you deliberately want the newest development code.

See [VERSIONING.md](VERSIONING.md) for the full policy.

## 5. Create a Python environment

From the cloned project folder:

```powershell
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

## 6. Install Prompt Master

Normal use:

```powershell
python -m pip install -e .
```

Development/testing:

```powershell
python -m pip install -e ".[dev]"
```

Verify:

```powershell
pm --version
```

## 7. Normal workflow

```text
rough request
    ↓
pm "..."
    ↓
review generated prompt
    ↓
copy prompt
    ↓
paste into your preferred LLM
```

Example:

```powershell
pm "make this SQL faster"
```

## 8. Commands

### Automatic mode

```powershell
pm "Create a BigQuery query to find duplicate customer IDs"
```

### Force a mode

```powershell
pm "Make this query faster" --mode sql
pm "Write a professional project update" --mode writing
pm "Create a cinematic portrait prompt" --mode image
pm "Design an ETL validation approach" --mode data
```

Supported modes:

`auto`, `coding`, `sql`, `data`, `research`, `writing`, `analysis`, `creative`, `image`, `agent`

### Lint

```powershell
pm "Create a SQL query to find customers with more than 3 orders" --lint
```

Checks include missing output instructions, missing constraints, unusual length, duplicate instructions, conflicting length guidance, vague references, question-heavy prompts, and possible credentials/secrets.

### Compress

```powershell
pm "Make this SQL request concise without losing requirements" --compress
```

Compression is local and conservative. It does not claim semantic equivalence.

### Evaluate

```powershell
pm "Make this SQL query faster" --evaluate
```

The local score measures prompt-construction quality. It is not a prediction of model-answer correctness.

### Compare

Put another prompt in `candidate.txt`:

```powershell
pm "Make this SQL query faster" --compare-with candidate.txt
```

### JSON

```powershell
pm "Explain this Python error and give me a production-safe fix" --lint --evaluate --compress --json
```

### Stdin

```powershell
echo "Make this SQL faster" | pm --mode sql
```

## 9. Optional semantic optimization

The normal engine is deterministic and local. Semantic mode intentionally sends the generated prompt to the configured OpenAI-compatible endpoint.

Set credentials in the terminal environment, never in GitHub files:

```powershell
$env:PROMPT_MASTER_API_KEY="your-key"
$env:PROMPT_MASTER_MODEL="gpt-4.1-mini"
```

Then:

```powershell
pm "Rewrite this technical request to be clearer" --semantic
```

Optional endpoint:

```powershell
$env:PROMPT_MASTER_BASE_URL="https://your-compatible-endpoint/v1"
```

Never commit API keys, passwords, tokens, or other credentials to the repository.

## 10. Updating your workspace

### If using `main`

```powershell
git pull
```

### If using release tags

Keep the workspace on the selected version until you intentionally upgrade:

```powershell
git fetch --tags
git checkout v1.3.0
```

If packaging/dependencies changed:

```powershell
python -m pip install -e ".[dev]"
```

You do not need to maintain versions manually inside VS Code. GitHub tags and the package version are authoritative.

## 11. Development workflow

If you are contributing changes to Prompt Master itself:

1. Work from a development checkout.
2. Change source under `src/prompt_master/`.
3. Add/update tests under `tests/`.
4. Run:

```powershell
python -m pytest
python -m build
```

5. Review:

```powershell
git status
git diff
```

6. Commit and push changes to GitHub.

Release versions should then follow the policy in `VERSIONING.md`.

## 12. Useful commands cheat sheet

| Goal | Command |
|---|---|
| Clone | `git clone https://github.com/Ashwinx0x/prompt-master.git` |
| Select release | `git checkout v1.2.0` |
| Latest development | `git checkout main` |
| Check version | `pm --version` |
| Basic optimization | `pm "your request"` |
| Force mode | `pm "your request" --mode sql` |
| Lint | `pm "your request" --lint` |
| Compress | `pm "your request" --compress` |
| Evaluate | `pm "your request" --evaluate` |
| Compare | `pm "your request" --compare-with candidate.txt` |
| JSON | `pm "your request" --json` |
| Semantic | `pm "your request" --semantic` |
| Run tests | `python -m pytest` |
| Build | `python -m build` |
| Update tags | `git fetch --tags` |

## 13. Troubleshooting

### `pm` is not recognized

Activate the virtual environment and reinstall:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Or use:

```powershell
python -m prompt_master "your request"
```

### `python` is not recognized

Try:

```powershell
py --version
py -m venv .venv
```

### PowerShell blocks activation

Use Command Prompt:

```cmd
.venv\Scripts\activate
```

### Semantic mode fails

Check the API key, model name, base URL, and network access. The deterministic mode should continue to work without an API key.

## 14. Versioning principle

The important separation is:

```text
                    GITHUB
             canonical source
                     │
        ┌────────────┴────────────┐
        │                         │
     v1.2.0                    v1.3.0
     stable                    future
        │                         │
        ↓                         ↓
   VS Code copy              VS Code copy
```

**GitHub is authoritative. VS Code is disposable.**

If a workspace is deleted or replaced, it can always be recreated from the required GitHub version.

## 15. Design principle

Prompt Master is not trying to make every prompt longer.

> **The target is the smallest prompt that reliably communicates intent, constraints, and the desired quality bar.**
