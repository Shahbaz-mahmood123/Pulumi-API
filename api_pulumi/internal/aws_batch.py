from core.debug_aws_batch import DebugAWSBatch

class AWSBatch():
    
    def __init__(self, compute_env_id: str, debug_aws_batch: DebugAWSBatch):
        self.compute_env_id = compute_env_id
        self.debug_aws_batch = debug_aws_batch

    