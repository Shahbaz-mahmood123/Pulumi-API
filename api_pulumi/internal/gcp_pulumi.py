import os

from infrastructure.pulumi import PulumiExecution
from infrastructure.gcp_compute_engine import PulumiGCP
from infrastructure.pulumi_config import PulumiGCPConfig


class SelectGCP():
    
    def __init__(self) -> None:
        pass

    def preview_compute_engine_instance(self):
        
        
        config = PulumiGCPConfig(f"/code/api_pulumi/minimal-gcp-compute.yaml")

        project_id = config.project_id
        stack_name = config.stack_name
        location = config.location
        name = config.resource_name
        zone = config.zone 
        region = config.region
        instance_name = config.instance_name
        tower_env_secret = config.tower_env_secret
        tower_yaml_secret = config.tower_yaml_secret
        harbor_creds = config.harbor_creds
        current_working_directory = os.getcwd()
        work_dir = current_working_directory
        groundswell = config.groundswell_secret
        source_ranges=config.source_ranges
        tags = config.tags
        source_tags = config.source_tags

        pulumi_gcp = PulumiGCP(project_id=project_id, location=location, name=name, region=region, zone=zone, instance_name=instance_name,
                            tower_env_secret=tower_env_secret, tower_yaml_secret=tower_yaml_secret, harbor_creds=harbor_creds,
                            groundswell_secret=groundswell, source_ranges=source_ranges, tags=tags, source_tags=source_tags)

        pulumi_execution = PulumiExecution(project_id, stack_name,work_dir, pulumi_gcp)

        pulumi_execution.preview()
    

