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
    stderr = preview.stderr
    multiline_output = ""
    for line in output.splitlines():
        
       multiline_output += f"""<p>{line}</p>"""
    
    return "<div>" + multiline_output + "</div>"
 
@router.get("/compute/minimal/up", response_class=HTMLResponse)
def up():
    up = select_gcp_type.up_compute_engine_instance()
    print(up.stdout)
    stdout = up.stdout
    multiline_output = ""
    for line in stdout.splitlines():
        
       multiline_output += f"""<p>{line}</p>"""
    
    return "<div>" + multiline_output + "</div>"

@router.get("/compute/minimal/destroy", response_class=HTMLResponse)
def destroy():
    destroy = select_gcp_type.destroy_compute_engine_instance()
    print(destroy)
    output = destroy.stdout
    stderr = destroy.stderr
    multiline_output = ""
    for line in output.splitlines():
        
       multiline_output += f"""<p>{line}</p>"""
    
    return "<div>" + multiline_output + "</div>"

@router.get("/compute/minimal/destroy_stack", response_class=HTMLResponse)
def destroy_stack():
    destroy_stack = select_gcp_type.destroy_stack_compute_engine_instance()
    output = destroy_stack.stdout
    stderr = destroy_stack.stderr
    multiline_output = ""
    for line in output.splitlines():
        
       multiline_output += f"""<p>{line}</p>"""
    
    return "<div>" + multiline_output + "</div>"

@router.get("/compute/minimal/refresh")
def refresh():
    refresh = select_gcp_type.refresh_stack_compute_engine_instance()
    output = refresh.stdout
    stderr = refresh.stderr
    multiline_output = ""
    for line in output.splitlines():
        
       multiline_output += f"""<p>{line}</p>"""
    
    return refresh

