import os
import shutil
from typing import Optional
from datetime import datetime, timezone

from pydantic import BaseModel
from fastapi import Form, UploadFile, File

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
    status : str = Form("Active")):

    os.makedirs("uploads/sub_category", exist_ok=True)
    file_path = f"uploads/sub_category/{datetime.now(timezone.utc)}{icon.filename}"

    with open(file_path, "wb") as file:
        shutil.copyfileobj(icon.file, file)

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