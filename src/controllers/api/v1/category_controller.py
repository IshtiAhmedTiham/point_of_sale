import os
import shutil
from typing import Annotated
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import APIRouter, status, Depends, Query, HTTPException

from src.config.database import get_db
from src.models.category_model import CategoryModel
from src.filters.category_filters import CategoryFilter
from src.models.sub_category_model import SubCategoryModel
from src.models.product_template_model import ProductTemplateModel
from src.validators.category_validator import validate_unique_code
from src.schemas.category_schema import CreateCategory, CategoryResponse, create_category_form


router = APIRouter()


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(data : CreateCategory = Depends(validate_unique_code), db : Session = Depends(get_db)):
    category = CategoryModel(
        name = data.name,
        code = data.code,
        description = data.description,
        icon = data.icon,
        status = data.status,
        deleted_at = data.deleted_at
    )

    try:
        db.add(category)
        db.commit()
        db.refresh(category)

        return category
    
    except Exception:
        os.remove(data.icon)
        db.rollback()
        raise



@router.get("/", response_model=Page[CategoryResponse], status_code=status.HTTP_200_OK)
def read_category(filters : Annotated[CategoryFilter,Query()] = None, db : Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.deleted_at.is_(None))

    if filters.name:
        category = category.filter(CategoryModel.name.like(f"%{filters.name}%"))

    if filters.code:
        category = category.filter(CategoryModel.code.like(f"%{filters.code}%"))

    return paginate(db, category, params=Params(size=20))



@router.put("/{id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def update_category(id : int, data : CreateCategory = Depends(create_category_form), db : Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == id, CategoryModel.deleted_at.is_(None)).first()

    if not category:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data Not Found"
        )
    
    file_path = category.icon

    try:
        updated_data = data.model_dump()
        for key,value in updated_data.items():
            setattr(category,key,value)

        db.commit()
        db.refresh(category)

        os.remove(f"{file_path}")

        return category
    
    except Exception:
        db.rollback()
        os.remove(data.icon)
        raise



@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_category(id : int, db : Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == id, CategoryModel.deleted_at.is_(None)).first()
    if not category:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data Not Found"
        )
    
    
    sub_category = db.query(SubCategoryModel).filter(SubCategoryModel.category_id == id, SubCategoryModel.deleted_at.is_(None)).first()
    if sub_category:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "In Sub Category, Category is exists"
        )


    product_template = db.query(ProductTemplateModel).filter(ProductTemplateModel.category_id == id, ProductTemplateModel.deleted_at.is_(None)).first()
    if product_template:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "In Product Template, Category is exists"
        )
    

    try:
        file_path = category.icon

        category.deleted_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(category)

        file = os.path.basename(f"{file_path}")

        os.makedirs("deleted_file/category", exist_ok=True)
        destination = f"deleted_file/category/{file}"

        shutil.move(f"{file_path}", destination)

        return ("status : Data successfuly deleted")
    
    except Exception:
        db.rollback()
        raise