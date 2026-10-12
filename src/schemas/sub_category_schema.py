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

from src.utils.files import save_file

class CreateSubCategory(BaseModel):
    name : str
    category_name : str
    code : str
    icon : str
    description : str
    status : Optional[str] = "Active"
    deleted_at : Optional[datetime] = None



def create_sub_category_form(
    name : str = Form(...),
    category_name : str = Form(...),
    code : str = Form(...),
    icon : UploadFile = File(...),
    description : str = Form(...),
    status : str = Form("Active")
):

    file_path = save_file(icon, "sub_category")

    return CreateSubCategory(
        name = name,
        category_name = category_name,
        code = code,
        icon = file_path,
        description = description,
        status = status
    )



class ResponseSubCategory(BaseModel):
    id : int
    name : str
    category_id : int
    code : str
    icon : str
    description : str
    status : str
    deleted_at : Optional[datetime] = None