from pydantic import BaseModel

class user_info(BaseModel):
    username :str
    email :str
    phone_number:int
    password:str
    DOB:str
    user_profile:str
    address:str
    city:str
    state:str
    zip_code:int
    country:str

class user_update(BaseModel):
    username:str
    phone_number:str
    DOB:str
    user_profile:str
    user_address:str
    city:str
    state:str
    zip_code:int
    country:str

