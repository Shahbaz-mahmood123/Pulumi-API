import pprint
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session,select

from ..db import models
from ..db.database import Database

class ComputeEnvs():
        
    def __init__(self) -> None:
        self.database = Database()
        
    def get_current_compute_env(self) ->models.ComputeEnv:
        with Session(self.database.engine) as session:
            ce = session.exec(select(models.ComputeEnv)).first()
            return ce
        
    def create_ce(self, name: str):
        new_ce = models.ComputeEnv(name=name)
        try:
            self.database.newRecord(new_ce)
        except Exception as e:
            return {SQLAlchemyError: e}
              
    def update_current_ce(self, compute_env_id: int, new_name: str):
        with Session(self.database.engine) as session:
            statement = select(models.ComputeEnv)
            ce = session.exec(statement).first()

            if ce == None:
                # Handle case when no compute environment is found
                new_ce = self.create_ce(new_name)
                return new_ce

            # Update the compute environment name
            ce.name = new_name
            session.commit()
            session.refresh(ce)
            print("update ce")
            return ce


                

