from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str # e.g., "sqlite:///./test.db"
    broker_url: str # e.g., "redis://localhost:6379/0"
    topic_name: str # e.g., "user-events"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

def set_settings(new_settings: Settings) -> None:
    global settings
    settings = new_settings
    
def get_settings() -> Settings:
    return settings