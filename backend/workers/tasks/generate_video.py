from api.workers.celery_app import celery_app
from api.services.video_gen import generate_video_from_slides
from api.db import sync_session, init_db
from api.models.models import Task
import json, datetime, uuid, logging

logger = logging.getLogger('autoscillab.tasks.video')

@celery_app.task(name='task.generate_video', bind=True)
def generate_video(self, slides, lang='en'):
    try:
        init_db()
    except Exception:
        pass
    task_id = str(self.request.id) if hasattr(self.request, 'id') else str(uuid.uuid4().hex)
    with sync_session() as session:
        t = Task(task_id=task_id, job_type='video', params=json.dumps({'slides': slides}), status='running', created_at=datetime.datetime.utcnow())
        session.add(t); session.commit()
    try:
        path = generate_video_from_slides(slides, lang=lang)
        with sync_session() as session:
            t = session.query(Task).filter(Task.task_id==task_id).first()
            t.status = 'success'; t.result = path; t.updated_at = datetime.datetime.utcnow()
            session.add(t); session.commit()
        return path
    except Exception as e:
        logger.exception('video task failed: %s', e)
        with sync_session() as session:
            t = session.query(Task).filter(Task.task_id==task_id).first()
            t.status = 'failed'; t.result = str(e); t.updated_at = datetime.datetime.utcnow()
            session.add(t); session.commit()
        raise

