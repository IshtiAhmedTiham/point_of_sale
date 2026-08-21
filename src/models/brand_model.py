from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime
)

from src.config.database import Base


class BrandModel(Base):
    __tablename__ = "brands"

    id = Column(Integer, nullable=False ,primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False)
    logo = Column(String, nullable=False,)
    status = Column(String, nullable=False, default="Active")
    deleted_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    supliers = relationship(
        "SuplierModel",
        back_populates="brands",
        cascade="all, delete-orphan"
    )