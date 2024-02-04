import os
from typing import Any

from infrastructure.pulumi import PulumiExecution
from infrastructure.minimal_gcp_compute_engine import MinimalPulumiGCP
from infrastructure.pulumi_config import MinimalPulumiGCPConfig

class SelectGCP():
    
    def __init__(self) -> None:
        
        # This is the dir in the container where the yaml file lives. Need to figure out if i use DB or yaml files
        self.config = MinimalPulumiGCPConfig(f"/code/api_pulumi/minimal-gcp-compute.yaml")
        
        if self.config.type == 'minimal':
            self.pulumi_gcp = MinimalPulumiGCP(project_id=self.config.project_id, location=self.config.location, name=self.config.resource_name, region=self.config.region,
                                        zone=self.config.zone, instance_name=self.config.instance_name,tower_env_secret=self.config.tower_env_secret, 
                                        tower_yaml_secret=self.config.tower_yaml_secret, harbor_creds=self.config.harbor_creds,
                                        groundswell_secret=self.config.groundswell_secret, source_ranges=self.config.source_ranges, 
                                        tags=self.config.tags, source_tags=self.config.source_tags)

    #TODO: DRY DRY DRY 
    def preview_compute_engine_instance(self):
        
        current_work_dir = os.getcwd()
        
        pulumi_execution = PulumiExecution(self.config.project_id, self.config.stack_name,current_work_dir, self.pulumi_gcp)

        pulumi_execution.preview()
    
    def up_compute_engine_instance(self):
        current_work_dir = os.getcwd()
        
        pulumi_execution = PulumiExecution(self.config.project_id, self.config.stack_name,current_work_dir, self.pulumi_gcp)

        pulumi_execution.execute()
    
    def destroy_compute_engine_instance(self):
        
        current_work_dir = os.getcwd()
        
        pulumi_execution = PulumiExecution(self.config.project_id, self.config.stack_name,current_work_dir, self.pulumi_gcp)

        pulumi_execution.destroy()
    
    def destroy_stack_compute_engine_instance(self):
        pass
    
    def refresh_stack_compute_engine_instance(self):
        pass


