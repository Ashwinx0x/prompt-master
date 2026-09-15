"""Deterministic first-generation optimizer.

This layer deliberately does not call an LLM. It converts a rough request into a
portable prompt structure and can later be wrapped by provider-specific semantic
optimizers.
"""

import re
from .schemas import OptimizationResult, Prompt

MODES = {
    "coding": ("code", "python", "javascript", "bug", "api", "function", "program"),
    "sql": ("sql", "query", "bigquery", "database", "join", "select"),
    "data": ("data", "etl", "pipeline", "warehouse", "pandas", "dataset"),
    "research": ("research", "sources", "paper", "literature", "compare"),
    "writing": ("write", "rewrite", "email", "article", "resume", "blog"),
    "analysis": ("analyze", "analyse", "evaluate", "explain", "reason"),
    "creative": ("story", "creative", "poem", "script", "character"),
    "image": ("image", "photo", "portrait", "render", "visual", "prompt"),
    "agent": ("agent", "tool", "workflow", "automate", "automation"),
}


def classify(text: str) -> str:
    low = text.lower()
    scores = {mode: sum(low.count(k) for k in keys) for mode, keys in MODES.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else "auto"


def _questions(mode: str, text: str) -> list[str]:
    questions = []
    if mode in {"coding", "sql", "data"}:
        if not any(x in text.lower() for x in ("schema", "table", "code", "query", "input")):
            questions.append("What is the relevant code, schema, input, or sample data?")
    if mode == "research":
        questions.append("What scope, geography, timeframe, and source-quality requirements should be used?")
    if mode in {"writing", "creative"}:
        questions.append("Who is the audience, and what tone or length should the output have?")
    return questions[:2]


def render(p: Prompt) -> str:
    sections = [f"## Objective\n{p.objective.strip()}"]
    if p.context:
        sections.append("## Context\n" + "\n".join(f"- {x}" for x in p.context))
    if p.inputs:
        sections.append("## Inputs\n" + "\n".join(f"- {x}" for x in p.inputs))
    if p.constraints:
        sections.append("## Constraints\n" + "\n".join(f"- {x}" for x in p.constraints))
    if p.steps:
        sections.append("## Approach\n" + "\n".join(f"{i}. {x}" for i, x in enumerate(p.steps, 1)))
    if p.quality_criteria:
        sections.append("## Quality bar\n" + "\n".join(f"- {x}" for x in p.quality_criteria))
    if p.output_format:
        sections.append(f"## Output format\n{p.output_format}")
    if p.assumptions:
        sections.append("## Assumptions\n" + "\n".join(f"- {x}" for x in p.assumptions))
    return "\n\n".join(sections)


def optimize(request: str, mode: str = "auto") -> OptimizationResult:
    request = re.sub(r"\s+", " ", request).strip()
    if not request:
        raise ValueError("Request cannot be empty")
    selected = classify(request) if mode == "auto" else mode
    if selected not in {"auto", *MODES}:
        raise ValueError(f"Unknown mode: {mode}")

    questions = _questions(selected, request)
    prompt = Prompt(
        objective=request,
        context=["Treat the user's request as the source of truth."],
        constraints=[
            "Do not invent missing facts, requirements, data, or sources.",
            "State important assumptions explicitly.",
            "Prefer a concise, practical answer over unnecessary theory.",
        ],
        steps=[
            "Identify the requested outcome and important constraints.",
            "Use only information supported by the request or clearly stated assumptions.",
            "Produce the requested result and briefly flag any material uncertainty.",
        ],
        quality_criteria=["Correctness", "Relevance", "Completeness", "Clarity"],
        output_format="Give the answer directly. Use structured sections, bullets, tables, or code when they improve usability.",
        assumptions=[f"Detected task mode: {selected}"],
        clarification_questions=questions,
        mode=selected,
    )
    diagnostics = []
    if questions:
        diagnostics.append("Some context may be missing; the prompt preserves this instead of guessing.")
    score = min(100, 60 + len(prompt.constraints) * 5 + len(prompt.quality_criteria) * 5)
    return OptimizationResult(prompt=prompt, rendered=render(prompt), diagnostics=diagnostics, score=score)
