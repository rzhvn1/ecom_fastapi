import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, status
from app.dependencies.db import SessionDep
from app.dependencies.user import CurrentUser
from app.models.user import User, UserPublic, UserUpdateMe
from app.crud import user as user_crud

router = APIRouter(tags=["users"])

@router.get("/me", response_model=UserPublic)
async def read_user_me(current_user: CurrentUser) -> Any:
    return current_user


@router.get("/{user_id}", response_model=UserPublic)
async def read_user_by_id(session: SessionDep, user_id: uuid.UUID, current_user: CurrentUser) -> Any:
    user = session.get(User, user_id)
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


@router.patch("/me", response_model=UserPublic)
async def update_user_me(session: SessionDep, current_user: CurrentUser, user_in: UserUpdateMe) -> Any:
    if user_in.email:
        existing_user = user_crud.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="User with this email already exists"
            )
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user
