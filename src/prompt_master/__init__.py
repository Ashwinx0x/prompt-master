"""Prompt Master: universal prompt engineering toolkit."""

from .core import optimize
from .schemas import Prompt, OptimizationResult

__all__ = ["Prompt", "OptimizationResult", "optimize"]
__version__ = "0.1.0"
