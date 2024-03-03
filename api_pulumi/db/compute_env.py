# from sqlalchemy.orm import Session

# from . import models

# def get_stack(db: Session, stack_name: str):
#     return db.query(models.Stack).filter(models.Stack.name == stack_name).first()

# def create_stack(db: Session, stack: schema.Stack):
#     db_stack = models.Stack(name = stack.name)
#     db.add(db_stack)
#     db.commit()
#     db.refresh(db_stack)
#     return db_stack

# def create_compute_env(db: Session, compute_env: schema.ComputeEnv):
#     db_compute_env = models.ComputeEnv(name = compute_env.name)
    
#     db.add(db_compute_env)
#     db.commit()
#     db.refresh(db_compute_env)
    
#     return db_compute_env

# def get_compute_env( db: Session, compute_env_name: str):
#     return db.query(models.ComputeEnv).filter(models.ComputeEnv.name == compute_env_name).first()