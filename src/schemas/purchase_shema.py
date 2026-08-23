from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime

from fastapi import Form

class CreatePurchase(BaseModel):
    date : datetime
    suplier_name : str
    product_name : str
    unit_cost : float
    quantity : int
    tax : float
    sub_total : float
    brand_name : str
    total : float
    discount : float
    net_total : float
    payment_method : str
    pay : float
    due : float


def create_purchase_form(
    date : datetime = Form(...),
    suplier_name : str = Form(...),
    product_name : str = Form(...),
    unit_cost : float = Form(...),
    quantity : int = Form(...),
    tax : float = Form(...),
    sub_total : float = Form(...),
    brand_name : str = Form(...),
    total : float = Form(...),
    discount : float = Form(...),
    net_total : float = Form(...),
    payment_method : str = Form(...),
    pay : float = Form(...),
    due : float = Form(...)
):
    return CreatePurchase(
        date=date,
        suplier_name = suplier_name,
        product_name = product_name,
        unit_cost = unit_cost,
        quantity = quantity,
        tax = tax,
        sub_total=sub_total,
        brand_name = brand_name,
        total = total,
        discount = discount,
        net_total = net_total,
        payment_method = payment_method,
        pay = pay,
        due = due
    )


class ResponseBilling(BaseModel):
    id : int
    total : float
    discount : float
    net_total : float
    payment_method : str
    pay : float
    due : float
    deleted_at : Optional[datetime]

class ResponseStock(BaseModel):
    id : int
    code : str
    deleted_at : Optional[datetime]


class ResponsePurchase(BaseModel):
    id : int
    date: datetime
    suplier_id : int
    product_id : int
    unit_cost : float
    quantity : int
    tax : float
    sub_total : float
    brand_id : int
    deleted_at : Optional[datetime]
    purchase_billing : ResponseBilling
    purchase_stock : list[ResponseStock] = Field(default_factory=list)