from dataclasses import dataclass
from core import Settings
import requests


@dataclass
class GoogleClient:
    settings:Settings


    def get_user_info(self, code:str):
        access_token = self._get_user_access_token(code=code)
        user_info = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo", headers={"Authorization": f"Bearer {access_token}"}
            )
        
        return user_info.json()


    def _get_user_access_token(self,code:str):
        data = {
            "code": code,
            "client_id": self.settings.CLIENT_ID,
            "client_secret": self.settings.SECRET_KEY,
            "redirect_uri": self.settings.REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        
        response = requests.post(url=self.settings.TOKEN_URL, data=data)
        return response.json()["access_token"]