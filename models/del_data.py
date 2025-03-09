from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

del_Base=declarative_base()

class del_info(del_Base):
    __tablename__='delivery_partner'

    staff_id = Column(String, primary_key=True,nullable=False)
    staffname = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    phone_number=Column(String,nullable=False)
    password=Column(String,nullable=False)
    DOB=Column(DateTime,nullable=False)
    staff_profile=Column(String,nullable=True)
    verify=Column(String,nullable=False)
    address=Column(String,nullable=False)
    city=Column(String,nullable=False)
    zip_code=Column(String,nullable=False)
    created_at = Column(DateTime, default=func.now())