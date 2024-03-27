import os
from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from core.debug_aws_batch import DebugAWSBatch
from core.compute_envs import SeqeraComputeEnvsWrapper

from ..db import compute_env
from .settings import Settingsdto
from ..internal.compute_envs import ComputeEnvs

router = APIRouter(prefix="/aws")

debug_aws = DebugAWSBatch()

id ="ShahbazCompute-60DYsGNvv7ePgububNBqE7-work" 

class AWS():
    def __init__(self) -> None:
        self.debug_aws = DebugAWSBatch()
        self.workspace_id = None
        self.platform_url = None     
        
@router.get("/job-queue",  response_class=PlainTextResponse)
async def get_job_queue_status() -> str:
    db = ComputeEnvs()
    ce_list = db.get_current_compute_env()
    print(ce_list.name)
    job_queue = debug_aws.get_job_queue_status(ce_list.name)
    if not job_queue:
        return HTTPException(status_code=400, detail="Unable to fetch job queue validate your credentials or region")
    status = job_queue.get("jobQueueState", "")
    return status

@router.get("/compute-env", response_class=PlainTextResponse)
async def get_compute_enviornment_status() -> str:
    
    db = ComputeEnvs()
    ce_list = db.get_current_compute_env()
    compute_env = debug_aws.get_compute_env_status(ce_list.name)
    status = compute_env.get("computeEnviornmentState", "")
    return status
    
@router.get("/ecs",  response_class=PlainTextResponse)
async def get_ecs_cluster_status() :
    db = ComputeEnvs()
    ce_list = db.get_current_compute_env()
    ecs_cluster = debug_aws.get_ecs_cluster(ce_list.name)
    if ecs_cluster:
        cluster = ecs_cluster.get("clusters", "")
        cluster_state = cluster[0].get("status", "")
        return cluster_state
    else:
        return f"Error: {ecs_cluster}"
    
@router.get("/ecs-cluster",  response_class=HTMLResponse)
async def get_ecs_cluster_status() :
    db = ComputeEnvs()
    ce_list = db.get_current_compute_env()
    ecs = debug_aws.get_ecs_cluster(ce_list.name)
    print(ecs)
    ecs_cluster = ecs.get("clusters", [])
    if ecs_cluster:  # Check if the list is not empty
        html = ""
        for cluster in ecs_cluster:
            print(cluster)
            html += f"""
            <div class="flex w-full">
                {create_info_card("Cluster Name", cluster.get('clusterName', 'N/A'))}
                {create_info_card("ARN", cluster.get('clusterArn', 'N/A'))}  
            </div>
            <div class="divider divider-horizontal"></div>
            <div class="flex w-full">
                {create_info_card("Running Tasks", cluster.get('runningTasksCount', 'N/A'))}
                {create_info_card("Pending Tasks", cluster.get('pendingTasksCount', 'N/A'))}  
                {create_info_card("Active Services", cluster.get('activeServicesCount', 'N/A'))}  
            </div>
            """
        return html
    else:
        return "No ECS clusters found."
    
    
@router.get("/job-queue/running")
async def get_running_jobs():
    db = ComputeEnvs()
    ce_list = db.get_current_compute_env()
    running_jobs = debug_aws.get_running_jobs(ce_list.name)
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

def create_info_card(label, value):
    return f"""
    <div class="card w-96 bg-base-100 shadow-xl">
        <div class="card-body">
        <h2 class="card-title">{label}</h2>
        <p>{value}</p>
    </div>
    </div>
    """
    
