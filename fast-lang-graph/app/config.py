from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    """Centralized application configuration."""

    # Application
    APP_NAME: str = "FastAPI multi model LangGraph"
    APP_VERSION: str = "0.0.1"
    APP_DESCRIPTION: str = "This is a FastAPI and LangGraph minimal project for lang graph multi model usage."

    # OpenAI models
    OPENAI_API_KEY: SecretStr
    OPENAI_MODEL: str = "gpt-4.1"
    OPENAI_MODEL_MINI: str = "gpt-4.1-mini"
    OPENAI_MODEL_NANO: str = "gpt-4.1-nano"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_default=True,
    )
