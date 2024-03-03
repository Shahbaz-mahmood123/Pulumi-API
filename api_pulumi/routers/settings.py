
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from ..db import models
from ..db.database import  Database
from ..internal.settings import Settingsdto


router = APIRouter(prefix="/settings")
    

class Settings():
    def __init__(self) -> None:
        pass 
               
    @router.get("/")
    def get_settings():
        config = Settingsdto()
        settings = config.get_settings()
        return {HTMLResponse(status_code=200, content=settings)}
    
    @router.post("/create")
    def create_settings(settings: models.Settings):
        config = Settingsdto()
        set = config.create_settings(workspace_id = settings.workspace_id,platform_url = settings.platform_url, token = settings.token)
        return {HTMLResponse(status_code=200, content="Success")}
    
    