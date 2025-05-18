from pydantic import BaseModel


class GoogleSchema(BaseModel):
    email: str
    name: str


class YandexSchema(BaseModel):
    default_email: str
    login: str


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str
