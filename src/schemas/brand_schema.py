import os
import shutil
from typing import Optional
from datetime import datetime, timezone

from fastapi import UploadFile, File, Form
from pydantic import BaseModel, EmailStr


class CreateBrand(BaseModel):
    name : str
    email : EmailStr
    phone : str
    address : str
    logo : str
    status : Optional[str] = "Active"


def create_brand_form(
    name : str = Form(...),
    email : str = Form(...),
    phone : str = Form(...),
    address : str = Form(...),
    logo : UploadFile = File(...),
    status : str = Form("Active")):

    os.makedirs("uploads/brand", exist_ok=True)

    file_path = f"uploads/brand/{datetime.now(timezone.utc)}{logo.filename}"
    with open(file_path, "wb") as file:
        shutil.copyfileobj(logo.file, file)


    return CreateBrand(
        name = name,
        email = email,
        phone = phone,
        address = address,
        logo = file_path,
        status = status
    )



class ResponseBrand(BaseModel):
    id : int
    name : str
    email : EmailStr
    phone : str
    address : str
    logo : str
    status : str
