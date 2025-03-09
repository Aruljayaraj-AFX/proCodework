from database.DB import session
from datetime import datetime
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
from models.del_data import del_info
from models.inventory import inven_cour,inven_del,inven
from schema.deli_info import deli_data
from schema.courier_status import del_update


load_dotenv()
token_expiry_minutes = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
algorithm = os.getenv('ALGORITHM')
secret_key = os.getenv('JWT_SECRET_KEY')
db_url = os.getenv('DB_URL')


def send_otp_email(user,):
    sender_email = "aruljayarajj826@gmail.com"
    subject = "Your OTP Code"
    otp_o = random.randint(100000, 999999)
    '''connection = psycopg2.connect(os.getenv('DB_URL'))
    cursor = connection.cursor()
    cursor.execute("INSERT INTO dummy_otp_verify (email_id, otp) VALUES (%s, %s)", (seller.email_id, otp_o))
    connection.commit()
    cursor.close()
    connection.close()'''
    try:
        check=session.query(dummy.email_id).filter(dummy.email_id== user.email).first()
        print(check)
        if not check:
            new_in = dummy( email_id=user.email,otp=otp_o)
            session.add(new_in)
            session.commit()
            session.close()
        else:
            session.rollback()  
            raise HTTPException(status_code=500, detail=f"Database error")
    except Exception as e:
        session.rollback()  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    body = f"Your OTP is: {otp_o}"
    sender_password = os.getenv('EMAIL_PASSWORD')
    if sender_password is None:
        print("Error: The EMAIL_PASSWORD environment variable is not set.")
        return
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = user.email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email,user.email, msg.as_string())


generated_ids = set(session.query(del_info.staff_id).all())
session.close()

def generate_unique_del_id():
    while True:
        random_number = random.randint(100000, 999999)
        sell_id = f"DEL{random_number}"
        if sell_id not in generated_ids:
            generated_ids.add(sell_id)
            return sell_id

class get_del_info_signup:
    def __call__(self, DEL_INFO: deli_data):
        encoded_password = hashword(DEL_INFO.password)
        user_d=generate_unique_del_id()
        DOB_s = datetime.strptime(DEL_INFO.DOB, "%Y-%m-%d")
        new_user = del_info(staff_id=user_d,staffname=DEL_INFO.username, DOB=DOB_s, phone_number=DEL_INFO.phone_number,email=DEL_INFO.email,password=encoded_password,created_at=datetime.now(),staff_profile=DEL_INFO.user_profile,verify="False",address=DEL_INFO.address,city=DEL_INFO.city,zip_code=DEL_INFO.zip_code)
        try:
            session.add(new_user)
            session.commit()
            session.close()
        except Exception as e:
            session.rollback()  
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        otp=send_otp_email(DEL_INFO)


class checkDotp:
    def __call__(self, email_id: str, otp: int):
        try:
            result = session.query(dummy).filter(dummy.otp == otp).first()
            print("h")
            session.close()
            if result:
                print("h")
                token=hashword(result.email_id)
                return token
            else:
                return "otp or email is invalid"
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


