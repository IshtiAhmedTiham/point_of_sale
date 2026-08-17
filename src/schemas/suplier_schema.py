import os
import shutil
from typing import Optional
from datetime import datetime, timezone

from pydantic import BaseModel
from fastapi import (
    UploadFile, 
    File, 
    Form
)

class CreateSuplier(BaseModel):
    name : str
    brand_name : str
    phone : str
    address : str
    account_no : str
    opening_balance : float
    image : str
    deleted_at : Optional[datetime] = None


def create_suplier_form(
    name : str = Form(...),
    brand_name : str = Form(...),
    phone : str = Form(...),
    address : str = Form(...),
    account_no : str = Form(...),
    opening_balance : float = Form(...),
    image : UploadFile = File(...)):

    os.makedirs("uploads/suplier", exist_ok=True)
    file_path = f"uploads/suplier/{datetime.now(timezone.utc)}{image.filename}"

    with open(file_path, "wb") as file:
        shutil.copyfileobj(image.file, file)

    return CreateSuplier(
        name = name,
        brand_name = brand_name,
        phone = phone,
        address = address,
        account_no = account_no,
        opening_balance = opening_balance,
        image = file_path
    )


class ResponseSuplier(BaseModel):
    id : int
    name : str
    brand_id : int
    phone : str
    address : str
    account_no : str
    opening_balance : float
    image : str
    deleted_at : Optional[datetime] = None