
from fastapi import APIRouter
from ..schemas.ppt import PPTRequest
from ..services.ppt_creator import PPTCreator

router = APIRouter()

@router.post("/create")
async def create_ppt(req: PPTRequest):
    ppt_path = PPTCreator().create(req.title, req.slides)
    return {"status": "ppt_created", "path": ppt_path}
