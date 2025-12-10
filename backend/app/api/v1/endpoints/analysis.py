from typing import Any
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from app.api import deps
from app.models.user import User
from app.services.analysis_service import analysis_service

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    """
    Upload a data file (CSV/Excel) and get basic EDA summary.
    """
    try:
        summary = await analysis_service.process_upload(file)
        return summary
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to process file")
