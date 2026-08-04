from typing import List, Annotated

from fastapi import APIRouter, status, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.category_model import CategoryModel
from src.schemas.category_schema import CreateCategory, CategoryResponse, create_category_form
from src.validators.category_validator import validate_unique_code
from src.filters.category_filters import CategoryFilter


router = APIRouter()


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(data : CreateCategory = Depends(validate_unique_code), db : Session = Depends(get_db)):
    category = CategoryModel(
        name = data.name,
        code = data.code,
        description = data.description,
        icon = data.icon,
        status = data.status
    )

    try:
        db.add(category)
        db.commit()
        db.refresh(category)

        return category
    
    except Exception:
        db.rollback()
        raise



@router.get("/", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
def read_category(filters : Annotated[CategoryFilter,Query()], db : Session = Depends(get_db)):
    category = db.query(CategoryModel)

    if filters.name:
        category = category.filter(CategoryModel.name.like(f"%{filters.name}%"))

    if filters.code:
        category = category.filter(CategoryModel.code.like(f"%{filters.code}%"))

    return category.all()



@router.put("/{id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def update_category(id : int, data : CreateCategory = Depends(create_category_form), db : Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == id).first()

    if not category:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data Not Found"
        )

    updated_data = data.model_dump()
    for key,value in updated_data.items():
        setattr(category,key,value)

    try:
        db.commit()
        db.refresh(category)

        return category
    
    except Exception:
        db.rollback()
        raise


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_category(id : int, db : Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == id).first()

    if not category:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data Not Found"
        )

    try:
        db.delete(category)
        db.commit()

        return ("status : Data successfuly deleted")
    
    except Exception:
        db.rollback()
        raise