from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # App
    app_name: str = "memory-agent-api"
    app_version: str = "0.0.0.1"
    app_description: str = "GenAI + Fastapi application with memory agent api by using OpenAI, Qdrant, Mem0, Neo4j"

    # OpenAI model and key
    openai_api_key: SecretStr = Field(..., description="OpenAI API key")
    openai_chat_model: str = Field(default="gpt-4o-mini")
    openai_embedding_model: str = Field(default="text-embedding-3-small")

def get_settings()->Settings:
    return Settings()
