from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    DB_DRIVER:str = 'postgresql+asyncpg'
    DB_HOST:str = ''
    DB_PORT:str = ''
    DB_USER:str = ''
    DB_PASS:str = ''
    DB_NAME:str = ""
    TEST_DB_NAME:str
    CACHE_HOST:str = 'localhost'
    CACHE_PORT:int = 6379
    CACHE_DB:int = 0
    TEST_CACHE_HOST:str = 'localhost'
    TEST_CACHE_PORT:int = 6379
    TEST_CACHE_DB:int = 1

    JWT_SECRET:str = ''
    JWT_ALGORITM:str = ''

    CLIENT_ID:str
    REDIRECT_URI:str
    TOKEN_URL: str
    SECRET_KEY:str

    Y_CLIENT_ID: str
    Y_SECRET_KEY: str
    Y_REDIRECT_URI: str
    Y_TOKEN_URL:str

    @property
    def get_db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
    
    @property
    def get_test_db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.TEST_DB_NAME}'
    
    @property
    def get_url_redirect(self):
        return f'''https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={self.CLIENT_ID}&redirect_uri={self.REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline'''
    
    
    @property
    def get_yandex_url_redirect(self):
        return f'''https://oauth.yandex.ru/authorize?response_type=code&client_id={self.Y_CLIENT_ID}&redirect_uri={self.Y_REDIRECT_URI}'''
    


settings = Settings()