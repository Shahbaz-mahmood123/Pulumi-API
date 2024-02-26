import os
from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import compute_env
from ..db.database import engine, SessionLocal

router = APIRouter(prefix="/debug")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/compute-env")
def get_compute_envs(name: str ,db: Session = Depends(get_db)):
    db_ce = compute_env.get_compute_env (db=db, compute_env_name=name)
    if db_ce is None:
        return HTTPException(status_code=404, detail="Compute enviornment does not exist")
    return db_ce