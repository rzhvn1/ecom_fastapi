from typing import Any

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select, func

from app.models.user import User, UserPublic, UsersPublic, UserCreate
from app.crud import user as user_crud
from app.core.config import settings
from app.dependencies.db import SessionDep
from app.dependencies.user import CurrentSuperUser
from app.utils.email import generate_new_account_email, send_email

router = APIRouter(tags=["admin"])

@router.get("/users", dependencies=CurrentSuperUser, response_model=UsersPublic)
async def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
	count_statement = select(func.count()).select_from(User)
	count = session.exec(statement=count_statement).one()

	statement = select(User).offset(skip).limit(limit)
	users = session.exec(statement=statement)

	return UsersPublic(data=users, count=count)


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
	


	