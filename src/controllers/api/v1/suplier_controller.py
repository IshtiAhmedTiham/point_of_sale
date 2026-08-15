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
from src.models.suplier_model import SuplierModel
from src.filters.suplier_filters import SuplierFilters
from src.validators.suplier_validator import validate_suplier
from src.schemas.suplier_schema import CreateSuplier, ResponseSuplier, create_suplier_form


router = APIRouter()


@router.post("", response_model=ResponseSuplier, status_code=status.HTTP_201_CREATED)
def create_suplier(data : CreateSuplier = Depends(validate_suplier), db : Session = Depends(get_db)):
    brand = db.query(BrandModel).filter(BrandModel.name == data.brand_name, BrandModel.deleted_at.is_(None)).first()

    if not brand:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Brand not found"
        )

    suplier = SuplierModel(
        name = data.name,
        brand_id = brand.id,
        phone = data.phone,
        address = data.address,
        account_no = data.account_no,
        opening_balance = data.opening_balance,
        image = data.image,
        deleted_at = data.deleted_at
    )

    try:
        db.add(suplier)
        db.commit()
        db.refresh(suplier)

        return suplier
    
    except Exception:
        os.remove(data.image)
        db.rollback()
        raise



@router.get("", response_model=Page[ResponseSuplier], status_code=status.HTTP_200_OK)
def read_suplier(filters : Annotated[SuplierFilters, Query()] = None, db : Session = Depends(get_db)):
    suplier = db.query(SuplierModel).filter(SuplierModel.deleted_at.is_(None))

    if filters.name:
        suplier = suplier.filter(SuplierModel.name.like(f"%{filters.name}%"))

    if filters.phone:
        suplier = suplier.filter(SuplierModel.phone.like(f"%{filters.phone}%"))

    return paginate(db, suplier, params=Params(size=20))



@router.put("/{id}", response_model=ResponseSuplier, status_code=status.HTTP_200_OK)
def update_suplier(id : int, data : CreateSuplier = Depends(create_suplier_form), db : Session = Depends(get_db)):
    suplier = db.query(SuplierModel).filter(SuplierModel.id == id, SuplierModel.deleted_at.is_(None)).first()

    if not suplier:
        file_path = data.image
        os.remove(f"{file_path}")

        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Suplier not found"
        )
    

    brand = db.query(BrandModel).filter(BrandModel.name == data.brand_name, BrandModel.deleted_at.is_(None)).first()
    if not brand:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Brand not found"
        )

    old_file_path = suplier.image

    try:
        update_data = data.model_dump(exclude={"brand_name"})
        for key,value in update_data.items():
            setattr(suplier, key, value)

        suplier.brand_id = brand.id
        
        db.commit()
        db.refresh(suplier)

        os.remove(f"{old_file_path}")

        return suplier
    
    except Exception:
        db.rollback()
        os.remove(data.image)
        raise



@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_suplier(id : int, db : Session = Depends(get_db)):
    suplier = db.query(SuplierModel).filter(SuplierModel.id == id, SuplierModel.deleted_at.is_(None)).first()
    if not suplier:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Suplier not found"
        )


    try:
        file_path = suplier.image

        suplier.deleted_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(suplier)

        file = os.path.basename(f"{file_path}")

        os.makedirs("deleted_file/suplier", exist_ok=True)
        destination = f"deleted_file/suplier/{file}"

        shutil.move(f"{file_path}", destination)

        return {"stauts" : "Data successfuly deleted"}
    
    except Exception:
        db.rollback()
        raise