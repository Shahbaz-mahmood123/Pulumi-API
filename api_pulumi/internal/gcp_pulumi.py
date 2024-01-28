import os
from typing import Any

from infrastructure.pulumi import PulumiExecution
from infrastructure.gcp_compute_engine import PulumiGCP
from infrastructure.pulumi_config import PulumiGCPConfig

class SelectGCP():
    
    def __init__(self) -> None:
        
        self.config = PulumiGCPConfig(f"/code/api_pulumi/minimal-gcp-compute.yaml")

        if self.config.type == 'minimal':
            self.pulumi_gcp = PulumiGCP(project_id=self.config.project_id, location=self.config.location, name=self.config.name, region=self.config.region,
                                        zone=self.config.zone, instance_name=self.config.instance_name,tower_env_secret=self.config.tower_env_secret, 
                                        tower_yaml_secret=self.config.tower_yaml_secret, harbor_creds=self.config.harbor_creds,
                                        groundswell_secret=self.config.groundswell, source_ranges=self.config.source_ranges, 
                                        tags=self.config.tags, source_tags=self.config.source_tags)
            
    def preview_compute_engine_instance(self):
        
        pulumi_execution = PulumiExecution(self.config.project_id, self.config.stack_name,self.config.work_dir, self.pulumi_gcp.pulumi_program)

        pulumi_execution.preview()
    
    def up_compute_engine_instance(self):
        pass
    
    def destroy_compute_engine_instance(self):
        pass
    
    def destroy_stack_compute_engine_instance(self):
        pass

