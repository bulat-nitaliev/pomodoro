from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_DRIVER:str = 'postgresql+psycopg2'
    DB_HOST:str = '0.0.0.0'
    DB_PORT:str = '5432'
    DB_USER:str = 'postgres'
    DB_PASS:str = 'SA-testing-1'
    DB_NAME:str = "pomodor"
    CACHE_HOST:str = 'localhost'
    CACHE_PORT:int = 6379
    CACHE_DB:int = 0

    @property
    def get_db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

settings = Settings()