"""
Embeddings service.

- Uses sentence-transformers when available (recommended).
- Fallback: simple character-based hashing to a fixed-length numeric vector.
"""

from typing import List
import os

try:
    from sentence_transformers import SentenceTransformer
    _st_model = SentenceTransformer(os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2"))
except Exception:
    _st_model = None

def _hash_fallback(text: str, dim: int = 128) -> List[float]:
    vec = [0.0] * dim
    for i, ch in enumerate(text[:dim*4]):
        vec[i % dim] += ord(ch)
    # normalize
    s = sum(v*v for v in vec) ** 0.5 or 1.0
    return [v / s for v in vec]

class Embeddings:
    def __init__(self, model_name: str = None):
        self.model = _st_model

    def embed(self, text: str) -> List[float]:
        if not text:
            return []
        if self.model is not None:
            try:
                vec = self.model.encode([text], show_progress_bar=False)[0]
                return vec.tolist() if hasattr(vec, "tolist") else list(map(float, vec))
            except Exception:
                pass
        # fallback
        return _hash_fallback(text, dim=128)
