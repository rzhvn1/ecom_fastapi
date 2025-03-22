import uuid
from typing import Any

from sqlmodel import Session, select, func

from app.dependencies.user import CurrentUser
from app.models.shop import Shop, ShopCategoriesPublic, ShopCategory, ShopCategoryCreateUpdate, ShopCreate, ShopPublic, ShopsPublic


def get_shop_categories(*, session: Session, skip: int, limit: int) -> ShopCategoriesPublic:
    count_statement = select(func.count()).select_from(ShopCategory)
    count = session.exec(statement=count_statement).one()

    statement = select(ShopCategory).offset(skip).limit(limit)
    shop_categories = session.exec(statement=statement)

    return ShopCategoriesPublic(data=shop_categories, count=count)


def get_category_by_id(*, session: Session, id: uuid.UUID) -> ShopCategory | None:
    statement = select(ShopCategory).where(ShopCategory.id == id)
    session_category = session.exec(statement=statement).first()
    return session_category


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


def get_shops(*, session: Session, skip: int, limit: int) -> ShopsPublic:
    count_statement = select(func.count()).select_from(Shop)
    count = session.exec(statement=count_statement).one()

    statement = select(Shop).offset(skip).limit(limit)
    shops = session.exec(statement=statement)

    return ShopsPublic(data=shops, count=count)


def create_shop(*, session: Session, current_user: CurrentUser, shop_create: ShopCreate) -> Shop:
    db_shop = Shop.model_validate(shop_create, update={"user_id": current_user.id})
    session.add(db_shop)
    session.commit()
    session.refresh(db_shop)
    return db_shop
