"""
A lightweight persistent vector store using SQLite.

- Stores vectors as JSON text along with metadata.
- Queries using a naive cosine similarity. If numpy is available, uses it for speed.
- This is a development/demo alternative to Pinecone/Weaviate.
"""

import sqlite3
import json
import os
from typing import List, Dict, Optional
try:
    import numpy as np
except Exception:
    np = None

DB_PATH = os.getenv("VECTOR_DB_PATH", "/tmp/autoscillab_vectors.db")

def _cosine(a, b):
    if np is not None:
        a = np.array(a); b = np.array(b)
        na = np.linalg.norm(a); nb = np.linalg.norm(b)
        if na == 0 or nb == 0: return 0.0
        return float(np.dot(a,b) / (na*nb))
    # pure python
    dot = sum(x*y for x,y in zip(a,b))
    na = sum(x*x for x in a) ** 0.5
    nb = sum(x*x for x in b) ** 0.5
    if na == 0 or nb == 0: return 0.0
    return dot / (na*nb)

class VectorDB:
    def __init__(self, path: str = None):
        self.path = path or DB_PATH
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self._ensure_table()

    def _ensure_table(self):
        cur = self.conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS vectors (
            id TEXT PRIMARY KEY,
            vector TEXT NOT NULL,
            metadata TEXT
        )""")
        self.conn.commit()

    def upsert(self, id: str, vector: List[float], metadata: Dict = None):
        cur = self.conn.cursor()
        cur.execute("""INSERT OR REPLACE INTO vectors (id,vector,metadata) VALUES (?,?,?)""",
                    (id, json.dumps(vector), json.dumps(metadata or {})))
        self.conn.commit()
        return True

    def query(self, vector: List[float], top_k: int = 5):
        cur = self.conn.cursor()
        cur.execute("SELECT id, vector, metadata FROM vectors")
        rows = cur.fetchall()
        results = []
        for rid, vtxt, mtxt in rows:
            v = json.loads(vtxt)
            score = _cosine(vector, v)
            results.append((score, {"id": rid, "meta": json.loads(mtxt)}))
        results.sort(key=lambda x: x[0], reverse=True)
        return [r for s,r in results[:top_k]]
