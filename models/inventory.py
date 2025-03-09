from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func,Column,Boolean
from sqlalchemy.ext.declarative import declarative_base

winven = declarative_base()

class inven(winven):
    __tablename__ = 'inventory'
    inventory_id=Column(String,primary_key=True,nullable=False)
    inventory_address=Column(String)
    inventory_pass=Column(String,nullable=True)
    inventory_city=Column(String,nullable=False)

class inven_cour(winven):
    __tablename__ = 'inventory_cour'
    from_inventory_city=Column(String,primary_key=True,nullable=False)
    order_id=Column(String,unique=True,nullable=False)
    courier_id=Column(String,nullable=False)
    courier_name=Column(String,nullable=False)
    courier_fee=Column(String,nullable=False)
    to_inventory_city=Column(String,nullable=False)
    from_inventory_status=Column(String)
    to_inventory_status=Column(String)

class inven_del(winven):
    __tablename__ = 'inventory_del'
    inventory_city=Column(String,primary_key=True,nullable=False)
    order_id=Column(String,unique=True,nullable=False)
    staff_id=Column(String)
    delivery_mode=Column(String)
    delivery_status=Column(String,nullable=False)
    delivery_address=Column(String)
    delivery_city=Column(String)
    shipping_address=Column(String)
    shipping_city=Column(String)
    verify=Column(Boolean)
    coor1=Column(String)
    coor2=Column(String)
    coor_d1=Column(String)
    coor_d2=Column(String)