from utils.security import hashword,decode
from fastapi import APIRouter, HTTPException,Depends,Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.SELLER.seller_ser import Authorization
from database.DB import session
from schema.SELLER.category import Catgo
from models.SELLER.catgories import Category
from models.SELLER.seller_info import SellersInfo
import random
from datetime import datetime

generated_ids = set(session.query(Category.category_id).all())
session.close()

def generate_unique_sell_id():
    while True:
        random_number = random.randint(100000, 999999)
        ca_id = f"CAT{random_number}"
        if ca_id not in generated_ids:
            generated_ids.add(ca_id)
            return ca_id

class req_c:
    def __call__(self,catgo:Catgo,token:str=Depends(Authorization())):
        use = token['password']
        print(use)
        res=session.query(SellersInfo).filter(SellersInfo.email == use).first()
        print(res)
        session.close()
        if res:
            sellers_id = res.seller_id
            print(sellers_id)
        else:
            return "error in fetching the seller_id"
        cat_id = generate_unique_sell_id()
        if not cat_id:
            return "error in category_id generate"
        try:
            res=Category(category_id=cat_id,category_name=catgo.category_name,description=catgo.description,verify=False,created_at=datetime.now())
            session.add(res)
            session.commit()
            session.close()
        except Exception as e:
            session.rollback()
            session.close()
            raise HTTPException(status_code=500, detail=f"Error: {str(e)} and problem in categories inserting")
        return "successfully categories requested so wait for admin approval"