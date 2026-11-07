import os
import shutil
from typing import Annotated, cast
from datetime import datetime, timezone

from sqlalchemy.orm import Session
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
from app.src.models.user_model import UserModel
from app.src.filters.user_filters import UserFilters
from app.src.validators.user_validator import validate_user
from app.src.services.user.create_email_service import send_user_email
from app.src.services.user.update_email_service import send_user_email_for_update
from app.src.services.user.delete_email_service import send_user_email_for_delete
from app.src.utils.files import delete_file
from app.src.schemas.user_schema import (
    CreateUser, 
    ResponseUser, 
    create_user_form
)


router = APIRouter()


@router.post("/", response_model=ResponseUser, status_code=status.HTTP_201_CREATED)
def create_user(
    db : DbSession,
    background_task:BackgroundTasks, 
    data : CreateUser = Depends(validate_user)
):
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
        status = data.status,
        deleted_at = data.deleted_at
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    
    except Exception:
        os.remove(data.image)
        db.rollback()
        raise

    background_task.add_task(send_user_email, user)
    return user



@router.get("/", response_model=Page[ResponseUser], status_code=status.HTTP_200_OK)
def read_user(
    db : DbSession,
    filters : Annotated[UserFilters, Query()]
):
    suplier = (
        db.query(UserModel)
        .filter(UserModel.deleted_at.is_(None))
    )

    if filters.name:
        suplier = suplier.filter(UserModel.name.like(f"%{filters.name}%"))

    if filters.phone:
        suplier = suplier.filter(UserModel.phone.like(f"%{filters.phone}%"))

    return paginate(db, suplier, params=Params(size=20))



@router.put("/{id}", response_model=ResponseUser, status_code=status.HTTP_200_OK)
def update_user(
    db : DbSession,
    background_task : BackgroundTasks, 
    id : int, 
    data : CreateUser = Depends(create_user_form)
):
    if data.password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Password not match"
        )

    user = (
        db.query(UserModel)
        .filter(
            UserModel.id == id, 
            UserModel.deleted_at.is_(None)
        )
        .first()
    )
    if not user:
        if data.image and os.path.exists(data.image):
            os.remove(data.image)

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    old_file_path = cast(str, user.image)
    new_file_path = cast(str, data.image)

    try:
        updated_data = data.model_dump(exclude={"image"})
        for key, value in updated_data.items():
            setattr(user, key, value)

        user.updated_at = datetime.now(timezone.utc)

        if new_file_path:
            user.image = new_file_path

        db.commit()
        db.refresh(user)

        if (data.image and old_file_path != data.image and os.path.exists(old_file_path)):
            os.remove(old_file_path)

    except Exception:
        db.rollback()

        if data.image and os.path.exists(data.image):
            os.remove(data.image)

        raise

    background_task.add_task(send_user_email_for_update, user)
    return user
    
    


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_user(
    db : DbSession,
    background_task : BackgroundTasks, 
    id: int
):
    user = (
        db.query(UserModel)
        .filter(
            UserModel.id == id, 
            UserModel.deleted_at.is_(None)
        )
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    try:
        file_path = user.image

        user.deleted_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(user)

        if file_path and os.path.exists(file_path):
            delete_file(f"{file_path}", "user")


    except Exception:
        db.rollback()
        raise

    background_task.add_task(send_user_email_for_delete, user)
    return {"status": "Data successfully deleted"}