@router.get("/autoscaling-group", response_class=HTMLResponse)
async def get_autoscaling_group():
    db = ComputeEnvs()
    ce_list = db.get_current_compute_env()
    asg = debug_aws.get_autoscaling_group(ce_list.name)
    
    if asg == None:
        return  f"No match found for the autoscaling group, {ce_list.name}. Ensure you have run at least one compute so the resource is generated"
    
    asg_name = asg.get("AutoScalingGroupName")
    
    html =f"""
    
    <div class="flex w-full">
        {create_info_card("Auto Scaling Group Name", asg.get("AutoScalingGroupName"))}
        {create_info_card("ARN", asg.get("AutoScalingGroupARN"))}  {create_info_card("Region", asg.get("Region"))}
    </div>
    <div class="divider divider-horizontal"></div>
    <div class="flex w-full">
        {create_info_card("Min Size", str(asg.get("MinSize")))}
        {create_info_card("Max Size", str(asg.get("MaxSize")))}
        {create_info_card("Desired Capacity", str(asg.get("DesiredCapacity")))}
    </div>
    <div class="divider divider-horizontal"></div>
    <div class="flex w-full">
        {create_info_card("VPC Subnets", asg.get("VPCZoneIdentifier"))}
        {create_info_card("Created Time", asg.get("CreatedTime").strftime("%Y-%m-%d %H:%M:%S"))}
    </div>
    <div class="divider divider-horizontal"></div>
    <div class="flex w-full">
        {create_info_card("Instance Types", ", ".join([x["InstanceType"] for x in asg.get("MixedInstancesPolicy", {}).get("LaunchTemplate", {}).get("Overrides", [])]))}
    </div>
        """
    return html

@router.get("/autoscaling-group/activity")
async def get_autoscaling_group_activity():
    db = ComputeEnvs()
    ce_list = db.get_current_compute_env()
    ag = debug_aws.get_autoscaling_group(ce_list.name)
    activity = debug_aws.get_scaling_activities(ag)
    return activity

@router.get("/cloudwatch/logs", response_class=HTMLResponse)
async def get_cloud_watch_logs(): 
    asg = debug_aws.get_autoscaling_group(id)
    logs = debug_aws.get_recent_forge_cloudwatch_logs(asg)
    return f"<div> {logs} </div>"

@router.get("/launch-template", response_class=HTMLResponse)
async def get_launch_template():
    launch_template_id = debug_aws.get_aws_batch_compute_env_launch_template_id(id)
    launch_template_object = debug_aws.get_user_data_from_launch_template(launch_template_id)            
    launch_template_userdata = debug_aws.extract_and_decode_user_data(launch_template_object)
    
    return f"<div> {launch_template_userdata} </div>"

def fetch_compute_enviornments():
    settings = Settingsdto()
    setting = settings.get_settings()
    print(setting.workspace_id, setting.platform_url, setting.token)
    seqera = SeqeraComputeEnvsWrapper(workspace_id=setting.workspace_id, 
                                    platform_token=setting.token,
                                    platform_url=setting.platform_url)

    ce_list = seqera.list_compute_envs(status="AVAILABLE")
    ids = [env.id for env in ce_list.compute_envs if env.platform == "aws-batch"]
    new_ce_list = []
    for id in ids:
        new_ce_list.append(f'ShahbazCompute-{id}-head')
        new_ce_list.append(f'ShahbazCompute-{id}-work')

    return new_ce_list

@router.get("/compute_envs/list", response_class=HTMLResponse)
async def get_options():

    options = fetch_compute_enviornments()
    options_html = ""
    for option in options:
        options_html += f"""
        <li><a hx-post="/aws/compute_envs/set?compute_env_id={option}" id="{option}" hx-target="#current-env">{option}</a></li>
        """
    # Return the options as an HTML string.
    return options_html

@router.post("/compute_envs/set", response_class=PlainTextResponse)
async def set_current_ce(compute_env_id: str):
    db = ComputeEnvs()
    ce_list = db.get_current_compute_env()
    
    if ce_list != None:
        updated_ce = db.update_current_ce(ce_list.name, compute_env_id)
        print(updated_ce)
        return updated_ce.name
    else:
        new_ce = db.create_ce(compute_env_id)
        return new_ce.name 

@router.get("/jobs_table", response_class=HTMLResponse)
async def get_jobs_table():
    db = ComputeEnvs()
    ce_list = db.get_current_compute_env()
    suceeded_jobs = debug_aws.get_succeeded_jobs(ce_list.name)
    failed_jobs = debug_aws.get_failed_jobs(ce_list.name)
    runnable_jobs = debug_aws.get_runnable_jobs(ce_list.name)
    jobs_html = ""
    count = 1
    
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
            count+=1
        
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
            count+=1
            
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
            count+=1

    if jobs_html == "":
        jobs_html += f"""
                <tr class="hover">
                <th>0</th>
                <td>No jobs found</td>
                <td>COMPLETED</td>
                <td>Unknown</td>
                </tr>
            """

    return jobs_html 



