from typing import Any

from fastapi import APIRouter
from sqlmodel import select, func

from app.models.user import User, UserPublic, UsersPublic, UserCreate
from crud import user as user_crud
from app.dependencies.db import SessionDep
from app.dependencies.user import CurrentSuperUser

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
	# user = user_crud.get_user_by_email(session=session, email=user_in.email)
	# if not user:
	# 	raise
	pass



	