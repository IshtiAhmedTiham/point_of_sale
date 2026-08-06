from fastapi import status, HTTPException, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.schemas.brand_schema import CreateBrand, create_brand_form
from src.config.database import get_db
from src.models.brand_model import BrandModel


def validate_unique_email_and_phone(data : CreateBrand = Depends(create_brand_form), db : Session = Depends(get_db)):
    existing_brand = db.query(BrandModel).filter(or_(BrandModel.email == data.email , BrandModel.phone == data.phone)).first()

    if existing_brand:
        if existing_brand.email == data.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )

        if existing_brand.phone == data.phone:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Phone already exists"
            )


    return data
