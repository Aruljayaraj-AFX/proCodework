from sqlalchemy import Column, String, Integer, DateTime, func,LargeBinary,Boolean
from sqlalchemy.ext.declarative import declarative_base

product=declarative_base()

class products(product):
    __tablename__="products"

    product_id = Column(String, primary_key=True, nullable=False)
    category_id = Column(String, nullable=False)  
    subcategory_id = Column(String, nullable=False)
    seller_id = Column(String, nullable=False)  
    price = Column(String, nullable=False) 
    discount = Column(String, nullable=False)
    product_details = Column(String, nullable=False)
    product_status = Column(String, nullable=False)
    verify = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=func.now())
    product_name = Column(String(255), nullable=False)
    product_description = Column(String, nullable=True)
    stock_quantity = Column(Integer, nullable=False)
    weight = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=True)
    product_image = Column(String, nullable=True)
    product_tags = Column(String(255), nullable=True)
    warranty_period = Column(Integer, nullable=True)
    return_policy = Column(String, nullable=True)
    