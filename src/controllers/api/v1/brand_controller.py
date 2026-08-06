from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate

from src.schemas.brand_schema import CreateBrand, ResponseBrand, create_brand_form
from src.config.database import get_db
from src.models.brand_model import BrandModel
from src.validators.brand_validator import validate_unique_email_and_phone
from src.filters.brand_filters import BrandFilters


router = APIRouter()


@router.post("", response_model=ResponseBrand, status_code=status.HTTP_201_CREATED)
def create_brand(data : CreateBrand = Depends(validate_unique_email_and_phone), db : Session = Depends(get_db)):
    brand = BrandModel(
        name = data.name,
        email = data.email,
        phone = data.phone,
        address = data.address,
        logo = data.logo,
        status = data.status
    )

    try:
        db.add(brand)
        db.commit()
        db.refresh(brand)

        return brand
    
    except Exception:
        db.rollback()
        raise



@router.get("", response_model=Page[ResponseBrand], status_code=status.HTTP_200_OK)
def read_brand(filters : Annotated[BrandFilters, Query()] = None, db : Session = Depends(get_db)):
    brand = db.query(BrandModel)

    if filters.name:
        brand = brand.filter(BrandModel.name.like(f"%{filters.name}%"))

    if filters.email:
        brand = brand.filter(BrandModel.email.like(f"%{filters.email}%"))

    return paginate(db, brand, params=Params(size=20))



@router.put("/{id}", response_model=ResponseBrand, status_code=status.HTTP_200_OK)
def update_brand(id : int, data : CreateBrand = Depends(create_brand_form),  db : Session = Depends(get_db)):
    brand = db.query(BrandModel).filter(BrandModel.id == id).first()

    if not brand:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data not found"
        )

    update_data = data.model_dump()
    for key, value in update_data.items():
        setattr(brand, key, value)

    try:
        db.commit()
        db.refresh(brand)

        return brand
    
    except Exception:
        db.rollback()
        raise



@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_brand(id : int, db : Session = Depends(get_db)):
    brand = db.query(BrandModel).filter(BrandModel.id == id).first()

    if not brand:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data not found"
        )

    try:
        db.delete(brand)
        db.commit()
        db.refresh(brand)

        return {"status" : "Data successfuly delete"}
    
    except Exception:
        db.rollback()
        raise