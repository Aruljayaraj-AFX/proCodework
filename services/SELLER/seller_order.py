from utils.security import hashword,decode
from database.DB import session
from fastapi import APIRouter, HTTPException,Depends,Query
from services.SELLER.seller_ser import Authorization
from models.SELLER.seller_info import SellersInfo
from datetime import datetime
from models.SELLER.order import orders
from models.SELLER.return_order import r_orders


class new_o:
    def __call__(self, token: str = Depends(Authorization())):
        use = token['password']
        print("User Password:", use)

        res = session.query(SellersInfo).filter(SellersInfo.email == use).first()
        print("Seller Info:", res)

        if not res:
            return {"error": "Error in fetching the seller_id"}

        sellers_id = res.seller_id
        print("Seller ID:", sellers_id)

       
        orders_list = session.query(orders).filter(orders.delivery_date.is_(None) & ((orders.verify == False)&(orders.seller_id == sellers_id))).all()


        if not orders_list:
            return {"message": "No data found in new_order"}

        for order in orders_list:
            order.verify = True
            print(order.order_id)
        
        session.commit()  

        return {"updated_orders": [order.order_id for order in orders_list]}



class current_o:
    def __call__ (self,token:str=Depends(Authorization())):
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

        orders_list = session.query(orders).filter(orders.delivery_date.is_(None) & ((orders.verify == True)&(orders.seller_id == sellers_id))).all()

        if not orders_list:
            return {"message": "No data found in current_order"}

        for order in orders_list:
            order.verify = True
        
        session.commit()   

        return {"current_orders": [order.order_id for order in orders_list]}



class past_o:
    def __call__ (self,token:str=Depends(Authorization())):
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

        orders_list = session.query(orders).filter((orders.delivery_date.is_not(None))&((orders.verify == True)&(orders.seller_id == sellers_id))).all()

        if not orders_list:
            return {"message": "No data found in new_order"}

        for order in orders_list:
            order.verify = True
        
        session.commit() 
  

        return {"updated_orders": [order.order_id for order in orders_list]}

class r_orders_o:
    def __call__ (self,token:str=Depends(Authorization())):
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
        orders_list=session.query(r_orders).filter(r_orders.seller_id == sellers_id)

        if not orders_list:
            return {"message": "No data found in new_order"}

        for order in orders_list:
            order.verify = True
        
        session.commit() 
  

        return {"updated_orders": [order.order_id for order in orders_list]} 


class returnstatus_o:
    def __call__(self,return_statusb:str,return_id:str,token:str=Depends(Authorization())):
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
        res1=session.query(r_orders).filter(r_orders.return_id == return_id).first()
        if res1:
            res1.return_status = return_statusb
            session.commit()
            return{
                "successfully_update the return_status"
            }
        else:
            return{
                "no data found in return_order"
            }


class currentstatus_o:
    def __call__(self,o_id:str,order_statusb:str,shipping_addressb:str,token:str=Depends(Authorization())):
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
        res1=session.query(orders).filter(orders.order_id==o_id).first()
        if res1:
            res1.shipping_address = shipping_addressb
            res1.order_status = order_statusb
            print(res1.order_status)
            print(order_statusb)
            session.commit()
            res11=session.query(orders).filter(orders.order_id==o_id).first()
            print(res11.shipping_address)
            return{
                "successfully update the order status by seller"
            }
        else:
            return{
                "no data found in past_order"
            }