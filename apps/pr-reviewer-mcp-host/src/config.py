from loguru import logger
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration class that loads and validates environment variables for the application.
    """

    # --- Environment loading ---
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    # --- OpenAI/Gemini Configuration ---
    GEMINI_API_KEY: str = Field(
        description="API key for Gemini service authentication."
    )

    SLACK_CHANNEL_ID : str = Field(description="Reviews channel ID for Slack integration")

    @field_validator("GEMINI_API_KEY", "SLACK_CHANNEL_ID")
    @classmethod
    def check_not_empty(cls, value: str, info) -> str:
        """
        Validator to ensure that required fields are not empty.
        Logs an error and raises ValueError if a required field is missing or blank.
        """
        if not value or value.strip() == "":
            logger.error(f"{info.field_name} cannot be empty.")
            raise ValueError(f"{info.field_name} cannot be empty.")
        return value

try:
    settings = Settings()
except Exception as e:
    logger.error(f"❌ Failed to load configuration: {e}")
    raise SystemExit(e)
