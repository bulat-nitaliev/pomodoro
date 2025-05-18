from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    DB_DRIVER: str = "postgresql+asyncpg"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_NAME: str = "pomodor"
    TEST_DB_NAME: str = "test_pomodor"
    CACHE_HOST: str = "localhost"
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    TEST_CACHE_HOST: str = "localhost"
    TEST_CACHE_PORT: int = 6379
    TEST_CACHE_DB: int = 1

    JWT_SECRET: str = "secret_key"
    JWT_ALGORITM: str = "HS256"

    CLIENT_ID: str = "ddddd"
    REDIRECT_URI: str = "http://localhost:8000/auth/google"
    TOKEN_URL: str = "https://oauth2.googleapis.com/token"
    SECRET_KEY: str = "ssssss"

    Y_CLIENT_ID: str = "ddddd"
    Y_SECRET_KEY: str = "ssssss"
    Y_REDIRECT_URI: str = "http://localhost:8000/auth/yandex"
    Y_TOKEN_URL: str = "https://oauth.yandex.ru/token"
    # EMAIL_BACKEND:str
    EMAIL_HOST: str = "smtp.yandex.ru"
    EMAIL_PORT: int = 465
    EMAIL_USE_SSL: bool = True

    EMAIL_HOST_USER: str = "bulatnitaliev@yandex.ru"
    EMAIL_HOST_PASSWORD: str = "aaaaaa"

    EMAIL_SUBJECT: str = "Welcome message"
    EMAIL_TEXT: str = "Allhamdulillah"

    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"

    BROKER_URL: str = "localhost:9092"
    EMAIL_TOPIC: str = "email_topic"
    EMAIL_CALLBACK_TOPIC: str = "callback_email_topic"

    @property
    def get_db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def get_test_db_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.TEST_DB_NAME}"

    @property
    def get_url_redirect(self):
        return f"""https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.CLIENT_ID}&redirect_uri={self.REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"""

    @property
    def get_yandex_url_redirect(self):
        return f"""https://oauth.yandex.ru/authorize?response_type=code&client_id={self.Y_CLIENT_ID}&redirect_uri={self.Y_REDIRECT_URI}"""


settings = Settings()
