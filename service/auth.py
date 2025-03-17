from dataclasses import dataclass
from schema import UserLoginSchema

@dataclass
class AuthService:

    def login(username:str, password:str)->UserLoginSchema:
        pass