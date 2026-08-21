from random import randint
from datetime import datetime, timezone

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate

from src.config.database import get_db
from src.models.purchase_billing_model import PurchaseBillingModel
from src.models.purchase_order_model import PurchaseOrderModel
from src.models.purchase_stock_model import PurchaseStockModel
from src.models.suplier_model import SuplierModel
from src.models.product_template_model import ProductTemplateModel
from src.models.brand_model import BrandModel
from src.schemas.purchase_schema import (
    CreatePurchase, 
    ResponsePurchase, 
    create_purchase_form
)


router = APIRouter()


@router.post("", response_model=ResponsePurchase, status_code=status.HTTP_201_CREATED)
def create_purchase(
    data : CreatePurchase = Depends(create_purchase_form), 
    db : Session = Depends(get_db)
):
    suplier = (
        db.query(SuplierModel)
        .filter(
            SuplierModel.name == data.supplier_name, 
            SuplierModel.deleted_at.is_(None)
        )
        .first()
    )

    if not suplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="suplier not found"
        )


    product = (
        db.query(ProductTemplateModel)
        .filter(
            ProductTemplateModel.name == data.product_name,
            ProductTemplateModel.deleted_at.is_(None)
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="product not found"
        )


    brand = (
        db.query(BrandModel)
        .filter(
            BrandModel.name == data.brand_name,
            BrandModel.deleted_at.is_(None)
        )
        .first()
    )

    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="brand not found"
        )


    purchase_order = PurchaseOrderModel(
        date = data.date,
        suplier_id = suplier.id,
        product_id = product.id,
        unit_cost = data.unit_cost,
        quantity = data.quantity,
        tax = data.tax,
        sub_total = data.sub_total,
        brand_id = brand.id
    )


    quantity = data.quantity

    for i in range(quantity):
        stock = PurchaseStockModel(
            code = str(randint(1, 1000))
        )

        purchase_order.purchase_stocks.append(stock)



    purchase_billing = PurchaseBillingModel(
        total = data.total,
        discount = data.discount,
        net_total = data.net_total,
        payment_method = data.payment_method,
        pay = data.pay,
        due = data.due
    )

    purchase_order.purchase_billing = purchase_billing

    try:
        db.add(purchase_order)
        db.commit()
        db.refresh(purchase_order)
        db.refresh(purchase_billing)

        return purchase_order
    
    except Exception:
        db.rollback()
        raise



@router.get("", response_model=Page[ResponsePurchase], status_code=status.HTTP_200_OK)
def read_purchase(db : Session = Depends(get_db)):  

    purchase = (
        db.query(PurchaseOrderModel)
        .filter(PurchaseOrderModel.deleted_at.is_(None))
    )

    return paginate(db, purchase, params=Params(size=20))



@router.put("/{id}", response_model=ResponsePurchase, status_code=status.HTTP_200_OK)
def update_purchase(
    id : int,
    data : CreatePurchase = Depends(create_purchase_form),
    db : Session = Depends(get_db)
):  
    purchase = (
        db.query(PurchaseOrderModel)
        .filter(
            PurchaseOrderModel.id == id,
            PurchaseOrderModel.deleted_at.is_(None)
        )
        .first()
    )

    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="purchase not found"
        )


    suplier = (
        db.query(SuplierModel)
        .filter(
            SuplierModel.name == data.supplier_name, 
            SuplierModel.deleted_at.is_(None)
        )
        .first()
    )

    if not suplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="suplier not found"
        )
    

    product = (
        db.query(ProductTemplateModel)
        .filter(
            ProductTemplateModel.name == data.product_name,
            ProductTemplateModel.deleted_at.is_(None)
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="product not found"
        )


    brand = (
        db.query(BrandModel)
        .filter(
            BrandModel.name == data.brand_name,
            BrandModel.deleted_at.is_(None)
        )
        .first()
    )

    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="brand not found"
        )


    purchase_data = data.model_dump(
        exclude={ 
            "supplier_name",
            "product_name",
            "brand_name",
            "total",
            "net_total",
            "payment_method",
            "pay",
            "due"
        }
    )

    purchase_data.update(
        {
            "suplier_id": suplier.id,
            "product_id": product.id,
            "brand_id": brand.id
        }
    )

    for key,value in purchase_data.items():
        setattr(purchase, key, value)



    billing = purchase.purchase_billing

    if not billing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bills not found"
        )


    billing_data = data.model_dump(
        include={ 
            "total",
            "discount",
            "net_total",
            "payment_method",
            "pay",
            "due"
        }
    )

    for key,value in billing_data.items():
        setattr(billing, key, value)



    purchase.purchase_stocks.clear()

    quantity = data.quantity

    for i in range(quantity):
        code = randint(1,1000)

        stock = PurchaseStockModel(
            code = str(code)
        )
 
        purchase.purchase_stocks.append(stock)

    try:
        db.commit()
        db.refresh(purchase)

        return purchase
    
    except Exception:
        db.rollback()
        raise



@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_purchase(
    id : int, 
    db : Session = Depends(get_db)
):
    purchase = (
        db.query(PurchaseOrderModel)
        .filter(
            PurchaseOrderModel.id == id, 
            PurchaseOrderModel.deleted_at.is_(None)
        )
        .first()
    )
    
    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Purchase not found"
        )

    try:
        now = datetime.now(timezone.utc)

        purchase.deleted_at = now

        if purchase.purchase_billing:
            purchase.purchase_billing.deleted_at = now

        for stock in purchase.purchase_stocks:
            stock.deleted_at = now

        db.commit()
        db.refresh(purchase)

        return {"status" : "Data successfully deleted"}
    
    except Exception:
        db.rollback()
        raise