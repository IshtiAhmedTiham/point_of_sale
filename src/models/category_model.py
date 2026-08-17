from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    DateTime
)

from src.config.database import Base

class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    icon = Column(String, nullable=False, unique=True)
    status = Column(String, nullable=False, default="Active")
    deleted_at = Column(DateTime, nullable=True)
