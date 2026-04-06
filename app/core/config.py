from pydantic_settings import BaseSettings, SettingsConfigDict
import urllib.parse


class Settings(BaseSettings):
    PARSEUR_API_KEY: str
    PARSEUR_MAILBOX_ID: str

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str

    @property
    def database_url(self) -> str:
        password = urllib.parse.quote_plus(self.DB_PASSWORD)
        return f"postgresql+psycopg://{self.DB_USER}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="app/.env", extra="ignore")


settings = Settings()

