from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_PATH: str
    DB_ROOT_NODE: str

    model_config = SettingsConfigDict(env_file=".env")
