from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

user_Base = declarative_base()

class users(user_Base):
    __tablename__='users'

    user_id = Column(String, primary_key=True,nullable=False)
    username = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    phone_number=Column(String,nullable=False)
    password=Column(String,nullable=False)
    DOB=Column(DateTime,nullable=False)
    user_profile=Column(String,nullable=True)
    created_at = Column(DateTime, default=func.now())  