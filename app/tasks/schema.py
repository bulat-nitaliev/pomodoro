from pydantic import BaseModel
from typing import Optional

class TasksSchema(BaseModel):
    name: Optional[str]
    pomodoro_count: int 
    category_id: int
    user_id:int

    class Config:
        from_attributes = True


class TasksSchemaPartial(BaseModel):
    name: Optional[str]
    pomodoro_count: Optional[int] 
    category_id: Optional[int]



class Category(BaseModel):
    name: Optional[str]
    type: int


class TasksCreateSchema(BaseModel):
    name: Optional[str]
    pomodoro_count: int 
    category_id: int