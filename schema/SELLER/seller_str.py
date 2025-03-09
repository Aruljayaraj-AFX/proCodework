from pydantic import BaseModel

class seller_str(BaseModel):
    seller_name:str
    email_id:str
    phone_number:int
    password:str
    DOB:str
    address:str
    city:str
    zip_code:int

class seller_str1(BaseModel):
    seller_name:str
    email_id:str
    phone_number:int
    DOB:str
    address:str
    city:str
    zip_code:str

