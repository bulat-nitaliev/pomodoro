from pydantic import BaseModel


class GoogleSchema(BaseModel):
    email:str
    name: str