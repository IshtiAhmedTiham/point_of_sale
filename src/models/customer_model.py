from sqlalchemy import Column, Integer, String, Float, DateTime

from src.config.database import Base


class CustomerModel(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False)
    account_no = Column(String, nullable=False)
    opening_balance = Column(Float, nullable=False)
    discount = Column(Float, nullable=False)
    taxable = Column(Float, nullable=False)
    icon = Column(String, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
