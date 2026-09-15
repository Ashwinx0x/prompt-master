"""Command-line interface for Prompt Master."""

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .adapters import OpenAICompatibleAdapter
from .core import MODES, optimize, optimize_with_adapter
from .evaluation import compare, evaluate
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
    parser.add_argument("--evaluate", action="store_true", help="Evaluate the generated prompt with the local rubric.")
    parser.add_argument("--compare-with", metavar="FILE", help="Compare the generated prompt against a prompt stored in FILE.")
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
    evaluation = evaluate(result.rendered) if args.evaluate or args.compare_with else None
    comparison = None
    if args.compare_with:
        try:
            candidate = Path(args.compare_with).read_text(encoding="utf-8")
        except OSError as exc:
            parser.error(f"cannot read comparison file: {exc}")
        comparison = compare(result.rendered, candidate)

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
            "evaluation": evaluation.__dict__ if evaluation else None,
            "comparison": comparison.__dict__ if comparison else None,
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

    if evaluation:
        print(f"\n## Evaluation\nLocal prompt-construction score: {evaluation.score}/100")
        for strength in evaluation.strengths:
            print(f"- ✓ {strength}")
        for issue in evaluation.issues:
            print(f"- ⚠ {issue}")

    if comparison:
        print("\n## A/B comparison")
        print(f"Winner: {comparison.winner} | A: {comparison.score_a}/100 | B: {comparison.score_b}/100 | margin: {comparison.margin}")
        for reason in comparison.reasons:
            print(f"- {reason}")

    if issues:
        print("\n## Lint")
        for issue in issues:
            print(f"- [{issue.severity}] {issue.code}: {issue.message}")


if __name__ == "__main__":
    main()
