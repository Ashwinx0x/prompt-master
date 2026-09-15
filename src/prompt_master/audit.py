"""Deterministic completeness checks for rough requests."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class AuditIssue:
    code: str
    message: str
    severity: str = "warning"


def audit(request: str, mode: str, *, normalized: bool = False) -> list[AuditIssue]:
    """Find high-value missing context without inventing requirements."""
    text = request if normalized else " ".join(request.casefold().split())
    issues: list[AuditIssue] = []

    if mode in {"coding", "sql", "data"} and not re.search(r"\b(code|query|schema|table|input|sample|example|file|data)\b", text):
        issues.append(AuditIssue("PMA001", "Technical context is missing: provide code, schema, input, sample data, or an example."))
    if mode == "sql" and not re.search(r"\b(performance|faster|optimi[sz]e|result|output|query)\b", text):
        issues.append(AuditIssue("PMA002", "SQL goal is unclear: specify the expected result or optimization goal."))
    if mode == "research" and not re.search(r"\b(scope|timeframe|year|years|region|country|source|sources|recent|latest)\b", text):
        issues.append(AuditIssue("PMA003", "Research scope is unspecified: consider timeframe, geography, and source-quality requirements."))
    if mode in {"writing", "creative"} and not re.search(r"\b(audience|tone|formal|casual|concise|short|long|length|style)\b", text):
        issues.append(AuditIssue("PMA004", "Audience, tone, or length is unspecified; the result may vary significantly without it."))
    if mode == "image" and not re.search(r"\b(aspect|ratio|vertical|portrait|square|landscape|resolution|size|platform)\b", text):
        issues.append(AuditIssue("PMA005", "Image framing is unspecified: consider aspect ratio, size, or target platform."))
    if not re.search(r"\b(output|return|provide|give|create|write|explain|produce|generate)\b", text):
        issues.append(AuditIssue("PMA006", "The requested output is not explicit."))
    return issues[:4]
