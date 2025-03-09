from fastapi import APIRouter, HTTPException,Depends,Query
from services.inventory import login,inven_Authorization,inven_courier,courier_update,delv_update

router_inven=APIRouter()

@router_inven.get("/inventory")
def inven(printl:str=Depends(login())):
    return printl

@router_inven.get("/security_check/")
async def invens(token: object = Depends(inven_Authorization())):
    return token 

@router_inven.get("/inven_show")
async def inven_show(result:str=Depends(inven_courier())):
    return result

@router_inven.put("/courier_status")
async def inven_c_up(result:str=Depends(courier_update())):
    return result

@router_inven.put("/del_update")
async def inven_d_up(result:str=Depends(delv_update())):
    return result