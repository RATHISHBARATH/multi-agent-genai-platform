
from fastapi import APIRouter, BackgroundTasks
from ..schemas.research import ResearchRequest
from ..services.summarizer import Summarizer

router = APIRouter()

@router.post("/summarize")
async def summarize(req: ResearchRequest, background_tasks: BackgroundTasks):
    # enqueue background summarization (placeholder)
    background_tasks.add_task(Summarizer().summarize, req.text)
    return {"message": "summarization started", "title": req.title}
