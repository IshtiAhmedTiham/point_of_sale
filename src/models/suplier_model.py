from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Float,ForeignKey, DateTime

from src.config.database import Base


class SuplierModel(Base):
    __tablename__ = "supliers"

    id = Column(Integer, nullable=False, primary_key=True, index=True)
    name = Column(String, nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    phone = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False)
    account_no = Column(String, nullable=False)
    opening_balance = Column(Float, nullable=False)
    image = Column(String, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    brand = relationship("BrandModel")
