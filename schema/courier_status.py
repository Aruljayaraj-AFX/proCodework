from pydantic import BaseModel

class courier_update(BaseModel):
    order_id:str
    courier_id:str
    courier_name:str
    courier_fee:str
    from_inventory_status:str
    to_inventory_status:str

class del_update(BaseModel):
    order_id:str
    delivery_status:str

