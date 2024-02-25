from sqlalchemy.orm import Session

from . import models, schema


def get_stack(db: Session, stack_name: str):
    return db.query(models.Stack).filter(models.Stack.name == stack_name).first()

def create_stack(db: Session, stack: schema.Stack):
    db_stack = models.Stack(name = stack.name)
    db.add(db_stack)
    db.commit()
    db.refresh(db_stack)
    return db_stack