from fastapi import APIRouter, status, Depends, Query, HTTPException
from src.schemas.customer_schema import CreateCustomer, CustomerResponse, create_customer_form
from src.models.customer_model import CustomerModel
from src.config.database import get_db
from sqlalchemy.orm import Session
from src.validators.customer_validator import validators
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from typing import Annotated
from src.filters.customer_filters import CustomerFilter

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
        icon = data.icon
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
    customer = db.query(CustomerModel)

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
def update_customer(id: int, data : CreateCustomer = Depends(validators), db : Session = Depends(get_db)):
    customer = db.query(CustomerModel).filter(CustomerModel.id == id).first()

    if not customer:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data not found"
        )

    update_data = data.model_dump()
    for key,value in update_data.items():
        setattr(customer, key, value)

    try:
        db.commit()
        db.refresh(customer)
        
        return customer

    except Exception:
        db.rollback()
        raise



@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_customer(id : int, db : Session = Depends(get_db)):
    customer = db.query(CustomerModel).filter(CustomerModel.id == id).first()

    if not customer:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Data not found"
        )

    try:
        db.delete(customer)
        db.commit()

        return {"status" : "Data successfuly deleted"}

    except Exception:
        db.rollback()
        raise

