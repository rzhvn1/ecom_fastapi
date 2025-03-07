import uuid
from typing import Any

from sqlmodel import Session, select

from app.models.shop import ShopCategory, ShopCategoryCreateUpdate


def create_shop_category(*, session: Session, category_create: ShopCategoryCreateUpdate) -> ShopCategory:
    db_category = ShopCategory.model_validate(category_create)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)

    return db_category


def update_shop_category(*, session: Session, db_category: ShopCategory, category_update: ShopCategoryCreateUpdate) -> ShopCategory:
    category_data = category_update.model_dump(exclude_unset=True)
    db_category.sqlmodel_update(category_data)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)

    return db_category
