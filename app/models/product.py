import uuid
from .base import Base

from sqlmodel import Relationship, SQLModel, Field


class ProductBase(Base):
    title: str = Field(max_length=255, nullable=False)
    description: str | None = None
    quantity: int = Field(default=0, nullable=False)
    image: str | None = Field(default=None, max_length=2083)


class Product(ProductBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    shop_id: uuid.UUID = Field(foreign_key="shop.id", nullable=False)
    category_id: uuid.UUID = Field(foreign_key="productcategory.id", nullable=False)

    shop: "Shop" = Relationship(back_populates="products")  # type: ignore
    category: "ProductCategory" = Relationship(back_populates="products")


class ProductCategoryBase(Base):
    name: str = Field(max_length=255)


class ProductCategory(ProductCategoryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    products: list[Product] = Relationship(back_populates="category")


class ProductCategoryPublic(ProductCategoryBase):
    id: uuid.UUID


class ProductCategoriesPublic(SQLModel):
    data: list[ProductCategoryPublic]
    count: int


class ProductCategoryCreateUpdate(SQLModel):
    name: str = Field(max_length=255)