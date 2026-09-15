# Prompt Master Versioning

Prompt Master uses **GitHub as the single source of truth for versions**.

Your VS Code workspace is a local copy of one GitHub version. It is not a second place where versions are maintained.

## Version model

Prompt Master follows semantic versioning:

```text
MAJOR.MINOR.PATCH
```

- **MAJOR** — incompatible changes to the public API or workflow.
- **MINOR** — new backwards-compatible capabilities.
- **PATCH** — backwards-compatible fixes, documentation corrections, or small improvements.

The package version in `pyproject.toml` and `src/prompt_master/__init__.py` must agree.

## GitHub branches vs releases

### `main`

`main` is the active development line. It may change between releases.

### `vX.Y.Z` tags

Each usable release is represented by an immutable Git tag such as:

```text
v1.2.0
v1.3.0
v1.3.1
```

A tag identifies the exact source that should be copied into a workspace when reproducibility matters.

## Recommended VS Code workflow

For normal use, clone the repository and select a release:

```bash
git clone https://github.com/Ashwinx0x/prompt-master.git
cd prompt-master
git fetch --tags
git checkout v1.2.0
```

Then open the folder in VS Code:

```bash
code .
```

Your workspace is now a copy of `v1.2.0`.

## Moving to a newer release

When a new version is released:

```bash
git fetch --tags
git checkout v1.3.0
```

If packaging or dependencies changed, reinstall the package in the local virtual environment:

```bash
python -m pip install -e ".[dev]"
```

Do not manually edit version numbers in the workspace just to keep them in sync. The GitHub release/tag is the version you selected.

## Release checklist

Before a release:

1. Update the package version in `pyproject.toml`.
2. Update `src/prompt_master/__init__.py` to the same version.
3. Update the changelog/documentation.
4. Add or update tests for the change.
5. Run the test suite and package build.
6. Commit the release state to `main`.
7. Create the matching Git tag, for example `v1.3.0`.
8. Use that tag as the stable source for VS Code workspaces.

## Important rule

**GitHub is authoritative. VS Code is disposable.**

If a local workspace is lost, it can be recreated from the required GitHub tag. This keeps version history, source code, and release points centralized in the repository.
