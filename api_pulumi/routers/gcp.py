import os
from typing import Union
import json

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from ..internal.gcp_pulumi import SelectGCP

select_gcp_type = SelectGCP()

router = APIRouter(prefix="/gcp")

def format_preview_output():
    pass

@router.get("/compute/minimal/preview", response_class=HTMLResponse)
def preview():
    preview = select_gcp_type.preview_compute_engine_instance()

    output = preview.stdout
    multiline_output = ""
    
    for line in output.splitlines():
        
       multiline_output += f"""<p>{line}</p>"""
    
    return "<div>" + multiline_output + "</div"
 
@router.get("/compute/minimal/up")
def up():
    up = select_gcp_type.up_compute_engine_instance()
    return {"up": up}

@router.get("/compute/minimal/destroy")
def destroy():
    destroy = select_gcp_type.destroy_compute_engine_instance()
    return {"destroy": destroy}

@router.get("/compute/minimal/destroy_stack")
def destroy_stack():
    destroy_stack = select_gcp_type.destroy_stack_compute_engine_instance()
    return {"destroy_stack": destroy_stack}

@router.get("/compute/minimal/refresh")
def refresh():
    refresh = select_gcp_type.refresh_stack_compute_engine_instance()
    if refresh is None:
        return 0
    return refresh

