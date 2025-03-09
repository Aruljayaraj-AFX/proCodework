from sqlalchemy import Column, String, Integer, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base

order=declarative_base()

class orders(order):
    __tablename__="orders"

    order_id=Column(String,primary_key=True,nullable=False)
    customer_id=Column(String,nullable=False)
    seller_id=Column(String,nullable=False)
    product_id=Column(String,nullable=False)
    order_date=Column(DateTime,nullable=False)
    total_amount=Column(Integer,nullable=False)
    order_quantity=Column(Integer,nullable=False)
    payment_status=Column(String,nullable=False)
    payment_method=Column(String,nullable=False)
    shipping_address=Column(String,nullable=False)
    ship_city=Column(String,nullable=False)
    ship_zip=Column(Integer,nullable=False)
    billing_address=Column(String,nullable=False)
    bill_city=Column(String,nullable=False)
    bill_zip=Column(Integer,nullable=False)
    order_status=Column(String,nullable=False)
    delivery_date=Column(DateTime)
    notes=Column(String)
    fullname=Column(String,nullable=False)
    verify=Column(Boolean,default=False)
    created_at = Column(DateTime, default=func.now())   