from api.workers.celery_app import celery_app
from api.services.orchestrator import Orchestrator
import asyncio
from api.db import sync_session, init_db
from api.models.models import Task
import json, datetime, uuid, logging

logger = logging.getLogger('autoscillab.tasks.orch')

@celery_app.task(name='task.orchestrate_research', bind=True)
def orchestrate_research(self, query, user_meta=None):
    # ensure DB tables exist (for demo); in prod use migrations
    try:
        init_db()
    except Exception:
        pass
    # create a Task row using sync_session
    task_id = str(self.request.id) if hasattr(self.request, 'id') else str(uuid.uuid4().hex)
    with sync_session() as session:
        t = Task(task_id=task_id, job_type='research', params=json.dumps({'query': query}), status='running', created_at=datetime.datetime.utcnow())
        session.add(t); session.commit()
    try:
        res = asyncio.run(Orchestrator().run_research_pipeline(query, user_meta=user_meta))
        with sync_session() as session:
            t = session.query(Task).filter(Task.task_id==task_id).first()
            t.status = 'success'
            t.result = json.dumps(res)
            t.updated_at = datetime.datetime.utcnow()
            session.add(t); session.commit()
        return res
    except Exception as e:
        logger.exception('orchestrate failed: %s', e)
        with sync_session() as session:
            t = session.query(Task).filter(Task.task_id==task_id).first()
            t.status = 'failed'
            t.result = str(e)
            t.updated_at = datetime.datetime.utcnow()
            session.add(t); session.commit()
        raise

