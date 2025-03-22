import uuid
from .base import Base

from sqlmodel import SQLModel, Field


class ProductCategoryBase(Base):
    name: str = Field(max_length=255)


class ProductCategory(ProductCategoryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class ProductCategoryPublic(ProductCategoryBase):
    id: uuid.UUID


class ProductCategoriesPublic(SQLModel):
    data: list[ProductCategoryPublic]
    count: int


class ProductCategoryCreateUpdate(SQLModel):
    name: str = Field(max_length=255)