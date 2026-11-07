import os
from typing import Annotated, cast
from datetime import datetime, timezone

from sqlalchemy.orm import Session, selectinload
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import (
    APIRouter, 
    status, 
    Depends, 
    HTTPException, 
    Query, 
    BackgroundTasks
)

from app.src.config.database import get_db, DbSession
from app.src.models.brand_model import BrandModel
from app.src.models.suplier_model import SuplierModel
from app.src.filters.brand_filters import BrandFilters
from app.src.validators.brand_validator import validators
from app.src.models.product_template_model import ProductTemplateModel
from app.src.services.brand.create_email_service import send_brand_email
from app.src.services.brand.update_email_service import send_brand_email_for_update
from app.src.services.brand.delete_email_service import send_brand_email_for_delete
from app.src.utils.files import delete_file
from app.src.schemas.brand_schema import (
    CreateBrand, 
    ResponseBrand, 
    create_brand_form
)


router = APIRouter()


@router.post("/", response_model=ResponseBrand, status_code=status.HTTP_201_CREATED)
def create_brand(
    db : DbSession,
    background_tasks : BackgroundTasks, 
    data : CreateBrand = Depends(validators), 
):
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
        db.rollback()
        os.remove(data.logo)
        raise

    background_tasks.add_task(send_brand_email, brand)
    return brand



@router.get("/", response_model=Page[ResponseBrand], status_code=status.HTTP_200_OK)
def read_brand(
    db : DbSession,
    filters : Annotated[BrandFilters, Query()]
):
    brand = (
        db.query(BrandModel)
        .options(selectinload(BrandModel.supliers))
        .filter(BrandModel.deleted_at.is_(None))
    )

    if filters.name:
        brand = brand.filter(BrandModel.name.like(f"%{filters.name}%"))

    if filters.email:
        brand = brand.filter(BrandModel.email.like(f"%{filters.email}%"))

    return paginate(db, brand, params=Params(size=20))



@router.put("/{id}", response_model=ResponseBrand, status_code=status.HTTP_200_OK)
def update_brand(
    db : DbSession,
    background_tasks : BackgroundTasks, 
    id : int, 
    data : CreateBrand = Depends(create_brand_form)  
):
    brand = (
        db.query(BrandModel)
        .filter(
            BrandModel.id == id, 
            BrandModel.deleted_at.is_(None)
        )
        .first()
    )
    if not brand:
        if data.logo and os.path.exists(data.logo):
            os.remove(data.logo)

        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data not found"
        )

    old_logo = cast(str, brand.logo)
    new_logo = cast(str, data.logo)

    try:
        update_data = data.model_dump(exclude={"logo"})
        for key, value in update_data.items():
            setattr(brand, key, value)

        if new_logo:
            brand.logo = new_logo

        db.commit()
        db.refresh(brand)

        if old_logo and (old_logo != brand.logo):
            os.remove(old_logo)

    except Exception:
        db.rollback()
        os.remove(data.logo)
        raise

    background_tasks.add_task(send_brand_email_for_update, brand)
    return brand



@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_brand(
    db : DbSession,
    background_task : BackgroundTasks, 
    id : int 
):
    brand = (
        db.query(BrandModel)
        .filter(
            BrandModel.id == id, 
            BrandModel.deleted_at.is_(None)
        )
        .first()
    )
    if not brand:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data not found"
        )


    product_template = (
        db.query(ProductTemplateModel)
        .filter(
            ProductTemplateModel.brand_id == id, 
            ProductTemplateModel.deleted_at.is_(None)
        )
        .first()
    )
    if product_template:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "In Product Template, Brand is exists"
        )
    

    suplier = (
        db.query(SuplierModel)
        .filter(
            SuplierModel.brand_id == id, 
            SuplierModel.deleted_at.is_(None)
        )
        .first()
    )
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

        delete_file(f"{file_path}", "brand")

    except Exception:
        db.rollback()
        raise
    
    background_task.add_task(send_brand_email_for_delete, brand)
    return {"status" : "Data successfuly delete"}