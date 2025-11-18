from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # General settings
    APP_NAME: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    BACKEND_CORS_ORIGINS: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @model_validator(mode='after')
    def assemble_cors_origins(self) -> 'Settings':
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            self.BACKEND_CORS_ORIGINS = [item.strip() for item in self.BACKEND_CORS_ORIGINS.split(',')]
        return self

    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        # Build the database URL
        port = f":{self.POSTGRES_PORT}" if self.POSTGRES_PORT else ""
        url = f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}{port}/{self.POSTGRES_DB}"
        return url


settings = Settings()
