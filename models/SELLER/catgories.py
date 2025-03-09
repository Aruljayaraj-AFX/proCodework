from sqlalchemy import Column, String, Integer, DateTime, func, Boolean
from sqlalchemy.ext.declarative import declarative_base

catgories1 = declarative_base()

class Category(catgories1):
    __tablename__ = 'categories_info'

    category_id = Column(String, nullable=False, primary_key=True)  
    category_name = Column(String, nullable=False)  
    description = Column(String)
    created_at = Column(DateTime, default=func.now())
    verify = Column(Boolean, nullable=False, default=False)  