from pydantic import BaseModel

class Catgo(BaseModel):
    category_name :str
    description:str
