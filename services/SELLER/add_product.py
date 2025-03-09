from utils.security import hashword,decode
import random
from database.DB import session
from models.SELLER.product_data import products
from models.SELLER.catgories import Category
from fastapi import APIRouter, HTTPException,Depends,Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.SELLER.seller_ser import Authorization
from models.SELLER.seller_info import SellersInfo
from models.SELLER.subcategories import SubCategory
from datetime import datetime
from schema.SELLER.product import Product



def fetch_category():
    res=session.query(Category).all()
    session.close()
    print(res)
    return res

generated_ids = set(session.query(products.product_id).all())

def generate_unique_pro_id():
    while True:
        random_number = random.randint(100000, 999999)
        pro_id = f"PRO{random_number}"
        if pro_id not in generated_ids:
            generated_ids.add(pro_id)
            return pro_id


class add_product:
    def __call__(self, product_item: Product, token: str = Depends(Authorization())):
        try:
            use=token['password']
            print(use)
            print(type(use))
            res=session.query(SellersInfo).filter(SellersInfo.email == use).first()
            session.close()
            print(res)

            if res:
                sellers_id = res.seller_id
                print(sellers_id)
            
            else:
                print("hello") 

            if not sellers_id:
                print("Email not found.")
                raise HTTPException(status_code=404, detail="Seller not found.")

            print("Email found:", sellers_id)

    
            product_id = generate_unique_pro_id()

            print(product_id)

            cat = session.query(Category).filter(Category.category_name == product_item.categories).first()
            print(cat)
            if cat:
                cat_id = cat.category_id
                print(cat_id)

            cat1 = session.query(SubCategory).filter(SubCategory.subcategory_name == product_item.subcategories).first()
            if cat1:
                cat1_id = cat1.subcategory_id
                print(cat1_id)
            

            ress = products(
                product_id=product_id,
                category_id=cat_id,
                subcategory_id=cat1_id,
                seller_id=sellers_id,
                price=product_item.price,
                discount=product_item.discount,
                product_details=product_item.product_details,
                product_status=product_item.product_status,
                verify=False,
                created_at=datetime.now(),
                product_name=product_item.product_name,
                product_description=product_item.product_description,
                stock_quantity=product_item.stock_quantity,
                weight=product_item.weight,
                brand=product_item.brand,
                product_image=product_item.product_image,
                product_tags=product_item.product_tags,
                return_policy=product_item.return_policy,
                warranty_period=product_item.warranty_period
            )

            session.add(ress)
            session.commit()
            session.close()
            return {"message": "Product added successfully!"}

        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

class show_product:
    def __call__(self, token: str = Depends(Authorization())):
        try:
            use=token['password']
            print(use)
            print(type(use))
            res=session.query(SellersInfo).filter(SellersInfo.email == use).all()
            if not res:
                return {"message": "No data found in new_order"}
            for order in res:
                return order
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")