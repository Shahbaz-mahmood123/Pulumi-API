from pydantic import BaseModel


class Stack(BaseModel):
    id: int
    name: str 
    is_active: bool
