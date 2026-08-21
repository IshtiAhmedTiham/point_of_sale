from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.config.database import Base

class PurchaseStockModel(Base):
    __tablename__ = "purchase_stock_model"

    id = Column(Integer, nullable=False, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey("purchase_order_model.id"))
    code = Column(String, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    purchase_order = relationship(
        "PurchaseOrderModel",
        back_populates="purchase_stocks"
    )