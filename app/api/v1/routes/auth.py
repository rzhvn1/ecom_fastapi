from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.crud import user as user_crud
from app.models.user import UserPublic, UserRegister, User
from app.dependencies.db import SessionDep


router = APIRouter(tags=["auth"])

@router.post("/register", response_model=UserPublic)
async def register_user(
	session: SessionDep,
	user_in: UserRegister
) -> Any:
	user_db = user_crud.get_user_by_email(session=session, email=user_in.email)
	if user_db:
		raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system",
        )
	user = user_crud.create_user(session=session, user_create=user_in)
	
	return user