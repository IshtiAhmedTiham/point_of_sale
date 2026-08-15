import os

from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends

from src.config.database import get_db
from src.models.brand_model import BrandModel
from src.schemas.brand_schema import CreateBrand, create_brand_form


def validators(data : CreateBrand = Depends(create_brand_form), db : Session = Depends(get_db)):
    existing_brand = db.query(BrandModel).filter(or_(BrandModel.email == data.email , BrandModel.phone == data.phone), BrandModel.deleted_at == None).first()

    if existing_brand:
        file_path = data.logo
        os.remove(f"{file_path}")

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
