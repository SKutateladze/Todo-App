from app.dependencies import Base
from sqlalchemy import Column, Integer, String

class Users(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    role = Column(String)