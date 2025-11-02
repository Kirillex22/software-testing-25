from dataclasses import dataclass

@dataclass
class Settings:
    database_url: str = None # e.g., "sqlite:///./test.db"
    broker_url: str = None # e.g., "redis://localhost:6379/0"
    topic_name: str = None # e.g., "user-events"

settings = Settings()

def set_settings(new_settings: Settings) -> None:
    global settings
    settings = new_settings
    
def get_settings() -> Settings:
    return settings