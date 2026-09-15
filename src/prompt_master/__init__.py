"""Prompt Master: universal, provider-neutral prompt engineering toolkit."""

from .adapters import LLMAdapter, OpenAICompatibleAdapter
from .audit import AuditIssue, audit
from .classification import ClassificationResult, classify_detailed
from .core import MODES, classify, optimize, optimize_with_adapter, render
from .lint import LintIssue, lint
from .schemas import OptimizationResult, Prompt

__all__ = [
    "MODES",
    "Prompt",
    "OptimizationResult",
    "LintIssue",
    "AuditIssue",
    "ClassificationResult",
    "LLMAdapter",
    "OpenAICompatibleAdapter",
    "classify",
    "classify_detailed",
    "audit",
    "optimize",
    "optimize_with_adapter",
    "render",
    "lint",
]
__version__ = "1.0.0"
