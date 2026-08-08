import os
from typing import Annotated

from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import APIRouter, status, Depends, HTTPException, Query

from src.config.database import get_db
from src.models.user_model import UserModel
from src.filters.user_filters import UserFilters
from src.validators.user_validator import validate_user
from src.schemas.user_schema import CreateUser, ResponseUser, create_user_form


router = APIRouter()


@router.post("", response_model=ResponseUser, status_code=status.HTTP_201_CREATED)
def create_suplier(data : CreateUser = Depends(validate_user), db : Session = Depends(get_db)):
    if not data.password == data.confirm_password:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail = "Password not match"
        )

    user = UserModel(
        name = data.name,
        email = data.email,
        password = data.password,
        confirm_password = data.confirm_password,
        role = data.role,
        branch = data.branch,
        phone = data.phone,
        address = data.address,
        image = data.address,
        status = data.status
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    
    except Exception:
        os.remove(data.image)
        db.rollback()
        raise



@router.get("", response_model=Page[ResponseUser], status_code=status.HTTP_200_OK)
def read_suplier(filters : Annotated[UserFilters, Query()] = None, db : Session = Depends(get_db)):
    suplier = db.query(UserModel)

    if filters.name:
        suplier = suplier.filter(UserModel.name.like(f"%{filters.name}%"))

    if filters.phone:
        suplier = suplier.filter(UserModel.phone.like(f"%{filters.phone}%"))

    return paginate(db, suplier, params=Params(size=20))



@router.put("/{id}", response_model=ResponseUser, status_code=status.HTTP_200_OK)
def update_suplier(id : int, data : CreateUser = Depends(create_user_form), db : Session = Depends(get_db)):
    if not data.password == data.confirm_password:
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail = "Password not match"
        )

    user = db.query(UserModel).filter(UserModel.id == id).first()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )

    file_path = user.image
    os.remove(f"{file_path}")

    update_data = data.model_dump()
    for key,value in update_data.items():
        setattr(user, key, value)

    try:
        db.commit()
        db.refresh(user)

        return user
    
    except Exception:
        os.remove(data.image)
        db.rollback()
        raise



@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_suplier(id : int, db : Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )

    file_path = user.image
    os.remove(f"{file_path}")

    try:
        db.delete(user)
        db.commit()

        return {"stauts" : "Data successfuly deleted"}
    
    except Exception:
        db.rollback()
        raise