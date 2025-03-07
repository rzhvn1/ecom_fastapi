import uuid
from .base import Base
from sqlmodel import SQLModel, Field


class ShopCategoryBase(Base):
    name: str = Field(max_length=255)


class ShopCategory(ShopCategoryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class ShopCategoryPublic(ShopCategoryBase):
    id: uuid.UUID


class ShopCategoryCreateUpdate(SQLModel):
    name: str = Field(max_length=255)
