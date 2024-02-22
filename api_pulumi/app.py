import os
from typing import Annotated, Union

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from starlette.requests import Request

from .routers.gcp import gcp_router

app = FastAPI()

#add additional routes here
app.include_router(gcp_router)

templates = Jinja2Templates(directory="api_pulumi/templates")

app.mount("/static", StaticFiles(directory="api_pulumi/static"), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    
@app.get("/")
def read_root():
    dummy_request = Request(scope={"type": "http"})
    return templates.TemplateResponse("base.html", context={"test": "test", "request": dummy_request})

@app.get("/gcp")
def gcp():
    dummy_request = Request(scope={"type": "http"})
    return templates.TemplateResponse("gcp.html", context={"test": "test", "request": dummy_request})

@app.get("/auth")
def auth(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.get("/get-message")
def get_message():
    message = "Hello from the backend!"
    return {"message": message}

if __name__ == "app":
    app()