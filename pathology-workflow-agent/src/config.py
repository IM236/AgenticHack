"""Configuration management."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""

    # API Configuration
    app_name: str = "Pathology Workflow Agent"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4-turbo-preview"

    # Epic Integration
    epic_fhir_base_url: Optional[str] = None
    epic_client_id: Optional[str] = None
    epic_client_secret: Optional[str] = None

    # PhenoML Configuration
    phenoml_api_url: Optional[str] = None
    phenoml_model_path: Optional[str] = None

    # Notification Settings
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None

    # Database (for future expansion)
    database_url: Optional[str] = "sqlite:///./pathology_workflow.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
