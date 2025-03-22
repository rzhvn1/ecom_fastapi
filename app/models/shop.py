import uuid

from datetime import time

from .base import Base
from sqlmodel import SQLModel, Field, Relationship


class ShopBase(Base):
    name: str = Field(max_length=255, nullable=False)
    description: str | None = None
    opens_at: time = Field(nullable=False)
    closes_at: time = Field(nullable=False)
    address: str = Field(max_length=500, nullable=False)
    image: str | None = Field(default=None, max_length=2083)


class Shop(ShopBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    category_id: uuid.UUID = Field(foreign_key="shopcategory.id", nullable=False)

    owner: "User" = Relationship(back_populates="shops")  # type: ignore # ✅ Owner (User) relationship
    category: "ShopCategory" = Relationship(back_populates="shops")
    products: list["Product"] = Relationship(back_populates="shop") # type: ignore


class ShopCreate(SQLModel):
    name: str = Field(max_length=255, nullable=False)
    description: str | None = None
    opens_at: time = Field(nullable=False)
    closes_at: time = Field(nullable=False)
    address: str = Field(max_length=500, nullable=False)
    image: str | None = Field(default=None, max_length=2083)
    category_id: uuid.UUID


class ShopUpdate(SQLModel):
    name: str | None = Field(default=None, max_length=255)
    description: str | None = None
    opens_at: time | None = None
    closes_at: time | None = None
    address: str | None = Field(default=None, max_length=500)
    image: str | None = Field(default=None, max_length=2083)
    category_id: uuid.UUID | None = None


class ShopPublic(ShopBase):
    id: uuid.UUID
    user_id: uuid.UUID
    category_id: uuid.UUID


class ShopsPublic(SQLModel):
    data: list[ShopPublic]
    count: int


class ShopCategoryBase(Base):
    name: str = Field(max_length=255)


class ShopCategory(ShopCategoryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    shops: list[Shop] = Relationship(back_populates="category")


class ShopCategoryPublic(ShopCategoryBase):
    id: uuid.UUID


class ShopCategoriesPublic(SQLModel):
    data: list[ShopCategoryPublic]
    count: int


class ShopCategoryCreateUpdate(SQLModel):
    name: str = Field(max_length=255)
