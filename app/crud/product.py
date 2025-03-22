import uuid
from typing import Any

from sqlmodel import Session, select, func

from app.dependencies.user import CurrentUser
from app.models.product import ProductCategory, ProductCategoryCreateUpdate


def create_product_category(*, session: Session, category_create: ProductCategoryCreateUpdate) -> ProductCategory:
    db_category = ProductCategory.model_validate(category_create)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)

    return db_category