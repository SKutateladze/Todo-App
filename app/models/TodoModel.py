from app.dependencies import Base
from sqlalchemy import Integer, String, Column, Boolean, ForeignKey

class Todos(Base):
    __tablename__ = "todos"

    todo_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean)
    owner_id = Column(Integer, ForeignKey("users.user_id"))