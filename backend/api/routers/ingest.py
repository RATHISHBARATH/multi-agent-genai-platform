from fastapi import APIRouter, BackgroundTasks
from ..services.paper_retriever import PaperRetriever
from ..services.orchestrator import Orchestrator

router = APIRouter()

@router.post("/papers")
async def ingest_papers(query: dict, background_tasks: BackgroundTasks):
    q = query.get("q", "")
    retriever = PaperRetriever()
    results = retriever.search(q)
    # kick off orchestration in background
    orch = Orchestrator()
    background_tasks.add_task(orch.run_research_pipeline, q)
    return {"count": len(results), "results": results[:5]}
