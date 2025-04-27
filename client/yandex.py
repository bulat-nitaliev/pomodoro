from dataclasses import dataclass
from core import Settings
import httpx


@dataclass
class YandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code:str):
        access_token = self._get_user_access_token(code=code)
        async with self.async_client() as client:
            user_info = await client.get(
                    "https://login.yandex.ru/info?format=json", headers={"Authorization": f"OAuth {access_token}"}
                )
        
        return user_info.json()


    async def _get_user_access_token(self,code:str):
        data = {
            "grant_type":"authorization_code",
            "code": code,
            "client_id": self.settings.Y_CLIENT_ID,
            "client_secret": self.settings.Y_SECRET_KEY
        }

        headers = {
            "Content-type": "application/x-www-form-urlencoded"
        }
        async with self.async_client() as client:
            response = await client.post(url=self.settings.Y_TOKEN_URL, data=data, headers=headers)
        print(response.json())
        
        return response.json()["access_token"]