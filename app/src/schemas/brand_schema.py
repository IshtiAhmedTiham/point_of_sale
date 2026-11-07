from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
from fastapi import (
    UploadFile, 
    File, 
    Form
)

from app.src.schemas.suplier_schema import ResponseSuplier
from app.src.utils.files import save_file

class CreateBrand(BaseModel):
    name : str
    email : EmailStr
    phone : str
    address : str
    logo : str
    status : Optional[str] = "Active"
    deleted_at : Optional[datetime] = None



def create_brand_form(
    name : str = Form(...),
    email : str = Form(...),
    phone : str = Form(...),
    address : str = Form(...),
    logo : UploadFile = File(...),
    status : str = Form("Active")
):

    file_path = save_file(logo, "brand")

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
    deleted_at : Optional[datetime] = None
    supliers: list[ResponseSuplier] = Field(
        default_factory=list
    )
