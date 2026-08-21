import os
import shutil
from typing import Optional
from datetime import datetime, timezone

from pydantic import BaseModel, Field
from fastapi import (
    UploadFile, 
    File, 
    Form
)

from src.schemas.sub_category_schema import ResponseSubCategory


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
    descripton : str = Form(...),
    icon : UploadFile = File(...),
    status : Optional[str] = Form("Active")
):
    
    os.makedirs("uploads/category", exist_ok=True)
    file_path = f"uploads/category/{datetime.now(timezone.utc)}{icon.filename}"

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
    deleted_at : Optional[datetime] = None
    sub_categories: list[ResponseSubCategory] = Field(
        default_factory=list
    )
