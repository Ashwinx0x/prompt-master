import argparse
from .core import optimize


def main() -> None:
    parser = argparse.ArgumentParser(description="Turn rough requests into robust, provider-neutral prompts.")
    parser.add_argument("request", nargs="+", help="The request to optimize")
    parser.add_argument("--mode", default="auto", help="auto, coding, sql, data, research, writing, analysis, creative, image, agent")
    args = parser.parse_args()
    result = optimize(" ".join(args.request), args.mode)
    print(result.rendered)
    if result.prompt.clarification_questions:
        print("\n## Optional clarifications")
        for q in result.prompt.clarification_questions:
            print(f"- {q}")
    print(f"\nPrompt quality score: {result.score}/100")


if __name__ == "__main__":
    main()
