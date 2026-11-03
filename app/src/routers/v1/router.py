from fastapi import APIRouter

from app.src.controllers.api.v1 import (
    brand_controller, 
    category_controller, 
    customer_controller, 
    product_template_controller, 
    purchase_controller, 
    sub_category_controller, 
    suplier_controller,
    user_controller
    )


router = APIRouter()


router.include_router(category_controller.router, prefix="/category", tags=["Category"])
router.include_router(sub_category_controller.router, prefix="/subcategory", tags=["SubCategory"])
router.include_router(brand_controller.router, prefix="/brand", tags=["Brand"])
router.include_router(product_template_controller.router, prefix="/product_template", tags=["Product Template"])
router.include_router(customer_controller.router, prefix="/customer", tags=["Customer"])
router.include_router(suplier_controller.router, prefix="/suplier", tags=["Suplier"])
router.include_router(user_controller.router, prefix="/user", tags=["User"])
router.include_router(purchase_controller.router, prefix="/purchase", tags=["Purchase"])
