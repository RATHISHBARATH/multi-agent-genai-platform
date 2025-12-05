"""
A robust summarizer service.

Behavior:
- If transformers and a summarization model are available, uses transformers.pipeline("summarization").
- Else, falls back to a simple extractive summarizer: returns the first N sentences.
- Designed to be plug-and-play with LLM-based summarization when available.
"""

try:
    from transformers import pipeline
    _hf_summarizer = pipeline("summarization")
except Exception:
    _hf_summarizer = None

import re
from typing import Optional

class Summarizer:
    def __init__(self, max_length: int = 256, min_length: int = 30):
        self.max_length = max_length
        self.min_length = min_length

    def _extractive(self, text: str, sentences: int = 3) -> str:
        # naive sentence splitter
        parts = re.split(r'(?<=[.!?])\s+', text.strip())
        if not parts:
            return ""
        return " ".join(parts[:sentences]).strip()

    def summarize(self, text: str, method: Optional[str] = None) -> str:
        """
        Summarize `text`.
        - method: None | 'hf' | 'extractive'
        """
        if not text:
            return ""

        # Prefer HF if requested or available
        if (method == "hf" or (method is None and _hf_summarizer is not None)):
            try:
                # transformers handles long inputs poorly; we truncate conservatively
                chunk = text[:2000]
                out = _hf_summarizer(chunk, max_length=self.max_length, min_length=self.min_length, truncation=True)
                if isinstance(out, list) and out:
                    return out[0].get("summary_text", "").strip()
            except Exception:
                # fallthrough to extractive
                pass

        # fallback extractive
        return self._extractive(text, sentences=3)
