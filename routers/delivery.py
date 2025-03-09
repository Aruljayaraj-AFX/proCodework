from fastapi import APIRouter, HTTPException,Depends,Query
from services.inventory import login,inven_Authorization,inven_courier,courier_update,delv_update
from services.delivery.del_signup import get_del_info_signup
from services.delivery.del_signup import checkDotp,del_Authorization,del_login,del_email,resetd_password,staff_update,order_list,pick_order,update_order
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from pydantic import EmailStr


router_del=APIRouter()

@router_del.post("/get_user_info")
def user_info(otp_sent:str=Depends(get_del_info_signup())):
    return{
        "successfully otp sent to email"
    }
 
@router_del.get("/verify_otp")
def verify_otp(verify:str=Depends(checkDotp())):
    return verify

  
@router_del.get("/security_check/")
async def read(token: object = Depends(del_Authorization())):
    return token 


@router_del.get("/seller.login")
async def login(mes:str=Depends(del_login())):
    return mes


@router_del.get("/reset_for/{email}")
def login_check(c:str = Depends(del_email())):
    return c


templates = Jinja2Templates(directory="html")
@router_del.get("/r/{email}", response_class=HTMLResponse)
async def read_form(request: Request, email: str = None):
    return templates.TemplateResponse("del_html.html", {"request": request, "email": email})

@router_del.get("/submit/{email}")
async def submit_password(email: EmailStr,new_password: str = Query(..., alias="new_password"),conform_password: str = Query(..., alias="conform_password")):
    res=resetd_password(email,new_password,conform_password)
    return res

@router_del.put("/update_profile")
async def update_profile(res:str=Depends(staff_update())):
    return res

@router_del.get("/order_list")
async def order_list(res:dict=Depends(order_list())):
    return res

@router_del.put("/pick_order")
async def pick_order(res:dict=Depends(pick_order())):
    return res

@router_del.put("/update_delivery_status")
async def up_del(res:dict=Depends(update_order())):
    return res