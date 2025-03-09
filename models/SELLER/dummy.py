from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

otp=declarative_base()

class dummy(otp):
    __tablename__="dummy_otp_verify"

    email_id=Column(String,primary_key=True,nullable=False)
    otp=Column(Integer,nullable=False)
    