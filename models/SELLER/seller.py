from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

seller=declarative_base()

class seller_d(seller):
    __tablename__="seller_work"

    seller_id=Column(String,nullable=False)
    order_id=Column(String,primary_key=True,nullable=False)
    return_period=Column(DateTime,nullable=False)
    return_info=Column(String,nullable=False)
    seller_message=Column(String,nullable=False)
    user_status=Column(String,nullable=False)
    created_at = Column(DateTime, default=func.now())  
