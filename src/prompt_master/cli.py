import argparse
import json
from .core import optimize
from .lint import lint


def main() -> None:
    parser = argparse.ArgumentParser(description="Turn rough requests into robust, provider-neutral prompts.")
    parser.add_argument("request", nargs="+", help="The request to optimize")
    parser.add_argument("--mode", default="auto", help="auto, coding, sql, data, research, writing, analysis, creative, image, agent")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument("--lint", action="store_true", help="Run static quality and security checks")
    args = parser.parse_args()

    request = " ".join(args.request)
    result = optimize(request, args.mode)
    issues = lint(result.rendered) if args.lint else []

    if args.json:
        payload = {
            "version": "0.2",
            "mode": result.prompt.mode,
            "score": result.score,
            "prompt": result.rendered,
            "diagnostics": result.diagnostics,
            "lint": [issue.__dict__ for issue in issues],
            "clarifications": result.prompt.clarification_questions,
        }
        print(json.dumps(payload, indent=2))
        return

    print(result.rendered)
    if result.prompt.clarification_questions:
        print("\n## Optional clarifications")
        for q in result.prompt.clarification_questions:
            print(f"- {q}")
    print(f"\nPrompt quality score: {result.score}/100")

    if issues:
        print("\n## Lint")
        for issue in issues:
            print(f"- [{issue.severity}] {issue.code}: {issue.message}")


if __name__ == "__main__":
    main()
