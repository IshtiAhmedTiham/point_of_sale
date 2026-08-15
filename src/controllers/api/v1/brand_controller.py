import os
import shutil
from typing import Annotated
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import APIRouter, status, Depends, HTTPException, Query, BackgroundTasks

from src.config.database import get_db
from src.models.brand_model import BrandModel
from src.models.suplier_model import SuplierModel
from src.filters.brand_filters import BrandFilters
from src.validators.brand_validator import validators
from src.services.email_service import send_brand_email
from src.models.product_template_model import ProductTemplateModel
from src.schemas.brand_schema import CreateBrand, ResponseBrand, create_brand_form


router = APIRouter()


@router.post("", response_model=ResponseBrand, status_code=status.HTTP_201_CREATED)
def create_brand(background_tasks : BackgroundTasks, data : CreateBrand = Depends(validators), db : Session = Depends(get_db)):
    brand = BrandModel(
        name = data.name,
        email = data.email,
        phone = data.phone,
        address = data.address,
        logo = data.logo,
        status = data.status,
        deleted_at = data.deleted_at
    )

    try:
        db.add(brand)
        db.commit()
        db.refresh(brand)
    
    except Exception:
        os.remove(data.logo)
        db.rollback()
        raise

    background_tasks.add_task(send_brand_email, brand)

    return brand



@router.get("", response_model=Page[ResponseBrand], status_code=status.HTTP_200_OK)
def read_brand(filters : Annotated[BrandFilters, Query()] = None, db : Session = Depends(get_db)):
    brand = db.query(BrandModel).filter(BrandModel.deleted_at.is_(None))

    if filters.name:
        brand = brand.filter(BrandModel.name.like(f"%{filters.name}%"))

    if filters.email:
        brand = brand.filter(BrandModel.email.like(f"%{filters.email}%"))

    return paginate(db, brand, params=Params(size=20))



@router.put("/{id}", response_model=ResponseBrand, status_code=status.HTTP_200_OK)
def update_brand(id : int, data : CreateBrand = Depends(create_brand_form),  db : Session = Depends(get_db)):
    brand = db.query(BrandModel).filter(BrandModel.id == id, BrandModel.deleted_at.is_(None)).first()
    if not brand:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data not found"
        )

    file_path = brand.logo

    try:
        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(brand, key, value)

        db.commit()
        db.refresh(brand)

        os.remove(f"{file_path}")

        return brand
    
    except Exception:
        db.rollback()
        os.remove(data.logo)
        raise



@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_brand(id : int, db : Session = Depends(get_db)):
    brand = db.query(BrandModel).filter(BrandModel.id == id, BrandModel.deleted_at.is_(None)).first()
    if not brand:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data not found"
        )


    product_template = db.query(ProductTemplateModel).filter(ProductTemplateModel.brand_id == id, ProductTemplateModel.deleted_at.is_(None)).first()
    if product_template:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "In Product Template, Brand is exists"
        )
    

    suplier = db.query(SuplierModel).filter(SuplierModel.brand_id == id, SuplierModel.deleted_at.is_(None)).first()
    if suplier:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "In Suplier, Brand is exists"
        )
    
    
    try:
        file_path = brand.logo

        brand.deleted_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(brand)

        file_name = os.path.basename(f"{file_path}")

        os.makedirs(f"deleted_file/brand", exist_ok=True)
        destination = f"deleted_file/brand/{file_name}"

        shutil.move(f"{file_path}", destination)

        return {"status" : "Data successfuly delete"}
    
    except Exception:
        db.rollback()
        raise