"""Core deterministic prompt optimization engine.

Prompt Master deliberately has no network dependency. The deterministic engine
creates a portable prompt structure that can later be enhanced by optional
LLM adapters without changing the public Prompt representation.
"""

import re
from .schemas import OptimizationResult, Prompt

MODES = {
    "coding": ("code", "python", "javascript", "typescript", "bug", "api", "function", "program", "class"),
    "sql": ("sql", "query", "bigquery", "database", "join", "select", "table", "cte"),
    "data": ("data", "etl", "pipeline", "warehouse", "pandas", "dataset", "dwh", "ingestion"),
    "research": ("research", "sources", "paper", "literature", "compare", "evidence", "study"),
    "writing": ("write", "rewrite", "email", "article", "resume", "blog", "message", "document"),
    "analysis": ("analyze", "analyse", "evaluate", "explain", "reason", "investigate", "assess"),
    "creative": ("story", "creative", "poem", "script", "character", "fiction", "lyrics"),
    "image": ("image", "photo", "portrait", "render", "visual", "illustration", "photorealistic"),
    "agent": ("agent", "tool", "workflow", "automate", "automation", "mcp", "orchestrate"),
}

VALID_MODES = {"auto", *MODES}


def classify(text: str) -> str:
    """Infer the most likely task mode using deterministic keyword scoring."""
    low = text.lower()
    scores = {mode: sum(len(re.findall(rf"\b{re.escape(k)}\b", low)) for k in keys) for mode, keys in MODES.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] else "auto"


def _questions(mode: str, text: str) -> list[str]:
    """Return at most two high-value clarification questions."""
    low = text.lower()
    questions: list[str] = []
    if mode in {"coding", "sql", "data"}:
        if not any(x in low for x in ("schema", "table", "code", "query", "input", "sample")):
            questions.append("What is the relevant code, schema, input, or sample data?")
    if mode == "research":
        questions.append("What scope, geography, timeframe, and source-quality requirements should be used?")
    if mode in {"writing", "creative"}:
        if not any(x in low for x in ("audience", "tone", "formal", "casual", "concise", "long")):
            questions.append("Who is the audience, and what tone or length should the output have?")
    if mode == "image" and not any(x in low for x in ("aspect", "ratio", "vertical", "square", "landscape")):
        questions.append("What aspect ratio or target platform should the image use?")
    return questions[:2]


def render(p: Prompt) -> str:
    """Render the portable Prompt structure as readable Markdown."""
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
    """Turn a rough request into a robust, provider-neutral prompt."""
    request = re.sub(r"\s+", " ", request).strip()
    if not request:
        raise ValueError("Request cannot be empty")
    if mode not in VALID_MODES:
        raise ValueError(f"Unknown mode: {mode}. Choose from: {', '.join(sorted(VALID_MODES))}")

    selected = classify(request) if mode == "auto" else mode
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
    diagnostics: list[str] = []
    if questions:
        diagnostics.append("Some context may be missing; the prompt preserves this instead of guessing.")
    score = min(100, 70 + len(prompt.constraints) * 5 + len(prompt.quality_criteria) * 5)
    return OptimizationResult(prompt=prompt, rendered=render(prompt), diagnostics=diagnostics, score=score)
