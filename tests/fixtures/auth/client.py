
from dataclasses import dataclass
from app.config import Settings
import httpx
import pytest


@dataclass
class FakeGoogleClient:
    settings:Settings
    async_client: httpx.AsyncClient


    async def get_user_info(self, code:str):
        
        async with self.async_client as client:
            access_token = 'fake acces_token'
            user_info = {
                'acces_token': access_token
            }
        
        return user_info
    

@dataclass
class FakeYandexClient:
    settings:Settings
    async_client: httpx.AsyncClient


    async def get_user_info(self, code:str):
        
        async with self.async_client as client:
            access_token = 'fake acces_token'
            user_info = {
                'acces_token': access_token
            }
        
        return user_info
    


@pytest.fixture
def google_client():
    return FakeGoogleClient(
        settings=Settings(),
        async_client=httpx.AsyncClient()
    )


@pytest.fixture
def yandex_client():
    return FakeYandexClient(
        settings=Settings(),
        async_client=httpx.AsyncClient()
    )