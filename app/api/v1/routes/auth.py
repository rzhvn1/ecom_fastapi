from datetime import timedelta
from typing import Any, Annotated

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.crud import user as user_crud
from app.models.user import UserPublic, UserRegister, Token
from app.models.message import Message
from app.dependencies.db import SessionDep
from app.dependencies.user import CurrentUser
from app.core.config import settings
from app.core.security import create_access_token
from app.utils.email import generate_password_reset_token, generate_reset_password_email, send_email


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


@router.post("/login", response_model=Token)
async def login(
	session: SessionDep,
	form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
	user = user_crud.authenticate(
		session=session, 
		email=form_data.username, 
		password=form_data.password
	)
	if not user:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
	elif not user.is_active:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
	
	access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

	return Token(
		access_token=create_access_token(user.id, expires_delta=access_token_expires)
	)


@router.post("/login/test-token", response_model=UserPublic)
async def test_token(current_user: CurrentUser) -> Any:
	return current_user


@router.post("/password-recovery/{email}")
def recover_password(email: str, session: SessionDep) -> Message:
    user = user_crud.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this email does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    send_email(
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Password recovery email sent")