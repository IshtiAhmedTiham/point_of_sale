import os

from sqlalchemy import or_
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends

from src.config.database import get_db
from src.models.customer_model import CustomerModel
from src.schemas.customer_schema import CreateCustomer, create_customer_form


def validators(data : CreateCustomer = Depends(create_customer_form), db : Session = Depends(get_db)):
    existing_data = db.query(CustomerModel).filter(or_(CustomerModel.email == data.email, CustomerModel.phone == data.phone, CustomerModel.account_no == data.account_no,), CustomerModel.deleted_at == None).first()

    if existing_data:
        file_path = data.icon
        os.remove(f"{file_path}")

        if existing_data.email:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "Email already exists"
            )
        
        if existing_data.phone:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "Phone already exists"
            )
        if existing_data.account_no:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "Account Number already exists"
            )
        
    return data

