import os
import shutil
from typing import Optional
from datetime import datetime, timezone

from pydantic import BaseModel, EmailStr
from fastapi import (
    UploadFile, 
    File, 
    Form
)

from app.src.utils.files import save_file


class CreateCustomer(BaseModel):
    name : str
    email : EmailStr
    phone : str
    address : str
    account_no : str
    opening_balance : float
    discount : float
    taxable : float
    icon : str
    deleted_at : Optional[datetime] = None


def create_customer_form(
    name : str = Form(...),
    email : EmailStr = Form(...),
    phone : str = Form(...),
    address : str = Form(...),
    account_no : str = Form(...),
    opening_balance : float = Form(...),
    discount : float = Form(...),
    taxable : float = Form(...),
    icon : UploadFile = File(...)
):
    
    file_path = save_file(icon, "customer")

    return CreateCustomer(
        name = name,
        email = email,
        phone = phone,
        address = address,
        account_no = account_no,
        opening_balance = opening_balance,
        discount = discount,
        taxable = taxable,
        icon = file_path
    )


class CustomerResponse(BaseModel):
    id : int
    name : str
    email : EmailStr
    phone : str
    address : str
    account_no : str
    opening_balance : float
    discount : float
    taxable : float
    icon : str
    deleted_at : Optional[datetime] = None
