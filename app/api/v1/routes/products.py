from typing import Any
from fastapi import APIRouter

from app.dependencies.db import SessionDep
from app.models.product import ProductCategoriesPublic
from app.crud import product as product_crud


router = APIRouter(tags=["products"])

# shop category routes
@router.get("/shop-category", response_model=ProductCategoriesPublic)
async def read_shop_categories(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
	return product_crud.get_product_categories(session=session, skip=skip, limit=limit)
