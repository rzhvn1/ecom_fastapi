from fastapi import APIRouter, HTTPException, status
from typing import Any

from app.dependencies.db import SessionDep
from app.dependencies.user import CurrentUser
from app.models.shop import Shop, ShopCategoriesPublic, ShopCreate, ShopPublic
from app.crud import shop as shop_crud


router = APIRouter(tags=["shops"])


@router.get("/shop-category", response_model=ShopCategoriesPublic)
async def read_shop_categories(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
	return shop_crud.get_shop_categories(session=session, skip=skip, limit=limit)


@router.post("/", response_model=ShopPublic)
async def create_shop(session: SessionDep, current_user: CurrentUser, shop_in: ShopCreate) -> Any:
    category = shop_crud.get_category_by_id(session=session, id=shop_in.category_id)
    if not category:
        raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Shop Category not found"
		)
    
    shop = shop_crud.create_shop(session=session, current_user=current_user, shop_create=shop_in)

    return shop
    


