"""Static quality and safety checks for prompts."""

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
_OUTPUT_RE = re.compile(r"(?i)\b(output|return|provide|give|create|write|explain|produce|generate|list|summarize|summarise)\b")
_CONSTRAINT_RE = re.compile(r"(?i)\b(do not|don't|avoid|must|should|constraint|format|limit|only|exactly)\b")


def lint(text: str) -> list[LintIssue]:
    """Return deterministic quality/safety issues without network calls."""
    issues: list[LintIssue] = []
    stripped = text.strip()
    normalized = " ".join(stripped.casefold().split())

    if len(stripped) < 12:
        issues.append(LintIssue("PM001", "Prompt is very short; verify that the desired outcome is explicit."))
    if not _OUTPUT_RE.search(stripped):
        issues.append(LintIssue("PM002", "No clear output/action verb was detected."))
    if not _CONSTRAINT_RE.search(stripped):
        issues.append(LintIssue("PM003", "No explicit constraint or quality instruction was detected."))
    if any(pattern.search(stripped) for pattern in _SECRET_PATTERNS):
        issues.append(LintIssue("PMSEC001", "Possible credential or secret detected; remove it before sharing the prompt.", "error"))
    if len(stripped) > 12000:
        issues.append(LintIssue("PM004", "Prompt is unusually long; consider separating reference material from instructions."))

    lines = [line.strip() for line in stripped.splitlines() if line.strip()]
    seen: set[str] = set()
    duplicate_count = 0
    for line in lines:
        key = re.sub(r"[^a-z0-9]+", " ", line.casefold()).strip()
        if key in seen:
            duplicate_count += 1
        seen.add(key)
    if duplicate_count:
        issues.append(LintIssue("PM005", f"Prompt contains {duplicate_count} duplicate instruction line(s)."))

    if re.search(r"(?i)\b(be concise|be detailed|as detailed as possible)\b", stripped) and re.search(r"(?i)\b(short|brief|one sentence|one paragraph)\b", stripped):
        issues.append(LintIssue("PM006", "Potentially conflicting length instructions detected."))

    vague = re.findall(r"(?i)\b(this|that|it|something|stuff|good|better|appropriate|proper)\b", normalized)
    if len(vague) >= 3:
        issues.append(LintIssue("PM007", "Several vague references were detected; replace them with concrete requirements or examples."))

    if stripped.count("?") >= 5:
        issues.append(LintIssue("PM008", "Prompt contains many questions; consider stating one primary objective and explicit sub-tasks."))

    return issues
