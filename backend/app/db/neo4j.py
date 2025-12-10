from neo4j import GraphDatabase, AsyncGraphDatabase
from app.core.config import settings

class Neo4jManager:
    def __init__(self):
        self.driver = None

    def connect(self):
        if not self.driver:
            self.driver = AsyncGraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
            )

    async def close(self):
        if self.driver:
            await self.driver.close()
            self.driver = None

    async def verify_connectivity(self):
        if not self.driver:
            self.connect()
        await self.driver.verify_connectivity()

neo4j_driver = Neo4jManager()
