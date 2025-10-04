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
    openai_model: str = "gpt-5"  # GPT-5 for all agentic workflows

    # Epic Integration
    epic_fhir_base_url: Optional[str] = None
    epic_client_id: Optional[str] = None
    epic_client_secret: Optional[str] = None

    # PhenoML Configuration
    phenoml_api_url: Optional[str] = None
    phenoml_model_path: Optional[str] = None
    phenoml_username: Optional[str] = None
    phenoml_password: Optional[str] = None
    phenoml_base_url: Optional[str] = None
    provider: Optional[str] = None

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
        extra = "ignore"  # Ignore extra fields in .env


settings = Settings()
