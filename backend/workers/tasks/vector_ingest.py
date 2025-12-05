
from api.services.embeddings import Embeddings
from api.services.vector_db import VectorDB
from api.workers.celery_app import celery_app
import uuid

@celery_app.task(name="task.vector_ingest")
def vector_ingest_task(text: str, meta: dict = None):
    emb = Embeddings().embed(text)
    vid = uuid.uuid4().hex
    VectorDB().upsert(vid, emb, meta or {})
    return vid
