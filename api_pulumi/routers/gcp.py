import os
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import APIRouter

from ..internal.gcp_pulumi import SelectGCP


select_gcp_type = SelectGCP()

router = APIRouter(prefix="/gcp")

@router.get("/compute/minimal/preview")
def read_root():
    preview = select_gcp_type.preview_compute_engine_instance()
    return preview

@router.get("/compute/minimal/up")
def read_root():
    up = select_gcp_type.preview_compute_engine_instance()
    return up

@router.get("/compute/minimal/destroy")
def read_root():
    destroy = select_gcp_type.preview_compute_engine_instance()
    return destroy

@router.get("/compute/minimal/destroy_stack")
def read_root():
    destroy_stack = select_gcp_type.preview_compute_engine_instance()
    return destroy_stack