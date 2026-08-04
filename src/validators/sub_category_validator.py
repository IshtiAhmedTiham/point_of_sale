from fastapi import status, HTTPException, Depends
from sqlalchemy.orm import Session

from src.schemas.sub_category_schema import CreateSubCategory, create_sub_category_form
from src.config.database import get_db
from src.models.sub_category_model import SubCategoryModel


def validate_unique_code(data : CreateSubCategory = Depends(create_sub_category_form), db : Session = Depends(get_db)):
    is_code_exists = db.query(SubCategoryModel).filter(SubCategoryModel.code == data.code).first()

    if is_code_exists:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Code already exists"
        )

    return data
