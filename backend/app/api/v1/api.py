from fastapi import APIRouter
from app.api.v1.endpoints import auth, chat, analysis, video, payment, sns

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(video.router, prefix="/video", tags=["video"])
api_router.include_router(payment.router, prefix="/payment", tags=["payment"])
api_router.include_router(sns.router, prefix="/sns", tags=["sns"])
