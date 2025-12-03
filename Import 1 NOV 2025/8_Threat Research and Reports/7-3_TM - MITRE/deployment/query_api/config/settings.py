"""
AEON MITRE Query API Configuration
File: config/settings.py
Created: 2025-11-08
Purpose: Application configuration management
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Neo4j Configuration
    neo4j_uri: str = Field(default="bolt://localhost:7687", env="NEO4J_URI")
    neo4j_user: str = Field(default="neo4j", env="NEO4J_USER")
    neo4j_password: str = Field(env="NEO4J_PASSWORD")
    neo4j_database: str = Field(default="neo4j", env="NEO4J_DATABASE")
    neo4j_max_connection_pool_size: int = Field(default=50, env="NEO4J_MAX_CONNECTION_POOL_SIZE")
    neo4j_connection_acquisition_timeout: int = Field(default=60, env="NEO4J_CONNECTION_ACQUISITION_TIMEOUT")

    # Redis Configuration
    redis_host: str = Field(default="localhost", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    redis_db: int = Field(default=0, env="REDIS_DB")
    redis_password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")

    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_workers: int = Field(default=4, env="API_WORKERS")
    api_key_header: str = Field(default="X-API-Key", env="API_KEY_HEADER")
    api_keys: str = Field(default="", env="API_KEYS")

    # Query Configuration
    max_query_timeout: int = Field(default=30, env="MAX_QUERY_TIMEOUT")
    default_page_size: int = Field(default=100, env="DEFAULT_PAGE_SIZE")
    max_page_size: int = Field(default=1000, env="MAX_PAGE_SIZE")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")

    # CORS
    cors_origins: str = Field(default="*", env="CORS_ORIGINS")
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")

    @property
    def api_keys_list(self) -> List[str]:
        """Parse API keys from comma-separated string"""
        if not self.api_keys:
            return []
        return [key.strip() for key in self.api_keys.split(",") if key.strip()]

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
