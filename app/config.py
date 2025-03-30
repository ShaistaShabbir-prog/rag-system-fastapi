from pathlib import Path

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    OPENAI_API_KEY: str
    DATA_DIR: Path = Path("data")

    class Config:
        env_file = ".env"  # Load environment variables from a .env file


# Load config
config = Config()
