import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, status
from app.dependencies.db import SessionDep
from app.dependencies.user import CurrentUser
from app.models.user import User, UserPublic

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
