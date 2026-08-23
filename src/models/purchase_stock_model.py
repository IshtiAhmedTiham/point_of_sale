from sqlalchemy import (
    Column, 
    Integer, 
    Float,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship

from src.config.database import Base


class PurchaseStockModel(Base):
    __tablename__ = "purchase_stock_model"

    id = Column(Integer, nullable=False, primary_key=True, index=True)
    code = Column(String, nullable=False)
    purchase_order_id = Column(Integer, ForeignKey("purchase_order_model.id"), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    purchase_order = relationship(
        "PurchaseOrderModel",
        back_populates="purchase_stock"
    )