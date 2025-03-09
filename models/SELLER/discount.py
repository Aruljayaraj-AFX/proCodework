from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

discount=declarative_base()

class discount_details(discount):
    __tablename__="discout"
    discount_name=Column(String,nullable=False)
    discount_id=Column(Integer,nullable=False,primary_key=True)
    product_id=Column(Integer,nullable=False)
    discount_type=Column(String,nullable=False)
    discount=Column(Integer,nullable=False)
    discount_period=Column(Integer,nullable=False)
    created_at = Column(DateTime, default=func.now())  
