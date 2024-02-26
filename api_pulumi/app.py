import os
from typing import Annotated, Union

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from starlette.requests import Request
from sqlalchemy.orm import Session

from .db import models, schema, pulumi
from .db.database import engine, SessionLocal
from .routers import aws, gcp, compute_env

app = FastAPI()

#add additional routes here
app.include_router(gcp.router)
app.include_router(compute_env.router)
app.include_router(aws.router)

templates = Jinja2Templates(directory="api_pulumi/templates")

app.mount("/static", StaticFiles(directory="api_pulumi/static"), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("base.html", context)

@app.get("/gcp")
def gcp():
    dummy_request = Request(scope={"type": "http"})
    return templates.TemplateResponse("gcp.html", context={"test": "test", "request": dummy_request})

@app.get("/gke")
def gcp():
    dummy_request = Request(scope={"type": "http"})
    return templates.TemplateResponse("gke.html", context={"test": "test", "request": dummy_request})

@app.get("/debug")
def debug():
    dummy_request = Request(scope={"type": "http"})
    return templates.TemplateResponse("debugging.html", context={"test": "test", "request": dummy_request})

@app.get("/auth")
def auth(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.post("/pulumi/stack")
def create_stack( stack: schema.Stack ,db: Session = Depends(get_db)):
    db_stack = pulumi.get_stack(db=db , stack_name=stack.name)
    if db_stack:
        raise HTTPException(status_code=400, detail="Email already registered")
    return pulumi.create_stack(db=db, stack=stack)
        
    
@app.get("/pulumi/stack")
def read_stack(stack_name: str , db: Session = Depends(get_db)):
    db_stack = pulumi.get_stack(db=db , stack_name=stack_name)
    if db_stack is None:
        return HTTPException(status_code=404, detail="stack does not exist")
    return db_stack
    
if __name__ == "app":
    app()