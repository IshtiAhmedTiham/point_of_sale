from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.config.database import Base


class ProductTemplateModel(Base):
    __tablename__ = "product_template"

    id = Column(Integer, nullable=False, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    sub_category_id = Column(Integer, ForeignKey("sub_categories.id"), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False)
    mrp = Column(Float, nullable=False)
    tax = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    openstock = Column(String, nullable=False)
    image = Column(String, nullable=False, unique=True)

    category = relationship("CategoryModel")
    sub_category = relationship("SubCategoryModel")
    brand = relationship("BrandModel")
