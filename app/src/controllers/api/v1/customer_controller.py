import os
import shutil
from typing import Annotated,cast
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import (
    APIRouter, 
    status, 
    Depends, 
    Query, 
    HTTPException, 
    BackgroundTasks
)

from app.src.config.database import get_db, DbSession
from app.src.models.customer_model import CustomerModel
from app.src.filters.customer_filters import CustomerFilter
from app.src.validators.customer_validator import validators
from app.src.services.customer.create_email_service import send_customer_email
from app.src.services.customer.update_email_service import send_customer_email_for_update
from app.src.services.customer.delete_email_service import send_customer_email_for_delete
from app.src.utils.files import delete_file
from app.src.schemas.customer_schema import (
    CreateCustomer, 
    CustomerResponse, 
    create_customer_form
)


router = APIRouter()


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
     db : DbSession,
    background_task : BackgroundTasks, 
    data : CreateCustomer = Depends(validators)
):
    customer = CustomerModel(
        name = data.name,
        email = data.email,
        phone = data.phone,
        address = data.address,
        account_no = data.account_no,
        opening_balance = data.opening_balance,
        discount = data.discount,
        taxable = data.taxable,
        icon = data.icon,
        deleted_at = data.deleted_at
    )

    try:
        db.add(customer)
        db.commit()
        db.refresh(customer)

    except Exception:
        db.rollback()
        raise
    
    background_task.add_task(send_customer_email, customer)
    return customer



@router.get("/", response_model=Page[CustomerResponse], status_code=status.HTTP_200_OK)
def read_customer(
     db : DbSession,
    filters : Annotated[CustomerFilter, Query()] 
):
    customer = (
        db.query(CustomerModel)
        .filter(CustomerModel.deleted_at.is_(None))
    )

    if filters.name:
        customer = customer.filter(CustomerModel.name.like(f"%{filters.name}%"))

    if filters.email:
            customer = customer.filter(CustomerModel.email.like(f"%{filters.email}%"))

    if filters.phone:
            customer = customer.filter(CustomerModel.phone.like(f"%{filters.phone}%"))

    if filters.account_no:
            customer = customer.filter(CustomerModel.account_no.like(f"%{filters.account_no}%"))

    return paginate(db, customer, params=Params(size=20))



@router.put("/{id}", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
def update_customer(
     db : DbSession,
    background_task : BackgroundTasks, 
    id: int, 
    data : CreateCustomer = Depends(create_customer_form)
):
    customer = (
        db.query(CustomerModel)
        .filter(
            CustomerModel.id == id, 
            CustomerModel.deleted_at.is_(None)
        )
        .first()
    )

    if not customer:
        if data.icon and os.path.exists(data.icon):
            os.remove(data.icon)

        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data not found"
        )

    old_file_path = cast(str, customer.icon)
    new_file_path = cast(str, data.icon)

    try:
        update_data = data.model_dump(exclude={"icon"})
        for key,value in update_data.items():
            setattr(customer, key, value)

        if new_file_path:
            customer.icon = new_file_path
        
        db.commit()
        db.refresh(customer)
        
        if new_file_path and old_file_path and os.path.exists(old_file_path):
            os.remove(old_file_path)

    except Exception:
        db.rollback()
        os.remove(data.icon)
        raise

    background_task.add_task(send_customer_email_for_update, customer)
    return customer



@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_customer(
    db : DbSession,
    background_task : BackgroundTasks, 
    id : int
):
    customer = (
        db.query(CustomerModel)
        .filter(
            CustomerModel.id == id, 
            CustomerModel.deleted_at.is_(None)
        )
        .first()
    )
    if not customer:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data not found"
        )
    

    try:
        file_path = customer.icon

        customer.deleted_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(customer)

        delete_file(f"{file_path}", "customer")

    except Exception:
        db.rollback()
        raise

    background_task.add_task(send_customer_email_for_delete, customer)
    return {"status" : "Data successfuly deleted"}

