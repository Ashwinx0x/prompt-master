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

### `release/vX.Y.Z`

A release branch is a stable GitHub snapshot for a usable version. For example, the current 1.2.0 workspace is maintained at:

```text
release/v1.2.0
```

Release branches should not receive unrelated development changes after the version is published.

### Release tags

When GitHub release/tag automation is used, the preferred immutable identifier is:

```text
v1.2.0
v1.3.0
v1.3.1
```

A tag identifies the exact source that should be copied into a workspace. Until tag automation is enabled, the `release/vX.Y.Z` branch serves as the stable version reference.

## Recommended VS Code workflow

For the current stable version:

```bash
git clone https://github.com/Ashwinx0x/prompt-master.git
cd prompt-master
git checkout release/v1.2.0
code .
```

Your workspace is now a copy of the GitHub 1.2.0 release branch.

When release tags are available, the equivalent preferred workflow is:

```bash
git fetch --tags
git checkout v1.2.0
```

## Moving to a newer release

When a new release is published, select it explicitly:

```bash
git fetch --all
git checkout release/v1.3.0
```

Or, when tags are available:

```bash
git fetch --tags
git checkout v1.3.0
```

If packaging or dependencies changed, reinstall the package in the local virtual environment:

```bash
python -m pip install -e ".[dev]"
```

Do not manually edit version numbers in the workspace just to keep them in sync. The GitHub release reference and package version are authoritative.

## Release checklist

Before a release:

1. Update the package version in `pyproject.toml`.
2. Update `src/prompt_master/__init__.py` to the same version.
3. Update the changelog/documentation.
4. Add or update tests for the change.
5. Run the test suite and package build.
6. Commit the release state to `main`.
7. Create `release/vX.Y.Z` from that exact commit.
8. When tag automation is available, create the matching `vX.Y.Z` tag.
9. Use the release reference as the stable source for VS Code workspaces.

## Important rule

**GitHub is authoritative. VS Code is disposable.**

If a local workspace is lost, it can be recreated from the required GitHub release reference. This keeps version history, source code, and release points centralized in the repository.
