from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field
from fastapi import (
    UploadFile, 
    File, 
    Form
)

from app.src.schemas.sub_category_schema import ResponseSubCategory
from app.src.utils.files import save_file


class CreateCategory(BaseModel):
    name: str
    code: str
    description: str
    icon : str
    status: Optional[str] = "Active"
    deleted_at: Optional[datetime] = None



def create_category_form(
    name : str = Form(...),
    code : str = Form(...),
    description : str = Form(...),
    icon : UploadFile = File(...),
    status : Optional[str] = Form("Active")
):
    
    file_path = save_file(icon, "category")

    return CreateCategory(
        name = name,
        code = code,
        description = description,
        icon = file_path,
        status = status 
    )



class UpdateCategory(BaseModel):
    name: str
    code: str
    description: str
    icon: Optional[str] = None
    status: Optional[str] = "Active"



def update_category_form(
    name : str = Form(...),
    code : str = Form(...),
    description : str = Form(...),
    icon : Optional[UploadFile] = File(None),
    status : Optional[str] = Form("Active")
):
    file_path = None

    if icon is not None and icon.filename:
        file_path = save_file(icon, "category")

    return UpdateCategory(
        name = name,
        code = code,
        description = description,
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
    deleted_at : Optional[datetime] = None
    sub_categories: list[ResponseSubCategory] = Field(
        default_factory=list
    )
