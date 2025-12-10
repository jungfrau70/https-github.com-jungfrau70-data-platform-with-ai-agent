from typing import Any
from fastapi import APIRouter, Depends, Body
from app.api import deps
from app.models.user import User
from app.services.video_service import video_service

router = APIRouter()

@router.post("/generate")
async def generate_video(
    script: str = Body(..., embed=True),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Request video generation from a script.
    """
    return await video_service.generate_video(script)

@router.get("/status/{job_id}")
async def check_video_status(
    job_id: str,
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Check the status of a video generation job.
    """
    return await video_service.check_status(job_id)
