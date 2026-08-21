from datetime import datetime
from typing import Optional

from fastapi import Form
from pydantic import BaseModel, Field



class CreatePurchase(BaseModel):
    date : datetime
    supplier_name : str
    product_name : str
    unit_cost : float
    quantity : int
    tax : float
    sub_total : float
    brand_name  : str
    total : float
    discount : float
    net_total : float
    payment_method : str
    pay : float
    due : float



def create_purchase_form(
    date : datetime = Form(...),
    supplier_name : str = Form(...),
    product_name : str = Form(...),
    unit_cost : float = Form(...),
    quantity : int = Form(...),
    tax : float = Form(...),
    sub_total : float = Form(...),
    brand_name  : str = Form(...),
    total : float = Form(...),
    discount : float = Form(...),
    net_total : float = Form(...),
    payment_method : str = Form(...),
    pay : float = Form(...),
    due : float = Form(...)
):

    return CreatePurchase(
        date = date,
        supplier_name = supplier_name,
        product_name = product_name,
        unit_cost = unit_cost,
        quantity = quantity,
        tax = tax,
        sub_total = sub_total,
        brand_name  = brand_name,
        total = total,
        discount = discount,
        net_total = net_total,
        payment_method = payment_method,
        pay = pay,
        due = due
    )



class ResponsePurchaseBilling(BaseModel):
    total: float
    discount: float
    net_total: float
    payment_method: str
    pay: float
    due: float

class ResponsePurchaseStock(BaseModel):
    id : int
    code : str


class ResponsePurchase(BaseModel):
    id : int
    date : datetime
    suplier_id :  int
    product_id :  int
    unit_cost : float
    quantity : int
    tax : float
    sub_total : float
    brand_id  : int
    purchase_billing: ResponsePurchaseBilling
    purchase_stocks: list[ResponsePurchaseStock] = Field(
        default_factory=list
    )
    deleted_at : Optional[datetime] = None
    