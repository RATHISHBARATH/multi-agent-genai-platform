
from api.services.summarizer import Summarizer
from api.workers.celery_app import celery_app

@celery_app.task(bind=True, name="task.summarize")
def summarize_task(self, text: str):
    s = Summarizer()
    return s.summarize(text)
