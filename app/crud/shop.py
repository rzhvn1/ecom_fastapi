import uuid
from typing import Any

from sqlmodel import Session, select

from app.models.shop import ShopCategory, ShopCategoryCreateUpdate


def create_shop_category(*, session: Session, shop_category_create: ShopCategoryCreateUpdate) -> ShopCategory:
    db_shop_category = ShopCategory.model_validate(shop_category_create)
    session.add(db_shop_category)
    session.commit()
    session.refresh(db_shop_category)

    return db_shop_category