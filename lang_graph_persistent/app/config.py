from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    """Centralized application configuration."""
    
    # Application
    APP_NAME: str = "FastAPI Persistent checkpointing LangGraph"
    APP_VERSION: str = "0.0.1"
    APP_DESCRIPTION: str = "This is FastAPI, LangGraph Persistent checkpointing"
    
    # OpenAI models
    OPENAI_API_KEY: SecretStr
    OPENAI_MODEL: str = "gpt-4.1"

    # Database
    DATABASE_URL: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_default=True,
    )


def get_settings() -> Settings:
    return Settings()
