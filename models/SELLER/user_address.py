from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

user_ABase = declarative_base()

class usersA(user_ABase):
    __tablename__='users_a'

    user_id = Column(String, primary_key=True,nullable=False)
    address=Column(String,nullable=False)
    city=Column(String,nullable=False)
    state=Column(String,nullable=False)
    zip_code=Column(Integer,nullable=False)
    country=Column(String,nullable=False)
    created_at = Column(DateTime, default=func.now())  