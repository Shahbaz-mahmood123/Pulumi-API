
from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine


class Stack(SQLModel, table=True):
    id: Optional[int] =Field(default=None, primary_key=True)
    name: str
    is_active:  bool
    # work_dir = Column(String)
    # project_name = Column(String, unique=True)

class ComputeEnv(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name:  str

class Settings(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    platform_url: str
    workspace_id: int
    token:  str
    
    