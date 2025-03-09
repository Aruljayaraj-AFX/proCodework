from sqlalchemy import Column, String, Integer, DateTime, Date, Boolean, func
from sqlalchemy.ext.declarative import declarative_base

Seller_info = declarative_base()

class SellersInfo(Seller_info):
    __tablename__ = "sellers_info"

    seller_id = Column(String, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String,unique=True, nullable=False)
    phone_number = Column(String, nullable=False)  
    password = Column(String, nullable=False)
    DOB_s = Column(DateTime) 
    order_id = Column(Integer)
    verify = Column(Boolean, default=False)  
    city = Column(String,  default="chennai")
    zip_code = Column(Integer,  default=600040)
    created_at = Column(DateTime, default=func.now())
    address=Column(String)
 