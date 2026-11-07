import os
import shutil
from typing import Annotated, cast
from datetime import datetime, timezone

from sqlalchemy.orm import Session, selectinload
from fastapi_pagination import Page, Params 
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import (
    APIRouter, 
    status, 
    Depends, 
    Query, 
    HTTPException
)

from app.src.config.database import get_db,DbSession
from app.src.models.category_model import CategoryModel
from app.src.filters.category_filters import CategoryFilter
from app.src.models.sub_category_model import SubCategoryModel
from app.src.models.product_template_model import ProductTemplateModel
from app.src.validators.category_validator import validate_unique_code
from app.src.utils.files import delete_file
from app.src.schemas.category_schema import (
    CreateCategory, 
    UpdateCategory,
    CategoryResponse, 
    create_category_form,
    update_category_form
)


router = APIRouter()


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    db : DbSession,
    data : CreateCategory = Depends(validate_unique_code) 
):
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
        db.rollback()
        os.remove(data.icon)
        raise



@router.get("/", response_model=Page[CategoryResponse], status_code=status.HTTP_200_OK)
def read_category(
    db : DbSession,
    filters : Annotated[CategoryFilter,Query()]
):
    category = (
        db.query(CategoryModel)
        .options(selectinload(CategoryModel.sub_categories))
        .filter(CategoryModel.deleted_at.is_(None))
    )

    if filters.name:
        category = category.filter(CategoryModel.name.like(f"%{filters.name}%"))

    if filters.code:
        category = category.filter(CategoryModel.code.like(f"%{filters.code}%"))

    return paginate(db, category, params=Params(size=20))



@router.put("/{id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
def update_category(
    db : DbSession,
    id : int, 
    data : UpdateCategory = Depends(update_category_form)
):
    category = (
        db.query(CategoryModel)
        .filter(
            CategoryModel.id == id, 
            CategoryModel.deleted_at.is_(None)
        )
        .first()
    )

    if not category:
        if data.icon and os.path.exists(data.icon):
            os.remove(data.icon)

        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data Not Found"
        )
    
    old_file_path = cast(str,category.icon)
    new_file_path = cast(str,data.icon)

    try:
        updated_data = data.model_dump(exclude={"icon"})
        for key,value in updated_data.items():
            setattr(category,key,value)

        if new_file_path:
            category.icon = new_file_path

        db.commit()
        db.refresh(category)

        if new_file_path and old_file_path and os.path.exists(old_file_path):
            os.remove(old_file_path)

        return category
    
    except Exception:
        db.rollback()

        if new_file_path and os.path.exists(new_file_path):
            os.remove(new_file_path)
        raise



@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_category(
    db : DbSession,
    id : int
):
    category = (
        db.query(CategoryModel)
        .filter(
            CategoryModel.id == id, 
            CategoryModel.deleted_at.is_(None)
        )
        .first()
    )
    if not category:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data Not Found"
        )
    
    
    sub_category = (
        db.query(SubCategoryModel)
        .filter(
            SubCategoryModel.category_id == id, 
            SubCategoryModel.deleted_at.is_(None)
        )
        .first()
    )
    if sub_category:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "In Sub Category, Category is exists"
        )


    product_template = (
        db.query(ProductTemplateModel)
        .filter(
            ProductTemplateModel.category_id == id, 
            ProductTemplateModel.deleted_at.is_(None)
        )
        .first()
    )
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

        delete_file(f"{file_path}", "category")

        return ("status : Data successfuly deleted")
    
    except Exception:
        db.rollback()
        raise