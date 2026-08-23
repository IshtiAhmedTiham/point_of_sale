from datetime import datetime, timezone

from sqlalchemy import (
    Column, 
    Integer, 
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship

from src.config.database import Base


class PurchaseOrderModel(Base):
    __tablename__ = "purchase_order_model"

    id = Column(Integer, nullable=False, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    suplier_id = Column(Integer, ForeignKey("supliers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product_template.id"), nullable=False)
    unit_cost = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    tax = Column(Float, nullable=False)
    sub_total = Column(Float, nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    suplier = relationship("SuplierModel")
    product_tamplate = relationship("ProductTemplateModel")
    brand = relationship("BrandModel")

    purchase_billing = relationship(
        "PurchaseBillingModel",
        back_populates="purchase_order",
        cascade="all, delete-orphan",
        uselist=False
    )

    purchase_stock = relationship(
        "PurchaseStockModel",
        back_populates="purchase_order",
        cascade="all, delete-orphan"
    )

