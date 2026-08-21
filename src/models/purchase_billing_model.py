from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.config.database import Base


class PurchaseBillingModel(Base):
    __tablename__ = "purchase_billing_model"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    purchase_order_id = Column(Integer, ForeignKey("purchase_order_model.id"), nullable=False, unique=True)    
    total = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    net_total = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    pay = Column(Float, nullable=False)
    due = Column(Float, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    purchase_order = relationship(
        "PurchaseOrderModel",
        back_populates="purchase_billing"
    )
