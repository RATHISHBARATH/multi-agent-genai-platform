from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from ..workers.celery_app import celery_app
from ..workers.tasks.orchestrate_research import orchestrate_research
from ..workers.tasks.generate_video import generate_video
from ..workers.tasks.generate_ppt import generate_ppt
from ..auth import oauth2_scheme
from ..db import async_session, init_db
from ..models.models import Task
import uuid, json, datetime

router = APIRouter()

@router.post('/start_research')
async def start_research(payload: dict, token: str = Depends(oauth2_scheme)):
    query = payload.get('q')
    if not query:
        raise HTTPException(400, 'query required')
    # call celery task
    job = orchestrate_research.delay(query)
    return {'task_id': job.id}

@router.post('/start_video')
async def start_video(payload: dict, token: str = Depends(oauth2_scheme)):
    slides = payload.get('slides', [])
    job = generate_video.delay(slides)
    return {'task_id': job.id}

@router.post('/start_ppt')
async def start_ppt(payload: dict, token: str = Depends(oauth2_scheme)):
    title = payload.get('title', 'auto-ppt')
    slides = payload.get('slides', [])
    job = generate_ppt.delay(title, slides)
    return {'task_id': job.id}

@router.get('/task_status/{task_id}')
async def task_status(task_id: str, token: str = Depends(oauth2_scheme)):
    # query DB for task status (async)
    try:
        async with async_session() as session:
            t = await session.execute("""SELECT * FROM task WHERE task_id = :tid""", {'tid': task_id})
            row = t.first()
            if not row:
                return {'status': 'unknown'}
            # row is Row object; serialize
            return dict(row._mapping)
    except Exception:
        return {'status': 'unknown'}
