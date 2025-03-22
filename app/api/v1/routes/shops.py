import uuid
from fastapi import APIRouter, HTTPException, status
from typing import Any

from app.dependencies.db import SessionDep
from app.dependencies.user import CurrentUser
from app.models.shop import ShopCategoriesPublic, ShopCreate, ShopPublic, ShopUpdate, ShopsPublic
from app.crud import shop as shop_crud


router = APIRouter(tags=["shops"])

# shop category routes
@router.get("/shop-category", response_model=ShopCategoriesPublic)
async def read_shop_categories(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
	return shop_crud.get_shop_categories(session=session, skip=skip, limit=limit)


# shop routes
@router.get("/", response_model=ShopsPublic)
async def read_shops(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
     return shop_crud.get_shops(session=session, skip=skip, limit=limit)


@router.get("/{shop_id}", response_model=ShopPublic)
async def read_shop(session: SessionDep, shop_id: uuid.UUID) -> Any:
     shop = shop_crud.get_shop_by_id(session=session, id=shop_id)
     if not shop:
        raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Shop not found"
		)
     
     return shop


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


@router.put("/{shop_id}", response_model=ShopPublic)
async def update_shop(session: SessionDep, current_user: CurrentUser, shop_id: uuid.UUID, shop_in: ShopUpdate) -> Any:
    shop = shop_crud.get_shop_by_id(session=session, id=shop_id)
    if not shop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shop not found"
        )
    if shop_in.category_id:
        category = shop_crud.get_category_by_id(session=session, id=shop_in.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shop Category not found"
            )
    if not current_user.is_superuser and (shop.user_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough permissions")
    
    shop = shop_crud.update_shop(session=session, shop=shop, shop_in=shop_in)

    return shop
    
    