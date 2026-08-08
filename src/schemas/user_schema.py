import os
import shutil
from typing import Optional
from datetime import datetime, timezone

from pydantic import BaseModel, EmailStr
from fastapi import Form, UploadFile, File


class CreateUser(BaseModel):
    name : str
    email : EmailStr
    password : str
    confirm_password : str
    role : Optional[str] = "user"
    branch : str
    phone : str
    address : str
    image : str
    status : Optional[str] = "Active"


def create_user_form(
    name : str = Form(...),
    email : EmailStr = Form(...),
    password : str = Form(...),
    confirm_password : str = Form(...),
    role : str = Form("user"),
    branch : str = Form(...),
    phone : str = Form(...),
    address : str = Form(...),
    image : UploadFile = File(...),
    status : str = Form("Active")):


    os.makedirs("uploads/user", exist_ok=True)

    file_path = f"uploads/user/{datetime.now(timezone.utc)}{image.filename}"
    with open(file_path, "wb") as file:
        shutil.copyfileobj(image.file, file)

    return CreateUser(
        name = name,
        email = email,
        password = password,
        confirm_password = confirm_password,
        role = role,
        branch = branch,
        phone = phone,
        address = address,
        image = file_path,
        status = status
    )



class ResponseUser(BaseModel):
    id : int
    name : str
    email : EmailStr
    password : str
    confirm_password : str
    role : str
    branch : str
    phone : str
    address : str
    image : str
    status : str