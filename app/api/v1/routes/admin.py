import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select, func

from app.models.user import User, UserPublic, UsersPublic, UserCreate, UserUpdate
from app.models.message import Message
from app.models.shop import ShopCategory, ShopCategoryPublic, ShopCategoriesPublic, ShopCategoryCreateUpdate
from app.crud import user as user_crud
from app.crud import shop as shop_crud
from app.core.config import settings
from app.dependencies.db import SessionDep
from app.dependencies.user import CurrentSuperUser, CurrentUser
from app.utils.email import generate_new_account_email, send_email

router = APIRouter(tags=["admin"])

# users routes
@router.get("/users", dependencies=CurrentSuperUser, response_model=UsersPublic)
async def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
	users = user_crud.get_users(session=session, skip=skip, limit=limit)

	return users


@router.post("/users", dependencies=CurrentSuperUser, response_model=UserPublic)
async def create_user(*, session: SessionDep, user_in: UserCreate) -> UserPublic:
	user = user_crud.get_user_by_email(session=session, email=user_in.email)
	if user:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="The user with this email already exists in the system."
		)
	user = user_crud.create_user(session=session, user_create=user_in)
	if settings.emails_enabled and user_in.email:
		email_data = generate_new_account_email(
			email_to=user_in.email, username=user_in.email, password=user_in.password
		)
		send_email(
			email_to=user_in.email,
			subject=email_data.subject,
			html_content=email_data.html_content
		)

	return user


@router.patch("/users/{user_id}", dependencies=CurrentSuperUser, response_model=UserPublic)
async def update_user(*, session: SessionDep, user_id: uuid.UUID, user_in: UserUpdate) -> Any:
	db_user = session.get(User, user_id)
	if not db_user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="The user with this id does not exist in the system"
		)
	if user_in.email:
		existing_user = user_crud.get_user_by_email(session=session, email=user_in.email)
		if existing_user and existing_user.id != user_id:
			raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="User with this email already exists"
		)

	db_user = user_crud.update_user(session=session, db_user=db_user, user_in=user_in)

	return db_user


@router.delete("/users/{user_id}", dependencies=CurrentSuperUser)
async def delete_user(*, session: SessionDep, current_user: CurrentUser, user_id: uuid.UUID) -> Message:
	user = session.get(User, user_id)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="The user with this id does not exist in the system"
		)
	if current_user == user:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Super users are not allowed to delete themselves"
		)
	
	session.delete(user)
	session.commit()

	return Message(message="User deleted successfully")


# shop category routes
@router.get("/shop-category", dependencies=CurrentSuperUser, response_model=ShopCategoriesPublic)
async def read_shop_categories(*, session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
	count_statement = select(func.count()).select_from(ShopCategory)
	count = session.exec(statement=count_statement).one()

	statement = select(ShopCategory).offset(skip).limit(limit)
	shop_categories = session.exec(statement=statement)

	return ShopCategoriesPublic(data=shop_categories, count=count)


@router.post("/shop-category", dependencies=CurrentSuperUser, response_model=ShopCategoryPublic)
async def create_shop_category(*, session: SessionDep, category_in: ShopCategoryCreateUpdate) -> ShopCategoryPublic:
	category = shop_crud.create_shop_category(session=session, category_create=category_in)

	return category


@router.patch("/shop-categories/{category_id}", dependencies=CurrentSuperUser, response_model=ShopCategoryPublic)
async def update_shop_category(*, session: SessionDep, category_id: uuid.UUID, caregory_in: ShopCategoryCreateUpdate) -> ShopCategoryPublic:
	db_category = session.get(ShopCategory, category_id)
	if not db_category:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Shop Category not found"
		)
	
	db_category = shop_crud.update_shop_category(session=session, db_category=db_category, category_update=caregory_in)

	return db_category


@router.delete("/shop-categories/{category_id}", dependencies=CurrentSuperUser, response_model=Message)
async def delete_shop_category(*, session: SessionDep, category_id: uuid.UUID) -> Message:
	db_category = session.get(ShopCategory, category_id)
	if not db_category:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Shop Category not found"
		)
	
	session.delete(db_category)
	session.commit()

	return Message(message="Shop Category deleted successfully")

	
	
	
	


	