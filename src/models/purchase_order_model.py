from datetime import datetime, timezone

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey

from src.config.database import Base

class PurchaseOrderModel(Base):
    __tablename__ = "purchase_order_model"

    id = Column(Integer, nullable=False, primary_key=True, index=True)
    date = Column(DateTime, nullable=True, default=datetime.now(timezone.utc))
    suplier_id = Column(Integer, ForeignKey("supliers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product_template.id"), nullable=False)
    unit_cost = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    tax = Column(Float, nullable=False)
    sub_total = Column(Float, nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    deleted_at = Column(DateTime, nullable=True, default=None)

    suplier = relationship("SuplierModel")
    product = relationship("ProductTemplateModel")
    brand = relationship("BrandModel")

    purchase_billing = relationship(
        "PurchaseBillingModel",
        back_populates="purchase_order",
        cascade="all, delete-orphan",
        uselist=False
    )
    

    purchase_stocks = relationship(
        "PurchaseStockModel",
        back_populates="purchase_order",
        cascade="all, delete-orphan"
    )   