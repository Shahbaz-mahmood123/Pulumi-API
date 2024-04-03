import os
from typing import Any

from infrastructure.pulumi import PulumiExecution
from infrastructure.minimal_gcp_compute_engine import MinimalPulumiGCP
from infrastructure.pulumi_config import MinimalPulumiGCPConfig, MinimalPulumiGCPConfigYAML
from infrastructure.models.pulumi import PreviewResult, UpResult, DestroyResult, RefreshResult

class SelectGCP():
    
    def __init__(self) -> None:
        
        # This is the dir in the container where the yaml file lives. Need to figure out if i use DB or yaml files
        self.yaml = MinimalPulumiGCPConfigYAML(file_path=f"./api_pulumi/minimal-gcp-compute.yaml")
        #self.config = MinimalPulumiGCP(config=yaml.config_model)
        
        if self.yaml.config_model.stack.type == 'minimal': 
            self.pulumi_gcp = MinimalPulumiGCP(config=self.yaml.config_model)
        if self.yaml.config_model.stack.type  == 'standard':
            pass 
        if self.yaml.config_model.stack.type  == 'private':
            pass 
        
        ##TODO: use cloud provider bucket
        self.current_dir = os.getcwd()
        
        self.pulumi_execution = PulumiExecution(self.yaml.config_model.project_id, self.yaml.config_model.stack.stack ,self.current_dir, self.pulumi_gcp)
            
    def preview_compute_engine_instance(self) -> PreviewResult:
        
       preview = self.pulumi_execution.preview()
       return preview
    
    def up_compute_engine_instance(self) -> UpResult:
        up_result = self.pulumi_execution.execute()
        return [up_result]
    
    def destroy_compute_engine_instance(self) -> DestroyResult:
        response = self.pulumi_execution.destroy()
        return response
    
    def destroy_stack_compute_engine_instance(self) -> DestroyResult:
        self.pulumi_execution.destroy_stack()
    
    def refresh_stack_compute_engine_instance(self) -> RefreshResult:
        response = self.pulumi_execution.refresh()
        return response


