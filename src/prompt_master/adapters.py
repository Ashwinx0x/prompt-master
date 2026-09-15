"""Optional semantic optimizer adapters.

The adapter layer keeps the core provider-neutral. No provider SDK is required;
callers can supply their own adapter or use the stdlib OpenAI-compatible adapter.
"""

from dataclasses import dataclass
import json
import os
from typing import Protocol
from urllib import request as urlrequest


class LLMAdapter(Protocol):
    """Minimal contract for an optional semantic prompt optimizer."""

    def optimize(self, prompt: str) -> str:
        """Return an improved prompt while preserving the user's intent."""


@dataclass
class OpenAICompatibleAdapter:
    """Call any OpenAI-compatible chat endpoint using only the Python stdlib.

    Defaults are environment-driven so credentials are never stored in the
    repository. This also works with compatible local servers such as Ollama.
    """

    api_key: str
    model: str
    base_url: str = "https://api.openai.com/v1/chat/completions"
    timeout: int = 60

    @classmethod
    def from_env(cls) -> "OpenAICompatibleAdapter":
        api_key = os.getenv("PROMPT_MASTER_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Set PROMPT_MASTER_API_KEY or OPENAI_API_KEY before using the LLM adapter")
        return cls(
            api_key=api_key,
            model=os.getenv("PROMPT_MASTER_MODEL", "gpt-4.1-mini"),
            base_url=os.getenv("PROMPT_MASTER_BASE_URL", "https://api.openai.com/v1/chat/completions"),
        )

    def optimize(self, prompt: str) -> str:
        system = (
            "You are Prompt Master, a provider-neutral prompt engineer. "
            "Improve the supplied prompt without changing its intent. Remove redundancy, "
            "make constraints explicit, preserve important user details, and do not invent facts. "
            "Return only the optimized prompt."
        )
        payload = json.dumps({
            "model": self.model,
            "temperature": 0.1,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        }).encode("utf-8")
        req = urlrequest.Request(
            self.base_url,
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urlrequest.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            raise RuntimeError(f"LLM adapter request failed: {exc}") from exc
        try:
            return data["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("LLM adapter returned an unexpected response shape") from exc
