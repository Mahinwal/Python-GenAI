from mem0 import Memory
from app.config import get_settings

settings = get_settings()


# mem0ai + qdrant configuration
# Configure Mem0 + Qdrant
memory = Memory.from_config(
    {
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "collection_name": "user_memories",
                "host": "localhost",
                "port": 6333,
            },
        },
        "llm": {
            "provider": "openai",
            "config": {
                "model": "gpt-4.1-mini",
                "temperature": 0,
                "api_key": settings.openai_api_key.get_secret_value(),
            },
        },
        "embedder": {
            "provider": "openai",
            "config": {
                "model": "text-embedding-3-small",
                "api_key": settings.openai_api_key.get_secret_value(),
            },
        },
        "graph_store": {
            "provider": "neo4j",
            "config": {
                "url": "bolt://localhost:7687",
                "username": "neo4j",
                "password": "reform-william-center-vibrate-press-5829",
            },
        },
    }
)