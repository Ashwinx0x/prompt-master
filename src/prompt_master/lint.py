"""Static quality and safety checks for generated prompts."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class LintIssue:
    code: str
    message: str
    severity: str = "warning"


_SECRET_PATTERNS = (
    re.compile(r"(?i)\b(api[_ -]?key|secret|password|token)\s*[:=]\s*\S+"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{12,}\b"),
)


def lint(text: str) -> list[LintIssue]:
    """Return deterministic issues without sending prompt content anywhere."""
    issues: list[LintIssue] = []
    if len(text.strip()) < 12:
        issues.append(LintIssue("PM001", "Prompt is very short; verify that the desired outcome is explicit."))
    if not re.search(r"(?i)\b(output|return|provide|give|create|write|explain|produce)\b", text):
        issues.append(LintIssue("PM002", "No clear output/action verb was detected."))
    if not re.search(r"(?i)\b(do not|avoid|must|should|constraint|format)\b", text):
        issues.append(LintIssue("PM003", "No explicit constraint or quality instruction was detected."))
    if _SECRET_PATTERNS and any(pattern.search(text) for pattern in _SECRET_PATTERNS):
        issues.append(LintIssue("PMSEC001", "Possible credential or secret detected; remove it before sharing the prompt.", "error"))
    if len(text) > 12000:
        issues.append(LintIssue("PM004", "Prompt is unusually long; consider separating reference material from instructions."))
    return issues
