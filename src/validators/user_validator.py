import os

from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import (
    status, 
    HTTPException, 
    Depends
)

from src.config.database import get_db
from src.models.user_model import UserModel
from src.schemas.user_schema import CreateUser, create_user_form


def validate_user(
    data : CreateUser = Depends(create_user_form), 
    db : Session = Depends(get_db)
):
    user = (
        db.query(UserModel)
        .filter(
            or_(
                UserModel.email == data.email, 
                UserModel.phone == data.phone
            ), 
            UserModel.deleted_at == None
        )
        .first()
    )
    
    if user:
        os.remove(f"{data.image}")

        if user.email == data.email:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "Email Already Exists"
            )
        if user.phone == data.phone:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "Phone Already Exists"
            )

    return data