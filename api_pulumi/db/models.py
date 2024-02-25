from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Stack(Base):
    __tablename__ = "stack"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)

