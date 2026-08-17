import os

from sqlalchemy.orm import Session
from fastapi import (
    status, 
    HTTPException, 
    Depends
)

from src.config.database import get_db
from src.models.category_model import CategoryModel
from src.schemas.category_schema import CreateCategory, create_category_form


def validate_unique_code(
    data : CreateCategory = Depends(create_category_form), 
    db : Session = Depends(get_db)
):

    is_code_exists = (
        db.query(CategoryModel)
        .filter(
            CategoryModel.code == data.code, 
            CategoryModel.deleted_at == None
        )
        .first()
    )
    
    if is_code_exists:
        file_path = data.icon
        os.remove(f"{file_path}")
        
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Code already exists"
        )

    return data

