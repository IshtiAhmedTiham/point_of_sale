from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.models.suplier_model import SuplierModel
from fastapi import status, Depends, HTTPException
from src.schemas.suplier_schema import CreateSuplier, create_suplier_form


def validate_suplier(data : CreateSuplier = Depends(create_suplier_form), db : Session = Depends(get_db)):
    suplier = db.query(SuplierModel).filter(or_(SuplierModel.phone == data.phone, SuplierModel.account_no == data.account_no)).first()

    if suplier:
        if suplier.phone == data.phone:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "Phone Already Exists"
            )
        if suplier.account_no == data.account_no:
            raise HTTPException(
                status_code = status.HTTP_409_CONFLICT,
                detail = "Accout Number Already Exists"
            )

    return data