from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func,Column
from sqlalchemy.ext.declarative import declarative_base

wBase = declarative_base()

class Wishlist(wBase):
    __tablename__ = 'wishlist'
    
    Wishlist_id = Column(String, primary_key=True, nullable=False)
    products = Column(String)
    created_at = Column(DateTime, default=func.now())
