import os
from typing import List, Union
from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "GC101"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 14
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Database
    NEO4J_URI: str
    NEO4J_PASSWORD: str
    NEO4J_USERNAME: str = "neo4j"
    
    QDRANT_HOST: str
    QDRANT_PORT: int = 6333

    # AI
    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(env_file=os.getenv("ENV_FILE", ".env"), case_sensitive=True, extra="ignore")

settings = Settings()
