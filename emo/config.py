from functools import lru_cache
from pydantic_settings import BaseSettings


# Default User-Agent for outbound HTTP requests
USER_AGENT: str = "EMO-Core/1.0 (research; contact@example.org)"


class Settings(BaseSettings):
    """
    Global configuration for EMO-Core.

    Values are read from environment variables, with safe defaults for
    local development.
    """

    env: str = "development"

    # Database (future Interface Registry & pipelines)
    database_url: str = "postgresql+psycopg2://emo:emo@localhost:5432/emo"

    # External data sources (indicative defaults; see docs for real endpoints)
    gdelt_doc_api_base: str = "https://api.gdeltproject.org/api/v2/doc/doc"
    openalex_base: str = "https://api.openalex.org"
    destine_base: str = "https://destine.ecmwf.int"  # indicative only
    undrr_base: str = "https://www.undrr.org"
    wmo_base: str = "https://wmo.int"

    class Config:
        env_prefix = "EMO_"
        case_sensitive = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
