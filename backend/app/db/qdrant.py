from qdrant_client import QdrantClient
from app.core.config import settings

class QdrantManager:
    def __init__(self):
        self.client = None

    def connect(self):
        if not self.client:
            self.client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT
            )

    def close(self):
        self.client = None

qdrant_client = QdrantManager()
