import os
import shutil
from typing import Optional

from fastapi import Form, UploadFile, File
from pydantic import BaseModel


class CreateCategory(BaseModel):
    name: str
    code: str
    description: str
    icon : str
    status: Optional[str] = "Active"


def create_category_form(
    name : str = Form(...),
    code : str = Form(...),
    descripton : str = Form(...),
    icon : UploadFile = File(...),
    status : Optional[str] = Form("Active")):
    
    os.makedirs("uploads/category", exist_ok=True)
    file_path = f"uploads/category/{icon.filename}"

    with open(file_path, "wb") as file:
        shutil.copyfileobj(icon.file, file)

    return CreateCategory(
        name = name,
        code = code,
        description = descripton,
        icon = file_path,
        status = status 
    )


class CategoryResponse(BaseModel):
    id : int
    name : str
    code : str
    description : str
    icon : str
    status : str