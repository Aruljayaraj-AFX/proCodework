from pydantic import BaseModel

class deli_data(BaseModel):
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