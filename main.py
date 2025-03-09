from fastapi import FastAPI
import uvicorn
from routers.seller import router
from routers.user import router_u
from routers.ventory import router_inven
from routers.delivery import router_del

app = FastAPI()

app.include_router(router,prefix="/codework/v1/seller", tags=["seller_dashboard"])
app.include_router(router_u,prefix="/codework/v1/user", tags=["user_dashboard"])
app.include_router(router_inven,prefix="/codework/v1/inven", tags=["inven_dashboard"])
app.include_router(router_del,prefix="/codework/v1/del", tags=["delivery_partner_dashboard"])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)