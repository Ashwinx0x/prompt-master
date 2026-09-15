"""Command-line interface for Prompt Master."""

import argparse
import json
import sys

from . import __version__
from .adapters import OpenAICompatibleAdapter
from .core import MODES, optimize, optimize_with_adapter
from .lint import lint


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prompt-master",
        description="Turn rough requests into robust, provider-neutral prompts.",
    )
    parser.add_argument("request", nargs="*", help="The request to optimize. Reads stdin when omitted.")
    parser.add_argument("--mode", choices=["auto", *MODES], default="auto", help="Task mode (default: auto).")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    parser.add_argument("--lint", action="store_true", help="Run static quality and security checks.")
    parser.add_argument("--semantic", action="store_true", help="Run an optional LLM-backed semantic optimization pass.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    request = " ".join(args.request).strip()
    if not request and not sys.stdin.isatty():
        request = sys.stdin.read().strip()
    if not request:
        parser.error("provide a request or pipe one through stdin")

    if args.semantic:
        try:
            result = optimize_with_adapter(request, args.mode, OpenAICompatibleAdapter.from_env())
        except (ValueError, RuntimeError) as exc:
            parser.error(str(exc))
    else:
        result = optimize(request, args.mode)

    issues = lint(request) if args.lint else []

    if args.json:
        payload = {
            "version": __version__,
            "mode": result.prompt.mode,
            "score": result.score,
            "prompt": result.rendered,
            "diagnostics": result.diagnostics,
            "lint": [issue.__dict__ for issue in issues],
            "clarifications": result.prompt.clarification_questions,
            "semantic": args.semantic,
        }
        print(json.dumps(payload, indent=2))
        return

    print(result.rendered)
    if result.prompt.clarification_questions:
        print("\n## Optional clarifications")
        for question in result.prompt.clarification_questions:
            print(f"- {question}")
    if result.diagnostics:
        print("\n## Diagnostics")
        for diagnostic in result.diagnostics:
            print(f"- {diagnostic}")
    print(f"\nPrompt quality score: {result.score}/100")

    if issues:
        print("\n## Lint")
        for issue in issues:
            print(f"- [{issue.severity}] {issue.code}: {issue.message}")


if __name__ == "__main__":
    main()
