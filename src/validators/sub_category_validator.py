import os

from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends

from src.config.database import get_db
from src.models.sub_category_model import SubCategoryModel
from src.schemas.sub_category_schema import CreateSubCategory, create_sub_category_form


def validate_unique_code(data : CreateSubCategory = Depends(create_sub_category_form), db : Session = Depends(get_db)):
    is_code_exists = db.query(SubCategoryModel).filter(SubCategoryModel.code == data.code, SubCategoryModel.deleted_at == None).first()

    if is_code_exists:
        file_path = data.icon
        os.remove(f"{file_path}")
        
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Code already exists"
        )

    return data
