from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # OpenAI and LLM credentials and connection settings
    OPENAI_API_URL: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    LLM_MODEL_NAME: Optional[str] = None

    # Generation parameters
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 1024

    # Default system prompt
    SYSTEM_PROMPT: str = "You are a helpful and concise AI assistant."


# Create a single instance of settings for the entire application
settings = Settings()
