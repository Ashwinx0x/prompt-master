"""Deterministic prompt evaluation and A/B comparison.

Evaluation is intentionally provider-neutral. It scores observable prompt
properties locally; it does not claim to measure an LLM's final answer quality.
An optional semantic evaluator can be layered on later without changing this API.
"""

from dataclasses import dataclass, field
import re


@dataclass(frozen=True)
class EvaluationResult:
    """Quality assessment for a single prompt."""

    score: int
    dimensions: dict[str, int]
    strengths: list[str] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ComparisonResult:
    """A/B comparison between two prompt candidates."""

    winner: str
    score_a: int
    score_b: int
    margin: int
    reasons: list[str] = field(default_factory=list)


_OUTPUT_WORDS = re.compile(r"(?i)\b(output|return|provide|give|create|write|explain|produce|generate|respond)\b")
_CONSTRAINT_WORDS = re.compile(r"(?i)\b(must|should|do not|don't|avoid|constraint|format|limit|only|include|exclude)\b")
_QUALITY_WORDS = re.compile(r"(?i)\b(correct|accurate|relevant|complete|concise|clear|quality|verify|validate|cite)\b")
_STRUCTURE_MARKERS = re.compile(r"(?m)^#{1,6}\s|^[-*]\s|^\d+[.)]\s")


def _score_dimension(prompt: str, pattern: re.Pattern[str], base: int = 0) -> int:
    return min(20, base + len(pattern.findall(prompt)) * 5)


def evaluate(prompt: str) -> EvaluationResult:
    """Score prompt quality using deterministic, explainable heuristics.

    The score reflects prompt construction quality, not whether a model will
    produce a factually correct answer.
    """
    text = prompt.strip()
    if not text:
        raise ValueError("Prompt cannot be empty")

    words = text.split()
    objective = min(20, 8 + min(12, len(words) // 8))
    output = 20 if _OUTPUT_WORDS.search(text) else 4
    constraints = _score_dimension(text, _CONSTRAINT_WORDS)
    quality = _score_dimension(text, _QUALITY_WORDS)
    structure = min(20, 5 + len(_STRUCTURE_MARKERS.findall(text)) * 3)

    dimensions = {
        "objective": objective,
        "output": output,
        "constraints": constraints,
        "quality": quality,
        "structure": structure,
    }
    score = min(100, sum(dimensions.values()))

    strengths: list[str] = []
    issues: list[str] = []
    if output >= 15:
        strengths.append("Clear output/action instruction detected.")
    else:
        issues.append("Add an explicit output or action requirement.")
    if constraints >= 15:
        strengths.append("Useful constraints are explicit.")
    else:
        issues.append("Add constraints or boundaries where they materially affect the result.")
    if quality >= 15:
        strengths.append("Quality expectations are stated.")
    else:
        issues.append("Define what a good result should optimize for.")
    if structure >= 12:
        strengths.append("Prompt has recognizable structure.")
    else:
        issues.append("Use sections, bullets, or numbered steps when they improve clarity.")
    if len(words) > 500:
        issues.append("Prompt is long; check for repeated or low-value context.")
    if len(words) < 8:
        issues.append("Prompt is very short; verify that important context is not missing.")

    return EvaluationResult(score=score, dimensions=dimensions, strengths=strengths, issues=issues)


def compare(prompt_a: str, prompt_b: str) -> ComparisonResult:
    """Compare two prompt candidates using the same deterministic rubric."""
    result_a = evaluate(prompt_a)
    result_b = evaluate(prompt_b)
    margin = abs(result_a.score - result_b.score)
    if result_a.score == result_b.score:
        winner = "tie"
    elif result_a.score > result_b.score:
        winner = "A"
    else:
        winner = "B"

    reasons: list[str] = []
    for dimension in result_a.dimensions:
        a = result_a.dimensions[dimension]
        b = result_b.dimensions[dimension]
        if a != b:
            better = "A" if a > b else "B"
            reasons.append(f"{better} scores higher on {dimension} ({max(a, b)} vs {min(a, b)}).")
    return ComparisonResult(
        winner=winner,
        score_a=result_a.score,
        score_b=result_b.score,
        margin=margin,
        reasons=reasons[:5],
    )
