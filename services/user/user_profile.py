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
from models.inventory import inven_cour,inven_del,inven


load_dotenv()
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


generated_ids = set(session.query(users.user_id).all())
session.close()


def generate_unique_user_id():
    while True:
        random_number = random.randint(100000, 999999)
        u_id = f"USER{random_number}"
        if u_id not in generated_ids:
            generated_ids.add(u_id)
            return u_id

class get_user_info_signup:
    def __call__(self, USER_INFO: user_info):
        encoded_password = hashword(USER_INFO.password)
        user_d=generate_unique_user_id()
        DOB_s = datetime.strptime(USER_INFO.DOB, "%Y-%m-%d")
        new_user = users(user_id=user_d,username=USER_INFO.username, DOB=DOB_s, phone_number=USER_INFO.phone_number,email=USER_INFO.email,password=encoded_password,created_at=datetime.now(),user_profile=USER_INFO.user_profile)
        new_info=usersA(user_id=user_d,address=USER_INFO.address,city=USER_INFO.city,state=USER_INFO.state,country=USER_INFO.country,zip_code=USER_INFO.zip_code)
        try:
            session.add(new_info)
            session.add(new_user)
            session.commit()
            session.close()
        except Exception as e:
            session.rollback()  
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        otp=send_otp_email(USER_INFO)

class checkUotp:
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

