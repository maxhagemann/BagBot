from pydantic_settings import BaseSettings, SettingsConfigDict

#loads settings from env
class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()