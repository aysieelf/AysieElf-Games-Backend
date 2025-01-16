from functools import lru_cache
import os
from pathlib import Path
from typing import List, Union

from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings

# Get the current working directory
cwd = os.getcwd()
possible_env_paths = [
    Path(cwd) / ".env",
    Path(cwd).parent / ".env",
    Path(__file__).parent.parent.parent / ".env",
]

# Check where is the .env file
env_file = None
for env_path in possible_env_paths:
    if env_path.exists():
        env_file = env_path
        load_dotenv(env_path)
        break


# Define the settings class with all the environment variables
class Settings(BaseSettings):
    # prefix for the API
    API_V1_STR: str = "/api/v1"

    # project name
    PROJECT_NAME: str = "AysieElf Games"

    # Domains allowed to make requests
    CORS_ALLOWED_HOSTS: list[str] = ["*"]

    # Development mode / Production mode
    DEBUG: bool = os.getenv("DEBUG", "false").lower() in ["true", "1"]

    @field_validator("CORS_ALLOWED_HOSTS", check_fields=False)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Validates the CORS_ALLOWED_HOSTS environment variable.

        Args:
            v (Union[str, List[str]]): The environment variable value.

        Returns:
            Union[List[str], str]: The validated value.
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v

    # Database connection URL format:
    # postgresql://username:password@host:port/database_name

    # Examples:
    # Local development:
    #   postgresql://postgres:password123@localhost:5432/aysieelf_games

    # Production/Heroku:
    #   postgres://user:password@ec2-xx-xxx-xxx-xx.compute-1.amazonaws.com:5432/d123abc456def7
    DATABASE_URL: str

    # JWT variables
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION: int
    BLACKLISTED_TOKENS: list[str] = []

    # Email notification variables
    EMAIL_SENDER: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str

    # Google OAuth variables
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    SECRET_KEY: str

    # AWS variables for S3 bucket
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_BUCKET_NAME: str
    AWS_REGION: str

    @field_validator("DATABASE_URL", check_fields=False)
    def normalize_database_url(cls, v: str) -> str:
        """
        Converts Heroku's `postgres://` URLs to `postgresql://`,
        which SQLAlchemy expects.

        Args:
            v (str): The database URL.

        Returns:
            str: The normalized database URL.
        """
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    # Pydantic model configuration
    model_config = {
        "case_sensitive": True,
        "env_file": str(env_file),
        "env_file_encoding": "utf-8",
        "extra": "allow",
    }

    @classmethod
    def from_heroku(cls):
        return cls(
            _env_file=None,
            _env_file_encoding="utf-8",
        )

    @classmethod
    def from_env(cls):
        return cls(
            _env_file=str(env_file),
            _env_file_encoding="utf-8",
        )


# Cache the settings to avoid reading the environment variables multiple times
@lru_cache()
def get_settings() -> Settings:
    if env_file is None:
        return Settings.from_heroku()
    else:
        return Settings.from_env()


settings = get_settings()
