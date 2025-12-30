import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# Enforce virtual environment usage
if sys.prefix == sys.base_prefix and not os.getenv("SKIP_VENV_CHECK"):
    print("Error: This application must be run within a virtual environment.")
    print("Please activate your virtual environment (e.g., 'source venv/bin/activate') or set SKIP_VENV_CHECK=1.")
    sys.exit(1)

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.neo4j import neo4j_driver
from app.db.qdrant import qdrant_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    neo4j_driver.connect()
    qdrant_client.connect()
    yield
    # Shutdown
    await neo4j_driver.close()
    qdrant_client.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {"status": "ok"}
