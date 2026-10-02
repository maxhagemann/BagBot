from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

#loads settings from env
class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    secret_key: str 
    #test_db: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    

settings = Settings()
