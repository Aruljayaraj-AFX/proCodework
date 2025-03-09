from fastapi import APIRouter, HTTPException,Depends,Query
from schema.SELLER.seller_str import seller_str
from services.SELLER.seller_ser import get_seller_info_signup,checkotp,Authorization,seller_login,for_email,reset_password,update_profile
from services.SELLER.add_product import add_product,fetch_category,show_product
from services.SELLER.cat_req import req_c
from models.SELLER.product_data import products
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from pydantic import EmailStr
from services.SELLER.seller_order import new_o,current_o,past_o,currentstatus_o,r_orders_o,returnstatus_o

router=APIRouter()

@router.post("/get_seller_info")
def seller_info(otp_sent:str=Depends(get_seller_info_signup())):
    return{
        "successfully otp sent to email"
    }
    
@router.get("/verify_otp")
def verify_otp(verify:str=Depends(checkotp())):
    return verify

@router.get("/security_check/")
async def read(token: object = Depends(Authorization())):
    return token 

@router.get("/seller.login")
async def login(mes:str=Depends(seller_login())):
    return mes

@router.get("/reset_for/{email}")
def login_check(c:str = Depends(for_email())):
    return c

templates = Jinja2Templates(directory="html")
@router.get("/r/{email}", response_class=HTMLResponse)
async def read_form(request: Request, email: str = None):
    return templates.TemplateResponse("reset.html", {"request": request, "email": email})

@router.get("/submit/{email}")
async def submit_password(email: EmailStr,new_password: str = Query(..., alias="new_password"),conform_password: str = Query(..., alias="conform_password")):
    res=reset_password(email,new_password,conform_password)
    return res

@router.get("/fetch_category")
async def fetch_c(c:list =Depends(fetch_category)):
    return c

@router.post("/show_product")
async def product(show:str=Depends(show_product())):
    return show

@router.post("/add_product")
async def product(add:str=Depends(add_product())):
    return add

@router.post("/category_request")
async def c_req(req_c:str=Depends(req_c())):
    return req_c

@router.get("/new_orders")
async def new_order(new_o:str=Depends(new_o())):
    return new_o

@router.get("/current_orders")
async def current_order(current_o:str=Depends(current_o())):
    return current_o

@router.put("/current.status_orders")
async def currentstatus_order(current_o:str=Depends(currentstatus_o())):
    return current_o

@router.get("/past_orders")
async def past_order(past_o:str=Depends(past_o())):
    return past_o

@router.get("/return_order")
async def r_order(return_o:str=Depends(r_orders_o())):
    return return_o

@router.put("/return.status_orders")
async def rstatus_order(returnstatus_o:str=Depends(returnstatus_o())):
    return returnstatus_o

@router.put("/update_profile")
async def update_profile(update:str=Depends(update_profile())):
    return update

