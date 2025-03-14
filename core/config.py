from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = 'postgresql+psycopg2://postgres:SA-testing-1@localhost:5432/pomodor'

settings = Settings()