import uuid
from typing import Any

from sqlmodel import Session, select, func

from app.dependencies.user import CurrentUser
from app.models.product import ProductCategoriesPublic, ProductCategory, ProductCategoryCreateUpdate


def get_product_categories(*, session: Session, skip: int, limit: int) -> ProductCategoriesPublic:
    count_statement = select(func.count()).select_from(ProductCategory)
    count = session.exec(statement=count_statement).one()

    statement = select(ProductCategory).offset(skip).limit(limit)
    product_categories = session.exec(statement=statement)

    return ProductCategoriesPublic(data=product_categories, count=count)


def get_category_by_id(*, session: Session, id: uuid.UUID) -> ProductCategory | None:
    statement = select(ProductCategory).where(ProductCategory.id == id)
    session_category = session.exec(statement=statement).first()
    return session_category


def create_product_category(*, session: Session, category_create: ProductCategoryCreateUpdate) -> ProductCategory:
    db_category = ProductCategory.model_validate(category_create)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)

    return db_category


def update_product_category(*, session: Session, db_category: ProductCategory, category_update: ProductCategoryCreateUpdate) -> ProductCategory:
    category_data = category_update.model_dump(exclude_unset=True)
    db_category.sqlmodel_update(category_data)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)

    return db_category