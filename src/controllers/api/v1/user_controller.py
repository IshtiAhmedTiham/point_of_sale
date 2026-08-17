import os
import shutil
from typing import Annotated
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

from src.config.database import get_db
from src.models.user_model import UserModel
from src.filters.user_filters import UserFilters
from src.validators.user_validator import validate_user
from src.services.user.create_email_service import send_user_email
from src.services.user.update_email_service import send_user_email_for_update
from src.services.user.delete_email_service import send_user_email_for_delete
from src.schemas.user_schema import (
    CreateUser, 
    ResponseUser, 
    create_user_form
)


router = APIRouter()


@router.post("", response_model=ResponseUser, status_code=status.HTTP_201_CREATED)
def create_user(
    background_task:BackgroundTasks, 
    data : CreateUser = Depends(validate_user), 
    db : Session = Depends(get_db)
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



@router.get("", response_model=Page[ResponseUser], status_code=status.HTTP_200_OK)
def read_user(
    filters : Annotated[UserFilters, Query()] = None, 
    db : Session = Depends(get_db)
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
    background_task : BackgroundTasks, 
    id : int, 
    data : CreateUser = Depends(create_user_form), 
    db : Session = Depends(get_db)
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

    old_file_path = user.image

    try:
        updated_data = data.model_dump(exclude={"image"})
        for key, value in updated_data.items():
            setattr(user, key, value)

        user.updated_at = datetime.now(timezone.utc)
        user.image = data.image

        db.commit()
        db.refresh(user)

        if (
            data.image and 
            old_file_path != data.image and 
            os.path.exists(old_file_path)
        ):
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
    background_task : BackgroundTasks, 
    id: int, 
    db: Session = Depends(get_db)
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
            filename = os.path.basename(file_path)

            os.makedirs("deleted_file/user", exist_ok=True)

            destination = os.path.join("deleted_file/user", filename)
            shutil.move(f"{file_path}", destination)

    except Exception:
        db.rollback()
        raise

    background_task.add_task(send_user_email_for_delete, user)
    return {"status": "Data successfully deleted"}