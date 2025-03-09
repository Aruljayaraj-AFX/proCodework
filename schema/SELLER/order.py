from pydantic import BaseModel

class Ord(BaseModel):
    product_id:str
    order_quantity:str
    payment_method:str
    billing_address:str
    bill_city:str
    bill_zip:str
    notes:str
    full_name:str
