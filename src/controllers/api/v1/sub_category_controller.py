import os
from typing import Annotated

from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import APIRouter, status, Depends, HTTPException, Query

from src.config.database import get_db
from src.models.category_model import CategoryModel
from src.models.sub_category_model import SubCategoryModel
from src.filters.sub_category_filters import SubCategoryFilter
from src.models.product_template_model import ProductTemplateModel
from src.validators.sub_category_validator import validate_unique_code
from src.schemas.sub_category_schema import CreateSubCategory, ResponseSubCategory, create_sub_category_form


router = APIRouter()


@router.post("", response_model = ResponseSubCategory, status_code=status.HTTP_201_CREATED)
def create_sub_category(data : CreateSubCategory = Depends(validate_unique_code), db : Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.name == data.category_name).first()

    if not category:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Category not found"
        )

    sub_category = SubCategoryModel(
        name = data.name,
        category_id = category.id,
        code = data.code,
        icon = data.icon,
        description =  data.description,
        status = data.status
    )

    try:
        db.add(sub_category)
        db.commit()
        db.refresh(sub_category)

        return sub_category

    except Exception:
        os.remove(data.icon)
        db.rollback()
        raise



@router.get("", response_model = Page[ResponseSubCategory], status_code = status.HTTP_200_OK)
def read_sub_category(filters : Annotated[SubCategoryFilter, Query()] = None, db : Session = Depends(get_db)):
    sub_category = db.query(SubCategoryModel)
    
    if filters.name:
        sub_category = sub_category.filter(SubCategoryModel.name.like(f"%{filters.name}%"))

    if filters.code:
        sub_category = sub_category.filter(SubCategoryModel.code.like(f"%{filters.code}%"))

    return paginate(db, sub_category, params=Params(size=20))



@router.put("/{id}", response_model=ResponseSubCategory, status_code=status.HTTP_200_OK)
def update_sub_category(id: int, data : CreateSubCategory = Depends(create_sub_category_form), db : Session = Depends(get_db)):
    sub_category = db.query(SubCategoryModel).filter(SubCategoryModel.id == id).first()

    if not sub_category:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data not found"
        )

    category = db.query(CategoryModel).filter(CategoryModel.name == data.category_name).first()
    
    if not category:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Category not found"
        )

    file_path = sub_category.icon
    os.remove(f"{file_path}")

    update_data = data.model_dump(exclude={"category_name"})
    for key,value in update_data.items():
        setattr(sub_category,key,value)

    sub_category.category_id = category.id

    try:
        db.commit()
        db.refresh(sub_category)

        return sub_category

    except Exception:
        os.remove(data.icon)
        db.rollback()
        raise

    

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_sub_category(id : int, db : Session = Depends(get_db)):
    sub_category = db.query(SubCategoryModel).filter(SubCategoryModel.id == id).first()

    if not sub_category:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data Not Found"
        )

    product_template = db.query(ProductTemplateModel).filter(ProductTemplateModel.sub_category == id).first()
    
    if product_template:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "In Product Template, Sub Category is exists"
        )

    file_path = sub_category.icon
    os.remove(f"{file_path}")

    try:
        db.delete(sub_category)
        db.commit()

        return ("status : Data successfuly deleted")
    
    except Exception:
        db.rollback()
        raise