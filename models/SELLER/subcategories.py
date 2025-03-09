from sqlalchemy import Column, Integer, String, DateTime, func,Text
from sqlalchemy.ext.declarative import declarative_base


Base_sub_c = declarative_base()

class SubCategory(Base_sub_c):
    __tablename__ = 'subcategories_info'

    subcategory_id = Column(String, nullable=False, primary_key=True)  
    subcategory_name = Column(String, nullable=False) 
    category_id = Column(String, nullable=False)  
    description = Column(String) 
    created_at = Column(DateTime, default=func.now())

   