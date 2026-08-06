import os
import shutil

from fastapi import UploadFile, File, Form
from pydantic import BaseModel


class CreateProductTemplate(BaseModel):
    name : str
    code : str
    category_name : str
    sub_category_name : str
    brand_name : str
    mrp : float
    tax : float
    description : str
    openstock : str
    image : str



def create_product_template_form(
    name : str = Form(...),
    code : str = Form(...),
    category_name : str = Form(...),
    sub_category_name : str = Form(...),
    brand_name : str = Form(...),
    mrp : float = Form(...),
    tax : float = Form(...),
    description : str = Form(...),
    openstock : str = Form(...),
    image : UploadFile = File(...)):

    os.makedirs("uploads/product_template", exist_ok=True)
    file_path = f"uploads/product_template/{image.filename}"

    with open(file_path, "wb") as file:
        shutil.copyfileobj(image.file, file)


    return CreateProductTemplate(
        name = name,
        code = code,
        category_name = category_name,
        sub_category_name = sub_category_name,
        brand_name = brand_name,
        mrp = mrp,
        tax = tax,
        description = description,
        openstock = openstock,
        image = file_path
    )



class ResponseProductTemplate(BaseModel):
    id : int
    name : str
    code : str
    category_id : int
    sub_category_id : int
    brand_id : int
    mrp : float
    tax : float
    description : str
    openstock : str
    image : str
