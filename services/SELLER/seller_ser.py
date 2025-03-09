from schema.SELLER.seller_str import seller_str,seller_str1
from database.DB import session
from datetime import datetime
from models.SELLER.seller_info import SellersInfo
from models.SELLER.dummy import dummy
import psycopg2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from models.SELLER.dummy import dummy
from datetime import datetime
import random
import hashlib
import string
from dotenv import load_dotenv
from utils.security import hashword,decode
from fastapi import HTTPException, status, Request,Depends
from sqlalchemy import Column, String, Integer, DateTime, func, Boolean
from jose import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

load_dotenv()
token_expiry_minutes = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
algorithm = os.getenv('ALGORITHM')
secret_key = os.getenv('JWT_SECRET_KEY')
db_url = os.getenv('DB_URL')

generated_ids = set(session.query(SellersInfo.seller_id).all())
session.close()


def generate_unique_sell_id():
    while True:
        random_number = random.randint(100000, 999999)
        sell_id = f"SELL{random_number}"
        if sell_id not in generated_ids:
            generated_ids.add(sell_id)
            return sell_id


load_dotenv()
def send_otp_email(seller,):
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
        check=session.query(dummy.email_id).filter(dummy.email_id== seller.email_id).first()
        print(check)
        if not check:
            new_in = dummy( email_id=seller.email_id,otp=otp_o)
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
    msg['To'] = seller.email_id
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, seller.email_id, msg.as_string())


class get_seller_info_signup:
    def __call__(self, SELLER_INFO: seller_str):
        encoded_password = hashword(SELLER_INFO.password)
        sell_d=generate_unique_sell_id()
        DOB_s = datetime.strptime(SELLER_INFO.DOB, "%Y-%m-%d")
        new_user = SellersInfo(seller_id=sell_d,username=SELLER_INFO.seller_name, DOB_s=DOB_s, phone_number=SELLER_INFO.phone_number,email=SELLER_INFO.email_id,password=encoded_password,verify=False,created_at=datetime.now(),address=SELLER_INFO.address,city=SELLER_INFO.city,zip_code=SELLER_INFO.zip_code)
        try:
            session.add(new_user)
            session.commit()
            session.close()
        except Exception as e:
            session.rollback()  
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        otp=send_otp_email(SELLER_INFO)

class checkotp:
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
        
class Authorization(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(Authorization, self).__init__(auto_error=auto_error)
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(Authorization, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code")
        token = decode(credentials.credentials)
        try:
            result=session.query(SellersInfo.email).filter(SellersInfo.email==token['password'])
            session.close()
            try:
                if result:
                    return token
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except:
            raise HTTPException(status_code=403, detail="Invalid authorization code")

class seller_login:
    def __call__(self, email_id: str, password:str):
        try:
            result=session.query(SellersInfo.verify,SellersInfo.password).filter(SellersInfo.email==email_id)
            session.close()
            if result:
                return "Waiting approval by admin"
            else:
                pas = hashword(password)
                if pas == result[1]:
                    return "successfully login"
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


class for_email:
    def __call__(self,email:str):
        sender_email = "aruljayarajj826@gmail.com"  
        subject = "Reset_Your_Password"
        body = f"use this link to reset your password http://127.0.0.1:8000/codework/v1/r/{email}"
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

def reset_password(email: str, new_password: str, confirm_password: str):
    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    user = session.query(SellersInfo).filter(SellersInfo.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="No matching user found.")

    try:
        encoded_password = hashword(new_password)
        SellersInfo.password = encoded_password  
        session.commit() 
        session.close() 
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return {"message": "Password updated successfully."}
    

class update_profile:
    def __call__(self, up:seller_str1,token:str=Depends(Authorization())):
        DOB_s = datetime.strptime(up.DOB, "%Y-%m-%d")
        use = token['password']
        try:
            res=session.query(SellersInfo).filter(SellersInfo.email == use).first()
            if res:  
                res.username = up.seller_name
                res.email = up.email_id
                res.phone_number = up.phone_number
                res.DOB_s= DOB_s
                res.address = up.address
                res.city=up.city
                res.zip_code=up.zip_code
                session.commit() 
                return "successfully_update the profile"
            
        except Exception as e:
            session.rollback()  
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")        