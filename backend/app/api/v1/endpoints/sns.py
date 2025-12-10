from typing import Any
from fastapi import APIRouter, Depends, Body
from app.api import deps
from app.models.user import User
from app.services.sns_service import sns_service

router = APIRouter()

@router.get("/youtube/auth-url")
async def get_youtube_auth_url(
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Get OAuth URL for YouTube authorization.
    """
    return {"url": sns_service.get_google_auth_url()}

@router.post("/youtube/upload")
async def upload_to_youtube(
    video_url: str = Body(...),
    title: str = Body(...),
    description: str = Body(...),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Upload a generated video to YouTube.
    """
    # In a real scenario, we need the user's stored OAuth token
    await sns_service.upload_video_to_youtube(video_url, title, description)
    return {"status": "processing", "message": "Upload started"}
