from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from api_pulumi.internal.settings import Settingsdto

#from ..db.database import engine, SessionLocal

router = APIRouter(prefix="/debug")

@router.get("/compute-env")
def get_compute_envs():
        config = Settingsdto()
        settings = config.get_settings()
        return {HTMLResponse(status_code=200, content=settings.model_dump_json())}