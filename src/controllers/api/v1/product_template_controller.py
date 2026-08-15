import os
import shutil
from typing import Annotated
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import APIRouter, status, Depends, HTTPException, Query

from src.config.database import get_db
from src.models.brand_model import BrandModel
from src.models.category_model import CategoryModel
from src.models.sub_category_model import SubCategoryModel
from src.models.product_template_model import ProductTemplateModel
from src.filters.product_template_filters import ProductTemplateFilters
from src.validators.product_template_validator import validate_unique_code
from src.schemas.product_template_schema import CreateProductTemplate, ResponseProductTemplate, create_product_template_form


router = APIRouter()


@router.post("", response_model=ResponseProductTemplate, status_code=status.HTTP_201_CREATED)
def create_product_template(data : CreateProductTemplate = Depends(validate_unique_code), db : Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.name == data.category_name, CategoryModel.deleted_at.is_(None)).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )


    sub_category = db.query(SubCategoryModel).filter(SubCategoryModel.name == data.sub_category_name, SubCategoryModel.deleted_at.is_(None)).first()
    if not sub_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sub category not found"
        )
    

    brand = db.query(BrandModel).filter(BrandModel.name == data.brand_name, BrandModel.deleted_at.is_(None)).first()  
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found"
        )


    product_template = ProductTemplateModel(
        name = data.name,
        code = data.code,
        category_id = category.id,
        sub_category_id = sub_category.id,
        brand_id = brand.id,
        mrp = data.mrp,
        tax = data.tax,
        description = data.description,
        openstock = data.openstock,
        image = data.image,
        deleted_at = data.deleted_at
    )

    try:
        db.add(product_template)
        db.commit()
        db.refresh(product_template)

        return product_template
    
    except Exception:
        os.remove(data.image)
        db.rollback()
        raise



@router.get("", response_model=Page[ResponseProductTemplate], status_code=status.HTTP_200_OK)
def read_product_template(filters : Annotated[ProductTemplateFilters, Query()] = None, db : Session = Depends(get_db)):
    product_template = db.query(ProductTemplateModel).filter(ProductTemplateModel.deleted_at.is_(None))

    if filters.name:
        product_template = product_template.filter(ProductTemplateModel.name.like(f"%{filters.name}%"))

    if filters.code:
        product_template = product_template.filter(ProductTemplateModel.code.like(f"%{filters.code}%"))
    
    return paginate(db, product_template, params=Params(size=20))



@router.put("/{id}", response_model=ResponseProductTemplate, status_code=status.HTTP_200_OK)
def update_product_template(id : int, data : CreateProductTemplate = Depends(create_product_template_form), db : Session = Depends(get_db)):
    product_template = db.query(ProductTemplateModel).filter(ProductTemplateModel.id == id, ProductTemplateModel.deleted_at.is_(None)).first()

    file_path = data.image

    if not product_template:
        os.remove(f"{file_path}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product Template not found"
        )
    

    category = db.query(CategoryModel).filter(CategoryModel.name == data.category_name, CategoryModel.deleted_at.is_(None)).first()
    if not category:
        os.remove(f"{file_path}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    
    sub_category = db.query(SubCategoryModel).filter(SubCategoryModel.name == data.sub_category_name, SubCategoryModel.deleted_at.is_(None)).first()
    if not sub_category:
        os.remove(f"{file_path}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sub category not found"
        )
    
    
    brand = db.query(BrandModel).filter(BrandModel.name == data.brand_name, BrandModel.deleted_at.is_(None)).first()
    if not brand:
        os.remove(f"{file_path}")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found"
        )

    old_file_path = product_template.image

    try:
        update_data = data.model_dump(exclude={"category_name", "sub_category_name", "brand_name"})
        for key, value in update_data.items():
            setattr(product_template, key, value)

        product_template.category_id = category.id
        product_template.sub_category_id = sub_category.id
        product_template.brand_id = brand.id

        db.commit()
        db.refresh(product_template)

        os.remove(f"{old_file_path}")

        return product_template
    
    except Exception:
        db.rollback()
        os.remove(data.image)
        raise



@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_product_template(id : int, db : Session = Depends(get_db)):
    product_template = db.query(ProductTemplateModel).filter(ProductTemplateModel.id == id, ProductTemplateModel.deleted_at.is_(None)).first()
    if not product_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found"
        )


    try:
        file_path = product_template.image

        product_template.deleted_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(product_template)

        file = os.path.basename(f"{file_path}")

        os.makedirs("deleted_file/product_template", exist_ok=True)
        destination = f"deleted_file/product_template/{file}"

        shutil.move(f"{file_path}", destination)

        return {"status" : "Data successfuly deleted"}

    except Exception:
        db.rollback()
        raise
