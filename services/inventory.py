from database.DB import session
from datetime import datetime
from fastapi import Depends
import psycopg2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import random
import hashlib
import string
from dotenv import load_dotenv
from utils.security import hashword,decode
from fastapi import HTTPException, status, Request,Depends,Query
from sqlalchemy import Column, String, Integer, DateTime, func, Boolean
from jose import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schema.user_info import user_info
from models.SELLER.user_data import users
from models.SELLER.user_address import usersA
from models.SELLER.dummy import dummy
from models.SELLER.product_data import products
from models.SELLER.wishlist import Wishlist
from models.SELLER.catgories import Category
from models.SELLER.subcategories import SubCategory
from models.SELLER.subcategories import SubCategory
from models.SELLER.cart import user_cart1 
from models.SELLER.order import orders
from models.SELLER.return_order import r_orders
from models.payment import Payment
from datetime import datetime,timedelta
from schema.user_info import user_update
import requests
import uuid
from schema.SELLER.order import Ord
from models.SELLER.seller_info import SellersInfo
from models.inventory import inven,inven_cour,inven_del
from schema.courier_status import courier_update,del_update


class login:
    def __call__(self, inventory_id:str,inventory_password:str):
        pass1=hashword(inventory_password)
        res=session.query(inven).filter(inven.inventory_id==inventory_id).first()
        if(res.inventory_pass==pass1):
            pass2=hashword(inventory_id)
            return f"successfully login{pass2}"
        else:
            return "invalid login"


class inven_Authorization(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(inven_Authorization, self).__init__(auto_error=auto_error)
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(inven_Authorization, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code")
        token = decode(credentials.credentials)
        c_tok=hashword(token["password"])
        try:
            result=session.query(inven).filter(inven.inventory_id==token['password']).first()
            print(result.inventory_id)
            session.close()
            print(token)
            print(c_tok)
            print(result)
            try:
                if result:
                    print(token)
                    return token
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except:
            raise HTTPException(status_code=403, detail="Invalid authorization code")
        

class inven_courier:
    def __call__(self, token: dict = Depends(inven_Authorization())):
        print(token['password'])
        city = token['password']
        invec = session.query(inven.inventory_city).filter(inven.inventory_id == city).first()
        if not invec:
            return {"error": "City not found"}
        inventory_city = invec.inventory_city
        result_c = session.query(inven_cour).filter((inven_cour.from_inventory_city == inventory_city) &(inven_cour.to_inventory_city == inventory_city)).all()
        result1 = [result_c] if result_c else []
        res = session.query(inven_del).filter(inven_del.inventory_city == inventory_city).all()
        result2 = res if res else []
        return [result1, result2]
    

class courier_update:
    def __call__(self, c_up:courier_update, token: dict = Depends(inven_Authorization())):
        result=session.query(inven_cour).filter(inven_cour.order_id==c_up.order_id).first()
        result.courier_id=c_up.courier_id
        result.courier_name=c_up.courier_name
        result.courier_fee=c_up.courier_fee
        result.from_inventory_status=c_up.from_inventory_status
        result.to_inventory_status=c_up.to_inventory_status
        session.commit()
        session.close()
        return "successfully update the courier status"

