from fastapi import APIRouter

from src.controllers.api.v1 import (
    category_controller, 
    sub_category_controller, 
    brand_controller, 
    product_template_controller,
    customer_controller,
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
