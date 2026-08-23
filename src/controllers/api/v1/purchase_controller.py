from random import randint
from datetime import datetime, timezone

from sqlalchemy.orm import Session
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi import (
    APIRouter, 
    status, 
    Depends,
    HTTPException
)

from src.models.purchase_order_model import PurchaseOrderModel
from src.models.purchase_billing_model import PurchaseBillingModel
from src.models.purchase_stock_model import PurchaseStockModel
from src.models.suplier_model import SuplierModel
from src.models.product_template_model import ProductTemplateModel
from src.models.brand_model import BrandModel
from src.config.database import get_db
from src.schemas.purchase_shema import (
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
            SuplierModel.name == data.suplier_name,
            SuplierModel.deleted_at.is_(None)
        )
        .first()
    )

    if not suplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Suplier data not found"
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
            detail="Product data not found"
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
            detail="Brand data not found"
        )    

    
    
    purchase = PurchaseOrderModel(
        date = data.date,
        suplier_id = suplier.id,
        product_id = product.id,
        unit_cost = data.unit_cost,
        quantity = data.quantity,
        tax = data.tax,
        sub_total = data.sub_total,
        brand_id = brand.id
    )


    billing = PurchaseBillingModel(
        total = data.total,
        discount = data.discount,
        net_total = data.net_total,
        payment_method = data.payment_method,
        pay = data.pay,
        due = data.due
    )

    purchase.purchase_billing = billing


    quantity = data.quantity

    for i in range(quantity):
        code = str(randint(1,1000))

        stock = PurchaseStockModel(code=code)

        purchase.purchase_stock.append(stock)


    try:
        db.add(purchase)
        db.commit()
        db.refresh(purchase)

        return purchase

    except Exception:
        db.rollback()
        raise


@router.get("", response_model=Page[ResponsePurchase], status_code=status.HTTP_200_OK)
def read_purchase(db : Session = Depends(get_db)):
    purchase = (
        db.query(PurchaseOrderModel)
        .filter(PurchaseOrderModel.deleted_at.is_(None))
    )

    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not found"
        )

    return paginate(db, purchase, params=Params(size=20))


@router.put("/{id}", response_model=ResponsePurchase, status_code=status.HTTP_200_OK)
def update_purchase(
    id : int,
    data : CreatePurchase = Depends(create_purchase_form),
    db : Session = Depends(get_db)
):
    suplier = (
        db.query(SuplierModel)
        .filter(
            SuplierModel.name == data.suplier_name,
            SuplierModel.deleted_at.is_(None)
        )
        .first()
    )

    if not suplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Suplier data not found"
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
            detail="Product data not found"
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
            detail="Brand data not found"
        ) 


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
            detail="Brand data not found"
        ) 

    updated_data = data.model_dump(
        exclude={
            "suplier_name",
            "product_name",
            "brand_name",
            "total",
            "discount",
            "net_total",
            "payment_method",
            "pay",
            "due"
        }
    )

    for key,value in updated_data.items():
        setattr(purchase, key, value)

    purchase.suplier_id = suplier.id
    purchase.product_id = product.id
    purchase.brand_id = brand.id


    billing = purchase.purchase_billing
    updated_data = data.model_dump(
        include={
            "total",
            "discount",
            "net_total",
            "payment_method",
            "pay",
            "due"
        }
    )

    for key,value in updated_data.items():
        setattr(billing, key, value)

    purchase.purchase_billing = billing


    quantity = data.quantity
    purchase.purchase_stock.clear()

    for i in range(quantity):
        code = str(randint(1,1000))
        stock = PurchaseStockModel(code=code)

        purchase.purchase_stock.append(stock)


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
            detail="Data not found"
        )


    purchase.deleted_at = datetime.now(timezone.utc)
    purchase.purchase_billing.deleted_at = datetime.now(timezone.utc)

    stocks = purchase.purchase_stock
    for i in stocks:
        i.deleted_at = datetime.now(timezone.utc)

    try:
        db.commit()
        db.refresh(purchase)

        return {"status" : "Data successfully deleted"}

    except Exception:
        db.rollback()
        raise