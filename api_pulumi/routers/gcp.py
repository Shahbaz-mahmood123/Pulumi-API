import os
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import APIRouter

from ..internal.gcp_pulumi import SelectGCP

select_gcp_type = SelectGCP()

gcp_router = APIRouter(prefix="/gcp")

@gcp_router.get("/compute/minimal/preview")
def preview():
    preview = select_gcp_type.preview_compute_engine_instance()
    return preview

@gcp_router.get("/compute/minimal/up")
def up():
    up = select_gcp_type.up_compute_engine_instance()
    return up

@gcp_router.get("/compute/minimal/destroy")
def destroy():
    destroy = select_gcp_type.destroy_compute_engine_instance()
    return destroy

@gcp_router.get("/compute/minimal/destroy_stack")
def destroy_stack():
    destroy_stack = select_gcp_type.destroy_stack_compute_engine_instance
    return destroy_stack
