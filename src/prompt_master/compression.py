"""Deterministic prompt compression heuristics.

Compression is intentionally conservative: it removes repeated whitespace and
near-duplicate instruction lines while preserving the prompt's wording as much
as practical. It does not use an LLM and does not claim semantic equivalence.
"""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class CompressionResult:
    original: str
    compressed: str
    original_words: int
    compressed_words: int
    reduction_percent: float


def _key(line: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", line.lower()).strip()


def compress(text: str) -> CompressionResult:
    """Apply safe local compression and report the before/after size."""
    original = text.strip()
    if not original:
        return CompressionResult("", "", 0, 0, 0.0)

    lines = [re.sub(r"\s+", " ", line).strip() for line in original.splitlines()]
    kept: list[str] = []
    seen: set[str] = set()
    for line in lines:
        if not line:
            if kept and kept[-1] != "":
                kept.append("")
            continue
        key = _key(line)
        if key and key in seen:
            continue
        if key:
            seen.add(key)
        kept.append(line)

    compressed = "\n".join(kept).strip()
    compressed = re.sub(r"\n{3,}", "\n\n", compressed)
    original_words = len(original.split())
    compressed_words = len(compressed.split())
    reduction = 0.0 if not original_words else round((1 - compressed_words / original_words) * 100, 1)
    return CompressionResult(original, compressed, original_words, compressed_words, reduction)
