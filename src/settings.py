from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with validation using Pydantic"""
    
    # API Keys and Credentials
    openai_api_key: str
    serper_api_key: str
    
    # Research Configuration
    max_search_results: int = Field(default=5, ge=1)
    max_scrape_retries: int = Field(default=3, ge=1)
    research_timeout: int = Field(default=300, ge=60)  # minimum 60 seconds
    
    # Model Configuration
    gpt_model: str = Field(default="gpt-4-turbo-preview")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    
    # Logging Configuration
    log_level: str = Field(
        default="INFO",
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Create settings instance
settings = Settings()

# Make variables available at module level for backward compatibility
OPENAI_API_KEY = settings.openai_api_key
SERPER_API_KEY = settings.serper_api_key
MAX_SEARCH_RESULTS = settings.max_search_results
MAX_SCRAPE_RETRIES = settings.max_scrape_retries
RESEARCH_TIMEOUT = settings.research_timeout
GPT_MODEL = settings.gpt_model
TEMPERATURE = settings.temperature
LOG_LEVEL = settings.log_level
