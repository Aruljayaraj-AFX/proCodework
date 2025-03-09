from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func,Column
from sqlalchemy.ext.declarative import declarative_base

payment = declarative_base()

class Payment(payment):
    __tablename__ = 'payment'
    
    order_id=Column(String,nullable=False,primary_key=True)
    customer_id=Column(String,nullable=False)
    name=Column(String,nullable=False)
    phone_number=Column(String,nullable=False)
    email=Column(String,nullable=False)
    total_amount=Column(String,nullable=False)
    created_at = Column(DateTime, default=func.now())
