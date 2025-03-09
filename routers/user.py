from fastapi import APIRouter, HTTPException,Depends,Query
from services.user.user_profile import get_user_info_signup
from services.user.user_profile import checkUotp,user_Authorization
from services.user.user_profile import user_login,user_email,resetu_password,userpageproduct,Wlist,Cat,SearchService,addtocart,my_order,my_return,returnable_order,profile_update,payment,payment_verify,c_order
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from pydantic import EmailStr
from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel
import json

router_u=APIRouter()

@router_u.post("/get_user_info")
def user_info(otp_sent:str=Depends(get_user_info_signup())):
    return{
        "successfully otp sent to email"
    }
 
@router_u.get("/verify_otp")
def verify_otp(verify:str=Depends(checkUotp())):
    return verify

  
@router_u.get("/security_check/")
async def read(token: object = Depends(user_Authorization())):
    return token 


@router_u.get("/seller.login")
async def login(mes:str=Depends(user_login())):
    return mes


@router_u.get("/reset_for/{email}")
def login_check(c:str = Depends(user_email())):
    return c


templates = Jinja2Templates(directory="html")
@router_u.put("/r/{email}", response_class=HTMLResponse)
async def read_form(request: Request, email: str = None):
    return templates.TemplateResponse("user_reset.html", {"request": request, "email": email})

@router_u.put("/submit/{email}")
async def submit_password(email: EmailStr,new_password: str = Query(..., alias="new_password"),conform_password: str = Query(..., alias="conform_password")):
    res=resetu_password(email,new_password,conform_password)
    return res

@router_u.get("/product_list/")
async def product_list(result:str=Depends(userpageproduct())):
    return result

@router_u.get("/wish_list/")
async def get_wishlist(wlist: str = Depends(Wlist())):  
    return wlist

@router_u.get("/categories")
async def get_cat(cat:str=Depends(Cat())):
    return cat

@router_u.get("/search/")
def search_items(keyword: str = Depends(SearchService())):
    return keyword

@router_u.post("/cart")
def cart(addpro:str=Depends(addtocart())):
    return addpro

@router_u.get("/my_order")
def my_order(my_order:str=Depends(my_order())):
    return my_order

@router_u.post("/my_return")
def my_return(return_order:str=Depends(my_return())):
    return return_order

@router_u.get("/returnable")
def returnable(returnable:str=Depends(returnable_order())):
    return returnable

@router_u.put("user_profile_update")
def user_update(update:str=Depends(profile_update())):
    return update

@router_u.post("paymenrs")
def pay(pa:str=Depends(payment())):
    return pa

@router_u.post("payment_verify")
def payv(ps:str=Depends(payment_verify())):
    return ps

@router_u.post("create_order")
def c_orders(co:str=Depends(c_order())):
    return co