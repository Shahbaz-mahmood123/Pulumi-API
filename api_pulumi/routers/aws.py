import os
from typing import Union

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.debug_aws_batch import DebugAWSBatch

from ..db import compute_env
from ..db.database import engine, SessionLocal

router = APIRouter(prefix="/aws")

debug_aws = DebugAWSBatch()

id ="ShahbazCompute-5tQSF2ahyA19GNS5b8rzNS-work" 


@router.get("/job-queue")
async def get_job_queue_status() -> str:
    job_queue = debug_aws.get_job_queue_status(id)
    if not job_queue:
        return HTTPException(status_code=400, detail="Unable to fetch job queue validate your credentials or region")
    status = job_queue.get("jobQueueState", "")
    return status

@router.get("/compute-env")
async def get_compute_enviornment_status() -> str:
    compute_env = debug_aws.get_compute_env_status(id)
    status = compute_env.get("computeEnviornmentState", "")
    return status
    
@router.get("/ecs")
async def get_ecs_cluster_status() :
    ecs_cluster = debug_aws.get_ecs_cluster(id)
    print(ecs_cluster)
    if ecs_cluster:
        cluster = ecs_cluster.get("clusters", "")
        print(cluster)
        cluster_state = cluster[0].get("status", "")
        return cluster_state
    else:
        return f"Error: {ecs_cluster}"
    

@router.get("/job-queue/running")
async def get_running_jobs():
    pass

@router.get("/job-queue/submitted")
async def get_running_jobs():
    pass

@router.get("/job-queue/failed")
async def get_running_jobs():
    pass

@router.get("/job-queue/failed")
async def get_running_jobs():
    pass

@router.get("/job-queue/completed")
async def get_running_jobs():
    pass

@router.get("/autoscaling-group")
async def get_autoscaling_group():
    pass

@router.get("autoscaling-group/activity")
async def get_autoscaling_grou_activity():
    pass

@router.get("cloud-watch/logs")
async def get_cloud_watch_logs(): 
    pass


