from fastapi import APIRouter
from src.controllers.api.v1 import category_controller, sub_category_controller

router = APIRouter()

router.include_router(category_controller.router, prefix="/category", tags=["Category"])
router.include_router(sub_category_controller.router, prefix="/subcategory", tags=["SubCategory"])