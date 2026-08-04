from sqlalchemy import Column, Integer, String, ForeignKey
from src.config.database import Base
from sqlalchemy.orm import relationship

class SubCategoryModel(Base):
    __tablename__ = "sub_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    code = Column(String, nullable=False, index=True, unique=True)
    icon = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False, default="Active")

    category = relationship("CategoryModel")