class del_Authorization(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(del_Authorization, self).__init__(auto_error=auto_error)
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(del_Authorization, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code")
        token = decode(credentials.credentials)
        try:
            result=session.query(del_info.email).filter(del_info.email==token['password'])
            session.close()
            try:
                if result:
                    return token
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except:
            raise HTTPException(status_code=403, detail="Invalid authorization code")


class del_login:
    def __call__(self, email_id: str, password:str):
        try:
            result=session.query(del_info).filter(del_info.email==email_id).first()
            session.close()
            pas = hashword(password)
            print(pas)
            print(result.password)
            if pas == result.password:
                    return "successfully login"
            else:
                return "invalid password"
        except Exception as e:
            session.rollback()
            session.commit()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        

class del_email:
    def __call__(self,email:str):
        sender_email = "aruljayarajj826@gmail.com"  
        subject = "Reset_Your_Password"
        body = f"use this link to reset your password http://127.0.0.1:8000/codework/v1/del/r/{email}"
        sender_password = os.getenv('EMAIL_PASSWORD')

        if sender_password is None:
            raise HTTPException(status_code=500, detail="Error: The EMAIL_PASSWORD environment variable is not set.")

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
            server.quit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

        return {"message": "Email successfully sent."}


def resetd_password(email: str, new_password: str, confirm_password: str):
    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    user = session.query(del_info).filter(del_info.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="No matching user found.")

    try:
        print(new_password)
        encoded_password = hashword(new_password)
        print(encoded_password)
        del_info.password = encoded_password  
        session.commit() 
        session.close() 
        return {"message": "Password updated successfully."}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


class staff_update:
    def __call__(self,DEL_INFO:deli_data,token:str=Depends(del_Authorization())):
        try:
            use = token['password']
            print(f"User Email (Password): {use}")
            res = session.query(del_info).filter(del_info.email == use).first()
            if not res:
                return {"error": "Error in fetching the user_id"}
            res.staffname=DEL_INFO.username
            res.phone_number=DEL_INFO.phone_number
            res.DOB=DEL_INFO.DOB
            res.staff_profile=DEL_INFO.user_profile
            res.address=DEL_INFO.address
            res.city=DEL_INFO.city
            res.zip_code=DEL_INFO.zip_code
            session.commit()
            session.close()
            return "successfully_update the profile"
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class order_list:
    def __call__(self, token:str= Depends(del_Authorization())):
        try:
            use = token['password']
            print(f"User Email (Password): {use}")
            res = session.query(del_info).filter(del_info.email == use).first()
            if not res:
                return {"error": "Error in fetching the user_id"}
            if res:
                resultf=[]
                past_order=[]
                staff_id1=res.staff_id
                order_list=session.query(inven_del).filter(inven_del.verify=="True").all()
                if order_list:
                    for pro in order_list:
                        print(pro.staff_id)
                        print(staff_id1)
                        if((pro.staff_id==staff_id1)&(pro.delivery_status!="delivered")):
                            return f"plz let you wish your delivery order{pro.order_id}"
                        elif ((pro.staff_id==staff_id1)&(pro.delivery_status=="delivered")):
                            past_order.append(pro)
                        else:
                            resultf.append(pro)
                    return {
                        "order":resultf,
                        "past_orders":past_order
                    }
                else:
                    return "no order"
            else:
                return "not autheticate staff_id"
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class pick_order:
    def __call__(self, order_id:str,request: Request,token:str=Depends(del_Authorization())):
        try:
            use = token['password']
            print(f"User Email (Password): {use}")
            res = session.query(del_info).filter(del_info.email == use).first()
            if not res:
                return {"error": "Error in fetching the user_id"}
            
            staff_id1=res.staff_id
            order_list=session.query(inven_del).filter(inven_del.verify=="True").all()
            for pro in order_list:
                if((pro.staff_id==staff_id1)&(pro.delivery_status!="delivered")):
                    return f"plz let you wish your delivery order{pro.order_id}"
            p_o=session.query(inven_del).filter(inven_del.order_id==order_id).first()
            p_o.delivery_status="pickup_order"
            p_o.staff_id=staff_id1
            client_ip = request.headers.get('X-Forwarded-For', request.client.host)
            if client_ip.startswith("127.") or client_ip.startswith("192.") or client_ip.startswith("10."):
                client_ip = requests.get('https://api64.ipify.org').text
            response = requests.get(f"http://ip-api.com/json/{client_ip}")
            if response.status_code == 200:
                data = response.json()
                print(data)
                if data['status'] == 'success':
                    p_o.coor1=data['lat']
                    p_o.coor2=data['lon']
                    session.commit()
                else:
                    return {
                            "error": "eruror in fetch the location"
                    }
            else:
                return {
                    "error": "error in feptch the location"
                }
            resd=session.query(orders).filter(orders.order_id==p_o.order_id).first()
            session.close()
            return{
                    "order_details": resd
                }
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f" error: {str(e)}")
        
class update_order:
    def __call__(self, u_d:del_update,request: Request,token:str=Depends(del_Authorization())):
        try:
            use = token['password']
            print(f"User Email (Password): {use}")
            res = session.query(del_info).filter(del_info.email == use).first()
            staff_id1=res.staff_id
            s_2=session.query(inven_del).filter(((inven_del.staff_id==staff_id1)&(inven_del.verify=="True"))&(inven_del.delivery_status=="delivered"))
            if s_2:
                return {
                    "invalid the order"
                }
            if not res:
                return {"error": "Error in fetching the user_id"}
            result=session.query(inven_del).filter(u_d.order_id==inven_del.order_id).first()
            client_ip = request.headers.get('X-Forwarded-For', request.client.host)
            if client_ip.startswith("127.") or client_ip.startswith("192.") or client_ip.startswith("10."):
                client_ip = requests.get('https://api64.ipify.org').text
            response = requests.get(f"http://ip-api.com/json/{client_ip}")
            if (u_d.delivery_status=="delivered"):
                if response.status_code == 200:
                    data = response.json()
                    print(data)
                    if data['status'] == 'success':
                        up=session.query(orders).filter(orders.order_id==u_d.order_id).first()
                        result.delivery_status=u_d.delivery_status
                        up.order_status=u_d.delivery_status
                        result.coor_d1=data['lat']
                        result.coor_d2=data['lon']
                        up.delivery_date=datetime.now()
                        session.commit()
                        return {
                            "successfully the order is delivered"
                        }
                    else:
                        return{
                            "error":"problem occur in fetch the location"
                        }
                else:
                    return{
                            "error":"problem occur in fetch the location"
                        }
            else:
                result.delivery_status=u_d.delivery_status
                return{
                    "successfully update the status the order"
                }

        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f" error: {str(e)}")
        





           
            
