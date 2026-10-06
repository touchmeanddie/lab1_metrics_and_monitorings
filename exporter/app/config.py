from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    api_url: str = "http://api:8080"
    scrape_interval_seconds: int = 15
    exporter_port: int = 9102


settings = Settings()
