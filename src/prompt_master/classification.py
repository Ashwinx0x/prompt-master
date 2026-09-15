"""Deterministic intent classification for Prompt Master.

The classifier is deliberately explainable: scores come from weighted phrases and
keywords rather than a hidden model or network call.
"""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class ClassificationResult:
    mode: str
    confidence: float
    scores: dict[str, int]
    matched_signals: list[str]


SIGNALS: dict[str, tuple[tuple[str, int], ...]] = {
    "coding": (
        ("write code", 5), ("python function", 5), ("debug", 4),
        ("stack trace", 4), ("api", 2), ("function", 2), ("code", 2),
        ("python", 2), ("javascript", 2), ("typescript", 2),
    ),
    "sql": (
        ("sql query", 5), ("optimize query", 5), ("bigquery", 5),
        ("cte", 3), ("join", 2), ("select", 2), ("database", 2),
        ("sql", 2), ("table", 1),
    ),
    "data": (
        ("etl", 5), ("data pipeline", 5), ("data warehouse", 5),
        ("data ingestion", 5), ("bigquery load", 4), ("dataset", 2),
        ("pandas", 2), ("pipeline", 2), ("data", 1),
    ),
    "research": (
        ("research", 5), ("literature review", 5), ("peer reviewed", 4),
        ("cite sources", 4), ("compare studies", 4), ("evidence", 2),
        ("sources", 2), ("paper", 2), ("study", 2),
    ),
    "writing": (
        ("write an email", 5), ("rewrite this", 5), ("write a resume", 5),
        ("draft a message", 4), ("email", 2), ("rewrite", 2),
        ("resume", 2), ("article", 2), ("blog", 2), ("write", 1),
    ),
    "analysis": (
        ("analyze", 4), ("analyse", 4), ("root cause", 5),
        ("tradeoffs", 4), ("evaluate", 3), ("explain why", 3),
        ("investigate", 3), ("assess", 2), ("reason", 2),
    ),
    "creative": (
        ("write a story", 5), ("creative writing", 5), ("poem", 4),
        ("fiction", 4), ("character", 3), ("story", 3), ("lyrics", 3),
    ),
    "image": (
        ("generate an image", 5), ("create an image", 5), ("image prompt", 5),
        ("photorealistic", 4), ("portrait", 3), ("render", 3),
        ("illustration", 3), ("photo", 2),
    ),
    "agent": (
        ("mcp", 5), ("build an agent", 5), ("tool calling", 5),
        ("automate", 4), ("workflow", 3), ("orchestrate", 3),
        ("agent", 3), ("automation", 3),
    ),
}


def _contains(text: str, signal: str) -> bool:
    return bool(re.search(rf"(?<!\w){re.escape(signal.lower())}(?!\w)", text))


def classify_detailed(text: str) -> ClassificationResult:
    """Classify text and expose confidence plus the signals that drove the result."""
    low = " ".join(text.lower().split())
    scores = {
        mode: sum(weight for signal, weight in signals if _contains(low, signal))
        for mode, signals in SIGNALS.items()
    }
    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    best_mode, best_score = ranked[0]
    second_score = ranked[1][1]
    total = sum(scores.values())
    if best_score == 0:
        return ClassificationResult("auto", 0.0, scores, [])
    confidence = min(1.0, best_score / max(best_score + second_score, 1))
    confidence = round(confidence * min(1.0, total / 5), 2)
    matched = [signal for signal, _ in SIGNALS[best_mode] if _contains(low, signal)]
    return ClassificationResult(best_mode, confidence, scores, matched)
