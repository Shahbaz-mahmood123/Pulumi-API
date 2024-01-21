import os
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

from .routers import gcp

app = FastAPI()

#add additional routes here
app.include_router(gcp.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "app":
    app()