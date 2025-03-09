from sqlalchemy import Column, String, Integer, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base

r_order=declarative_base()

class r_orders(r_order):
    __tablename__="r_orders"

    order_id=Column(String,primary_key=True,nullable=False)
    customer_id=Column(String,nullable=False)
    seller_id = Column(String, nullable=False)
    return_reason=Column(String,nullable=False)
    order_quantity=Column(Integer,nullable=False)
    complaint_date=Column(DateTime,default=func.now())
    seller_address=Column(String,nullable=False)
    pickup_address=Column(String,nullable=False)
    refund_amount=Column(Integer,nullable=False)
    refund_status=Column(String,nullable=False)
    return_status=Column(String,nullable=False)
    profit_loss=Column(Integer,nullable=False)
    feedback=Column(String,nullable=False)