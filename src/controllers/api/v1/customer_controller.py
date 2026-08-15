import os
import shutil
from typing import Annotated
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import APIRouter, status, Depends, Query, HTTPException

from src.config.database import get_db
from src.models.customer_model import CustomerModel
from src.filters.customer_filters import CustomerFilter
from src.validators.customer_validator import validators
from src.schemas.customer_schema import CreateCustomer, CustomerResponse, create_customer_form


router = APIRouter()


@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(data : CreateCustomer = Depends(validators), db : Session = Depends(get_db)):
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

        return customer

    except Exception:
        db.rollback()
        raise



@router.get("", response_model=Page[CustomerResponse], status_code=status.HTTP_200_OK)
def read_customer(filters : Annotated[CustomerFilter, Query()] = None, db : Session = Depends(get_db)):
    customer = db.query(CustomerModel).filter(CustomerModel.deleted_at.is_(None))

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
def update_customer(id: int, data : CreateCustomer = Depends(create_customer_form), db : Session = Depends(get_db)):
    customer = db.query(CustomerModel).filter(CustomerModel.id == id, CustomerModel.deleted_at.is_(None)).first()

    file_path = data.icon

    if not customer:
        os.remove(f"{file_path}")

        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data not found"
        )

    old_file_path = customer.icon

    try:
        update_data = data.model_dump()
        for key,value in update_data.items():
            setattr(customer, key, value)

        db.commit()
        db.refresh(customer)
        
        os.remove(f"{old_file_path}")

        return customer

    except Exception:
        db.rollback()
        os.remove(data.icon)
        raise



@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_customer(id : int, db : Session = Depends(get_db)):
    customer = db.query(CustomerModel).filter(CustomerModel.id == id, CustomerModel.deleted_at.is_(None)).first()
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

        file = os.path.basename(f"{file_path}")

        os.makedirs("deleted_file/customer", exist_ok=True)
        destination = f"deleted_file/customer/{file}"
        
        shutil.move(f"{file_path}", destination)

        return {"status" : "Data successfuly deleted"}

    except Exception:
        db.rollback()
        raise

