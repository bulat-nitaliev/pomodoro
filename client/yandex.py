from dataclasses import dataclass
from core import Settings
import requests


@dataclass
class YandexClient:
    settings: Settings

    def get_user_info(self, code:str):
        access_token = self._get_user_access_token(code=code)
        user_info = requests.get(
                "https://login.yandex.ru/info?format=json", headers={"Authorization": f"OAuth {access_token}"}
            )
        
        return user_info.json()


    def _get_user_access_token(self,code:str):
        data = {
            "grant_type":"authorization_code",
            "code": code,
            "client_id": self.settings.Y_CLIENT_ID,
            "client_secret": self.settings.Y_SECRET_KEY
        }

        headers = {
            "Content-type": "application/x-www-form-urlencoded"
        }
        
        response = requests.post(url=self.settings.Y_TOKEN_URL, data=data, headers=headers)
        print(response.json())
        return response.json()["access_token"]