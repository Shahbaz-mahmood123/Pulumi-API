from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session,select

from ..db import models
from ..db.database import Database

class Settingsdto():
    
    def __init__(self) -> None:
        self.database = Database()

    def get_settings(self) -> models.Settings:
        with Session(self.database.engine) as session:
            settings = session.exec(select(models.Settings)).first()
            return settings
    
    def create_settings(self, workspace_id: int, platform_url: str, token: str):
        
        new_settings = models.Settings(workspace_id=workspace_id, platform_url=platform_url, token=token) 
        try:
            self.database.newRecord(new_settings)
        except Exception as e:
            return {SQLAlchemyError: e}
            


