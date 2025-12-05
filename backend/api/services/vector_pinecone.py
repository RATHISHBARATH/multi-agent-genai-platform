"""Pinecone connector with graceful fallback to local VectorDB."""
import os, logging, time
logger = logging.getLogger("autoscillab.pinecone")

# try official pinecone client
try:
    import pinecone
    PINECONE_AVAILABLE = True
except Exception:
    PINECONE_AVAILABLE = False

from .vector_db import VectorDB

class PineconeClient:
    def __init__(self, index_name: str = None, dimension: int = 128):
        self.index_name = index_name or os.getenv('PINECONE_INDEX', 'autoscillab-index')
        self.dimension = int(os.getenv('PINECONE_DIM', dimension))
        self.api_key = os.getenv('PINECONE_API_KEY', '')
        self.environment = os.getenv('PINECONE_ENV', 'us-east1-gcp')
        self._local = False
        if PINECONE_AVAILABLE and self.api_key:
            try:
                pinecone.init(api_key=self.api_key, environment=self.environment)
                if self.index_name not in pinecone.list_indexes():
                    pinecone.create_index(self.index_name, dimension=self.dimension, metric='cosine')
                self.index = pinecone.Index(self.index_name)
                logger.info("Connected to Pinecone index %s", self.index_name)
            except Exception as e:
                logger.exception("Pinecone init failed, falling back: %s", e)
                self._fallback_init()
        else:
            self._fallback_init()

    def _fallback_init(self):
        logger.warning("Pinecone not available or API key missing. Using local VectorDB fallback.")
        self._local = True
        self.db = VectorDB()

    def upsert(self, id: str, vector, metadata: dict = None):
        if self._local:
            return self.db.upsert(id, vector, metadata)
        try:
            self.index.upsert([(id, vector, metadata or {})])
            return True
        except Exception as e:
            logger.exception("Pinecone upsert failed, using local DB: %s", e)
            return self.db.upsert(id, vector, metadata)

    def query(self, vector, top_k: int = 5):
        if self._local:
            return self.db.query(vector, top_k=top_k)
        try:
            res = self.index.query(vector=vector, top_k=top_k, include_metadata=True)
            # normalize response
            return res.to_dict()
        except Exception as e:
            logger.exception("Pinecone query failed, using local DB: %s", e)
            return self.db.query(vector, top_k=top_k)
