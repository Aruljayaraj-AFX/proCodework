from pydantic import BaseModel

class Product(BaseModel):
    categories: str
    subcategories: str
    price: int
    discount: str
    product_details: str  
    product_status: str
    product_name: str
    product_description: str
    stock_quantity: int
    weight: str
    brand: str
    status: str
    product_tags: str
    warranty_period: int
    return_policy: str
    product_image: str


