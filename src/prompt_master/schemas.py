from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Prompt:
    objective: str
    context: list[str] = field(default_factory=list)
    inputs: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)
    output_format: Optional[str] = None
    quality_criteria: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    clarification_questions: list[str] = field(default_factory=list)
    mode: str = "auto"


@dataclass
class OptimizationResult:
    prompt: Prompt
    rendered: str
    diagnostics: list[str] = field(default_factory=list)
    score: int = 0
