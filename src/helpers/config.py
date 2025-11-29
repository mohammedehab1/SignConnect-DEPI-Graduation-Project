from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
    )

    # App Info
    APP_NAME: str
    APP_VERSION: str

    # Fine-tuned Whisper Model Settings
    BASE_MODEL: str
    MODEL_NAME: str
    HF_REPO: str

    # HuggingFace Authentication
    HF_TOKEN: str
    HF_CACHE_DIR: str

    MODEL_PATH : str

    PROCESS_INTERVAL : float
    VOTE_REQUIRED : float
    COOLDOWN : float
    FLASH_DURATION : float

settings = Settings()