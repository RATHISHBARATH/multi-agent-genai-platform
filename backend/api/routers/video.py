
from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/generate")
async def generate_video(script: str):
    # stub: generate short MP4 from script (placeholder)
    return {"status": "video_generated", "script_preview": script[:120]}
