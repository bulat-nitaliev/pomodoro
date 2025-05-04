
from dataclasses import dataclass
from app.config import Settings
import httpx
import pytest
from app.users.auth.schema import GoogleSchema, YandexSchema
from faker import Factory as FakerFactory
from tests.fixtures.users.user_model import EXISTS_GOOGLE_USER, EXISTS_GOOGLE_PASSWORD


faker = FakerFactory.create()
 

@dataclass
class FakeGoogleClient:
    settings:Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code:str): 
        async with self.async_client as client:
            return GoogleSchema(
                email=EXISTS_GOOGLE_USER,
                name = EXISTS_GOOGLE_PASSWORD
            ).model_dump()
        
    

@dataclass
class FakeYandexClient:
    settings:Settings
    async_client: httpx.AsyncClient


    async def get_user_info(self, code:str): 
        async with self.async_client as client:
            return YandexSchema(
                default_email=faker.name(),
                login=faker.name()
            ).model_dump()
    


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