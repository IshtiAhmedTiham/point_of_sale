from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from src.schemas.category_schema import CreateCategory, create_category_form
from src.config.database import get_db
from src.models.category_model import CategoryModel


def validate_unique_code(data : CreateCategory = Depends(create_category_form), db : Session = Depends(get_db)):
    is_code_exists = db.query(CategoryModel).filter(CategoryModel.code == data.code).first()

    if is_code_exists:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Code already exists"
        )

    return data

