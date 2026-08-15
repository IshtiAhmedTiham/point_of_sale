import os

from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends

from src.config.database import get_db
from src.models.product_template_model import ProductTemplateModel
from src.schemas.product_template_schema import CreateProductTemplate, create_product_template_form


def validate_unique_code(data : CreateProductTemplate = Depends(create_product_template_form), db : Session = Depends(get_db)):
    is_code_exists = db.query(ProductTemplateModel).filter(ProductTemplateModel.code == data.code, ProductTemplateModel.deleted_at == None).first()

    if is_code_exists:
        file_path = data.image
        os.remove(f"{file_path}")

        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Code already exists"
        )

    return data

