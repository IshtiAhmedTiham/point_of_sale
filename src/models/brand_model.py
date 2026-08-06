from sqlalchemy import Column, Integer, String

from src.config.database import Base


class BrandModel(Base):
    __tablename__ = "brands"

    id = Column(Integer, nullable=False ,primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=False, unique=True, index=True)
    address = Column(String, nullable=False)
    logo = Column(String, nullable=False)
    status = Column(String, nullable=False, default="Active")
