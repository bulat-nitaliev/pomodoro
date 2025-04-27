from dataclasses import dataclass
from core import Settings
import httpx


@dataclass
class GoogleClient:
    settings:Settings
    async_client: httpx.AsyncClient


    async def get_user_info(self, code:str):
        data = {
            "code": code,
            "client_id": self.settings.CLIENT_ID,
            "client_secret": self.settings.SECRET_KEY,
            "redirect_uri": self.settings.REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        # access_token = self._get_user_access_token(code=code)
        async with self.async_client as client:
            response = await client.post(url=self.settings.TOKEN_URL, data=data)
            access_token = response.json()["access_token"]
            user_info = await client.get(
                    "https://www.googleapis.com/oauth2/v3/userinfo", headers={"Authorization": f"Bearer {access_token}"}
                )
        
        return user_info.json()


    # async def _get_user_access_token(self,code:str):
    #     data = {
    #         "code": code,
    #         "client_id": self.settings.CLIENT_ID,
    #         "client_secret": self.settings.SECRET_KEY,
    #         "redirect_uri": self.settings.REDIRECT_URI,
    #         "grant_type": "authorization_code",
    #     }
    #     async with self.async_client() as client:
    #         response = await client.post(url=self.settings.TOKEN_URL, data=data)
            
    #     return response.json()["access_token"]