class user_Authorization(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(user_Authorization, self).__init__(auto_error=auto_error)
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(user_Authorization, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code")
        token = decode(credentials.credentials)
        try:
            result=session.query(users.email).filter(users.email==token['password'])
            session.close()
            try:
                if result:
                    return token
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        except:
            raise HTTPException(status_code=403, detail="Invalid authorization code")

class user_login:
    def __call__(self, email_id: str, password:str):
        try:
            result=session.query(users).filter(users.email==email_id).first()
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
        

class user_email:
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

def resetu_password(email: str, new_password: str, confirm_password: str):
    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    user = session.query(users).filter(users.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="No matching user found.")

    try:
        print(new_password)
        encoded_password = hashword(new_password)
        print(encoded_password)
        user.password = encoded_password  
        session.commit() 
        session.close() 
        return {"message": "Password updated successfully."}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class userpageproduct:
     def __call__(self, product_list_no: int,product_in_page:int, token: str = Depends(user_Authorization())):
        use = token['password'] 
        print(f"User Email (Password): {use}")
        res = session.query(users.user_id).filter(users.email == use).first()
        print(res)
        if res:
            sellers_id = res.user_id  
            print(f"user ID: {sellers_id}")
        else:
            return {"error": "Error in fetching the user_id"}
        total_products = session.query(products).count()
        items_per_page = product_in_page
        offset = (product_list_no - 1) * items_per_page
        paginated_products = session.query(products).limit(items_per_page).offset(offset).all()
        if not paginated_products:
            return {"message": "No data found in current_product"}
        session.close()
        return {
            "page": product_list_no,
            "total_products": total_products,
            "products_list": [product for product in paginated_products]
        }


def product(product_id: str):
    product_details = session.query(products).filter(products.product_id == product_id).first()
    return product_details

class Wlist:
    def __call__(self, token: str = Depends(user_Authorization())):
        use = token['password']
        print(f"User Email (Password): {use}")

        res = session.query(users.user_id).filter(users.email == use).first()
        if not res:
            return {"error": "Error in fetching the user_id"}

        sellers_id = res[0] 
        print(f"user ID: {sellers_id}")

        try:
            wish_list = session.query(Wishlist.products).filter(Wishlist.Wishlist_id == sellers_id).first()
            if not wish_list or not wish_list.products:
                return {"message": "No data found"}

            
            result = wish_list.products.split(",")

            if not result:
                return {"message": "No data found"}

            return {"wishlist_products": result}

        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        finally:
            session.close()


class Cat:
    def __call__(self, token: str = Depends(user_Authorization())):
        use = token['password']
        print(f"User Email (Password): {use}")

        res = session.query(users.user_id).filter(users.email == use).first()
        if not res:
            return {"error": "Error in fetching the user_id"}

        sellers_id = res[0]  
        print(f"user ID: {sellers_id}")

        try:
            
            category_list = session.query(Category.category_id).all()
            print(f"Category List: {category_list}")

            category_subcategories = {}  

            for category in category_list:
                category_id = category[0]  
                print(f"Processing Category ID: {category_id}")

               
                subcategories = session.query(SubCategory).filter(SubCategory.category_id == category_id).all()
                

                category_subcategories[category_id] = [sub.subcategory_name for sub in subcategories]

            return category_subcategories

        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        finally:
            session.close()

class SearchService:
    def __call__(self,keyword: str = Query(..., min_length=2, description="Search keyword"),token: str = Depends(user_Authorization())):
        use = token['password']
        print(f"User Email (Password): {use}")

        res = session.query(users.user_id).filter(users.email == use).first()
        if not res:
            return {"error": "Error in fetching the user_id"}

        sellers_id = res[0]  
        print(f"user ID: {sellers_id}")
        try:
            categories = session.query(Category).filter(Category.category_name.ilike(f"%{keyword}%")).all()

            subcategories = session.query(SubCategory).filter(SubCategory.subcategory_name.ilike(f"%{keyword}%")).all()

            product1 = session.query(products).filter(products.product_name.ilike(f"%{keyword}%")).all()
            print(product1)
            print(categories)
            print(subcategories)

            response = {
                "categories": [{"id": cat.category_id, "name": cat.category_name} for cat in categories],
                "subcategories": [{"id": sub.subcategory_id, "name": sub.subcategory_name, "category_id": sub.category_id} for sub in subcategories],
                "products": [{"id": prod.product_id, "name": prod.product_name, "subcategory_id": prod.subcategory_id} for prod in product1]
            }
            print(response)
            if not product1:
                print("no product found from search keywords")
            else:
                print("h")
                result=session.query(Wishlist).filter(Wishlist.Wishlist_id==sellers_id).first()
                print("h")
                if result:
                     if result.products:  
                        wishlist_products = result.products.split(",")
                     else:
                        wishlist_products = []  
                        wishlist_products.extend([str(prod.product_id) for prod in product1]) 
                        result.products = ",".join(set(wishlist_products))
                        session.commit()
                        print("Updated Wishlist:", result.products)
                else:
                    print("h")
                    wishlist_products = [str(prod.product_id) for prod in product1]
                    print(wishlist_products)
                    new_entry = Wishlist(Wishlist_id=sellers_id, products=",".join(wishlist_products))
                    print(new_entry)
                    session.add(new_entry)
                    session.commit()
                    session.close()


            if not categories and not subcategories and not product1:
                return {"message": "No matching results found."}

            return response

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


class addtocart:
    def __call__ (self,product_id:str, token: str = Depends(user_Authorization())):
        use = token['password']
        print(f"User Email (Password): {use}")

        res = session.query(users.user_id).filter(users.email == use).first()
        if not res:
            return {"error": "Error in fetching the user_id"}

        sellers_id = res[0]  
        print(f"user ID: {sellers_id}")
        try:
            cart_check=session.query(user_cart1).filter(user_cart1.user_id==sellers_id).first()
            if cart_check:
                cart_products = cart_check.products.split(",") if cart_check.products else []
                cart_products.extend([product_id]) 
                cart_check.products = ",".join(set(cart_products))
                session.commit()
                session.close()
                return{
                    "product add in the cart"
                }
            else:
                cart_products = [product_id]
                new_entry = user_cart1(user_id=sellers_id, products=",".join(cart_products))
                print(new_entry)
                session.add(new_entry)
                session.commit()
                session.close()
                return{
                    "add one more product added in cart"
                }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class my_order:
    def __call__(self,token: str = Depends(user_Authorization())):
        use = token['password']
        print(f"User Email (Password): {use}")

        res = session.query(users.user_id).filter(users.email == use).first()
        if not res:
            return {"error": "Error in fetching the user_id"}

        sellers_id = res[0]  
        print(f"user ID: {sellers_id}")
        try:
            result=session.query(orders).filter(orders.customer_id==sellers_id).all()
            if not result:
                return {"message": "No orders"}
            return {
            "order_list": [product for product in result]
             }
            session.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class my_return:
    def __call__ (self,order_id:str,order_complain:str,pickup_address:str,feed_back:str,token: str = Depends(user_Authorization())):
        use = token['password']
        print(f"User Email (Password): {use}")

        res = session.query(users.user_id).filter(users.email == use).first()
        if not res:
            return {"error": "Error in fetching the user_id"}

        sellers_id = res[0]  
        print(f"user ID: {sellers_id}")
        det=session.query(orders).filter(orders.order_id==order_id).first()
        try:
            res=r_orders(order_id=order_id,customer_id=sellers_id,seller_id=det.seller_id,return_reason=order_complain,complaint_date=datetime.now(),seller_address=det.shipping_address,pickup_address=pickup_address,refund_amount=det.total_amount,refund_status="wait for approval",return_status="analysiing",profit_loss=det.total_amount,feedback=feed_back,order_quantity=det.order_quantity)
            session.add(res)
            session.commit()
            session.close()
            return{
                "successfully requested for return"
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class returnable_order:
    def __call__(self,token: str = Depends(user_Authorization())):
        use = token['password']
        print(f"User Email (Password): {use}")

        res = session.query(users.user_id).filter(users.email == use).first()
        if not res:
            return {"error": "Error in fetching the user_id"}

        sellers_id = res[0]  
        print(f"user ID: {sellers_id}")
        try:
            res=session.query(orders).filter(orders.customer_id==sellers_id)
            today = datetime.now()
            result = [str(o.order_id) for o in res if o.delivery_date and (o.delivery_date + timedelta(days=5) <= today)]
            return  result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

class profile_update:
    def __call__(self,update:user_update,token: str = Depends(user_Authorization())):
        use = token['password']
        print(f"User Email (Password): {use}")

        res = session.query(users.user_id).filter(users.email == use).first()
        if not res:
            return {"error": "Error in fetching the user_id"}

        sellers_id = res[0]  
        print(f"user ID: {sellers_id}")
        try:
            upres=session.query(users).filter(users.user_id==sellers_id).first()
            upres1=session.query(usersA).filter(usersA.user_id==sellers_id).first()
            upres.username=update.username
            upres.phone_number=update.phone_number
            upres.DOB=update.DOB
            upres.user_profile=update.user_profile
            upres1.user_address=update.user_address
            upres1.city=update.city
            upres1.state=update.state
            upres1.zip_code=update.zip_code
            upres1.country=update.country
            session.commit()
            session.close()
            return "successfully updated"
        except Exception as e:
            session.rollback()  # In case of error, rollback the transaction
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")



CASHFREE_MERCHANT_ID = os.getenv('CASHFREE_MERCHANT_ID')
CASHFREE_SECRET_KEY = os.getenv('CASHFREE_SECRET_KEY')
CASHFREE_PAYMENT_GATEWAY_URL = os.getenv('CASHFREE_PAYMENT_GATEWAY_URL')


class payment:
    def __call__ (self,order_id:str,order_quantity:str,token: str = Depends(user_Authorization())):
        use = token['password']
        print(f"User Email (Password): {use}")

        res = session.query(users).filter(users.email == use).first()
        if not res:
            return {"error": "Error in fetching the user_id"}

        try:
            mobile=f"+91{res.phone_number}"
            print(mobile)
            ord=session.query(orders).filter(orders.order_id==order_id).first()
            headers = {
            'Content-Type': 'application/json',
            'x-api-version': '2023-08-01',
            'x-client-id': CASHFREE_MERCHANT_ID,
            'x-client-secret': CASHFREE_SECRET_KEY
            }
            order_data = {
                "order_amount": ord.total_amount,
                "order_currency": "INR",
                "order_id": ord.order_id,
                "order_note": "Test Transaction",
                "customer_details": {
                    "customer_id": ord.customer_id,
                    "customer_email": res.email,
                    "customer_phone": mobile,
                }
            }
            print(order_data)
            response = requests.post(CASHFREE_PAYMENT_GATEWAY_URL, json=order_data, headers=headers)
            response_data = response.json()

            if response_data.get('order_status') == 'ACTIVE':
                return {'order_id': order_id,'response': response_data}
            else:
                raise HTTPException(status_code=400, detail="Failed to create order")

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


class payment_verify:
    def __call__ (self,order_id:str,token: str = Depends(user_Authorization())):
        try:
            use = token['password']
            print(f"User Email (Password): {use}")
            res = session.query(users).filter(users.email == use).first()
            if not res:
                return {"error": "Error in fetching the user_id"}
            headers = {
            'Content-Type': 'application/json',
            'x-api-version': '2023-08-01',
            'x-client-id': CASHFREE_MERCHANT_ID,
            'x-client-secret': CASHFREE_SECRET_KEY
            }
            verify_url = f"{CASHFREE_PAYMENT_GATEWAY_URL}/{order_id}"
            response = requests.get(verify_url, params={"order_id": order_id}, headers=headers)
            response_data = response.json()
            ord=session.query(orders).filter(orders.order_id==order_id).first()
            if response_data.get('order_status') == 'PAID' or response_data.get('order_status') == 'ACTIVE':
                new_recepit = Payment(
                order_id=order_id,
                customer_id=ord.customer_id,
                name=res.username,
                phone_number=res.phone_number,
                email=res.email,
                total_amount=ord.total_amount,
                created_at=datetime.now()
                )
                session.add(new_recepit)
                session.commit()
                ord.payment_method="completed"
                session.close()

                return {"order_id": order_id, "status": "success", 'response': response_data}
            elif response_data.get('order_status') == 'FAILED':
                return {"order_id": order_id, "status": "failed"}
            else:
                raise HTTPException(status_code=400, detail="Payment verification failed: Order not found or not yet processed")

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error occurred: {str(e)}")

generated_ids_ord = set(session.query(orders.order_id).all())
session.close()

class c_order:
    def __call__ (self,pOrd:Ord,token: str = Depends(user_Authorization())):
        use = token['password']
        print(f"User Email (Password): {use}")

        res = session.query(users).filter(users.email == use).first()
        if not res:
            return {"error": "Error in fetching the user_id"}
        random_number = random.randint(100000, 999999)
        ord_id = f"ORD{random_number}"
        if ord_id not in generated_ids_ord:
            generated_ids.add(ord_id)
        else:
            return "order_gernerate_problem7"
        try:
            pro_details=session.query(products).filter(products.product_id==pOrd.product_id).first()
            seller_id=pro_details.seller_id
            seller_details=session.query(SellersInfo).filter(SellersInfo.seller_id==seller_id).first()
            new_order=orders(
            order_id=ord_id,
            customer_id=res.user_id,
            seller_id=seller_id,
            product_id=pOrd.product_id,
            order_date=datetime.now(),
            total_amount=pro_details.price,
            order_quantity=pOrd.order_quantity,
            payment_status="pending",
            payment_method=pOrd.payment_method,
            shipping_address=seller_details.address,
            ship_city=seller_details.city,
            ship_zip=seller_details.zip_code,
            billing_address=pOrd.billing_address,
            bill_city=pOrd.bill_city,
            bill_zip=pOrd.bill_zip,
            order_status="init",
            notes=pOrd.notes,
            fullname=pOrd.full_name,
            )
            session.add(new_order)
            session.commit()
            if (seller_details.city==pOrd.bill_city):
                inv_d=session.query(inven).filter(inven.inventory_city==seller_details.city).first()
                new_cour=inven_del(inventory_city=seller_details.city,delivery_address=pOrd.billing_address,delivery_city=pOrd.bill_city,shipping_address=seller_details.address,shipping_city=seller_details.city,order_id=ord_id,delivery_status="pending",coor1="false",coor2="false",delivery_mode="seller_to_buyer",verify="True")
                session.add(new_cour)
                session.commit()
            else:
                new_del=inven_cour(from_inventory_city=seller_details.city,order_id=ord_id,courier_id="false",courier_name="false",courier_fee="false",to_inventory_city=pOrd.bill_city,from_inventory_status="pending",to_inventory_status="pending")
                new_cour=inven_del(inventory_city=seller_details.city,delivery_address=pOrd.billing_address,delivery_city=pOrd.bill_city,shipping_address=seller_details.address,shipping_city=seller_details.city,order_id=ord_id,delivery_status="pending",coor1="false",coor2="false",delivery_mode="seller_to_buyer",verify="True")
                session.add(new_del)
                session.commit()
            session.close()
            return "successfully order created"
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error occurred: {str(e)}")
        