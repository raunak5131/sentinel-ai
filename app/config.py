from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "SentinelAI"

    DATABASE_URL: str

    REDIS_URL: str = "redis://localhost:6379/0"

    STORAGE_DIR: str = "./uploads"

    GROQ_API_KEY: str 

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()