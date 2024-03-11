import os
from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from core.debug_aws_batch import DebugAWSBatch

from ..db import compute_env
from .settings import Settings

router = APIRouter(prefix="/aws")

debug_aws = DebugAWSBatch()

id ="ShahbazCompute-5jB4AbxLx2imTOtG1QcySO-head" 

class AWS():
    def __init__(self) -> None:
        self.debug_aws = DebugAWSBatch()
        self.workspace_id = None
        self.platform_url = None     
        
@router.get("/job-queue",  response_class=PlainTextResponse)
async def get_job_queue_status(id: str) -> str:
    job_queue = debug_aws.get_job_queue_status(id)
    if not job_queue:
        return HTTPException(status_code=400, detail="Unable to fetch job queue validate your credentials or region")
    status = job_queue.get("jobQueueState", "")
    return status

@router.get("/compute-env", response_class=PlainTextResponse)
async def get_compute_enviornment_status() -> str:
    compute_env = debug_aws.get_compute_env_status(id)
    status = compute_env.get("computeEnviornmentState", "")
    return status
    
@router.get("/ecs",  response_class=PlainTextResponse)
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
    running_jobs = debug_aws.get_running_jobs(id)
    print(running_jobs)
    return running_jobs

@router.get("/job-queue/submitted")
async def get_submitted_jobs():
    pass

@router.get("/job-queue/failed")
async def get_failed_jobs():
    pass

@router.get("/job-queue/runnable")
async def get_runnable_jobs():
    jobs = debug_aws.get_runnable_jobs(id)
    return jobs

@router.get("/job-queue/succeeded")
async def get_succeeded_jobs():
    jobs = debug_aws.get_succeeded_jobs(id)
    return jobs

@router.get("/autoscaling-group", response_class=HTMLResponse)
async def get_autoscaling_group():
    asg = debug_aws.get_autoscaling_group(id)
    
    asg_name = asg.get("AutoScalingGroupName")
    html = f"""

    <div> 
    {asg_name}
    </div>
    """
    
    return html

@router.get("autoscaling-group/activity")
async def get_autoscaling_group_activity():
    ag = debug_aws.get_autoscaling_group(id)
    activity = debug_aws.get_scaling_activities(ag)
    return activity

@router.get("cloud-watch/logs")
async def get_cloud_watch_logs(): 
    asg = debug_aws.get_autoscaling_group()
    logs = debug_aws.get_recent_forge_cloudwatch_logs(asg)
    return logs

# A sample function that simulates fetching options from a database or external service.
def fetch_compute_enviornments():
    
    #ce = debug_aws.get_tower_compute_envs_id_list()
    # These options would typically come from a database or some external service.
    return ["ShahbazCompute-5tQSF2ahyA19GNS5b8rzNS-work", "Option 2", "Option 3"]

@router.get("/compute_envs/list", response_class=HTMLResponse)
async def get_options():
    # Fetch options for the dropdown.
    options = fetch_compute_enviornments()
    # Convert the options to HTML list items.
    options_html = "".join(f"<li><a>{option}<a></li>" for option in options)
    # Return the options as an HTML string.
    return options_html

@router.get("/jobs_table", response_class=HTMLResponse)
async def get_jobs_table():
    
    suceeded_jobs = debug_aws.get_succeeded_jobs(id)
    failed_jobs = debug_aws.get_failed_jobs(id)
    runnable_jobs = debug_aws.get_runnable_jobs(id)
    jobs_html = ""
    count = 0
    
    exit_reason = "container issue"
   
    if type(suceeded_jobs) != str:
        succeded_jobs_dict = suceeded_jobs.get("jobSummaryList", [])
        for job in succeded_jobs_dict:
            status = job.get("status")
            job_name = job.get("jobName")
            exit_reason = job.get("statusReason")
            jobs_html += f"""
                <tr class="hover">
                <th>{count}</th>
                <td>{job_name}</td>
                <td>{status} </td>
                <td>{exit_reason}</td>
                </tr>
            """
            count+=count
        
    if type(runnable_jobs) != str :
        runnable_jobs_dict = runnable_jobs.get("jobSummaryList", [])
        for job in runnable_jobs_dict:
            status = job.get("status")
            job_name = job.get("jobName")
            exit_reason = job.get("statusReason")
            jobs_html += f"""
                <tr class="hover">
                <th>{count}</th>
                <td>{job_name}</td>
                <td>{status} </td>
                <td>{exit_reason}</td>
                </tr>
            """
            
    if type(failed_jobs) != str :
        failed_jobs_dict = failed_jobs.get("jobSummaryList", [])
        for job in failed_jobs_dict:
            status = job.get("status")
            job_name = job.get("jobName")
            exit_reason = job.get("statusReason")
            jobs_html += f"""
                <tr class="hover">
                <th>{count}</th>
                <td>{job_name}</td>
                <td>{status} </td>
                <td>{exit_reason}</td>
                </tr>
            """

    return jobs_html 

