from sqlalchemy import Column, String, Boolean, Integer
from database import Base


class TodoEntity(Base):
    __tableName__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean)
