import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, status
from app.dependencies.db import SessionDep
from app.dependencies.user import CurrentUser
from app.models.user import User, UserPublic, UserUpdateMe, UpdatePassword
from app.models.message import Message
from app.core.security import verify_password, get_password_hash
from app.crud import user as user_crud

router = APIRouter(tags=["users"])

@router.get("/me", response_model=UserPublic)
async def read_user_me(current_user: CurrentUser) -> Any:
    return current_user


@router.patch("/me", response_model=UserPublic)
async def update_user_me(session: SessionDep, current_user: CurrentUser, user_in: UserUpdateMe) -> Any:
    if user_in.email:
        existing_user = user_crud.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="User with this email already exists"
            )
    
    return user_crud.update_user_me(session=session, current_user=current_user, user_in=user_in)


@router.patch("/me/password", response_model=Message)
async def update_password_me(session: SessionDep, current_user: CurrentUser, body: UpdatePassword) -> Any:
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    if body.current_password == body.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password cannot be the same as the current one"
        )
    
    user_crud.update_password_me(session=session, current_user=current_user, body=body)

    return Message(message="Password updated successfully")


@router.delete("/me", response_model=Message)
async def delete_user_me(session: SessionDep, current_user: CurrentUser) -> Any:
    if current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super users are not allowed to delete themselves"
        )
    session.delete(current_user)
    session.commit()
    
    return Message(message="User deleted successfully")


@router.get("/{user_id}", response_model=UserPublic)
async def read_user_by_id(session: SessionDep, user_id: uuid.UUID, current_user: CurrentUser) -> Any:
    user = user_crud.get_user_by_id(session=session, id=user_id)
    if not user: 
        raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="The user with this id does not exist in the system"
		)
    if user == current_user:
        return user
    
    if not current_user.is_superuser:
          raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="The user doesn't have enough privileges"
		)
    
    return user