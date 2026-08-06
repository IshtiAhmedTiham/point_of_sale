from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException, Query
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from src.schemas.product_template_schema import CreateProductTemplate, ResponseProductTemplate, create_product_template_form
from src.config.database import get_db
from src.models.product_template_model import ProductTemplateModel
from src.models.category_model import CategoryModel
from src.models.sub_category_model import SubCategoryModel
from src.models.brand_model import BrandModel
from src.filters.product_template_filters import ProductTemplateFilters
from src.validators.product_template_validator import validate_unique_code


router = APIRouter()



@router.post("", response_model=ResponseProductTemplate, status_code=status.HTTP_201_CREATED)
def create_product_template(data : CreateProductTemplate = Depends(validate_unique_code), db : Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.name == data.category_name).first()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )


    sub_category = db.query(SubCategoryModel).filter(SubCategoryModel.name == data.sub_category_name).first()
    
    if not sub_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sub category not found"
        )
    

    brand = db.query(BrandModel).filter(BrandModel.name == data.brand_name).first()
    
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
        image = data.image
    )

    try:
        db.add(product_template)
        db.commit()
        db.refresh(product_template)

        return product_template
    
    except Exception:
        db.rollback()
        raise



@router.get("", response_model=Page[ResponseProductTemplate], status_code=status.HTTP_200_OK)
def read_product_template(filters : Annotated[ProductTemplateFilters, Query()] = None, db : Session = Depends(get_db)):
    product_template = db.query(ProductTemplateModel)

    if filters.name:
        product_template = product_template.filter(ProductTemplateModel.name.like(f"%{filters.name}%"))

    if filters.code:
        product_template = product_template.filter(ProductTemplateModel.code.like(f"%{filters.code}%"))
    
    return paginate(db, product_template, params=Params(size=20))



@router.put("/{id}", response_model=ResponseProductTemplate, status_code=status.HTTP_200_OK)
def update_product_template(id : int, data : CreateProductTemplate = Depends(create_product_template_form), db : Session = Depends(get_db)):
    product_template = db.query(ProductTemplateModel).filter(ProductTemplateModel.id == id).first()

    if not product_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    

    category = db.query(CategoryModel).filter(CategoryModel.name == data.category_name).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    
    sub_category = db.query(SubCategoryModel).filter(SubCategoryModel.name == data.sub_category_name).first()
    
    if not sub_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sub category not found"
        )
    
    
    brand = db.query(BrandModel).filter(BrandModel.name == data.brand_name).first()
    
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Brand not found"
        )

    update_data = data.model_dump(exclude={"category_name", "sub_category_name", "brand_name"})
    for key, value in update_data.items():
        setattr(product_template, key, value)

    product_template.category_id = category.id
    product_template.sub_category_id = sub_category.id
    product_template.brand_id = brand.id


    try:
        db.commit()
        db.refresh(product_template)

        return product_template
    
    except Exception:
        db.rollback()
        raise



@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_product_template(id : int, db : Session = Depends(get_db)):
    product_template = db.query(ProductTemplateModel).filter(ProductTemplateModel.id == id).first()

    if not product_template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found"
        )

    try:
        db.delete(product_template)
        db.commit()

        return {"status" : "Data successfuly deleted"}

    except Exception:
        db.rollback()
        raise
