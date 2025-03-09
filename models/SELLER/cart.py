from sqlalchemy import Column, String, Integer, DateTime, func, Boolean
from sqlalchemy.ext.declarative import declarative_base

user_cart = declarative_base()

class user_cart1(user_cart):
    __tablename__ = 'user_cart'

    user_id=Column(String,nullable=False,primary_key=True)
    products=Column(String)
    product_quantity=Column(Integer,nullable=False,default=1)
    created_at = Column(DateTime, default=func.now())